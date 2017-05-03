#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
cli.arguments: default arguments with the ability to override them
'''
import re

from utils.format import fmt
from utils.dictionary import merge
from cli.config import CFG

CALLS_STYLE = [
    'simple',
    'detail',
]

ORGANIZATIONS = [
    'f', 'Mozilla Foundation',
    'c', 'Mozilla Corporation',
]

class WrongBugFormatError(Exception):
    def __init__(self, bug):
        msg = fmt('WrongBugFormatError: string = {bug}')
        super(WrongBugFormatError, self).__init__(msg)

def bug_type(bug):
    pattern = '\d{7,8}'
    regex = re.compile(pattern)
    if regex.match(bug):
        return bug
    raise WrongBugFormatError(bug)

def organization_type(string):
    if string == 'f':
        return 'Mozilla Foundation'
    elif string == 'c':
        return 'Mozilla Corporation'
    return string

# these are the default values for these arguments
ARGS = {
    ('-o', '--organization-name'): dict(
        metavar='ORG',
        required=True,
        choices=ORGANIZATIONS,
        type=organization_type,
        help='which organization to take action under; choices=[%(choices)s]'
    ),
    ('-a', '--authority'): dict(
        metavar='AUTH',
        default=CFG.AUTHORITIES[0],
        choices=CFG.AUTHORITIES,
        help='default="%(default)s"; choose authority; choices=[%(choices)s]'
    ),
    ('-a', '--authorities'): dict(
        metavar='AUTH',
        required=True,
        choices=CFG.AUTHORITIES,
        nargs='+',
        help='default="%(default)s"; choose authorities; choices=[%(choices)s]'
    ),
    ('-d', '--destinations'): dict(
        metavar='DEST',
        required=True,
        choices=CFG.DESTINATIONS,
        nargs='+',
        help='default="%(default)s"; choose destinations; choices=[%(choices)s]'
    ),
    ('-b', '--bug'): dict(
        required=True,
        type=bug_type,
        help='the bug number assocated with this ssl|tls certificate'
    ),
    ('-w', '--within'): dict(
        metavar='DAYS',
        default=14,
        help='default="%(default)s"; within number of days from expiring'
    ),
    ('-s', '--sans'): dict(
        default=[],
        nargs='+',
        help='add additional [s]ubject [a]lternative [n]ame(s)'
    ),
    ('-y', '--validity-years'): dict(
        metavar='YEARS',
        default=1,
        type=int,
        help='default="%(default)s"; choose number of years for certificate'
    ),
    ('--repeat-delta',): dict(
        dest='repeat_delta',
        metavar='SECS',
        default=90,
        type=int,
        help='default="%(default)s"; repeat delta when getting cert from digicert'
    ),
    ('-c', '--calls'): dict(
        const=CALLS_STYLE[0],
        choices=CALLS_STYLE,
        nargs='?',
        help='const="%(const)s"; toggle and choose the call output format; choices=[%(choices)s]'
    ),
    ('-v', '--verbose'): dict(
        metavar='LEVEL',
        dest='verbosity',
        default=0,
        const=1,
        type=int,
        nargs='?',
        help='set verbosity level'
    ),
    ('--verify',): dict(
        action='store_true',
        help='force verification with authority'
    ),
    ('--expired',): dict(
        action='store_true',
        help='show expired certs'
    ),
    ('common_name',): dict(
        metavar='common-name',
        help='the commmon-name to be used for the certificate'
    ),
    ('cert_name_pns',): dict(
        metavar='cert-name',
        default='*',
        nargs='*',
        help='default="%(default)s"; <common-name>@<modhash>; glob expressions '
            'also accepted; if only a common-name is given, "*" will be appended'
    ),
}

# they can be overridden by supplying kwargs to this function
def add_argument(parser, *sig, **overrides):
    parser.add_argument(
        *sig,
        **merge(ARGS[sig], overrides))

