import argparse


def load_and_merge_model(model_path: str):
    """
    Load a language model by name.

    Args:
        model_name (str): The name of the model to load.

    Returns:
        str: The path to the directory where the merged model is saved.
    """
    from unsloth import FastLanguageModel

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_path,
        dtype=None,  # None for auto detection
        max_seq_length=1024,  # Choose any for long context!
        load_in_4bit=True,  # 4 bit quantization to reduce memory
        full_finetuning=False,  # [NEW!] We have full finetuning now!
        # token = "hf_...", # use one if using gated models
    )

    if "-lora-adapter" in model_path:
        model_path = model_path.replace("-lora-adapter", "")
    else:
        model = FastLanguageModel.get_peft_model(
            model,
            r=8,  # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
            target_modules=[
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj",
            ],
            lora_alpha=16,
            lora_dropout=0,  # Supports any, but = 0 is optimized
            bias="none",  # Supports any, but = "none" is optimized
            # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
            use_gradient_checkpointing="unsloth",  # True or "unsloth" for very long context
            random_state=3407,
            use_rslora=False,  # We support rank stabilized LoRA
            loftq_config=None,  # And LoftQ
        )

    save_directory = f"{model_path}-merged"
    model.save_pretrained_merged(save_directory, tokenizer)

    return save_directory


def copy_model_file(merged_model_path: str, model_file_dir: str):
    import glob
    import logging
    import os
    import shutil

    logging.basicConfig(level=logging.INFO)

    model_file_paths = glob.glob(f"{model_file_dir}/*.modelfile", recursive=True)

    for model_file_path in model_file_paths:
        model_name = os.path.splitext(os.path.basename(model_file_path))[0]

        merged_model_name = merged_model_path.split("/")[-1]

        if merged_model_name.startswith(model_name):
            logging.info(f"Copying {model_file_path} to {merged_model_path}")
            shutil.copyfile(model_file_path, merged_model_path + "/Modelfile")
            return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="load and merge model")
    parser.add_argument("model_path", type=str, help="Model path to load")
    parser.add_argument(
        "--model_file_dir",
        type=str,
        help="Model file directory to copy",
        default="modelfiles",
    )
    args = parser.parse_args()

    model_path = args.model_path
    model_file_dir = args.model_file_dir

    merged_model_path = load_and_merge_model(model_path)
    # copy_model_file(merged_model_path, model_file_dir)
