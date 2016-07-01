import argparse
from oauth2client import tools

class Cmd:
    def __init__(self):
        tools.argparser.add_argument('--backup-file-name', default='mysql-backup', help='Set backup file name')
        self.arguments = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

    def get_arguments(self):
        return self.arguments
