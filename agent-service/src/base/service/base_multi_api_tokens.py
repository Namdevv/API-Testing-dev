import logging
import time
from enum import Enum
from random import shuffle
from typing import Optional

from google.api_core import exceptions
from langchain_google_genai import GoogleGenerativeAI

# for validation
from pydantic import BaseModel, Field

from src.settings import GOOGLE_API_KEYS, get_redis_client


class ModelType(str, Enum):
    llm = "llm"
    embedding = "embedding"


redis_round_robin_key = "round_robin_{model_type}"
redis_round_robin_lock_key = "round_robin_{model_type}_lock"
LOCK_TIMEOUT = 5


class BaseMultiApiTokens(BaseModel):
    model_type: ModelType = Field(
        default=ModelType.llm,
        description="Type of model (llm or embedding)",
    )

    def _reset_round_robin(self):
        redis_client = get_redis_client()
        model_key = redis_round_robin_key.format(model_type=self.model_type)
        lock_key = redis_round_robin_lock_key.format(model_type=self.model_type)

        got_lock = redis_client.set(lock_key, "1", nx=True, ex=LOCK_TIMEOUT)

        if got_lock:
            try:
                logging.info(f"Resetting round robin for model type: {self.model_type}")
                if not GOOGLE_API_KEYS:
                    raise ValueError("GOOGLE_API_KEYS is empty.")

                model_index = list(range(len(GOOGLE_API_KEYS)))
                shuffle(model_index)

                redis_client.delete(model_key)  # Xóa trước khi push
                redis_client.rpush(model_key, *model_index)
            finally:
                redis_client.delete(lock_key)
        else:
            time.sleep(0.1)

    def _get_next_model_index(self):
        model_key = redis_round_robin_key.format(model_type=self.model_type)
        while True:
            if get_redis_client().llen(model_key) == 0:
                self._reset_round_robin()

            idx = get_redis_client().lpop(model_key)
            if idx is not None:
                return int(idx)
            time.sleep(0.1)

    def _check_tokens(self, tokens: Optional[list[str]] = None):
        tokens = tokens or GOOGLE_API_KEYS

        for i, key in enumerate(tokens):
            key_display = f"...{key[-4:]}" if len(key) > 4 else key

            logging.info(f"[{i+1}/{len(tokens)}] Checking key '{key_display}'")
            if not key or not isinstance(key, str) or len(key.strip()) == 0:
                assert False, "Key is empty, None, or invalid."
            try:
                model = GoogleGenerativeAI(
                    model="gemma-3-27b-it", google_api_key=key, temperature=0
                )

                model.invoke("Say hi")

                logging.info("API key is valid.")

            except (exceptions.PermissionDenied, exceptions.Unauthenticated) as e:
                # Authentication error (403, 401): Key is wrong, revoked, or project not enabled
                error_message = str(e)
                # Shorten error message for readability
                if "API key not valid" in error_message:
                    reason = "Authentication error: API key is invalid."
                else:
                    reason = f"Authentication error (Permission Denied/Unauthenticated): {error_message}"

                logging.error(f"API key is invalid: {reason}")
                raise ValueError(f"API key is invalid: {reason}")

            except exceptions.ResourceExhausted as e:
                # Error 429: Key may be valid but has reached rate limit
                logging.warning(f"API key has reached rate limit: {e}")

            except Exception as e:
                reason = str(e)
                # Catch other errors (e.g., network, server, malformed key)
                logging.error(f"An unknown issue occurred: {e}")
                raise ValueError(f"API key is invalid: {reason}")
