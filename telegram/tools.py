# -*- coding: utf-8 -*-

import flectra
import flectra.tools.config as config
from flectra import SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)


def get_parameter(dbname, key):
    db = flectra.sql_db.db_connect(dbname)
    flectra.registry(dbname).check_signaling()
    with flectra.api.Environment.manage(), db.cursor() as cr:
        env = flectra.api.Environment(cr, SUPERUSER_ID, {})
        return env['ir.config_parameter'].get_param(key)


def running_workers_num(workers):
    res = 0
    for r in workers:
        if r._running:
            res += 1
    return res


def db_list():
    if config['db_name']:
        db_names = config['db_name'].split(',')
    else:
        db_names = flectra.service.db.list_dbs(True)
    return db_names


def get_int_parameter(dbname, key, default=1):
    num = get_parameter(dbname, key)
    try:
        return int(num)
    except:
        _logger.info('Wrong value of %s: %s', key, num)
    return default


def token_is_valid(token):
    if token and len(token) > 10:
        _logger.debug('Valid token')
        return True
    _logger.debug('Invalid token')
    return False
