import json
from flask import Blueprint, Response, render_template, redirect, request, send_file, url_for, current_app, jsonify
from flask_login import login_required, current_user, logout_user

import uuid
import io

from db import configs_db as cdb
from parsers.parser import OBJECT_SEP
import parsers.parser as ps
from auth.validate_user_input import check_empty

home_bp = Blueprint(
    "home_bp",
    __name__,
    template_folder="templates",
    static_folder="static"
)


@home_bp.route('/home', methods=['GET'])
@login_required
def home():
    """
    Renders the landing page.
    """
    return render_template("home/home.html")


@home_bp.route('/edit-template', methods=['GET'])
@login_required
def template():
    """
    Gets the template editing page
    ready for user.
    """
    code = request.args.get('code')
    return render_template('home/template.html', code=code)


@home_bp.route('/save-template', methods=['POST'])
@login_required
def save_template():
    """
    Saves template into database.
    """
    data = request.json

    objects = []
    packages = []

    # concatenates the information
    # into object strings
    for object in data['objects']:
        objects.append("{}{}{}".format(object['is_file'], OBJECT_SEP, object['object']))
    
    # gets every package from the JSON dictionary
    for package in data['packages']:
        packages.append(package)
    
    # saves configs to database
    config_str = ps.create_config(objects, packages)

    # checks if name or description are empty, and is therefore invalid input
    if check_empty(data['name']) or check_empty(data['description']):
        return Response(status=404, mimetype="application/json", response=json.dumps(
            {'error': "Please make sure name and description aren't empty!"}
        ))

    # if no data code is found, the template must be saved to the database
    if data['code'] == 'None':
        cdb.insert_config(current_user.get_uuid(), data['name'], data['description'], config_str, current_app.config['db'])
    # if a data code is found, the template must be updated in the database
    else:
        cdb.update_config(uuid.UUID(data['code']), current_user.get_uuid(), data['name'], data['description'], config_str, current_app.config['db'])
    
    # returns a successful response
    return Response(status=200, content_type="application/json", response=json.dumps({
        'success': True
    }))


@home_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    Logs out user and returns them
    to landing page.
    """
    logout_user()
    return redirect('/')


@home_bp.route('/get-templates', methods=['POST'])
@login_required
def get_templates():
    """
    Returns a JSON response containing
    all templates.
    """
    templates = cdb.get_all_configs(current_user.get_uuid(), current_app.config['db'])

    return jsonify(templates)


@home_bp.route('/get-template', methods=['POST'])
@login_required
def get_template():
    """
    Gets a template given a code,
    returning a JSON response.
    """
    code_dict = request.json
    code = code_dict['code']
    config = cdb.get_config(code, current_user.get_uuid(), current_app.config['db'])
    data = ps.parse_config(config['config'])
    data['sep'] = OBJECT_SEP
    data['name'] = config['name']
    data['description'] = config['description']
    json_data = jsonify(data)
    return json_data


@home_bp.route('/delete-template', methods=['POST'])
@login_required
def delete_template():
    """
    Deletes a template given a
    code in JSON.
    """
    code_dict = request.json
    code = code_dict['code']
    cdb.delete_config(code, current_user.get_uuid(), current_app.config['db'])

    return json.dumps(({'success':True}, 200, {'ContentType':'application/json'}))


@home_bp.route('/download-template', methods=['POST'])
@login_required
def make_file():
    """
    Makes the config.ini file for a given
    template.
    """
    code = request.form.get('code')
    config = cdb.get_config(code, current_user.get_uuid(), current_app.config['db'])

    def generate():
        yield config['config']
    
    response = Response(generate(), mimetype='text/plain')
    response.headers['Content-Disposition'] = 'attachment; filename={}.txt'.format(config['name'])
    return response
