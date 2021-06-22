import mariadb
import sys

try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost",
        port=3306,
        database="phone_book"
    )
    conn.autocommit = True
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()


# decorator wrap to handle db exceptions
def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except mariadb.Error as e:
            print(f"Error executing MariaDB query: {e}")
            sys.exit(1)
    return wrapper


def init_db():
    """create the tables (users, records)"""
    # users table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTO_INCREMENT,"
        "name VARCHAR(255) NOT NULL,"
        "email VARCHAR(255) NOT NULL,"
        "password VARCHAR(30) NOT NULL,"
        "birthdate DATE);"
    )

    # users' phone records table
    cur.execute("CREATE TABLE IF NOT EXISTS records ("
                "id INTEGER PRIMARY KEY AUTO_INCREMENT,"
                "ownerID INTEGER,"
                "name VARCHAR(255),"
                "phone VARCHAR(22),"
                "birthdate DATE);")


def populate_db():
    # fill the db with sample data
    import csv
    create_user("test", "test@test.test", "2000-01-01", "12345")

    with open('../../sample_data.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            create_record(1, *row)


@handle_exception
def create_user(name, email, birthdate, password):
    users = []
    # attempt to find the same user
    cur.execute(f"SELECT name FROM users WHERE "
                f"name='{name}' AND "
                f"email='{email}' AND "
                f"birthdate='{birthdate}';")
    for name in cur:
        users.append(name)
    # return True if the same user already exists
    if users:
        return True
    # otherwise creates a new one with the given credentials
    cur.execute(f"INSERT INTO users "
                f"(name, email, password, birthdate)"
                f" VALUES (?, ?, ?, ?);",
                (name, email, password, birthdate))

    return False


@handle_exception
def authenticate(name, password):
    user = {}
    cur.execute(f"SELECT id, name, email from users "
                f"WHERE name='{name}' AND password='{password}';")
    for (user_id, name, email) in cur:
        user = {'name': name, 'email': email, 'user_id': user_id}
    return user


@handle_exception
def get_celebrants(user_id):
    # returns a list of celebreants for the next 7 days
    records = []
    cur.execute(f"SELECT name, birthdate FROM records "
                f"WHERE 1 = "
                f"(FLOOR(DATEDIFF(DATE_ADD(DATE(NOW()), INTERVAL 7 DAY), birthdate)/365.25))-"
                f"(FLOOR(DATEDIFF(DATE(NOW()), birthdate)/365.25)) "
                f"AND ownerID={user_id} ORDER BY birthdate ASC;")
    for record in cur:
        records.append(record)
    return records


@handle_exception
def create_record(user_id, name, phone, bdate):
    records = []
    cur.execute(f"SELECT name FROM records "
                f"WHERE ownerID=? AND "
                f"name=? AND "
                f"phone=? AND "
                f"birthdate=?;", (user_id, name, phone, bdate))
    for record in cur:
        records.append(record)
    if records:
        return False

    cur.execute(f"INSERT INTO records "
                f"(ownerID, name, phone, birthdate) VALUES "
                f"(?, ?, ?, ?)", (user_id, name, phone, bdate))

    return True


@handle_exception
def delete_record(user_id, name, phone, bdate):
    cur.execute(f"DELETE FROM records "
                f"WHERE ownerID=? AND "
                f"name=? AND "
                f"phone=? AND "
                f"birthdate=?;", (user_id, name, phone, bdate))


@handle_exception
def update_record(user_id, old_record, new_record):
    records = []
    cur.execute(f"SELECT * FROM records "
                f"WHERE ownerID=? AND "
                f"name=? AND "
                f"phone=? AND "
                f"birthdate=?;", [user_id]+new_record)
    for record in records:
        records.append(record)
    if records and records[0] != old_record:
        return False

    cur.execute(f"UPDATE records SET "
                f"name=?, phone=?, birthdate=? "
                f"WHERE ownerID=? AND name=? AND "
                f"phone=? AND birthdate=?;",
                new_record+[user_id]+old_record)

    return True


@handle_exception
def get_records(user_id, letterset):
    # splits letters into a form of: '(^A)|(^C)' for RLIKE querying
    params = '|'.join([f'(^{letter})' for letter in letterset])
    query = f"SELECT name, phone, birthdate FROM records WHERE " \
            f"ownerID=? AND name RLIKE ? " \
            f"ORDER BY name;"

    cur.execute(query, (user_id, params))
    data = []
    for record in cur:
        data.append(record)
    return data


if __name__ == "__main__":
    #: Uncomment to create tables
    init_db()

    #: Uncomment to populate the db with sample data
    populate_db()
    sys.exit(1)
