import subprocess
from typing import List, Optional, Tuple
from logging import getLogger
from butter import config
from typing import List
from logging import getLogger
from butter import config, supervisor


logger = getLogger(__name__)


def pid():
    return supervisorctl(["pid"], capture_output=True)



def ensure_running():
    if pid() is not None:
        return

    logger.info("starting supervisord...")
    supervisord([])



def start(programs: Tuple[str]) -> None:
    ensure_running()

    supervisorctl(["start"] + list(programs))


def restart(programs: List[str]) -> None:
    ensure_running()

    logger.info("restarting supervisord...")

    supervisorctl(["restart"] + list(programs))



def status(programs: Tuple[str]) -> None:
    ensure_running()

    supervisorctl(["status"]+list(programs))


def stop(programs:Tuple[str]) -> None:
    ensure_running()

    supervisorctl(["stop"] + list(programs))

def reload() -> None:
    ensure_running()

    supervisorctl(["reload"], capture_output=True)

def logs(program: str, follow: bool):
    supervisorctl(["tail"] + (["-f"] if follow else []) + [f"{program}"])


def supervisorctl(commands: List[str], capture_output: bool = False):
    return _run("supervisorctl", commands, capture_output=capture_output)

def supervisord(commands: List[str], capture_output: bool = False):
    return _run("supervisord", commands, capture_output=capture_output)

def _run(program, arguments: List[str], capture_output: bool = False) -> Optional[str]:
    process = subprocess.run(
           [program, "-c", config.path("supervisor.conf")]+
        arguments,
        capture_output=capture_output,
    )

    if capture_output and process.returncode == 0:
        return process.stdout.decode().strip()
