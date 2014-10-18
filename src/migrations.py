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
        if not os.path.isdir(new_conf_dir):
            log.info("Config directory not found, creating")
            os.mkdir(new_conf_dir)
        os.rename(old_conf_path, new_conf_path)