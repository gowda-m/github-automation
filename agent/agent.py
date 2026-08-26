from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def list_project_files():
    excluded = {".git"}

    files = []

    for path in ROOT.rglob("*"):
        if path.is_file() and not any(part in excluded for part in path.parts):
            files.append(path.relative_to(ROOT))

    return files


if __name__ == "__main__":
    print("AI Automation Agent")
    print("===================")
    print()
    print("Files in this repository:")

    for file in list_project_files():
        print(f"- {file}")
