from pathlib import Path
from openai import OpenAI


ROOT = Path(__file__).resolve().parent.parent

client = OpenAI()


def read_project_files():
    excluded = {".git", "__pycache__"}
    files = {}

    for path in ROOT.rglob("*"):
        if (
            path.is_file()
            and not any(part in excluded for part in path.parts)
        ):
            try:
                relative = path.relative_to(ROOT)
                content = path.read_text(encoding="utf-8")
                files[str(relative)] = content
            except (UnicodeDecodeError, OSError):
                pass

    return files


def analyze_repository(files):
    project = "\n\n".join(
        f"--- {name} ---\n{content}"
        for name, content in files.items()
    )

    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
You are reviewing a small GitHub automation project.

Analyze the repository below.

Identify:
1. Bugs or problems
2. Missing tests
3. Security concerns
4. Useful improvements

Do NOT write or modify any files.
Return a concise list of recommendations.

Repository:

{project}
""",
    )

    return response.output_text


if __name__ == "__main__":
    print("AI Automation Agent")
    print("===================")

    files = read_project_files()

    print(f"Files found: {len(files)}")

    analysis = analyze_repository(files)

    print("\nAI ANALYSIS")
    print("===========")
    print(analysis)
