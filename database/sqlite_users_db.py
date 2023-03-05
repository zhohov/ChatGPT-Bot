import sqlite3
from datetime import datetime


# create users db
def create_users_db() -> None:
    global connect, cursor
    try:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS users_table(id INTEGER, username TEXT, responses INEGER DEFAULT 0, max_responses INTEGER DEFAULT 10, subscription INTEGER DEFAULT 0, subscription_end_date INTEGER DEFAULT 0)')
        connect.commit()
        print('База данных успешно подключена')

    except:
        print('Ошибка подключения к базе данных')


# add new user in db
def add_user(id: int, username: str) -> None:
    check_unique_id = cursor.execute('SELECT * FROM users_table WHERE id = ?', (id,)).fetchone()

    if check_unique_id:
        print('Пользователь уже существует')

    else:
        cursor.execute('INSERT INTO users_table(id, username) VALUES(?, ?);', (id, username))
        connect.commit()


# check the number of responses if the user is not subscribed
def check_responses(id: int) -> int:
    responses = cursor.execute("SELECT responses FROM users_table WHERE id = ?", (id,)).fetchone()
    return responses[0]


# check the max number of responses if the user is not subscribed
def check_max_responses(id: int) -> int:
    max_responses = cursor.execute("SELECT max_responses FROM users_table WHERE id = ?", (id,)).fetchone()
    return max_responses[0]


# update the number of responses
def update_responses(id: int, responses_update: int) -> None:
    cursor.execute('UPDATE users_table SET responses = ? WHERE id = ?', (responses_update, id))
    connect.commit()


# update subscription to 1 if user buy subscription
def update_subscription(id: int) -> None:
    cursor.execute('UPDATE users_table SET subscription = 1 WHERE id = ?', (id,))
    connect.commit()


# update subscription to 0 (remove subscription)
def remove_subscription(id: int) -> None:
    cursor.execute('UPDATE users_table SET subscription = 0 WHERE id = ?', (id,))
    connect.commit()


# remove subscription end date after the end of subscription
def remove_subscription_end_date(id: int) -> None:
    cursor.execute('UPDATE users_table SET subscription_end_date = 0 WHERE id = ?', (id,))
    connect.commit()


# remove_number_of_responses
def remove_number_of_responses(id: int) -> None:
    cursor.execute('UPDATE users_table SET responses = 0 WHERE id = ?', (id,))
    connect.commit()


# update subscription end date if user buy subscription
def update_subscription_end_date(id: int) -> None:
    date = datetime.today().replace(microsecond=0)
    timestamp_date = int(datetime.timestamp(date))
    timestamp_date += 60 * 60 * 24 * 30
    cursor.execute('UPDATE users_table SET subscription_end_date = ? WHERE id = ?', (timestamp_date, id))
    connect.commit()


# check subscription
def check_subscription(id: int) -> bool:
    subscription = cursor.execute('SELECT subscription FROM users_table WHERE id = ?', (id,)).fetchone()
    if subscription[0] == 1:
        return True

    else:
        return False


# check subscription end date
def check_subscription_end_date(id: int) -> int:
    end_date = cursor.execute('SELECT subscription_end_date FROM users_table WHERE id = ?', (id,)).fetchone()
    return end_date[0]


# check number users
def check_number_users() -> int:
    users = cursor.execute('SELECT * FROM users_table').fetchall()
    return len(users)


# check number subscription users
def check_number_of_subscription_users() -> int:
    users = cursor.execute('SELECT * FROM users_table WHERE subscription = 1').fetchall()
    return len(users)