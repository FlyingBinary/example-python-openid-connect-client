##########################################################################
# Copyright 2016 Curity AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

import base64
import json
import random
import string
import ssl


def base64_urldecode(s):
    ascii_string = str(s)
    ascii_string += '=' * (4 - (len(ascii_string) % 4))
    return base64.urlsafe_b64decode(ascii_string)


def base64_urlencode(s):
    return base64.urlsafe_b64encode(s).split("=")[0].replace('+', '-').replace('/', '_')


def decode_token(token):
    """
    Decode a jwt into readable format.

    :param token:
    :return: A decoded jwt, or None if its not a JWT
    """
    parts = token.split('.')

    if token and len(parts) == 3:
        return base64_urldecode(parts[0]), base64_urldecode(parts[1])

    # It's not a JWT
    return None


def generate_random_string(size=20):
    """
    :return: a random string with a default size of 20 bytes using only ascii characters and digits
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


def get_ssl_context(config):
    """
    :return a ssl context with verify and hostnames settings
    """
    ctx = ssl.create_default_context()

    if 'verify_ssl_server' in config and not bool(config['verify_ssl_server']):
        print 'Not verifying ssl certificates'
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    if 'protocol' in config:
        protocol_numbers = {v:k for k,v in ssl._PROTOCOL_NAMES.iteritems()}
        if config['protocol'] in protocol_numbers:
            print 'Setting protocol to %s' % config['protocol']
            ctx.protocol = protocol_numbers[config['protocol']]
        else:
            print 'Unexpected protocol value %s' % config['protocol']
            print 'Continuing with default value'
    return ctx


def print_json(map):
    print json.dumps(map, indent=4, sort_keys=True)


def get_item_from_json(json_tuple, part, item):
    """

    :param json_tuple: a tuple or single json encoded string
    :param part: which part of the tuple, must be zero for single string
    :param item: name of the item to extract
    :return: value of the required item if found, else none
    """
    json_string = ""
    if isinstance(json_tuple, tuple):
        if part not in range(len(json_tuple)):
            return None
        json_string = json_tuple[part]
    if isinstance(json_tuple, str):
        if part != 0:
            return None
        json_string = json_tuple
    if not json_string:
        return None
    try:
        item_value = json.loads(json_string)[item]
    except ValueError:
        return None
    return item_value
