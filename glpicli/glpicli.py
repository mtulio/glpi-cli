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
import argparse
from glpi import GLPI


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

    def delete(self, item_name, item_id, flag_force=False):
        """ Wrapper to GLPI DELETE """
        item = {}
        try:
            item = self.glpi.delete(item_name, item_id)
        except Exception as e:
            item = "{ \"error_message\": \"%s\" }" % e

        return item


def main():
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

    parser.add_argument("-i", "--item", metavar='i', dest="item_name",
                        required=True,
                        help="GLPI Item Name. [ticket, knownbase]")

    parser.add_argument("-c", "--command", metavar='c', dest="command",
                        required=True,
                        help="Command could be: [get|get_all].")

    parser.add_argument("-id", "--id", metavar='id', dest="item_id",
                        type=int, required=False,
                        help="GLPI Item ID.")

    parser.add_argument("-f", "--force", action="store_true", dest="flag_force",
                        required=False, default=False,
                        help="GLPI Item ID.")

    parser.add_argument("-p", "--payload", metavar='p', dest="item_payload",
                        help="GLPI Item Payload to be updated.")

    args = parser.parse_args()

    # ID should be defined in...
    if (args.command == 'get') or \
       (args.command == 'delete') or \
       (args.command == 'update'):
        if not args.item_id:
            print '{ "error_message": "This command requires option --id ID" }'
            sys.exit(1)

    cli = CLI()
    item_dict = {}

    if (args.command == 'get'):
        print json.dumps(cli.get(args.item_name, args.item_id),
                         indent=4,
                         separators=(',', ': '),
                         sort_keys=True)

    elif (args.command == 'get_all'):
        try:
            print json.dumps(cli.get_all(args.item_name),
                             indent=4,
                             separators=(',', ': '),
                             sort_keys=True)
        except Exception as e:
            print('{ "error_message": "get_all: {}".format(e) }')
            sys.exit(1)

    elif (args.command == 'delete'):

        try:
            flag_force = False
            item = cli.get(args.item_name, args.item_id)

            print json.dumps(item,
                             indent=4,
                             separators=(',', ': '),
                             sort_keys=True)

            if not args.flag_force:
                yes = set(['yes','y', 'ye', ''])
                no = set(['no','n'])

                del_answer = raw_input("The item above will deleted, do you want to continue? [y/n]").lower()
                if del_answer in yes:
                    print("deleting")
                elif del_answer in no:
                   print("Ok, aborting...")
                   sys.exit(1)
                else:
                   print("Please respond with 'yes' or 'no'. Aborting")
                   sys.exit(1)

            print("Deleting item ID {}".format(args.item_id) )
            print json.dumps(cli.delete(args.item_name, args.item_id),
                              indent=4,
                              separators=(',', ': '),
                              sort_keys=True)
        except Exception as e:
            print('{ "error_message": "delete: %s" }' % e )

    elif (args.command == 'update'):
        print('{ "error_message": "Option unavailable yet" }')
        sys.exit(1)

    else:
        msg = ("Command [{}] not found".format(args.command))
        print('{ "error_message": "%s" }' % msg)
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
