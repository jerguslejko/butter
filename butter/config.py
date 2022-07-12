#!/usr/bin/env python -u

from functools import cache
import os
import sys
import shutil
from logging import getLogger
from typing import List, Tuple
from confuse import Configuration
from pydantic import ValidationError
from appdirs import user_config_dir
from butter.schema import Config
from butter.writer import write
from pathlib import Path

logger = getLogger(__name__)


def path(extra_path="") -> str:
    return os.path.join(os.path.normpath(user_config_dir("butter")), extra_path)


@cache
def load() -> Config:
    def parent_directories(start: str)-> List[str]:
        parents = []
        current = start

        while True:
            parents.append(current)
            
            if current == '/':
                break

            current = os.path.dirname(current)

        return parents

    def config_files(directories: List[str])->List[str]:
        results = []

        for directory in directories:
            if os.path.exists(os.path.join(directory, "butter.yaml")):
                results.append(directory + "/butter.yaml")
            if os.path.exists(os.path.join(directory, "butter.yml")):
                results.append(directory + "/butter.yml")

        return results


    config = Configuration("butter", __name__)

    for file in config_files(parent_directories(os.getcwd())):
        config.set_file(file)

    try:
        return Config(**config.get(), path=os.getcwd())
    except ValidationError as e:
        print(e)
        sys.exit(1)


def refresh():
    logger.info("refreshing configuration...")

    initialize()

    write(
        config:=load(),
        path(f"butters/{config.name}.ini"),
    )


def initialize() -> None:
    config_dir = Path(path())
    butters_dir = Path(path('butters')) 

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


def dump() -> List[Tuple[str, str]]:
    results = []

    for file in Path(path()).rglob("*.*"):
        with open(file) as f:
            results.append((file, f.read()))

    return results
