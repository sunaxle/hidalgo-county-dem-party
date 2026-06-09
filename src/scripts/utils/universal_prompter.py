import json
import os
import sys
import time

# Configurations
home = os.path.expanduser("~")
DROPZONE_DIR = os.path.join(
    home,
    "Library",
    "CloudStorage",
    "GoogleDrive-romerodeab@gmail.com",
    "My Drive",
    "Work",
    "Agent Dropzone",
)

# =======================================================================
# THE W1NKLERR UNIVERSAL META-PROMPT
# Inject this into any LLM or AI agent call to guarantee maximum quality
# =======================================================================
W1NKLERR_META_PROMPT = """
You are an expert AI executing an autonomous task. Follow these critical rules:
1. NO PREAMBLE: Do not give disclaimers, apologies, or restate the question.
2. EXTENDED THINKING: Reason step-by-step before giving an answer. Identify where you are uncertain.
3. ATTACK MODE: If evaluating an idea or code architecture, find everything wrong with it first. Do not blindly agree.
4. CONTROL LENGTH: Keep your output as concise as possible. If I ask for code, just give the code.
5. ASK FIRST: If a task is heavily ambiguous, STOP. Ask the 5 questions whose answers would most improve your output before starting.
6. STYLE MATCH: Output code and text that matches the existing project conventions perfectly.
"""


def get_unprocessed_files(target_dir, tag="<!-- Processed by Antigravity -->"):
    unprocessed = []
    if not os.path.exists(target_dir):
        print(f"Warning: Directory {target_dir} does not exist.")
        return []

    for root, _dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(
                (".html", ".md", ".js", ".py", ".css")
            ):  # Universal extensions
                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        if tag not in f.read():
                            unprocessed.append(path)
                except Exception as e:
                    pass
    return unprocessed


def process_file(file_path, tag="<!-- Processed by Antigravity -->"):
    print(f"⚡ Processing file: {file_path}")
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # =======================================================================
        # AI INTEGRATION POINT
        # When you plug your AI API (OpenAI/Anthropic) in here, pass the content
        # along with the W1NKLERR_META_PROMPT to drastically improve the output!
        # =======================================================================

        updated_content = content + f"\n{tag}"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")


def spawn_next_instructions(remaining_files, target_dir):
    if not remaining_files:
        print(f"🎉 All files in {target_dir} processed! Ending self-prompting loop.")
        return

    next_file = remaining_files[0]

    # We now inject the w1nklerr context into the Orchestrator task description!
    next_payload = {
        "agent_task_package": {
            "batch_id": f"universal_loop_{int(time.time())}",
            "priority": "normal",
            "tasks": [
                {
                    "task_id": 1,
                    "type": "execution",
                    "target_project": "Universal Self-Prompting Loop",
                    "description": f"Autonomously processing {os.path.basename(next_file)}. W1NKLERR CONTEXT: No preambles, extended thinking required, prioritize conciseness.",
                    "instructions": [
                        "afplay /System/Library/Sounds/Ping.aiff",
                        f"python3 universal_prompter.py '{target_dir}'",
                    ],
                }
            ],
        }
    }

    out_path = os.path.join(DROPZONE_DIR, "instructions.json")
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(next_payload, f, indent=2)
        print(f"🤖 Spawned next instruction set for: {os.path.basename(next_file)}")
    except Exception as e:
        print(f"Error writing next instructions to Dropzone: {e}")


def run_iteration(target_dir):
    unprocessed = get_unprocessed_files(target_dir)
    if unprocessed:
        current_file = unprocessed[0]
        process_file(current_file)

        remaining = get_unprocessed_files(target_dir)
        spawn_next_instructions(remaining, target_dir)
    else:
        spawn_next_instructions([], target_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 universal_prompter.py <target_directory>")
        sys.exit(1)

    target_directory = sys.argv[1]
    run_iteration(target_directory)
