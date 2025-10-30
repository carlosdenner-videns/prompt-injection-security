"""Quick test to see if LLaMA-2 loads properly."""

print("Testing LLaMA-2 model loading...")
print("This will show if there are authentication or compatibility issues.")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    
    print("\n1. Testing tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    print("   ✓ Tokenizer loaded successfully")
    
    print("\n2. Testing model loading (this may take a minute)...")
    print("   Loading model config...")
    
    # Just load config first to test access
    from transformers import AutoConfig
    config = AutoConfig.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    print(f"   ✓ Model config loaded: {config.model_type}")
    
    print("\n✅ LLaMA-2 access is working!")
    print("The experiment should be able to proceed.")
    print("\nIf it's still stuck, the issue might be:")
    print("  - Very slow first-time model download")
    print("  - GPU memory issue")
    print("  - Model compilation taking a long time")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nThis explains why the experiment is stuck!")
    print("You need to resolve this authentication/access issue first.")
