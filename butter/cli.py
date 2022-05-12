#!/usr/bin/env python -u

import os
import logging
from typing import Tuple
import click
from logging import getLogger
from butter import config, supervisor


logger = getLogger(__name__)


@click.group(no_args_is_help=True)
@click.option('-v', '--verbose', 'verbose', is_flag=True)
def cli(verbose:bool):
    if verbose:
        logging.basicConfig(level=logging.INFO)

### 

def validate_program(ctx, param, value):
    namespace = config.load().name

    if value == "all":
        return value

    if ":" in value:
        return value

    return f"{namespace}:{value}"

def validate_programs(ctx, param, value):
    namespace = config.load().name

    if value == ():
        return (f"{namespace}:*",)

    return tuple(map(lambda value: validate_program(ctx, param, value), value))



### butter-specific


@cli.command(help="initialize butter project")
@click.option("--force", is_flag=True)
def init(force):
    config.initialize(force=force)


### helpers


@cli.command(help="open web UI")
def ui():
    os.system("open http://localhost:9001")


@cli.command(help="passes args to [supervisorctl -c supervisor.conf ...]", hidden=True)
@click.argument("args", nargs=-1)
def ctl(args):
    supervisor.supervisorctl(list(args))

@cli.command(help="prints rendered supervisor configuration", hidden=True)
def dump():
    for name, contents in config.dump():
        click.echo(click.style(name, bold=True))
        click.echo(contents)


### supervisord-specific


@cli.command(help="start butter")
@click.argument('programs', callback=validate_programs, nargs=-1)
def start(programs: Tuple[str]):
    config.refresh()
    supervisor.reload()

    supervisor.start(programs)


@cli.command(help="restart butter")
@click.argument('programs', callback=validate_programs, nargs=-1)
def restart(programs:Tuple[str]):
    config.refresh()

    supervisor.restart(programs)


@cli.command(help="stop butter")
@click.argument('programs', callback=validate_programs, nargs=-1)
def stop(programs:Tuple[str]):
    config.refresh()

    supervisor.stop(programs)


### supervisorctl-specific


@cli.command(help="get status of process")
@click.argument('programs', callback=validate_programs, nargs=-1)
def status(programs: Tuple[str]):
    supervisor.status(programs)


@cli.command(help="print logs for a process")
@click.argument("program", callback=validate_program)
@click.option("-f", '--follow', 'follow', is_flag=True)
def logs(program, follow):
    supervisor.logs(program=program, follow=follow)



if __name__ == "__main__":
    cli()
