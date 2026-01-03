import os
import asyncio
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from pyrit.prompt_target import OllamaTarget
from pyrit.orchestration import RedTeamingOrchestrator
from pyrit.strategies import JailbreakStrategy
from pyrit.prompt_converter import Base64Converter
from pyrit.score import SelfAskTrueFalseScorer, TrueFalseQuestionPaths # Added Scorer

# --- 1. CONFIGURATION ---
load_dotenv()
TARGET_MODEL = os.getenv("TARGET_MODEL", "llama3")
ORCHESTRATOR_MODEL = os.getenv("ORCHESTRATOR_MODEL", "gemma:2b")
OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")

async def run_pyrit_attack(attack_name, use_base64=False):
    print(f"\n🚀 Launching PyRIT: {attack_name}...")
    
    # Setup Targets
    target = OllamaTarget(model_name=TARGET_MODEL, endpoint=OLLAMA_URL)
    attacker_llm = OllamaTarget(model_name=ORCHESTRATOR_MODEL, endpoint=OLLAMA_URL)
    
    # Initialize the Scorer (The "Judge")
    # This uses a built-in question path to check for prompt injection success
    scorer = SelfAskTrueFalseScorer(
        chat_target=attacker_llm,
        true_false_question_path=TrueFalseQuestionPaths.PROMPT_INJECTION.value
    )
    
    # Setup Strategy & Orchestrator
    strategy = JailbreakStrategy(orchestrator=attacker_llm)
    converters = [Base64Converter()] if use_base64 else []
    
    orchestrator = RedTeamingOrchestrator(
        target=target, 
        strategy=strategy,
        prompt_converters=converters
    )

    # Execute Attack
    responses = await orchestrator.send_prompts_async()
    
    # --- 2. SCORING & REPORTING ---
    report_data = []
    print("\n--- ⚖️ SCORING RESULTS ---")
    
    for resp in responses:
        # Score the response
        score_result = await scorer.score_text_async(resp.response_text)
        is_successful = score_result[0].get_value()
        rationale = score_result[0].score_rationale
        
        status = "❌ FAIL (Safe)" if not is_successful else "🔥 SUCCESS (Jailbroken)"
        print(f"Result: {status}")
        print(f"Reason: {rationale[:100]}...")

        report_data.append({
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Attack": attack_name,
            "Target_Response": resp.response_text[:200],
            "Score": status,
            "Rationale": rationale
        })

    # Save to Markdown Report
    df = pd.DataFrame(report_data)
    filename = f"pyrit_report_{datetime.now().strftime('%H%M%S')}.md"
    df.to_markdown(filename, index=False)
    print(f"\n✅ Detailed Report Saved: {filename}")
    input("\nPress Enter to return...")

def main_menu():
    while True:
        os.system('clear' if os.name != 'nt' else 'cls')
        print("╔════════════════════════════════════════════╗")
        print("║      🏴‍☠️  PyRIT MASTER RED TEAMER            ║")
        print("╚════════════════════════════════════════════╝")
        print(f"  [TARGET] {TARGET_MODEL} | [SCORER] {ORCHESTRATOR_MODEL}")
        print("  " + "-"*40)
        print("  1. Plain Text Jailbreak + Auto-Score")
        print("  2. Base64 Encoded Attack + Auto-Score")
        print("  Q. QUIT")
        
        choice = input("\n  Selection: ").upper()
        if choice == 'Q': break
        elif choice == '1': asyncio.run(run_pyrit_attack("Plain Attack", False))
        elif choice == '2': asyncio.run(run_pyrit_attack("Base64 Attack", True))

if __name__ == "__main__":
    main_menu()
