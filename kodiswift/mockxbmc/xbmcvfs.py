# -*- coding: utf-8 -*-

import os


def exists(target):
    return os.path.exists(target)


def rename(origin, target):
    return os.rename(origin, target)


def delete(target):
    if os.path.isfile(target) and not os.path.isdir(target):
        return os.unlink(target)
    return False


def mkdir(target):
    os.mkdir(target)


def listdir(target):
    return os.listdir(target)
