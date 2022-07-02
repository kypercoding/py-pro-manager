"""
Methods that handle common user
account functions, such as
registration, validation,
and deletion.
"""

from psycopg2 import connect
from contextlib import closing

from auth import password_handler as ph
from auth import uuid_handler as uh


def register(username, email, password, params):
    """
    Registers a user, given a unique
    username, email, and a password.
    """
    try:
        # generate key
        key = ph.generate_key(password)

        # generate random v4 uuid for user
        uuid = uh.generate_uuid_v4()

        # store the email, key, salt,
        # and uuid into the database
        with connect(params) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("""
                PREPARE insert_user (UUID, TEXT, TEXT, TEXT) AS
                INSERT INTO users VALUES($1, $2, $3, $4);

                EXECUTE insert_user('{}', '{}', '{}', '{}');
                """.format(uuid, username, email, key))
        
        return True
    except Exception as e:
        print(e)
        return False


def validate_user(username, password, params):
    """
    Validates a user against their
    password hash.
    """
    # retrieves username and key hash from database to verify
    with connect(params) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("""
            PREPARE validate_user (TEXT) AS
            SELECT password FROM users
            WHERE username = $1;

            EXECUTE validate_user('{}');
            """.format(username))

            # retrieve hash
            row = cursor.fetchone()
            
            if row == None:
                return False

            hash = str(row[0])

            # verify
            return ph.validate_key(password, hash)


def get_by_uuid(uuid, params):
    """
    Obtains user information by
    unique UUID.
    """
    with connect(params) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                """
                PREPARE get_user_info (UUID) AS
                SELECT uuid, username, email FROM users
                WHERE uuid = $1;

                EXECUTE get_user_info('{}');
                """.format(uuid)
            )

            # retrieve user info
            row = cursor.fetchone()

            if row == None:
                return None
            
            uuid = row[0]
            username = str(row[1])
            email = str(row[2])

            return {
                'uuid': uuid,
                'username': username,
                'email': email
            }


def get_by_user(user, params):
    """
    Obtains user information by
    unique username.
    """
    with connect(params) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                """
                PREPARE get_user_info (TEXT) AS
                SELECT uuid, username, email FROM users
                WHERE username = $1;

                EXECUTE get_user_info('{}');
                """.format(user)
            )

            # retrieve user info
            row = cursor.fetchone()

            if row == None:
                return None
            
            uuid = row[0]
            username = str(row[1])
            email = str(row[2])

            return {
                'uuid': uuid,
                'username': username,
                'email': email
            }


def delete(username, password):
    """
    Given a username, delete an account,
    provided that they provide the correct
    password.
    """
    pass


def check_user(username):
    """
    Check that a user is
    present in the database.
    """
    return False


def check_uuid(username):
    """
    Check that a user-unique uuid
    already exists in the database.
    """

    return False


def check_user_and_email(username, email):
    """
    Check that a user and email combination
    exists in the database.
    (i.e. user is registered
    in the database with username
    "brian21" and email "brian21@gmail.com").
    """

    return False


def change_pass(username, new_pass):
    """
    Change the password for username's account.
    """
    pass
