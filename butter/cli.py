#!/usr/bin/env python -u

import os
import logging
import click
from typing import List
from logging import getLogger
from butter import config, supervisor

logger = getLogger(__name__)

@click.group(no_args_is_help=True)
@click.option('-v', '--verbose', 'verbose', is_flag=True)
def cli(verbose:bool):
    if verbose:
        logging.basicConfig(level=logging.INFO)

### 

def validate_program(ctx, param, value) -> str:
    namespace = config.load().name

    if value == "all":
        return value

    if ":" in value:
        return value

    return f"{namespace}:{namespace}-{value}"

def validate_programs(ctx, param, value) -> List[str]: 
    namespace = config.load().name

    if value == ():
        return [f"{namespace}:*"]

    return list(map(lambda value: validate_program(ctx, param, value), value))

###

@cli.command(help="start butter")
@click.argument('programs', callback=validate_programs, nargs=-1)
def start(programs: List[str]):
    supervisor.start(programs)

@cli.command(help="restart butter")
@click.argument('programs', callback=validate_programs, nargs=-1)
def restart(programs: List[str]):
    supervisor.restart(programs)

@cli.command(help="stop butter")
@click.argument('programs', callback=validate_programs, nargs=-1)
def stop(programs: List[str]):
    supervisor.stop(programs)

@cli.command(help="get status of process")
@click.argument('programs', callback=validate_programs, nargs=-1)
def status(programs: List[str]):
    supervisor.status(programs)

@cli.command(help="print logs for a process")
@click.argument("program", callback=validate_program)
@click.option("-f", '--follow', 'follow', is_flag=True)
def logs(program, follow):
    supervisor.logs(program, follow=follow)

@cli.command(help="open web UI")
def ui():
    os.system("open http://localhost:9001")

### helpers

@cli.command(help="passes args to [supervisorctl -c supervisor.conf ...]", hidden=True)
@click.argument("args", nargs=-1)
def ctl(args):
    supervisor.supervisorctl(args)

@cli.command(help="prints rendered supervisor configuration", hidden=True)
def dump():
    for name, contents in config.dump():
        click.echo(click.style(name, bold=True))
        click.echo(contents)


if __name__ == "__main__":
    cli()
