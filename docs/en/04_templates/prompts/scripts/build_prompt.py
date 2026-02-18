from pathlib import Path
import yaml

TEMPLATE_PATH = Path("./quest-plan.template.md")
SEED_PATH = Path("./quest-seed.yaml")
OUTPUT_PATH = Path("./quest-plan.prompt.md")


def load_template(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Seed YAML not found: {path}")

    # YAML 유효성 검증 + 원문 유지
    raw = path.read_text(encoding="utf-8")
    yaml.safe_load(raw)  # parse check only
    return raw


import re


def inject_seed_into_template(template: str, seed_yaml: str) -> str:
    marker_start = "<attached_file>"
    marker_end = "</attached_file>"

    attached_block = (
        f"{marker_start}\n"
        f"{seed_yaml.strip()}\n"
        f"{marker_end}"
    )

    # 1️⃣ attached_file 블록이 이미 존재 → 교체
    if marker_start in template and marker_end in template:
        before = template.split(marker_start)[0]
        after = template.split(marker_end)[1]
        return before + attached_block + after

    # 2️⃣ 없으면 <input> 내부에 삽입
    input_pattern = re.compile(r"<input>(.*?)</input>", re.DOTALL)

    match = input_pattern.search(template)
    if not match:
        raise ValueError("Template missing <input> block")

    input_inner = match.group(1).rstrip()

    new_input_block = (
        "<input>\n"
        + input_inner
        + "\n\n"
        + attached_block
        + "\n</input>"
    )

    return template[:match.start()] + new_input_block + template[match.end():]

def main():
    template = load_template(TEMPLATE_PATH)
    seed_yaml = load_yaml(SEED_PATH)

    result = inject_seed_into_template(template, seed_yaml)

    OUTPUT_PATH.write_text(result, encoding="utf-8")
    print(f"✅ Generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
