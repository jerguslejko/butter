#!/usr/bin/env python -u

import os
import shutil
import sys
from functools import cache
from logging import getLogger
from pathlib import Path
from typing import List, Tuple

from appdirs import user_config_dir
from confuse import Configuration
from pydantic import ValidationError

from butter.schema import Config
from butter.writer import write

logger = getLogger(__name__)


def path(extra_path="") -> str:
    return os.path.join(os.path.normpath(user_config_dir("butter")), extra_path)


@cache
def load() -> Config:
    def parent_directories(start: str) -> List[str]:
        parents = []
        current = start

        while True:
            parents.append(current)

            if current == "/":
                break

            current = os.path.dirname(current)

        return parents

    def config_files(directories: List[str]) -> List[str]:
        results = []

        for directory in directories:
            if os.path.exists(os.path.join(directory, "butter.yaml")):
                results.append(directory + "/butter.yaml")
            if os.path.exists(os.path.join(directory, "butter.yml")):
                results.append(directory + "/butter.yml")

        return results

    config = Configuration("butter", __name__)
    configs = config_files(parent_directories(os.getcwd()))

    if len(configs) == 0:
        raise RuntimeError("no configuration found")

    for file in configs:
        config.set_file(file)

    try:
        return Config(**config.get(), path=os.path.dirname(file))
    except ValidationError as e:
        print(e)
        sys.exit(1)


def refresh():
    logger.info("refreshing configuration...")

    initialize()

    write(
        config := load(),
        path(f"butters/{config.name}.ini"),
    )


def initialize() -> None:
    config_dir = Path(path())
    butters_dir = Path(path("butters"))

    if not config_dir.exists():
        config_dir.mkdir()

    if not butters_dir.exists():
        butters_dir.mkdir()

    shutil.copyfile(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "../resources/supervisor.conf",
        ),
        path("supervisor.conf"),
    )

    logger.info("all done.")


def dump() -> List[Tuple[Path, str]]:
    results = []

    for file in Path(path()).rglob("*.*"):
        with open(file) as f:
            results.append((file, f.read()))

    return results
