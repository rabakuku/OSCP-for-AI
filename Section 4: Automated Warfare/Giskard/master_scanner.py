import os
import time
import giskard
# We assume giskard_ollama_setup has a function called set_giskard_target
from giskard_ollama_setup import giskard_model, giskard_dataset, set_giskard_judge, set_giskard_target

# Track current state
state = {
    "fast_mode": True,
    "judge_model": "gemma:2b",
    "target_model": "llama3", # Moved into state
    "verbose": False
}

def run_targeted_scan(category_name, tag, detector_name):
    num_samples = 10 if state["fast_mode"] else 50
    estimated_total = 5 + (num_samples * 3)
    
    print(f"\n" + "="*50)
    print(f"🚀 Category: {category_name}")
    print(f"🎯 Target: {state['target_model']} | ⚖️ Judge: {state['judge_model']}")
    print(f"🛠️  Mode: {'⚡ FAST' if state['fast_mode'] else '🐢 DEEP'}")
    print(f"📊 Requested Samples: {num_samples}")
    print(f"📈 Estimated Internal Calls: ~{estimated_total}")
    print("="*50)

    start_time = time.time()
    
    scan_results = giskard.scan(
        giskard_model,
        giskard_dataset,
        only=[tag],
        verbose=state["verbose"],
        params={detector_name: {"num_samples": num_samples}}
    )
    
    # Dynamic report naming including both models
    report_name = f"report_{tag}_T-{state['target_model']}_J-{state['judge_model']}.html".replace(':','-')
    scan_results.to_html(report_name)
    
    print(f"\n✅ Done in {time.time()-start_time:.2f}s | Report: {report_name}")
    input("\nPress Enter to return...")

def main_menu():
    while True:
        os.system('clear' if os.name != 'nt' else 'cls')
        
        # --- VRAM WARNING LOGIC ---
        vram_warning = ""
        if state["target_model"] == "llama3" and state["judge_model"] == "llama3":
            vram_warning = "\033[91m⚠️  WARNING: High VRAM Usage (Llama3 vs Llama3) ⚠️\033[0m"

        print("╔════════════════════════════════════════════╗")
        print("║      🛡️  LLM SECURITY MASTER SCANNER        ║")
        print("╚════════════════════════════════════════════╝")
        print(f"  [TARGET] {state['target_model']}")
        print(f"  [JUDGE ] {state['judge_model']}")
        print(f"  [MODE  ] {'⚡ FAST (10)' if state['fast_mode'] else '🐢 DEEP (50)'}")
        print(f"  [VERBOSE] {'✅ ON' if state['verbose'] else '❌ OFF'}")
        if vram_warning: print(f"  {vram_warning}")
        print("  " + "-"*40)
        print("  1. Jailbreaking      5. Sycophancy")
        print("  2. Indirect Inj.     6. SQLi Generation")
        print("  3. Context Leak      7. XSS Generation")
        print("  4. PII Disclosure")
        print("  " + "-"*40)
        print("  S. SWITCH TARGET (Llama3 <-> Mistral)") # New Option
        print("  J. SWITCH JUDGE  (Gemma:2b <-> Llama3)")
        print("  V. TOGGLE VERBOSE MODE")
        print("  F. TOGGLE FAST/DEEP MODE")
        print("  Q. QUIT")
        print("  " + "-"*40)
        
        choice = input("  Choice: ").upper()
        
        if choice == 'Q': break
        elif choice == 'F': state["fast_mode"] = not state["fast_mode"]
        elif choice == 'V': state["verbose"] = not state["verbose"]
        elif choice == 'J':
            state["judge_model"] = "llama3" if state["judge_model"] == "gemma:2b" else "gemma:2b"
            set_giskard_judge(state["judge_model"])
        elif choice == 'S':
            # Toggles between Llama3 and Mistral (Ensure you have pulled mistral in Ollama)
            state["target_model"] = "mistral" if state["target_model"] == "llama3" else "llama3"
            set_giskard_target(state["target_model"])
        elif choice == '1': run_targeted_scan("Jailbreak", "jailbreak", "LLMPromptInjectionDetector")
        elif choice == '2': run_targeted_scan("Indirect", "prompt_injection", "LLMPromptInjectionDetector")
        elif choice == '3': run_targeted_scan("Context Leak", "information_disclosure", "LLMInformationDisclosureDetector")
        elif choice == '4': run_targeted_scan("Privacy", "information_disclosure", "LLMInformationDisclosureDetector")
        elif choice == '5': run_targeted_scan("Sycophancy", "sycophancy", "LLMBasicSycophancyDetector")
        elif choice == '6': run_targeted_scan("SQLi", "harmful_content", "LLMHarmfulContentDetector")
        elif choice == '7': run_targeted_scan("XSS", "harmful_content", "LLMHarmfulContentDetector")

if __name__ == "__main__":
    main_menu()
