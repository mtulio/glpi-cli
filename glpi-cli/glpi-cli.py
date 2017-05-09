#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2017 Predict & Truly Systems All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# GLPI API Rest documentation:
# https://github.com/glpi-project/glpi/blob/9.1/bugfixes/apirest.md
# GLPI API Rest Python SDK:
# https://github.com/truly-systems/glpi-sdk-python

import json
import os
import sys
from dotenv import load_dotenv, find_dotenv
from glpi import GLPI
import argparse


load_dotenv(find_dotenv())
global glpi
glpi = glpi_url = glpi_user = glpi_pass = glpi_token = None


class CLI(object):

    def __init__(self):
        self.glpi = None
        self.load_env()

    def load_env(self):
        url = os.getenv("GLPI_API_URL") or None
        user = os.getenv("GLPI_USERNAME") or None
        password = os.getenv("GLPI_PASSWORD") or None
        token = os.getenv("GLPI_APP_TOKEN") or None

        if url is None:
            print "You should set GLPI_API_URL with API Rest URL"
            sys.exit(1)
        if user is None:
            print "You should set GLPI_USERNAME with API Rest URL"
            sys.exit(1)
        if password is None:
            print "You should set GLPI_PASSWORD with API Rest URL"
            sys.exit(1)
        if token is None:
            print "You should set GLPI_APP_TOKEN with API Rest URL"
            sys.exit(1)

        self.glpi = GLPI(url, token, (user, password))

    """ Common operations """
    def get(self, item_name, item_id):
        """ Wrapper to GLPI GET """
        item = {}
        try:
            item = self.glpi.get(item_name, item_id)
        except Exception as e:
            item = "{ \"error_message\": \"%s\" }" % e

        return item

    def get_all(self, item_name):
        """ Wrapper to GLPI Item """
        item = {}
        try:
            item = self.glpi.get_all(item_name)
        except Exception as e:
            item = "{ \"error_message\": \"%s\" }" % e

        return item


if __name__ == '__main__':
    """
    This CLI catch user entry and call GLPI Rest using GLPI SDK.
    Options allowed:
    --item    : Item Name
    --id      : ID of Item
    --command : CMD
    """

    parser = argparse.ArgumentParser(prog='glpi-cli',
                                     usage='%(prog)s --item item_name '
                                     '--command cmd [options]')

    parser.add_argument("--item", metavar='i', dest="item_name",
                        required=True,
                        help="GLPI Item Name. [ticket, knownbase]")

    parser.add_argument("--command", metavar='n', dest="command",
                        required=True,
                        help="Command could be: [get|get_all].")

    parser.add_argument("--id", metavar='n', dest="item_id",
                        type=int,
                        help="GLPI Item ID.")

    parser.add_argument("--payload", metavar='p', dest="item_payload",
                        help="GLPI Item Payload to be updated.")

    args = parser.parse_args()
    cli = CLI()
    item_dict = {}

    # ID should be defined in...
    if (args.command == 'get') or \
       (args.command == 'delete') or \
       (args.command == 'update'):
        if not args.item_id:
            print '{ "error_message": "This command requires --id optio" }'
            sys.exit(1)

    if (args.command == 'get'):
        print json.dumps(cli.get(args.item_name, args.item_id),
                         indent=4,
                         separators=(',', ': '),
                         sort_keys=True)

    elif (args.command == 'get_all'):
        print json.dumps(cli.get_all(args.item_name),
                         indent=4,
                         separators=(',', ': '),
                         sort_keys=True)

    elif (args.command == 'delete'):
        print '{ "error_message": "Option unavailable yet" }'

    elif (args.command == 'update'):
        print '{ "error_message": "Option unavailable yet" }'

    else:
        msg = "Command [%s] not found" % (args.command)
        print "{ \"message\": \"%s\" }" % msg

    sys.exit(0)
