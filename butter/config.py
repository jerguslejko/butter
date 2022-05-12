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
from butter.models import Config
from butter.writer import write
from pathlib import Path

logger = getLogger(__name__)


def path(extra_path="") -> str:
    return os.path.join(os.path.normpath(user_config_dir("butter")), extra_path)


@cache
def load() -> Config:
    config = Configuration("butter", __name__)
    # TODO: add up-level directory
    config.set_file("butter.yml")

    try:
        return Config(**config.get())
    except ValidationError as e:
        print(e)
        sys.exit(1)


def refresh():
    logger.info("refreshing configuration...")

    write(
        config:=load(),
        path(f"butters/{config.name}.ini"),
    )


def initialize(force: bool) -> None:
    config_dir = Path(path())

    if not force and config_dir.exists():
        logger.error("configuration already exists...")
        return

    if force:
        logger.info("removing old installation...")
        shutil.rmtree(config_dir)

    logger.info("installing butter...")

    config_dir.mkdir()
    Path(f"{path()}/butters").mkdir()
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
