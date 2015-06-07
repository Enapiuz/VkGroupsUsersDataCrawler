import sys
import argparse
from . import users_reciever
from . import users_parser


def get_users():
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-g', '--group')
    args = argParser.parse_args()
    group = args.group or ''

    if len(group) == 0:
        sys.exit(1)

    users = users_reciever.recieve_users(group)

    if len(users) > 0:
        users_parser.parse(users, 'vk')
