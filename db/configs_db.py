"""
Python script intended to
handle interactions with
SqLite database.
"""

from psycopg2 import connect
from contextlib import closing

from . import user_db as udb
import auth.uuid_handler as uh


def get_all_configs(uuid, params):
    """
    Return a list containing codes and
    their corresponding names and descriptions
    by username.
    """

    stmt = """
    PREPARE get_configs (UUID) AS
    SELECT * FROM configs INNER JOIN configs_users
    ON configs.uuid = configs_users.config_uuid
    WHERE configs_users.user_uuid = $1 ORDER BY configs.name;

    EXECUTE get_configs('{}');
    """.format(uuid)


    configs = []

    # obtains each row from statement
    # execution
    with connect(host=params['host'], user=params['user'], password=params['pass'], database=params['database'], port=params['port']) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(stmt)

            rows = cursor.fetchall()

            # return nothing if
            # there are no templates
            if len(rows) == 0:
                return None

            for row in rows:
               # adds bindings for configs
               # dictionary
               configs.append({
                'uuid': str(row[0]),
                'name': str(row[1]),
                'description': str(row[2])
                })
    

    return configs


def get_config(code, user_uuid, params):
    """
    Make dictionary with code, name, and config
    with specific code.
    """

    stmt = """
    PREPARE get_config (UUID, UUID) AS
    SELECT uuid, name, description, config FROM configs, configs_users
    WHERE configs_users.user_uuid = $1
    AND configs.uuid = $2
    AND configs.uuid = configs_users.config_uuid;
    
    EXECUTE get_config('{}', '{}');
    """.format(user_uuid, code)

    with connect(host=params['host'], user=params['user'], password=params['pass'], database=params['database'], port=params['port']) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(stmt)

            row = cursor.fetchone()

            # returns code, name, and config
            return {
                'code': str(row[0]),
                'name': str(row[1]),
                'description': str(row[2]),
                'config': str(row[3])
            }


def insert_config(user_uuid, name, description, config, params):
    """
    Make a new row in the database
    for a configuration.
    """

    uuid = uh.generate_uuid_v4()

    stmt = """
    PREPARE insert_config (UUID, TEXT, TEXT, TEXT) AS
    INSERT INTO configs VALUES ($1, $2, $3, $4);

    EXECUTE insert_config('{}', '{}', '{}', '{}');

    PREPARE insert_pair (UUID, UUID) AS
    INSERT INTO configs_users VALUES ($1, $2);

    EXECUTE insert_pair('{}', '{}');
    """.format(uuid, name, description, config, uuid, user_uuid)

    with connect(host=params['host'], user=params['user'], password=params['pass'], database=params['database'], port=params['port']) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(stmt)


def check_pair(code, user_uuid, params):
    """
    Ensures that a user has
    proper access to a given
    template.
    """
    
    stmt = """
    PREPARE check_pair (UUID, UUID) AS
    SELECT EXISTS (
        SELECT 1 FROM configs_users WHERE config_uuid=$1
        AND user_uuid = $2
    );

    EXECUTE check_pair('{}', '{}');
    """.format(code, user_uuid)

    with connect(host=params['host'], user=params['user'], password=params['pass'], database=params['database'], port=params['port']) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(stmt)

            row = cursor.fetchone()

            if str(row[0]) == 'True':
                return True
            else:
                return False


def update_config(code, user_uuid, name, description, config, params):
    """
    Update a row in the database
    for a configuration.
    """

    if check_pair(code, user_uuid, params) == False:
        return
    
    stmt = """
    PREPARE update_config (TEXT, TEXT, TEXT, UUID) AS
    UPDATE configs
    SET name = $1,
    description = $2,
    config = $3
    WHERE uuid = $4;

    EXECUTE update_config('{}', '{}', '{}', '{}');
    """.format(name, description, config, code)

    with connect(host=params['host'], user=params['user'], password=params['pass'], database=params['database'], port=params['port']) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(stmt)


def delete_config(code, user_uuid, params):
    if check_pair(code, user_uuid, params) == False:
        return
    
    stmt = """
    PREPARE delete_config (UUID, UUID) AS
    WITH j (config_uuid) AS (
    DELETE FROM configs_users WHERE configs_users.user_uuid = $1
    AND configs_users.config_uuid = $2 RETURNING config_uuid)
    DELETE FROM configs USING j WHERE configs.uuid = j.config_uuid;

    EXECUTE delete_config('{}', '{}');
    """.format(user_uuid, code)

    with connect(host=params['host'], user=params['user'], password=params['pass'], database=params['database'], port=params['port']) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(stmt)
