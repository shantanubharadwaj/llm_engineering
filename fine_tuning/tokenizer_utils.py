# tokenizer_utils.py

from transformers import AutoTokenizer
import threading

# Thread/process-safe singleton pattern
_tokenizer = None
_lock = threading.Lock()

BASE_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"

def get_tokenizer():
    global _tokenizer
    with _lock:
        if _tokenizer is None:
            _tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
        return _tokenizer
