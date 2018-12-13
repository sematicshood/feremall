import functools
import hashlib
import os
import werkzeug.wrappers
import ast
try:
    import simplejson as json
except ImportError:
    import json
import flectra
from flectra import http
from flectra.http import request
from flectra import fields
from ..rest_exception import *
from contextlib import closing

_logger = logging.getLogger(__name__)
#good

def eval_json_to_data(modelname, json_data, create=True):
    Model = request.env[modelname]
    model_fiels = Model._fields
    field_name = [name for name, field in Model._fields.items()]
    values = {}
    for field in json_data:
        if field not in field_name:
            continue
        if field not in field_name:
            continue
        val = json_data[field]
        if not isinstance(val, list):
            values[field] = val
        else:
            values[field] = []
            if not create and isinstance(model_fiels[field], fields.Many2many):
                values[field].append((5,))
            for res in val:
                recored = {}
                for f in res:
                    recored[f] = res[f]
                if isinstance(model_fiels[field], fields.Many2many):
                    values[field].append((4, recored['id']))

                elif isinstance(model_fiels[field], flectra.fields.One2many):
                    if create:
                        values[field].append((0, 0, recored))
                    else:
                        if 'id' in recored:
                            id = recored['id']
                            del recored['id']
                            values[field].append((1, id, recored)) if len(recored) else values[field].append((2, id))
                        else:
                            values[field].append((0, 0, recored))
    return values


def object_read(model_name, params, status_code):
    try:
        domain = []
        fields = []
        offset = 0
        limit = None
        order = None
        if 'filters' in params:
            domain += ast.literal_eval(params['filters'])
        if 'field' in params:
            fields += ast.literal_eval(params['field'])
        if 'offset' in params:
            offset = int(params['offset'])
        if 'limit' in params:
            limit = int(params['limit'])
        if 'order' in params:
            order = params['order']

        data = request.env[model_name].sudo().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
        if data:
            return valid_response(status=status_code, data={
                'count': len(data),
                'results': data
            })
        else:
            return object_not_found_all(model_name)
    except Exception as e:
        print(str(e))
        return object_not_found_all(model_name)


def object_read_one(model_name, rec_id, params, status_code):
    try:
        fields = []
        if 'field' in params:
            fields += ast.literal_eval(params['field'])
        try:
            rec_id = int(rec_id)
        except Exception as e:
            rec_id = False

        if not rec_id:
            return invalid_object_id()
        data = request.env[model_name].sudo().search_read(domain=[('id', '=', rec_id)], fields=fields)
        if data:
            return valid_response(status=status_code, data=data)
        else:
            return object_not_found(rec_id, model_name)
    except Exception as e:
        print(str(e))
        return object_not_found(rec_id, model_name)



def object_create_one(model_name, data, status_code):
    try:
        res = request.env[model_name].sudo().create(data)
    except Exception as e:
        return no_object_created(e)
    if res:
        return valid_response(status_code, {'id': res.id})


def object_update_one(model_name, rec_id, data, status_code):
    try:
        rec_id = int(rec_id)
    except Exception as e:
        rec_id = None

    if not rec_id:
        return invalid_object_id()

    try:
        
        res = request.env[model_name].sudo().search([('id', '=', rec_id)])        
        if res:
            reslt = res.write(data)
            print(reslt)
            if res is True:
                return valid_response(status_code, {'desc': 'Record Updated successfully!', 'update': True})
        else:
            return object_not_found(rec_id, model_name)
    except Exception as e:
        print(str(e))
        return no_object_updated(e)
    # print(res)
    # if res:
    #     return valid_response(status_code, {'desc': 'Record Updated successfully!', 'update': True})


def object_delete_one(model_name, rec_id, status_code):
    try:
        rec_id = int(rec_id)
    except Exception as e:
        rec_id = None

    if not rec_id:
        return invalid_object_id()

    try:
        res = request.env[model_name].sudo().search([('id', '=', rec_id)])
        if res:
            res.unlink()
        else:
            return object_not_found(rec_id, model_name)
    except Exception as e:
        return no_object_deleted(e)
    if res:
        return valid_response(status_code, {'desc': 'Record Successfully Deleted!', 'delete': True})


def user_auth(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        username = request.httprequest.headers.get('username')
        password = request.httprequest.headers.get('password')
        db_name = request.httprequest.headers.get('db_name')

        #cek header request
        if not username:
            info = "Missing username in request header!"
            error = 'username_not_found'
            _logger.error(info)
            return invalid_response(400, error, info)
        if not password:
            info = "Missing password in request header!"
            error = 'password_not_found'
            _logger.error(info)
            return invalid_response(400, error, info)
        if not db_name:
            info = "Missing database name in request header!"
            error = 'database_name_not_found'
            _logger.error(info)
            return invalid_response(400, error, info)
        
        #check database name
        if check_db_name(db_name) is False:
            info = "Database name is incorrect!!"
            error = 'database_name_incorrect'
            _logger.error(info)
            return invalid_response(400, error, info)
        
        #check user
        uid = request.session.authenticate(db_name, username, password)
        if uid is not False:
            return func(self, *args, **kwargs)
        else:
            info = "Username or Password is incorrect!!"
            error = 'username_or_password_name_incorrect'
            _logger.error(info)
            return invalid_response(400, error, info)
    return wrap

def check_db_name(db_name):
    try:
        temp = False
        print(list_dbs())
        for data in list_dbs():
            if data == db_name:
                temp = True
                return temp    
        return temp
    except Exception as e:
        print(str(e))

def list_dbs():
    try:
        chosen_template = flectra.tools.config['db_template']
        templates_list = tuple(set(['postgres', chosen_template]))
        db = flectra.sql_db.db_connect('postgres')
        with closing(db.cursor()) as cr:
            try:
                db_user = flectra.tools.config["db_user"]
                if not db_user and os.name == 'posix':
                    import pwd
                    db_user = pwd.getpwuid(os.getuid())[0]
                if not db_user:
                    cr.execute("select usename from pg_user where usesysid=(select datdba from pg_database where datname=%s)", (flectra.tools.config["db_name"],))
                    res = cr.fetchone()
                    db_user = res and str(res[0])
                if db_user:
                    cr.execute("select datname from pg_database where datdba=(select usesysid from pg_user where usename=%s) and not datistemplate and datallowconn and datname not in %s order by datname", (db_user, templates_list))
                else:
                    cr.execute("select datname from pg_database where not datistemplate and datallowconn and datname not in %s order by datname", (templates_list,))
                res = [flectra.tools.ustr(name) for (name,) in cr.fetchall()]
            except Exception as e:
                print(str(e))
                res = []
        res.sort()
        return res
    except Exception as e:
        print(str(e))

# Read OAuth2 constants and setup token store:
# db_name = flectra.tools.config.get('db_name')
# if not db_name:
#     _logger.warning("Warning: To proper setup OAuth - it's necessary to "
#                     "set the parameter 'db_name' in flectra config file!")

class ControllerDashboardStudioApi(http.Controller):
    @http.route([
        '/apiku/<model_name>',
        '/apiku/<model_name>/<id>'
    ], type='http', auth="none", methods=['GET'],
        csrf=False)
    @user_auth
    def get_data(self, model_name=False, id=False, **get):
        print("GET")
        if id:
            return object_read_one(model_name, id, get, status_code=200)
        return object_read(model_name, get, status_code=200)
    
    @http.route([
        '/apiku/<model_name>',
        '/apiku/<model_name>/<id>'
    ], type='json', auth="none", methods=['PUT'],
        csrf=False)
    @user_auth  
    def put_data(self, model_name=False, id=False, **put):
        print("PUT")
        put = request.jsonrequest
        return object_update_one(model_name, id, put, status_code=200)

    @http.route([
        '/apiku/<model_name>',
        '/apiku/<model_name>/<id>'
    ], type='json', auth="none", methods=['POST'],
        csrf=False)
    @user_auth  
    def post_data(self, model_name=False, **post):
        print("POST")
        post = request.jsonrequest
        print(post)
        return object_create_one(model_name, post, status_code=200)

    @http.route([
        '/apiku/<model_name>',
        '/apiku/<model_name>/<id>'
    ], type='http', auth="none", methods=['DELETE'],
        csrf=False)
    @user_auth  
    def delete_data(self, model_name=False, id=False):
        print("DELETE")
        return object_delete_one(model_name, id, status_code=200)