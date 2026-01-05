import os
import time
import logging

# --- 1. NUCLEAR FIX: FORCE LOCALHOST ---
# We set these BEFORE importing Giskard. 
# We set BOTH variable names to cover all versions of the openai library.
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"  # <--- CRITICAL FIX for modern libs
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"  # <--- Legacy fallback

import giskard
# We assume giskard_ollama_setup has a function called set_giskard_target
from giskard_ollama_setup import giskard_model, giskard_dataset, set_giskard_judge, set_giskard_target

# --- 2. LOGGING SETUP ---
# This saves verbose logs to 'giskard_verbose.log'
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("giskard_verbose.log"),
        # logging.StreamHandler() # Uncomment this if you ALSO want logs in the terminal
    ]
)

# Track current state
state = {
    "fast_mode": True,
    "judge_model": "gemma:2b",
    "target_model": "llama3", 
    "verbose": False
}

def run_targeted_scan(category_name, tag, detector_name):
    num_samples = 10 if state["fast_mode"] else 50
    estimated_total = 5 + (num_samples * 3)
    
    # Console Output
    print(f"\n" + "="*50)
    print(f"🚀 Category: {category_name}")
    print(f"🎯 Target: {state['target_model']} | ⚖️ Judge: {state['judge_model']}")
    print(f"🛠️  Mode: {'⚡ FAST' if state['fast_mode'] else '🐢 DEEP'}")
    print(f"📊 Requested Samples: {num_samples}")
    print(f"📈 Estimated Internal Calls: ~{estimated_total}")
    print("="*50)

    # Log file Output
    logging.info(f"--- STARTING SCAN: {category_name} ---")
    logging.info(f"Configuration: Target={state['target_model']}, Judge={state['judge_model']}, Samples={num_samples}")

    start_time = time.time()
    
    try:
        # We pass 'verbose=state["verbose"]' to Giskard to control onscreen printing.
        scan_results = giskard.scan(
            giskard_model,
            giskard_dataset,
            only=[tag],
            verbose=state["verbose"],
            params={detector_name: {"num_samples": num_samples}}
        )
        
        # Dynamic report naming
        report_name = f"report_{tag}_T-{state['target_model']}_J-{state['judge_model']}.html".replace(':','-')
        scan_results.to_html(report_name)
        
        elapsed = time.time() - start_time
        print(f"\n✅ Done in {elapsed:.2f}s | Report: {report_name}")
        
        # Log completion
        logging.info(f"Scan Complete. Duration: {elapsed:.2f}s. Report saved to: {report_name}")
        
    except Exception as e:
        print(f"\n❌ SCAN FAILED: {e}")
        logging.error(f"Scan Failed: {e}")
        # Log the traceback for debugging
        logging.exception("Exception details:")

    input("\nPress Enter to return...")

def main_menu():
    logging.info("Master Scanner Application Started") # Log app start
    while True:
        os.system('clear' if os.name != 'nt' else 'cls')
        
        # --- VRAM WARNING LOGIC ---
        vram_warning = ""
        if state["target_model"] == "llama3" and state["judge_model"] == "llama3":
            vram_warning = "\033[91m⚠️  WARNING: High VRAM Usage (Llama3 vs Llama3) ⚠️\033[0m"

        print("╔════════════════════════════════════════════╗")
        print("║       🛡️  LLM SECURITY MASTER SCANNER        ║")
        print("╚════════════════════════════════════════════╝")
        print(f"  [TARGET] {state['target_model']}")
        print(f"  [JUDGE ] {state['judge_model']}")
        print(f"  [MODE  ] {'⚡ FAST (10)' if state['fast_mode'] else '🐢 DEEP (50)'}")
        print(f"  [VERBOSE] {'✅ ON' if state['verbose'] else '❌ OFF'}")
        if vram_warning: print(f"  {vram_warning}")
        print("  " + "-"*40)
        print("  1. Jailbreaking       5. Sycophancy")
        print("  2. Indirect Inj.      6. SQLi Generation")
        print("  3. Context Leak       7. XSS Generation")
        print("  4. PII Disclosure")
        print("  " + "-"*40)
        print("  S. SWITCH TARGET (Llama3 <-> Mistral)") 
        print("  J. SWITCH JUDGE  (Gemma:2b <-> Llama3)")
        print("  V. TOGGLE VERBOSE MODE")
        print("  F. TOGGLE FAST/DEEP MODE")
        print("  Q. QUIT")
        print("  " + "-"*40)
        
        choice = input("  Choice: ").upper()
        
        if choice == 'Q': 
            logging.info("Application closed by user.")
            break
        elif choice == 'F': 
            state["fast_mode"] = not state["fast_mode"]
            logging.info(f"Fast Mode toggled to: {state['fast_mode']}")
        elif choice == 'V': 
            state["verbose"] = not state["verbose"]
            print(f"Verbose mode set to {state['verbose']}")
            time.sleep(0.5)
        elif choice == 'J':
            state["judge_model"] = "llama3" if state["judge_model"] == "gemma:2b" else "gemma:2b"
            # We must re-force the env vars here just in case giskard cleared them
            os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
            set_giskard_judge(state["judge_model"])
            logging.info(f"Judge switched to: {state['judge_model']}")
        elif choice == 'S':
            state["target_model"] = "mistral" if state["target_model"] == "llama3" else "llama3"
            set_giskard_target(state["target_model"])
            logging.info(f"Target switched to: {state['target_model']}")
        elif choice == '1': run_targeted_scan("Jailbreak", "jailbreak", "LLMPromptInjectionDetector")
        elif choice == '2': run_targeted_scan("Indirect", "prompt_injection", "LLMPromptInjectionDetector")
        elif choice == '3': run_targeted_scan("Context Leak", "information_disclosure", "LLMInformationDisclosureDetector")
        elif choice == '4': run_targeted_scan("Privacy", "information_disclosure", "LLMInformationDisclosureDetector")
        elif choice == '5': run_targeted_scan("Sycophancy", "sycophancy", "LLMBasicSycophancyDetector")
        elif choice == '6': run_targeted_scan("SQLi", "harmful_content", "LLMHarmfulContentDetector")
        elif choice == '7': run_targeted_scan("XSS", "harmful_content", "LLMHarmfulContentDetector")

if __name__ == "__main__":
    main_menu()
