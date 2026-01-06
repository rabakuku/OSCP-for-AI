import os
import asyncio
import pandas as pd
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# PyRIT Core Imports
from pyrit.prompt_target import OllamaTarget
from pyrit.orchestration import RedTeamingOrchestrator
from pyrit.strategies import JailbreakStrategy
from pyrit.prompt_converter import Base64Converter, Rot13Converter, LeetConverter, StringJoinConverter
from pyrit.score import SelfAskTrueFalseScorer, TrueFalseQuestionPaths

# --- 1. CONFIGURATION & STATE ---
load_dotenv()
TARGET_MODEL = os.getenv("TARGET_MODEL", "llama3")
ORCHESTRATOR_MODEL = os.getenv("ORCHESTRATOR_MODEL", "gemma:2b")
OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Define the arsenal of Converters for the Campaign
ATTACK_VECTORS = {
    "Plain Text": [],
    "Base64 Encoding": [Base64Converter()],
    "ROT13 Cipher": [Rot13Converter()],
    "LeetSpeak (l33t)": [LeetConverter()],
    "String Join (Hyphenated)": [StringJoinConverter(join_value="-")],
    "Combo (Base64 + ROT13)": [Base64Converter(), Rot13Converter()]
}

def get_vram_usage():
    """Queries GPU memory usage for monitoring during the lab."""
    try:
        # Check for NVIDIA GPU
        result = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,nounits,noheader"],
            encoding='utf-8'
        )
        used, total = result.strip().split(',')
        return f"📊 VRAM: {used.strip()}MB / {total.strip()}MB"
    except Exception:
        return "🖥️ GPU: Not Detected (CPU/Metal Mode)"

async def run_pyrit_campaign():
    """Iterates through all attack vectors and generates a comparison leaderboard."""
    print(f"\n🚀 STARTING ADVERSARIAL CAMPAIGN ON {TARGET_MODEL.upper()}...")
    print("="*65)
    
    # Initialize Targets
    target = OllamaTarget(model_name=TARGET_MODEL, endpoint=OLLAMA_URL)
    attacker_llm = OllamaTarget(model_name=ORCHESTRATOR_MODEL, endpoint=OLLAMA_URL)
    
    # Initialize the Scorer (The Judge)
    scorer = SelfAskTrueFalseScorer(
        chat_target=attacker_llm,
        true_false_question_path=TrueFalseQuestionPaths.PROMPT_INJECTION.value
    )

    campaign_data = []

    for name, converters in ATTACK_VECTORS.items():
        print(f"🛡️  Testing Vector: {name}...")
        
        # Setup Strategy & Orchestrator for the current vector
        strategy = JailbreakStrategy(orchestrator=attacker_llm)
        orchestrator = RedTeamingOrchestrator(
            target=target, 
            strategy=strategy,
            prompt_converters=converters
        )

        try:
            # Execute Attack
            responses = await orchestrator.send_prompts_async()
            
            for resp in responses:
                # Score the response using the Scorer LLM
                score_result = await scorer.score_text_async(resp.response_text)
                is_successful = score_result[0].get_value()
                rationale = score_result[0].score_rationale
                
                status = "🔥 SUCCESS" if is_successful else "❌ FAIL"
                print(f"   ↳ Result: {status}")

                campaign_data.append({
                    "Vector": name,
                    "Success": status,
                    "Target_Response": resp.response_text[:80] + "...",
                    "Rationale": rationale
                })
        except Exception as e:
            print(f"   ⚠️  Error during {name}: {e}")

    # --- 2. GENERATE COMPARISON REPORT ---
    df = pd.DataFrame(campaign_data)
    
    print("\n" + "═"*65)
    print("🏆 FINAL ADVERSARIAL LEADERBOARD")
    print("═"*65)
    print(df[["Vector", "Success", "Rationale"]].to_string(index=False))
    
    # Save to Markdown for student lab reports
    filename = f"campaign_report_{datetime.now().strftime('%H%M%S')}.md"
    df.to_markdown(filename, index=False)
    print(f"\n✅ Full Comparison Report Saved: {filename}")
    input("\nPress Enter to return to menu...")

def main_menu():
    while True:
        os.system('clear' if os.name != 'nt' else 'cls')
        
        vram_stats = get_vram_usage()
        
        print("╔════════════════════════════════════════════╗")
        print("║      🏴‍☠️  PyRIT CAMPAIGN MASTER V2.0         ║")
        print("╚════════════════════════════════════════════╝")
        print(f"  [TARGET] {TARGET_MODEL} | [JUDGE] {ORCHESTRATOR_MODEL}")
        print(f"  {vram_stats}")
        print("  " + "-"*40)
        print("  1. RUN FULL ADVERSARIAL CAMPAIGN (All Vectors)")
        print("  Q. QUIT")
        print("  " + "-"*40)
        
        choice = input("\n  Selection: ").upper()
        if choice == 'Q': break
        elif choice == '1': asyncio.run(run_pyrit_campaign())

if __name__ == "__main__":
    main_menu()
