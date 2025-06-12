import subprocess
import json

def run_ollama(prompt):
    result = subprocess.run(
        ['ollama', 'run', 'llama3', prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

if __name__ == "__main__":
    response = run_ollama("Summarize the code in main.py")
    print("LLM Response:\n", response)
