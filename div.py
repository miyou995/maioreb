import os
import re


def check_div_balance(file_path):
    """
    Checks if all opening <div> tags in a file have a matching closing </div>.
    Ignores tags inside Django template comments.
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Remove Django template tags to avoid confusion
    content = re.sub(r"{%.*?%}", "", content, flags=re.DOTALL)
    content = re.sub(r"{{.*?}}", "", content, flags=re.DOTALL)

    # Count opening and closing div tags
    open_divs = len(re.findall(r"<\s*div\b", content, flags=re.IGNORECASE))
    close_divs = len(re.findall(r"<\s*/\s*div\s*>", content, flags=re.IGNORECASE))

    return open_divs, close_divs


def scan_html_files(root_folder):
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(subdir, file)
                open_divs, close_divs = check_div_balance(path)
                if open_divs != close_divs:
                    print(f"⚠ ->>>{path}: open={open_divs}, close={close_divs}")


if __name__ == "__main__":
    project_dir = os.getcwd()
    scan_html_files(project_dir)
