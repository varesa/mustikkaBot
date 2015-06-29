#!/bin/env python
#
# A log utility class for twitch/irc bot MustikkaBot
#
# Author: Esa Varemo
#

import logging


def setup_logging(name):
    """
    Setup logging parameters
    :param name: root logger name
    :type name: string
    :return: None
    :rtype: None
    """
    log = logging.getLogger(name)

    log.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setFormatter(LogFormater())
    log.addHandler(sh)


class LogFormater(logging.Formatter):
    """
    Custom log formater to get aligned messages and submodule-"tags"
    """

    formatString1 = '%(asctime)s  [%(name)s]'
    formatString2 = '[%(levelname)s] %(message)s'

    def format(self, record):
        """
        Format an log message for printing
        :param record: log record to format
        :type record: logging.LogRecord
        :return: formated log message
        :rtype: str
        """

        record.name = record.name.split('.')[-1].upper()

        spaces = 23 - len(record.name) - len(record.levelname) - 4

        f1 = logging.Formatter(self.formatString1 + ' '*spaces + self.formatString2, "%Y-%m-%d %H:%M:%S")
        msg = f1.format(record)

        header = ']'.join(msg.split(']')[0:2]) + ']'
        message = ']'.join(msg.split(']')[2:])

        if '\n' in message:
            newmsg = header
            for line in message.splitlines():
                if line == message.splitlines()[0]:
                    newmsg += line
                else:
                    newmsg += '\n' + ' '*(len(header)+1) + line

            return newmsg

        else:
            return msg
