
import argparse
import logging
import logging.config
from ConfigParser import ConfigParser
from monkeyhorde import MonkeyHorde

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Monkey runner')
    parser.add_argument('--config', default='../monkey.config',
                        dest='config_file', help='configuration file')
    args = parser.parse_args()
    config = ConfigParser()
    config.read(args.config_file)
    logging.config.fileConfig(args.config_file)
    runner = MonkeyHorde(config)
    runner.unleash()
