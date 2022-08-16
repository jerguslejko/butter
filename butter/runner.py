import os
import shlex

from butter import config, supervisor
from butter.schema import Command


def run(command: Command, extra_args: list[str] = None) -> None:
    path = config.load().path
    namespace = config.load().name

    if command.mode == "downtime":
        supervisor.stop([f"{namespace}:*"])

    os.chdir(os.path.join(path, command.working_directory))

    if extra_args:
        os.system(command.command + " " + shlex.join(extra_args))
    else:
        os.system(command.command)

    if command.mode == "downtime":
        supervisor.start([f"{namespace}:*"])
