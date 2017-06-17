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

    def delete(self, item_name, item_id, flag_purge=False):
        """ Wrapper to GLPI DELETE """
        item = {}
        try:
            item = self.glpi.delete(item_name, item_id, force_purge=flag_purge)
        except Exception as e:
            item = "{ \"error_message\": \"%s\" }" % e

        return item

    def update(self, item_name, payload):
        """ Wrapper to GLPI UPDATE """
        item = {}
        try:
            item = self.glpi.update(item_name, payload)
        except Exception as e:
            item = "{ \"error_message\": \"%s\" }" % e

        return item


def get_prompt_yes_or_no(msg_input):
    """
    Show an prompt msg and check answer was yes/no/unknown.
    @return status of return and message_err

    status = 0 (yes), 1 (no), 2(unknonw)
    message_err = Error message when 1 or 2 was found
    """

    msg_output = ""
    msg_code = 2
    yes = set(['yes', 'y', 'ye', ''])
    no = set(['no', 'n'])

    msg_answer = raw_input(msg_input).lower()
    if msg_answer in yes:
        msg_code = 0
    elif msg_answer in no:
        msg_code = 1
        msg_output = "Ok, aborting..."
    else:
        msg_code = 2
        msg_output = "Please respond with 'yes' or 'no'."

    return msg_code, msg_output


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

    parser.add_argument("-f", "--force", action="store_true",
                        dest="flag_force", required=False, default=False,
                        help="Force changes.")

    parser.add_argument("-v", "--verbose", action="store_true",
                        dest="flag_verbose", required=False, default=False,
                        help="Verbose.")

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
            item = cli.get(args.item_name, args.item_id)

            if 'id' not in item:
                print("ID not found in GLPI server. Aborting...")
                sys.exit(1)

            print json.dumps(item,
                             indent=4,
                             separators=(',', ': '),
                             sort_keys=True)

            if not args.flag_force:
                msg = "The item will deleted, do you want to continue? [y/n]"
                rc, rm = get_prompt_yes_or_no(msg)
                if rc > 0:
                    print(rm)
                    sys.exit(1)

            print("Deleting item ID {}".format(args.item_id))
            print json.dumps(cli.delete(args.item_name, args.item_id),
                             indent=4,
                             separators=(',', ': '),
                             sort_keys=True)
        except Exception as e:
            print('{ "error_message": "delete: %s" }' % e)

    elif (args.command == 'update'):
        try:
            item = cli.get(args.item_name, args.item_id)
            k_update = {}

            if 'id' not in item:
                print("ID not found in GLPI server. Aborting...")
                sys.exit(1)

            payload = json.loads(args.item_payload)

            # looking for changes
            for k in payload:
                if k not in item:
                    if 'notFound' not in k_update:
                        k_update['notFound'] = {}
                    k_update['notFound'].update({k: payload[k]})
                    continue

                if k == 'id':
                    continue

                if payload[k] == item[k]:
                    if 'notChanged' not in k_update:
                        k_update['notChanged'] = {}
                    k_update['notChanged'].update({k: payload[k]})
                    continue

                if 'change' not in k_update:
                    k_update['change'] = {}

                k_update['change'].update({k: payload[k]})

            if args.flag_verbose:
                print("Original Item: ")
                print json.dumps(item,
                                 indent=4,
                                 separators=(',', ': '),
                                 sort_keys=True)

            if 'notFound' in k_update:
                print("The key(s) bellow was not found: ")
                print(json.dumps(k_update['notFound'], indent=4))

            if 'notChanged' in k_update:
                print("The key(s) bellow was not changed: ")
                print(json.dumps(k_update['notChanged'], indent=4))

            if 'change' not in k_update:
                print("Nothing to change, exiting...")
                sys.exit(0)

            print("Changing the key(s) bellow: ")
            print(json.dumps(k_update['change'], indent=4))
            if args.flag_verbose:
                print("Detailed changes: ")
                change_log = []
                for k in k_update['change']:
                    changes = {
                        k: {
                            "current": item[k],
                            "new": k_update['change'][k]
                        }
                    }
                    change_log.append(changes)
                print(json.dumps(change_log, indent=4))

            if not args.flag_force:
                rc, rm = get_prompt_yes_or_no("Do you want to continue? [y/n]")
                if rc > 0:
                    print(rm)
                    sys.exit(1)

            k_update['change'].update({"id": args.item_id})
            payload = k_update['change']

            print("Updating the item ID {}".format(args.item_id))
            print(json.dumps(cli.update(args.item_name, payload),
                             indent=4,
                             separators=(',', ': '),
                             sort_keys=True))

        except Exception as e:
            print('{ "error_message": "update: %s" }' % e)

    else:
        msg = ("Command [{}] not found".format(args.command))
        print('{ "error_message": "%s" }' % msg)
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
