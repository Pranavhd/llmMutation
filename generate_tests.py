import os
import re
import json
from pathlib import Path
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Or another Gemini model

def load_mutmut_meta(meta_path):
    data = json.loads(Path(meta_path).read_text())
    # return list of mutation keys with exit_code == 0
    return [k for k, v in data["exit_code_by_key"].items() if v == 0]

def extract_function(code: str, func_name: str) -> str:
    """
    Extracts the full source of def func_name(...) ... until the next top‑level def.
    """
    pattern = rf"^def {func_name}\b[^\:]*\:.*?(?=^def |\Z)"
    m = re.search(pattern, code, re.MULTILINE | re.DOTALL)
    return m.group(0) if m else ""

def generate_prompt(original_cd: str, original_fn: str, mutated_fn: str, existing_tests: str) -> str:
    return f"""
You are given a Python function and one of its mutated variants.
Generate pytest unit tests that:
 1. Pass against the original function.
 2. Fail against the mutated variant (i.e., kill the mutation).

Use only pytest (no unittest). Also use the original function not mutated function. Provide tests only. The function name should remain the same

Original code:
{original_cd}
Original function:
{original_fn}
Mutated variant:
{mutated_fn}
Existing tests:
{existing_tests}
"""

def call_llm(prompt: str) -> str:
    # Use Gemini to generate tests 
    response = model.generate_content(prompt)
    return response.text

def main():
    original_path = Path("example.py")
    meta_path = Path("mutants/example.py.meta")
    mutants_path = Path("mutants/example.py")
    tests_path = Path("tests/test_example.py")
    survivors = load_mutmut_meta(meta_path)
    full_code = mutants_path.read_text()
    existing_tests = tests_path.read_text()
    output_file = Path("tests/test_example_additional.py")
    header = "import pytest\nfrom example import divide\n\n"
    output_file.write_text(header)

    for key in survivors:
        # e.g. key == "example.x_divide__mutmut_3"
        func = key.split(".")[-1]
        orig = func.rsplit("__mutmut_", 1)[0] + "__mutmut_orig"
        orig_src = extract_function(full_code, orig)
        mut_src = extract_function(full_code, func)

        prompt = generate_prompt(original_path, orig_src, mut_src, existing_tests)
        new_tests = call_llm(prompt)

        current = output_file.read_text()
        output_file.write_text(current + new_tests + "\n\n")

    print(f"New tests written to {output_file}")

main()