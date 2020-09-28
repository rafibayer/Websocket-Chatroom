import unittest
import asyncio
import os
import sys
import test_helper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server')))
from config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):

    def test_from_file(self):
        cfg = ConfigManager("../config/test_config/chat.yaml")
        self.assertIsNotNone(cfg.config)
        self.assertIsInstance(cfg.config, dict)
        self.assertIsNotNone(cfg.get("meta"))
        self.assertEqual(cfg.get("meta"), cfg["meta"])

    def test_fron_stream(self):
        stream = open("../config/test_config/chat.yaml", "r")
        cfg = ConfigManager(stream)
        self.assertIsNotNone(cfg.config)
        self.assertIsInstance(cfg.config, dict)
        self.assertIsNotNone(cfg.get("meta"))
        self.assertEqual(cfg.get("meta"), cfg["meta"])
        stream.close()

    def test_default(self):
        cfg = ConfigManager("../config/test_config/chat.yaml")
        self.assertEqual(cfg.get("BADKEY", "DEFAULT"), "DEFAULT")
        self.assertIsNone(cfg.get("BADKEY"))


if __name__ == "__main__":
    unittest.main()
