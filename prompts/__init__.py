"""Load prompt templates from YAML"""

from pathlib import Path
import yaml

_PROMPTS_DIR = Path(__file__).parent


def load_prompt(name: str, version: str | None = None) -> str:
    """Return the template string for *name*

    Args:
        name:    Stem of the YAML file, e.g. ``"summarise_paper"``
        version: Explicit version tag such as ``"1.0"``.  Defaults to
                 the value of ``current_version`` in the file
    """
    path = _PROMPTS_DIR / f"{name}.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    tag = version or data["current_version"]
    return data["versions"][tag]["template"]
