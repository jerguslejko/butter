import os
from butter.schema import Config
from configparser import ConfigParser


def write(config: Config, path: str) -> None:
    parser = ConfigParser()

    parser[f"group:{config.name}"] = {
        "programs": ", ".join(f"{config.name}-{program.name}" for program in config.programs)
    }

    for program in config.programs:
        parser[f"program:{config.name}-{program.name}"] = {
            "command": program.command,
            "directory": os.path.join(config.path, program.working_directory),
            "redirect_stderr": "true",
            "autostart": "true",
            "autorestart": "true",
            "stopasgroup": "true",
            "killasgroup": "true",
        }

    with open(path, "w") as f:
        parser.write(f, space_around_delimiters=False)
