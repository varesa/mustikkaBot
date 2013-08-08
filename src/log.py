#!/bin/env python
#
# A log utility class for twitch/irc bot MustikkaBot
#
# Author: Esa Varemo
#


# Store the state of debug messages
logDebuggin = False
printDebugging = False


def printDebug(bool):
    printDebugging = bool


def logDebug(bool):
    logDebugging = bool


def d(str):
    print(str)


def log(str):
    print(str)