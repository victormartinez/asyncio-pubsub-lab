import argparse
import importlib.util
from pathlib import Path
from typing import Any
import asyncio


def load_module(name: str) -> Any:
    filepath = Path.cwd() / f"src/{name}.py"
    spec = importlib.util.spec_from_file_location(name, filepath)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(module)  # type: ignore
    return module


if __name__ == "__main__":
    CHOICES = ["command", "query"]
    parser = argparse.ArgumentParser()
    parser.add_argument("-module", required=True, choices=CHOICES)
    result = vars(parser.parse_args())
    module = load_module(result["module"])
    asyncio.run(module.execute())
