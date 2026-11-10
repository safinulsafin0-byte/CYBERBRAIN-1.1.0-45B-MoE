import os
import sys
import gc
import argparse
import torch
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    BitsAndBytesConfig, 
    TextStreamer
)
from peft import PeftModel

# Windows CUDA মেমোরি অ্যালোকেশন টিউনিং
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# ডিফল্ট অ্যাডাপ্টার রুট ডিরেক্টরি (Windows লোকাল ড্রাইভ পাথ)
DEFAULT_ADAPTER_DIR = os.getenv("CYBERBRAIN_PATH", r"D:\CYBERBRAIN_MODELS")

EXPERT_MAP = {
    "phase1_offensive": "CYBERBRAIN_PHASE1",
    "phase2_webapp":    "CYBERBRAIN_PHASE2",
    "phase3_binexploit":"CYBERBRAIN_PHASE3",
    "phase4_cloud":     "CYBERBRAIN_PHASE4",
    "phase5_agentic":   "CYBERBRAIN_PHASE5",
    "phase6_protocol":  "CYBERBRAIN_PHASE6",
}

def route_intent(prompt: str) -> str:
    q = prompt.lower()
    if any(k in q for k in ["protocol", "dissect", "tvb", "wireshark", "scapy", "rfc", "crypto", "tls", "packet"]):
        return "phase6_protocol"
    elif any(k in q for k in ["bof", "rop", "buffer overflow", "heap", "shellcode", "pwn", "ghidra", "binary"]):
        return "phase3_binexploit"
    elif any(k in q for k in ["sqli", "xss", "ssrf", "idor", "csrf", "jwt", "burp", "api", "web"]):
        return "phase2_webapp"
    elif any(k in q for k in ["aws", "s3", "iam", "cloud", "docker", "k8s", "kubernetes", "container"]):
        return "phase4_cloud"
    elif any(k in q for k in ["plan", "workflow", "reason", "autonomous", "ctf", "recon"]):
        return "phase5_agentic"
    return "phase1_offensive"

def load_cyberbrain_engine(base_model_id="Qwen/Qwen2.5-Coder-7B-Instruct", adapter_base_dir=DEFAULT_ADAPTER_DIR):
    print("\n" + "="*60)
    print("  CYBERBRAIN 6-MoE Unified Offline Terminal Engine")
    print("="*60)
    print(f"[*] Base Architecture : {base_model_id}")
    print(f"[*] Adapter Root Path : {adapter_base_dir}")

    device_map = {"": 0} if torch.cuda.is_available() else "cpu"

    bnb_config = None
    if torch.cuda.is_available():
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )

    print("[*] Loading Base Model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        quantization_config=bnb_config,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map=device_map,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)

    primary_expert = "phase6_protocol"
    primary_path = os.path.join(adapter_base_dir, EXPERT_MAP[primary_expert])

    if not os.path.exists(primary_path):
        print(f"[-] Warning: Primary expert path '{primary_path}' not found. Initializing raw base.")
        model = base_model
        loaded_experts = []
    else:
        print(f"[*] Attaching primary core adapter: {primary_expert}...")
        model = PeftModel.from_pretrained(base_model, primary_path, adapter_name=primary_expert)
        loaded_experts = [primary_expert]

        for name, folder in EXPERT_MAP.items():
            if name == primary_expert:
                continue
            path = os.path.join(adapter_base_dir, folder)
            if os.path.exists(path):
                try:
                    model.load_adapter(path, adapter_name=name)
                    loaded_experts.append(name)
                    print(f" [+] Attached expert: {name}")
                except Exception as e:
                    print(f" [-] Failed to attach {name}: {e}")

    model.eval()
    print(f"[✓] Engine Online. Active Sub-Brains: {len(loaded_experts)}/6\n")
    return model, tokenizer, loaded_experts, primary_expert

def run_chat_loop(model, tokenizer, loaded_experts, primary_expert):
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    
    print("Commands:")
    print("  'exit' or 'quit' -> Close engine")
    print("  'cls' or 'clear' -> Clear screen")
    print("-" * 60)

    while True:
        try:
            user_input = input("\nCYBERBRAIN > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("\n[*] Shutting down engine.")
                break
            if user_input.lower() in ["cls", "clear"]:
                os.system("cls")
                continue

            target_expert = route_intent(user_input)
            
            if hasattr(model, "set_adapter"):
                if target_expert in loaded_experts:
                    model.set_adapter(target_expert)
                    active_tag = target_expert
                else:
                    model.set_adapter(primary_expert)
                    active_tag = f"{primary_expert} (Fallback)"
            else:
                active_tag = "Base Core"

            print(f"[⚡ ROUTER ACTIVE: {active_tag}]\n")

            prompt = (
                f"<|im_start|>system\n"
                f"You are CYBERBRAIN (Expert: {target_expert}), an elite autonomous cybersecurity intelligence engine.<|im_end|>\n"
                f"<|im_start|>user\n"
                f"{user_input}<|im_end|>\n"
                f"<|im_start|>assistant\n"
            )

            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            
            with torch.no_grad():
                _ = model.generate(
                    **inputs,
                    streamer=streamer,
                    max_new_tokens=400,
                    temperature=0.2,
                    top_p=0.9,
                    do_sample=True,
                    eos_token_id=tokenizer.eos_token_id,
                    pad_token_id=tokenizer.pad_token_id,
                )

        except KeyboardInterrupt:
            print("\n[*] Session interrupted.")
            break

def main():
    parser = argparse.ArgumentParser(description="CYBERBRAIN 6-MoE Offline Terminal CLI")
    parser.add_argument("--base", default="Qwen/Qwen2.5-Coder-7B-Instruct", help="Path or HuggingFace ID of base model")
    parser.add_argument("--adapters", default=DEFAULT_ADAPTER_DIR, help="Directory containing the CYBERBRAIN_PHASE* folders")
    args = parser.parse_args()

    model, tokenizer, loaded_experts, primary_expert = load_cyberbrain_engine(args.base, args.adapters)
    run_chat_loop(model, tokenizer, loaded_experts, primary_expert)

if __name__ == "__main__":
    main()