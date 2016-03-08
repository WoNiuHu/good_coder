import ConfigParser


def loadconfig(config_file, block):
    config_info = {}
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    for (k, v) in config.items(block):
        config_info[k] = v
    return config_info
