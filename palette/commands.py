# -*- coding: utf-8 -*-
"""Click commands."""
import os
from glob import glob
from subprocess import call

import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from flask.helpers import get_debug_flag
from .settings import DevConfig, ProdConfig


HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


@click.command()
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main([TEST_PATH, '--verbose'])
    exit(rv)


@click.command()
@click.option('-f', '--fix-imports', default=False, is_flag=True,
              help='Fix imports using isort, before linting')
def lint(fix_imports):
    """Lint and check code style with flake8 and isort."""
    skip = ['requirements']
    root_files = glob('*.py')
    root_directories = [
        name for name in next(os.walk('.'))[1] if not name.startswith('.')]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo('{}: {}'.format(description, ' '.join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    if fix_imports:
        execute_tool('Fixing import order', 'isort', '-rc')
    execute_tool('Checking code style', 'flake8')


@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.

    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)


@click.command()
@click.option('--url', default=None,
              help='Url to test (ex. /static/image.png)')
@click.option('--order', default='rule',
              help='Property on Rule to order by (default: rule)')
@with_appcontext
def urls(url, order):
    """Display all of the url matching routes for the project.

    Borrowed from Flask-Script, converted to use Click.
    """
    rows = []
    column_length = 0
    column_headers = ('Rule', 'Endpoint', 'Arguments')

    if url:
        try:
            rule, arguments = (
                current_app.url_map
                           .bind('localhost')
                           .match(url, return_rule=True))
            rows.append((rule.rule, rule.endpoint, arguments))
            column_length = 3
        except (NotFound, MethodNotAllowed) as e:
            rows.append(('<{}>'.format(e), None, None))
            column_length = 1
    else:
        rules = sorted(
            current_app.url_map.iter_rules(),
            key=lambda rule: getattr(rule, order))
        for rule in rules:
            rows.append((rule.rule, rule.endpoint, None))
        column_length = 2

    str_template = ''
    table_width = 0

    if column_length >= 1:
        max_rule_length = max(len(r[0]) for r in rows)
        max_rule_length = max_rule_length if max_rule_length > 4 else 4
        str_template += '{:' + str(max_rule_length) + '}'
        table_width += max_rule_length

    if column_length >= 2:
        max_endpoint_length = max(len(str(r[1])) for r in rows)
        # max_endpoint_length = max(rows, key=len)
        max_endpoint_length = (
            max_endpoint_length if max_endpoint_length > 8 else 8)
        str_template += '  {:' + str(max_endpoint_length) + '}'
        table_width += 2 + max_endpoint_length

    if column_length >= 3:
        max_arguments_length = max(len(str(r[2])) for r in rows)
        max_arguments_length = (
            max_arguments_length if max_arguments_length > 9 else 9)
        str_template += '  {:' + str(max_arguments_length) + '}'
        table_width += 2 + max_arguments_length

    click.echo(str_template.format(*column_headers[:column_length]))
    click.echo('-' * table_width)

    for row in rows:
        click.echo(str_template.format(*row[:column_length]))


@click.command()
def powermode(path='palette/', recursive=True):
    """Hot reload tests and db schema."""
    schema_patterns = ["*models.py"]
    tests_ignore_patterns = ["*__pycache__", "*.webassets-cache"]

    class SchemaHandler(PatternMatchingEventHandler):
        def on_modified(self, event):
            commands = ['flask db migrate', 'flask db upgrade']
            for command in commands:
                print(event)
                print('Running:', command)
                rv = call(command.split(' '))
                if rv != 0:
                    exit(rv)
                print('Triggered by:', event.src_path)

    class TestsHandler(PatternMatchingEventHandler):
        def on_modified(self, event):
            commands = ['flask test']  # , 'flask run'
            for command in commands:
                print(event)
                print('Running:', command)
                rv = call(command.split(' '))
                if rv != 0:
                    exit(rv)
                print('Triggered by:', event.src_path)

    observer = Observer()
    schema_handler = SchemaHandler(patterns=schema_patterns)
    tests_handler = TestsHandler(ignore_patterns=tests_ignore_patterns)
    observer.schedule(schema_handler, path, recursive)
    observer.schedule(tests_handler, path, recursive)
    print('Watching:', path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def print_dict_items(dikt):
    for k, v in dikt.items():
        if not k.startswith('__'):  # exclude builtin class members
            print('  ', k, v)


@click.command()
def vars():
    """Show environment vars and config settings."""
    if get_debug_flag():
        CONFIG = DevConfig
    else:
        CONFIG = ProdConfig
    print('\n * Environment variables:')
    print_dict_items(os.environ)
    print('\n * App settings:')
    print_dict_items(CONFIG.__dict__)
    print('\n * Overlapping keys:')
    keys = [k for k in os.environ.keys() if k in CONFIG.__dict__.keys()]
    for key in keys:
        env_val = os.environ[key]
        app_val = CONFIG.__dict__[key]
        if env_val == app_val:
            print('  ', key, 'same')
        else:
            print('  ', key, 'diff')
            print('      ', '(env)', env_val)
            print('      ', '(app)', app_val)
