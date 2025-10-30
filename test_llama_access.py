from transformers import AutoTokenizer

print("Testing LLaMA-2 access...")
try:
    tok = AutoTokenizer.from_pretrained('meta-llama/Llama-2-7b-chat-hf')
    print("✓ LLaMA-2 access confirmed!")
    print(f"✓ Tokenizer loaded: {len(tok)} tokens in vocab")
except Exception as e:
    print(f"✗ LLaMA-2 access denied: {e}")
