from utils import log_message
import yaml
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Configuration manager to load config from yaml filepath or stream
    """

    def __init__(self, config):
        """
        Create a new configuration manager

        Args:
            config (str, stream): filepath or yaml file or yaml stream

        Raises:
            TypeError: config is not filepath or stream
            IOError: could not read config file
        """
        self.config = dict()

        if isinstance(config, str):
            # argument is filepath
            try:
                with open(config) as file:
                    self.config = yaml.safe_load(file)
            except IOError:
                raise IOError(f"Could not read {config} as file")
        else:
            # argument is stream
            try:
                self.config = yaml.safe_load(config)
            except IOError:
                raise TypeError(f"Could not read {config} as stream")

    def get(self, item, default=None):
        """
        Get an item from loaded config or default value

        Args:
            item (str): Item to get
            default (any, optional): optional default value. Defaults to None.

        Returns:
            dict: retrieved item
        """
        if item in self.config:
            return self.config[item]
        log_message(logger, f"Config item {item} not found, using default", logging.WARNING)
        return default

    def __getitem__(self, item):
        """
        get with no default

        Args:
            item (str): item to get

        Raises:
            KeyError: raised if item not found

        Returns:
            dict: retrieved item
        """
        if item not in self.config:
            raise KeyError(f"{item} not found in config")

        return self.config[item]
