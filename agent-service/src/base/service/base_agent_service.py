import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Union

# from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from langchain_ollama import OllamaLLM
from pydantic import Field, model_validator, validate_call

from src.base.service.base_multi_api_tokens import BaseMultiApiTokens
from src.common.common import split_by_size
from src.enums.enums import LanguageEnum, ModelTypeEnum
from src.settings import ENVIRONMENT, GOOGLE_API_KEYS, OLLAMA_BASE_URL


class BaseAgentService(BaseMultiApiTokens):
    llm_model: str = Field(default="gemini-2.0-flash", min_length=5, max_length=100)

    llm_temperature: Optional[float] = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Temperature for the LLM, controls randomness in responses.",
    )
    llm_top_p: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Top-p sampling for the LLM, controls diversity in responses.",
    )
    llm_top_k: Optional[int] = Field(
        default=None,
        ge=1,
        le=1000,
        description="Top-k sampling for the LLM, controls the number of highest probability tokens to consider.",
    )

    tools: Optional[List[object]] = Field(
        default_factory=list, description="List of tools that the agent can use."
    )

    path_to_prompt: dict[LanguageEnum, str] = Field(
        default_factory=dict, description="Prompts for different languages."
    )

    model_type: str = ModelTypeEnum.embedding.value

    # Private attributes with type hints
    _agents: list[Union[ChatGoogleGenerativeAI, GoogleGenerativeAI, OllamaLLM]]
    _system_prompts: dict[LanguageEnum, SystemMessage]
    _language: LanguageEnum = LanguageEnum.EN

    @model_validator(mode="after")
    def __after_init(self):
        models = {
            "gemini": ChatGoogleGenerativeAI,
            "gemma": GoogleGenerativeAI,
            "ollama": OllamaLLM,
        }

        model_params = {
            "model": self.llm_model,
            "temperature": self.llm_temperature,
            "top_p": self.llm_top_p,
            "top_k": self.llm_top_k,
        }

        llms: list[Union[ChatGoogleGenerativeAI, GoogleGenerativeAI, OllamaLLM]] = []

        model_type = self.llm_model.split("-")[0]

        if model_type == "ollama":
            _model_params = model_params.copy()
            _model_params["base_url"] = OLLAMA_BASE_URL

            llms.append(
                OllamaLLM(
                    **_model_params,
                )
            )
        elif model_type in ["gemini", "gemma"]:
            model_params["transport"] = "rest"

            for google_api_key in GOOGLE_API_KEYS:
                _model_params = model_params.copy()
                _model_params["google_api_key"] = google_api_key

                llms.append(models[model_type](**_model_params))
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

        self._reset_round_robin()

        if self.tools:
            self._agents = [llm.bind_tools(self.tools) for llm in llms]
        else:
            self._agents = llms

        self.load_system_prompt()
        return self

    def _get_agent(
        self,
    ) -> Union[ChatGoogleGenerativeAI, GoogleGenerativeAI, OllamaLLM]:
        return self._agents[self._get_next_model_index()]

    @validate_call
    def load_system_prompt(self):
        self._system_prompts = {}

        for lang, path in self.path_to_prompt.items():
            try:
                with open(path, "r") as f:
                    self._system_prompts[lang] = SystemMessage(f.read())
            except Exception as e:
                logging.error(f"Failed to load prompt for {lang} from {path}: {e}")

    @validate_call
    def set_system_lang(self, lang: LanguageEnum):
        if ENVIRONMENT == "dev":
            logging.info("Reloading system prompt...")
            self.load_system_prompt()

        if lang not in self._system_prompts:
            raise ValueError(f"System prompt for language {lang} not loaded.")

        self._language = lang

    def _get_messages(
        self, human: str, chat_history: List[AnyMessage] = []
    ) -> List[AnyMessage]:
        messages = [self._system_prompts[self._language]]
        messages.extend(chat_history)
        messages.append(HumanMessage(human))

        return messages

    @validate_call
    def run(self, human: str, chat_history: List[AnyMessage] = []) -> AIMessage:
        messages = self._get_messages(human, chat_history)

        agent = self._get_agent()

        response = agent.invoke(messages)
        return response

    @validate_call
    def runs(
        self,
        humans: List[str],
        chat_histories: List[List[AnyMessage]] = [],
        batch_size: int = -1,
    ):
        if len(chat_histories) != len(humans):
            raise ValueError("Length of chat_histories must match length of humans.")

        if len(chat_histories) == 0:
            chat_histories = [[] for _ in humans]

        messages_list = []
        for human, chat_history in zip(humans, chat_histories):
            messages = self._get_messages(human, chat_history)
            messages_list.append(messages)

        # Handle batch_size = -1 as "all in one batch"
        if batch_size == -1:
            batches = [messages_list]
        else:
            batches = split_by_size(messages_list, batch_size)

        responses = []
        for batch in batches:
            agent = self._get_agent()
            _responses = agent.batch_as_completed(batch)
            responses.extend(_responses)

        return responses

    @validate_call
    def runs_parallel(
        self,
        humans: List[str],
        chat_histories: List[List[AnyMessage]] = [],
        batch_size: int = -1,
        max_workers: int = 3,
    ):
        if len(chat_histories) != len(humans):
            raise ValueError("Length of chat_histories must match length of humans.")

        if len(chat_histories) == 0:
            chat_histories = [[] for _ in humans]

        batches = split_by_size(zip(humans, chat_histories), batch_size)

        responses = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results_iterator = executor.map(self.runs, batches)
            for result in results_iterator:
                responses.extend(result)

        return responses
