
import logging
import ConfigParser
import argparse
from monkeyrunner import MonkeyRunner

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Monkey runner')
    parser.add_argument('--config', default='../monkey.config',
                        dest='config_file', help='configuration file')
    args = parser.parse_args()

    runner = MonkeyRunner(args.config_file)
    runner.unleash()
