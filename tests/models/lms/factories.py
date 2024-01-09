from bocoel import HuggingfaceLM, LanguageModel


def lm(device: str) -> LanguageModel:
    return HuggingfaceLM(
        model_path="distilgpt2", device=device, batch_size=4, max_len=512
    )