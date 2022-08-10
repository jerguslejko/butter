import os
from butter import config, supervisor
from butter.schema import Command

def run(command : Command) -> None:
    path = config.load().path
    namespace = config.load().name

    if command.mode == 'downtime':
        supervisor.stop([f"{namespace}:*"])


    os.chdir(os.path.join(path, command.working_directory))
    os.system(command.command)
    
    if command.mode == 'downtime':
        supervisor.start([f"{namespace}:*"])
