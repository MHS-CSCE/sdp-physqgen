from json import load
from os.path import join

from physqgen.generator.config import Config


def registerConfig(configFolderPath: str) -> Config:
    """Stores the current Config on server run."""
    # get config on run
    global appConfig
    with open(join(configFolderPath, "active_config.json")) as file:
        with open(join(configFolderPath, load(file)["activeConfigName"])) as configFile:
            appConfig = Config.fromFile(load(configFile))
    return appConfig

