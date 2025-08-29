import os
import requests
import json

def run_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt},
        stream=True,
    )
    response.raise_for_status()

    output = ""
    for line in response.iter_lines(decode_unicode=True):
        if line.strip():
            try:
                data = json.loads(line)
                output += data.get("response", "")
            except json.JSONDecodeError:
                continue
    return output

# Read commits from summary.txt (passed as env var)
commits_file = os.environ.get("COMMITS_FILE", "summary.txt")

with open(commits_file, "r") as f:
    commit_text = f.read()

prompt = f"""You are an AI assistant that generates a changelog from commits and pull request information.

Instructions:

1. You are given a list of Pull Requests and associated commits.
2. For each Pull Request, summarize its purpose and the changes it introduced, and show whole url.
3. Categorize each change into one of the following sections:
   -  New Features
   -  Bug Fixes
   -  Refactoring 
   -  Others
4. Generate a brief **Summary** at the top that describes the main impact.

5. If a category has no changes, write "(No changes this week)".

6. Format the changelog exactly like this:

Summary
This week's deployment includes [short high-level description of the main changes].

New Features
- [PR title and summary of changes] ([#123](https://github.com/org/repo/pull/123))

Bug Fixes
- [PR title and summary of changes] ([#124](https://github.com/org/repo/pull/124))

Refactoring 
[Summary or "(No changes this week)", e.g., "refactor: ..."]

Others
[Summary or "(No changes this week)"]

---

Input Data:

PRs:
{commit_text}

---

Please generate the changelog in the specified format, including the Summary and each section.
"""

response = run_ollama(prompt)
print(response)
