from mysql.connector import *
import hashlib

HOST = "localhost"
USER = "root"
PASSWORD = "#spectro@paws&&123"
DATABASE = "carebuddy"
USERS_TABLE = "users"
CARETAKERS = "serviceproviders"


def authenticate(username, password):
    connector = connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    cursor = connector.cursor()
    cursor.execute("select * from " + USERS_TABLE + " where username=%s", (username,))
    fetched_user = cursor.fetchone()
    if not fetched_user:
        return None

    if fetched_user[3] == hashlib.md5(password.encode()).hexdigest():
        return fetched_user


# format: user(id, name, username, password, gender, role)
def create_user(user: tuple):
    connector = connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    cursor = connector.cursor()

    user_id, name, username, password, gender, role = user
    password_hash = hashlib.md5(password.encode()).hexdigest()

    # check if the user already exists
    cursor.execute("select * from " + USERS_TABLE + " where username=%s", (username,))

    if cursor.fetchone():
        return False

    # create user
    cursor.execute("insert into " + USERS_TABLE + " values(%s, %s, %s, %s, %s, %s)",
                   (user_id, name, username, password_hash, gender, role))
    if role != 0:
        cursor.execute("insert into " + CARETAKERS + " values(%s, %s, null, %s)", (user_id, username, int(False)))

    connector.commit()
    return True


def delete_account(username, password):
    # authenticate user before deletion
    if not authenticate(username, password):
        return False

    # delete authenticated user
    connector = connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    cursor = connector.cursor()
    cursor.execute("delete from " + USERS_TABLE + " where username=%s", (username,))
    cursor.execute("delete from " + CARETAKERS + " where username=%s", (username,))
    connector.commit()
    return True
