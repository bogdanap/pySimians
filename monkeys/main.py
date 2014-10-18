
import argparse
from monkeyhorde import MonkeyHorde

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Monkey runner')
    parser.add_argument('--config', default='../monkey.config',
                        dest='config_file', help='configuration file')
    args = parser.parse_args()

    runner = MonkeyHorde(args.config_file)
    runner.unleash()
