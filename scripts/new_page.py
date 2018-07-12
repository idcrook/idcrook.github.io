#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Python script to create a starter template for a blog post."""

__author__ = 'David Crook'
__copyright__ = 'Copyright 2018'
__credits__ = ''
__license__ = 'MIT'
__maintainer__ = 'David Crook'
__email__ = 'idcrook@users.noreply.github.com'

import datetime
import os
import re
from string import Template
import click  # pip3 install click
from titlecase import titlecase  # pip3 install titlecase

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILEPATH = os.path.join(SCRIPT_PATH, 'new_page.template')
OUTPUT_DIR = '_posts'
DEFAULT_IMAGE_NAME = 'images/github-identicon-idcrook.png'

TEMPLATE_FILEOBJ = open(TEMPLATE_FILEPATH, 'r')
TODAY = datetime.date.today()


@click.command()
@click.argument('title')  # TITLE required
@click.option(
    '--mathjax', default=False, is_flag=True, help='Enable mathjax on post.')
@click.option(
    '--comments', default=False, is_flag=True, help='Enable comments on post.')
@click.option(
    '--image',
    default=DEFAULT_IMAGE_NAME,
    type=click.Path(exists=True),
    help='An image for open graph twitter card.')
def cli(title, mathjax, comments, image):
    """Create a new blog post page with TITLE."""
    today_str = TODAY.isoformat()
    title_str = form_title_str_from_title(title)
    output_filepath = os.path.join(OUTPUT_DIR,
                                   form_filename(today_str, title_str))
    if not os.path.exists(image):
        click.secho(
            'WARNING: Cannot find image file "%s"' % image,
            bold=True,
            err=True)
        image = 'images/{imagepath}'

    if image == DEFAULT_IMAGE_NAME:
        click.secho('WARNING: Did not provide an image file', err=True)
        image = 'images/{imagepath}'

    # prepare for template expansion
    d = dict(
        title=title_str,
        date=today_str,
        use_mathjax=mathjax,
        use_comments=comments,
        imagepath=image)

    # click.echo('%s' % title)
    # click.echo('%s' % image)
    # click.echo('%s' % mathjax)
    # click.echo('%s' % comments)
    # click.echo('%s' % today_str)
    # click.echo('%s' % d)

    source = Template(TEMPLATE_FILEOBJ.read())
    output = source.safe_substitute(d)
    try:
        write_file(output_filepath, output)
        click.echo('Wrote %s' % output_filepath)
    except FileExistsError as e:
        click.echo(e.message, err=True)
        click.secho(
            'Change name or remove file and try again', bold=True, err=True)


def form_title_str_from_title(title):
    """Do any simple string normalization here."""
    s = titlecase(title)
    return s


def sanitize_title_str_for_filename(title_str):
    """Do any string normalization needed for a filename."""
    # lowercase the title string amd switch whitespace to hyphens
    s = re.sub(r"\s+", '-', title_str.lower())
    # drop apostrophes
    s = re.sub(r"'", '', s)
    return s


def form_filename(today_str, title_str):
    """Returns a string based on date and title strings for post filename."""
    title_fname_str = sanitize_title_str_for_filename(title_str)
    s = today_str + '-' + title_fname_str + '.md'
    return s


def write_file(filepath, contents):
    if os.path.exists(filepath):
        raise FileExistsError(filepath, 'Output file "%s" exists' % filepath)
    with open(filepath, 'w') as output:
        output.write(contents)


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class FileExistsError(Error):
    """Exception raised for output file existing.

    Attributes:
        filepath -- path to file that exists
        message -- explanation of the error
    """

    def __init__(self, filepath, message):
        self.filepath = filepath
        self.message = message


if __name__ == '__main__':
    cli()
