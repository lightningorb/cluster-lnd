# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2023-02-10 09:00:10
# @Last Modified by:   lnorb.com
# @Last Modified time: 2023-02-10 10:11:23

import sys
import json
import functools
from invoke import task
from time import sleep

from simple_chalk import chalk


def wait(func):
    """
    This is a waiter function. It tries running the given function,
    and patiently waits 5 seconds if it fails before trying again.
    """

    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except:
                sleep(5)

    return wrapper_decorator


def run_cmd(c, cmd_name, cmd, env={}):
    renv = dict(NETWORK="simnet")
    renv.update(env)
    print(chalk.green(cmd), end=" ")
    sys.stdout.flush()
    try:
        res = getattr(c, cmd_name)(cmd, env=renv, hide=True)
    except Exception as e:
        print("...")
        sys.stdout.flush()
        raise e
    print("⚡❌"[res.failed])
    return res


run = lambda c, cmd: run_cmd(c, "run", cmd=cmd)
sudo = lambda c, cmd: run_cmd(c, "sudo", cmd=cmd)


@task
def docker(c, cmd):
    return sudo(c, f"docker {cmd}")


exec = lambda c, name, cmd: docker(c, f"exec -i {name} {cmd}")
lncli = lambda c, name, cmd: exec(c, name, f"lncli --network=simnet {cmd}")

# the j function is just shorthand for loading json
j = lambda x: json.loads(x.stdout if hasattr(x, "stdout") else x)
