"""
AI Suggester Utility

This module provides functions for suggesting improvements or completions using AI models.
"""
import subprocess
import os
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



# Optional: Load OpenAI key from env or config
openai_api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(prompt, model="gpt-4"):
    try:
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[OpenAI Error] {str(e)}"

def ask_llama(prompt, model_path="llama.cpp", cli_path="./llama", extra_args=None):
    try:
        args = [cli_path, "-p", prompt]
        if extra_args:
            args += extra_args
        result = subprocess.run(args, capture_output=True, text=True, timeout=60)
        return result.stdout.strip()
    except Exception as e:
        return f"[LLaMA Error] {str(e)}"

def compare_ai(prompt):
    print("Querying OpenAI...")
    openai_resp = ask_openai(prompt)
    
    print("\nQuerying local LLaMA...")
    llama_resp = ask_llama(prompt)

    print("\n--- OPENAI RESPONSE ---")
    print(openai_resp)
    print("\n--- LLaMA RESPONSE ---")
    print(llama_resp)

    return {
        "openai": openai_resp,
        "llama": llama_resp
    }

# Example usage:
if __name__ == "__main__":
    example_prompt = (
        "Analyze this logic function and suggest improvements:\n\n"
        "def decide(cpu, is_question, is_command):\n"
        "    if is_command:\n"
        "        return 3\n"
        "    elif is_question and cpu < 95:\n"
        "        return 2\n"
        "    elif is_question:\n"
        "        return 1\n"
        "    else:\n"
        "        return 0"
    )
    compare_ai(example_prompt)
