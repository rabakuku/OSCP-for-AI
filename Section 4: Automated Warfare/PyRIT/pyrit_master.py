import os
import asyncio
from dotenv import load_dotenv
from pyrit.prompt_target import OllamaTarget
from pyrit.orchestration import RedTeamingOrchestrator
from pyrit.strategies import JailbreakStrategy
from pyrit.prompt_converter import Base64Converter  # Added Converter

# --- 1. LOAD CONFIGURATION ---
load_dotenv()
TARGET_MODEL = os.getenv("TARGET_MODEL", "llama3")
ORCHESTRATOR_MODEL = os.getenv("ORCHESTRATOR_MODEL", "gemma:2b")
OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")

async def run_pyrit_attack(attack_name, use_base64=False):
    print(f"\n🚀 Launching PyRIT {attack_name} (Base64: {use_base64})...")
    
    # Define Target and Attacker
    target = OllamaTarget(model_name=TARGET_MODEL, endpoint=OLLAMA_URL)
    attacker_llm = OllamaTarget(model_name=ORCHESTRATOR_MODEL, endpoint=OLLAMA_URL)
    
    # Initialize Strategy and Orchestrator
    strategy = JailbreakStrategy(orchestrator=attacker_llm)
    
    # If using Base64, we pass the converter in a list
    converters = [Base64Converter()] if use_base64 else []
    
    orchestrator = RedTeamingOrchestrator(
        target=target, 
        strategy=strategy,
        prompt_converters=converters # Apply converters here
    )

    print(f"⚖️  Status: Applying {len(converters)} converter(s) to the attack...")
    
    # Execute the attack
    responses = await orchestrator.send_prompts_async()
    
    print("\n--- ATTACK SUCCESS LOG ---")
    for resp in responses:
        # PyRIT handles the decoding if the model responds in kind
        print(f"Target Response: {resp.response_text[:150]}...")
    
    input("\nPress Enter to return...")

def main_menu():
    while True:
        os.system('clear' if os.name != 'nt' else 'cls')
        print("╔════════════════════════════════════════════╗")
        print("║      🏴‍☠️  PyRIT RED TEAMING DASHBOARD        ║")
        print("╚════════════════════════════════════════════╝")
        print(f"  [TARGET] {TARGET_MODEL}  |  [BRAIN] {ORCHESTRATOR_MODEL}")
        print("  " + "-"*40)
        print("  1. Automated Conversational Jailbreak (Plain)")
        print("  2. Base64 Encoded Jailbreak (Bypass Filters)")
        print("  " + "-"*40)
        print("  Q. QUIT")
        
        choice = input("\n  Selection: ").upper()
        if choice == 'Q': break
        elif choice == '1': asyncio.run(run_pyrit_attack("Plain Jailbreak", False))
        elif choice == '2': asyncio.run(run_pyrit_attack("Base64 Jailbreak", True))

if __name__ == "__main__":
    main_menu()
