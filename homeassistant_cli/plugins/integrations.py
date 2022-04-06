"""Integration (registry) plugin for Home Assistant CLI (hass-cli)."""
import logging
import re
import sys
from typing import Any, Dict, List, Pattern  # noqa

import click

import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
import homeassistant_cli.const as const
import homeassistant_cli.helper as helper
import homeassistant_cli.remote as api

_LOGGING = logging.getLogger(__name__)


@click.group('integrations')
@pass_context
def cli(ctx):
    """Get info and operate on integrations from Home Assistant (EXPERIMENTAL)."""


@cli.command('list')
@click.argument('integrationfilter', default=".*", required=False)
@pass_context
def listcmd(ctx: Configuration, integrationfilter: str):
    """List all integrations from Home Assistant."""
    ctx.auto_output("table")

    integrations = api.get_integrations(ctx)

    result = []  # type: List[Dict]
    if integrationfilter == ".*":
        result = integrations
    else:
        integrationfilterre = re.compile(integrationfilter)  # type: Pattern

        for integration in integrations:
            if integrationfilterre.search(integration['name']):
                result.append(integration)

    cols = [('NAME', 'name'), ('DOMAIN', 'domain'), ('VERSION', 'version'),
            ('BUILT IN', 'is_built_in')]

    ctx.echo(
        helper.format_output(
            ctx, result, columns=ctx.columns if ctx.columns else cols
        )
    )


@cli.command('info')
@click.argument('domain', required=True)
@pass_context
def infocmd(ctx: Configuration, domain: str):
    """List all integrations from Home Assistant."""
    ctx.auto_output("table")

    integrations = api.setup_info(ctx, domain)

    ctx.echo(
        helper.format_output(
            ctx, integrations, columns=ctx.columns
        )
    )
