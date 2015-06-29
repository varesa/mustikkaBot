#
# Handler for changed file locations between versions etc.
#
# Author: Esa Varemo
#

import os
import logging


def do_migrations(bot):
    log = logging.getLogger("mustikkabot.migrations")

    old_conf_path = os.path.join(bot.basepath, "src", "config.txt")
    new_conf_dir = bot.confdir
    new_conf_path = os.path.join(new_conf_dir, "config.txt")

    if os.path.isfile(old_conf_path):
        log.info("Found config.txt file at old location, moving")
        os.rename(old_conf_path, new_conf_path)
    if os.path.isfile(os.path.join(bot.basepath, "src", "commands.json")):
        log.info("Commands-datafile found at old location, moving")
        os.rename(os.path.join(bot.basepath, "src", "commands.json"), os.path.join(bot.datadir, "commands.json"))

def setup(bot):
    log = logging.getLogger("mustikkabot.setup")

    if not os.path.isdir(bot.confdir):
        os.mkdir(bot.confdir)
        log.info("Created config directory")

    if not os.path.isdir(bot.datadir):
        os.mkdir(bot.datadir)
        log.info("Created data directory")