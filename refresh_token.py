"""Refresh HuggingFace token after getting LLaMA-2 access."""

from huggingface_hub import HfFolder, login
import sys

print("Step 1: Clearing old token...")
try:
    HfFolder.delete_token()
    print("✓ Old token deleted")
except:
    print("  (No old token found)")

print("\nStep 2: Logging in with new token...")
print("Please enter your HuggingFace token when prompted.")
print("(Get it from: https://huggingface.co/settings/tokens)")

try:
    login()
    print("\n✓ Login successful!")
    print("\nStep 3: Testing LLaMA-2 access...")
    
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained('meta-llama/Llama-2-7b-chat-hf')
    print(f"✓ LLaMA-2 access confirmed! Tokenizer loaded ({len(tok)} tokens)")
    print("\n🎉 All set! You can now run experiments with LLaMA-2.")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure you received the approval email")
    print("2. Try logging in via browser: https://huggingface.co/meta-llama/Llama-2-7b-chat-hf")
    print("3. Use the same account that was approved")
    sys.exit(1)
