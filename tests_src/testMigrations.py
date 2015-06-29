import os
import shutil

import migrations


class DummyBot():
    basepath = "test_path"
    confdir = os.path.join(basepath, "config")


class TestMigrations():
    bot = DummyBot()
    testdata = "config.txt contents"

    old_conf_dir = os.path.join(bot.basepath, "src")
    new_conf_dir = os.path.join(bot.basepath, "config")

    def setup(self):
        if not os.path.isdir(DummyBot.basepath):
            os.mkdir(DummyBot.basepath)
        if not os.path.isdir(self.old_conf_dir):
            os.mkdir(self.old_conf_dir)

    def teardown(self):
        if os.path.isdir(self.old_conf_dir):
            shutil.rmtree(self.old_conf_dir)
        if os.path.isdir(DummyBot.basepath):
            shutil.rmtree(DummyBot.basepath)

    def test_migrations(self):
        with open(os.path.join(self.old_conf_dir, "config.txt"), 'w') as old_config:     # Setup testcase
            old_config.write(self.testdata)

        assert os.path.isfile(os.path.join(self.old_conf_dir, "config.txt"))             # Test setup
        assert not os.path.isfile(os.path.join(self.new_conf_dir, "config.txt"))

        migrations.do_migrations(self.bot)

        assert not os.path.isfile(os.path.join(self.old_conf_dir, "config.txt"))         # Test that migration was successful
        assert os.path.isfile(os.path.join(self.new_conf_dir, "config.txt"))

        with open(os.path.join(self.new_conf_dir, "config.txt"), 'r') as new_config:
            assert new_config.readline() == self.testdata

        migrations.do_migrations(self.bot)

        assert not os.path.isfile(os.path.join(self.old_conf_dir, "config.txt"))         # Test case where nothing to migrate
        assert os.path.isfile(os.path.join(self.new_conf_dir, "config.txt"))

        with open(os.path.join(self.new_conf_dir, "config.txt"), 'r') as new_config:
            assert new_config.readline() == self.testdata