import os
from contextlib import contextmanager
import kodiswift


@contextmanager
def preserve_cwd(cwd):
    existing = os.getcwd()
    os.chdir(cwd)
    yield
    os.chdir(existing)


@contextmanager
def preserve_cli_mode(cli_mode):
    existing = kodiswift.CLI_MODE
    kodiswift.CLI_MODE = cli_mode
    yield
    kodiswift.CLI_MODE = existing
