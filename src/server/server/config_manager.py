import yaml


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
            try:
                with open(config) as file:
                    self.config = yaml.safe_load(file)
            except IOError:
                raise IOError(f"Could not read {config} as file")
        else:
            try:
                self.config = yaml.safe_load(config)
            except IOError:
                raise TypeError(f"Could not read {config} as stream")

    def get(self, item, default=None):
        """
        Get an item from loaded config or default value

        Args:
            item (str): Item to get
            default (str, optional): optional default value. Defaults to None.

        Returns:
            dict: retrieved item
        """
        return self.config.get(item, default)

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
        result = self.get(item)
        if result is None:
            raise KeyError(f"{item} not found in config")
        return result