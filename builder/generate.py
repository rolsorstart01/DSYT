from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE_ROOT = ROOT / "templates"

TEMPLATE_FILES = [
    "README.md.j2",
    "requirements.txt.j2",
    "app_config.json.j2",
    "run.py.j2",
    ".env.example.j2",
    "app/__init__.py.j2",
    "app/models.py.j2",
    "app/market_engine.py.j2",
    "app/routes.py.j2",
    "app/seed.py.j2",
    "app/templates/base.html.j2",
    "app/templates/index.html.j2",
    "app/templates/market.html.j2",
    "app/templates/leaderboard.html.j2",
    "app/templates/portfolio.html.j2",
    "app/templates/admin.html.j2",
    "app/templates/auth.html.j2",
    "app/static/styles.css.j2",
    "tests/test_generation_smoke.py.j2",
]


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _replace_tokens(content: str, config: dict) -> str:
    mapping = {
        "[[PROJECT_NAME]]": config["project_name"],
        "[[SCHOOL_NAME]]": config["school_name"],
        "[[PRIMARY_COLOR]]": config["primary_color"],
        "[[ACCENT_COLOR]]": config["accent_color"],
        "[[ADMIN_USERNAME]]": config["admin"]["username"],
        "[[ADMIN_PASSWORD]]": config["admin"]["password"],
        "[[APP_CONFIG_JSON]]": json.dumps(config, indent=2),
    }
    for key, value in mapping.items():
        content = content.replace(key, str(value))
    return content


def render_project(config: dict, output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    for rel_path in TEMPLATE_FILES:
        source = TEMPLATE_ROOT / rel_path
        content = source.read_text(encoding="utf-8")
        rendered = _replace_tokens(content, config)
        destination = output_dir / rel_path.replace(".j2", "")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate DSYT no-code trading website")
    parser.add_argument("--config", default="builder/config/default.json", type=Path)
    parser.add_argument("--output", default="output/dsyt_site", type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    render_project(config, args.output)
    print(f"Generated project at {args.output}")


if __name__ == "__main__":
    main()
