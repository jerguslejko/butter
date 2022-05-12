import subprocess
from typing import List, Optional
from logging import getLogger
from butter import config


logger = getLogger(__name__)

###

def supervisorctl(commands: List[str], capture_output: bool = False) -> Optional[str]:
    return _run("supervisorctl", commands, capture_output=capture_output)

def supervisord(commands: List[str], capture_output: bool = False) -> Optional[str]:
    return _run("supervisord", commands, capture_output=capture_output)

def _run(program, arguments: List[str], capture_output: bool = False) -> Optional[str]:
    process = subprocess.run(
        [program, "-c", config.path("supervisor.conf")] + arguments,
        capture_output=capture_output,
    )

    if capture_output and process.returncode == 0:
        return process.stdout.decode().strip()

###

def refresh(f):
    def wrapper(*args, **kwargs):
        if supervisorctl(["pid"], capture_output=True) is None:
            logger.info("starting supervisord...")
            supervisord([])

        config.refresh()

        supervisorctl(["update"], capture_output=True)

        return f(*args, **kwargs)

    return wrapper

###

@refresh
def start(programs: List[str]) -> None:
    supervisorctl(["start"] + programs)

@refresh
def restart(programs: List[str]) -> None:
    supervisorctl(["restart"] + programs)

@refresh
def stop(programs: List[str]) -> None:
    supervisorctl(["stop"] + programs)

@refresh
def status(programs: List[str]) -> None:
    supervisorctl(["status"] + programs)

@refresh
def logs(program: str, follow: bool) -> None:
    supervisorctl(["tail"] + (["-f"] if follow else []) + [f"{program}"])
