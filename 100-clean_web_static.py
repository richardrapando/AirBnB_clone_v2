#!/usr/bin/python3
# Fabric script that deletes out-of-date archives
import os
from fabric.api import *

env.hosts = ["100.25.39.90", "44.200.178.6"]


def do_clean(number=0):
    """ Fabric script that deletes out-of-date archives.
    Args:
        number (int): number of archives to be kept.
    If number is 0 or 1, most recent archive kept. If
    number is 2, kmost and second-most recent archives kept,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
