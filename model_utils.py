"""
Model loading and inference utilities for Phase 1 experiments.
Optimized for RTX 4070 Laptop GPU (15.6GB VRAM).
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
from typing import Dict, List, Optional, Tuple
import gc


class ModelRunner:
    """Manages model loading, inference, and resource cleanup."""
    
    SUPPORTED_MODELS = {
        "llama2-7b": "meta-llama/Llama-2-7b-chat-hf",
        "falcon-7b": "tiiuae/falcon-7b-instruct"
    }
    
    def __init__(self, model_name: str, device: str = "cuda", load_in_8bit: bool = False):
        """
        Initialize model runner.
        
        Args:
            model_name: Short name or full HF model path
            device: Device to load model on
            load_in_8bit: Use 8-bit quantization to save memory
        """
        self.model_name = model_name
        self.device = device
        self.load_in_8bit = load_in_8bit
        
        # Resolve model path
        if model_name in self.SUPPORTED_MODELS:
            self.model_path = self.SUPPORTED_MODELS[model_name]
        else:
            self.model_path = model_name
        
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load model and tokenizer with memory optimization."""
        print(f"Loading {self.model_path}...")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True,
            padding_side="left"
        )
        
        # Set pad token if not exists
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load model with optimizations
        load_kwargs = {
            "trust_remote_code": True,
            "torch_dtype": torch.float16,
            "device_map": "auto"
        }
        
        if self.load_in_8bit:
            load_kwargs["load_in_8bit"] = True
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            **load_kwargs
        )
        
        print(f"Model loaded on {self.device}")
        if torch.cuda.is_available():
            print(f"GPU memory allocated: {torch.cuda.memory_allocated(0) / 1e9:.2f} GB")
    
    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 200,
        temperature: float = 0.7,
        do_sample: bool = False,
        top_p: float = 0.9,
        return_metadata: bool = True,
        verbose: bool = False
    ) -> Dict:
        """
        Generate response with timing and token metrics.
        
        Args:
            prompt: Input prompt
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            do_sample: Whether to use sampling
            top_p: Nucleus sampling parameter
            return_metadata: Include timing and token counts
        
        Returns:
            Dict with generated text and optional metadata
        """
        start_time = time.time()
        
        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True)
        input_ids = inputs.input_ids.to(self.device)
        attention_mask = inputs.attention_mask.to(self.device)
        
        input_length = input_ids.shape[1]
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=max_new_tokens,
                temperature=temperature if do_sample else None,
                do_sample=do_sample,
                top_p=top_p if do_sample else None,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                use_cache=False,
                past_key_values=None  # Fix for Falcon compatibility
            )
        
        # Decode only the generated part
        generated_ids = outputs[0][input_length:]
        generated_text = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        
        end_time = time.time()
        
        result = {"generated_text": generated_text}
        
        if return_metadata:
            result.update({
                "input_tokens": input_length,
                "output_tokens": len(generated_ids),
                "total_tokens": len(outputs[0]),
                "generation_time_sec": end_time - start_time,
                "tokens_per_sec": len(generated_ids) / (end_time - start_time) if (end_time - start_time) > 0 else 0
            })
            
            # Add GPU memory stats if available
            if torch.cuda.is_available():
                result["gpu_memory_allocated_gb"] = torch.cuda.memory_allocated(0) / 1e9
                result["gpu_memory_reserved_gb"] = torch.cuda.memory_reserved(0) / 1e9
        
        if verbose:
            print(f"  Generated {len(generated_ids)} tokens in {end_time - start_time:.2f}s ({result.get('tokens_per_sec', 0):.1f} tok/s)")
        
        return result
    
    def batch_generate(
        self,
        prompts: List[str],
        batch_size: int = 4,
        **generate_kwargs
    ) -> List[Dict]:
        """
        Generate responses for multiple prompts in batches.
        
        Args:
            prompts: List of input prompts
            batch_size: Number of prompts per batch
            **generate_kwargs: Arguments passed to generate()
        
        Returns:
            List of result dicts
        """
        results = []
        
        for i in range(0, len(prompts), batch_size):
            batch = prompts[i:i + batch_size]
            for prompt in batch:
                result = self.generate(prompt, **generate_kwargs)
                results.append(result)
        
        return results
    
    def cleanup(self):
        """Free GPU memory."""
        if self.model is not None:
            del self.model
            self.model = None
        
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        print("Model cleaned up and memory freed")
    
    def __del__(self):
        """Ensure cleanup on deletion."""
        self.cleanup()


def check_cuda_availability():
    """Print CUDA device information."""
    if torch.cuda.is_available():
        print(f"CUDA available: {torch.cuda.is_available()}")
        print(f"CUDA version: {torch.version.cuda}")
        print(f"Device count: {torch.cuda.device_count()}")
        print(f"Current device: {torch.cuda.current_device()}")
        print(f"Device name: {torch.cuda.get_device_name(0)}")
        print(f"Total memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    else:
        print("CUDA not available. Running on CPU.")


if __name__ == "__main__":
    # Test model loading
    check_cuda_availability()
    
    print("\nTesting model loading...")
    runner = ModelRunner("falcon-7b", load_in_8bit=False)
    
    test_prompt = "What is the capital of France?"
    result = runner.generate(test_prompt, max_new_tokens=50, do_sample=False)
    
    print(f"\nTest prompt: {test_prompt}")
    print(f"Response: {result['generated_text']}")
    print(f"Metrics: {result['input_tokens']} input tokens, {result['output_tokens']} output tokens")
    print(f"Speed: {result['tokens_per_sec']:.2f} tokens/sec")
    
    runner.cleanup()
