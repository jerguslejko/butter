import os
from configparser import ConfigParser

from butter.schema import Config


def write(config: Config, path: str) -> None:
    parser = ConfigParser()

    parser[f"group:{config.name}"] = {
        "programs": ", ".join(
            f"{config.name}-{program.name}" for program in config.programs
        )
    }

    for program in config.programs:
        parser[f"program:{config.name}-{program.name}"] = {
            "command": f'/bin/bash -c "{program.command}"',
            "directory": os.path.join(config.path, program.working_directory),
            # TODO: escape values
            "environment": ", ".join(
                f"{key}={value}" for key, value in (program.env or {}).items()
            ),
            "redirect_stderr": "true",
            "autostart": "true",
            "autorestart": "true",
            "stopasgroup": "true",
            "killasgroup": "true",
        }

    with open(path, "w") as f:
        parser.write(f, space_around_delimiters=False)
