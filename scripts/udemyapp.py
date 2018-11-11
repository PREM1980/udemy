#!/usr/bin/env python

from __future__ import print_function

"""
the udemy command line utility

"""

import os
import sys
import platform
from pprint import pprint
from configparser import ConfigParser
from builtins import input
from subprocess import call


def configure():    
    config_file = _conf_file()
    api_key = ''
    if os.environ.get('UDEMY_API_KEY'):
        print('The environment variable UDEMY_API_KEY is already set')
        api = os.environ['UDEMY_API_KEY']
    elif os.path.exists(config_file):
        parser = ConfigParser()
        parser.optionxform = str

        with open(config_file, 'r') as fdr:
            parser.readfp(fdr)

            if parser.has_option('udemy', 'UDEMY_API_KEY'):
                api_key = parser.get('udemy', 'UDEMY_API_KEY')

    api_key_input = input('UDEMY_API_KEY: [%s]: ' % _masked_api_key(api_key))

    if api_key_input:
        _setup(api_key_input)
    elif api_key:
        _setup(api_key)


def _setup(api_key):    
    """ write back UDEMY_API_KEY to config file
      config file is at ~/.udemy/config
    """

    os.environ['UDEMY_API_KEY'] = api_key

    conf_file = _conf_file()

    parser = ConfigParser()
    parser.optionxform = str

    if os.path.exists(conf_file):
        parser.readfp(open(conf_file, 'r'))

    if not parser.has_section('udemy'):
        parser.add_section('udemy')

    parser.set('udemy', 'UDEMY_API_KEY', api_key)

    with open(conf_file, 'w') as fdw:
        parser.write(fdw)


def _masked_api_key(api_key):
    return (len(api_key)-4) * '*' + api_key[-4:]


def _conf_file():    
    home_dir = os.environ['HOMEPATH'] if platform.system() == 'Windows' else os.environ['HOME']
    conf_dir = os.path.join(home_dir, '.udemy')
    if not os.path.exists(conf_dir):
        os.mkdir(conf_dir)
    elif not os.path.isdir(conf_dir):
        raise Exception('%s should be a directory, not a file' % conf_dir)    
    return os.path.join(conf_dir, 'config')


def print_help():
    """ show help """

    print("""DESCRIPTION:
    This script helps to set the CLARIFAI_API_KEY environment variable and to diagnose the
    environment in case of troubles
    USAGE:
    clarifai help                Show this help text
    clarifai config              Configure the environment
    clarifai diagnose            Diagnose the environment
    """)


def main():
    if len(sys.argv) < 2:
        print_help()
        exit()

    command = sys.argv[1]
    if command == 'configure' or command == 'config':
        configure()
#     elif command == 'diagnose':
#         diagnose()
    else:
        print_help()


if __name__ == '__main__':
    main()
