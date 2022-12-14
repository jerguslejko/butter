#!/usr/bin/env python -u

import logging
import os
from logging import getLogger
from typing import List

import click

from butter import config, runner, supervisor
from butter.schema import Command

logger = getLogger(__name__)


@click.group(no_args_is_help=True)
@click.option("-v", "--verbose", "verbose", is_flag=True)
@click.option("--config-path", "config_path")
def cli(verbose: bool, config_path: str | None):
    if config_path:
        config.register(config_path)

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


def validate_command(ctx, param, value) -> str:
    for command in config.load().commands:
        if command.name == value:
            return command

    raise click.BadParameter(f"command {value} not found")


###


@cli.command(help="start butter")
@click.argument("programs", callback=validate_programs, nargs=-1)
def start(programs: List[str]):
    supervisor.start(programs)


@cli.command(help="restart butter")
@click.argument("programs", callback=validate_programs, nargs=-1)
def restart(programs: List[str]):
    supervisor.restart(programs)


@cli.command(help="stop butter")
@click.argument("programs", callback=validate_programs, nargs=-1)
def stop(programs: List[str]):
    supervisor.stop(programs)


@cli.command(help="get status of process")
@click.argument("programs", callback=validate_programs, nargs=-1)
def status(programs: List[str]):
    supervisor.status(programs)


@cli.command(help="print logs for a process")
@click.argument("program", callback=validate_program)
@click.option("-f", "--follow", "follow", is_flag=True)
def logs(program, follow):
    supervisor.logs(program, follow=follow)


@cli.command(help="open web UI")
def ui():
    os.system("open http://localhost:9001")


@cli.command(
    help="run a custom command",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
@click.argument("command", callback=validate_command)
@click.pass_context
def run(ctx, command: Command):
    runner.run(command, extra_args=ctx.args)


# helpers


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
