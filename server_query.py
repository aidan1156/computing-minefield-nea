import sqlite3
import hashlib
import string
import random

def hash_data(data):
    encoded = data.encode()
    result = hashlib.sha256(encoded)
    return result.hexdigest()

def clean_for_sql(data):
    return data.replace("'","''")

##check if the given usernam matches the password in the db
def check_password(username,password):
    password = hash_data(password)
    username = clean_for_sql(username)

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    sql= f'''
        SELECT user_id FROM users 
        WHERE username='{username}' AND password='{password}'
    '''

    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()

    if result:
        return result[0][0]
    
    return False

def create_token(user_id):
    ##create and insert a new set of user tokens into the db
    token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
    hashed_token = hash_data(token)

    cookie_token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
    hashed_cookie_token = hash_data(cookie_token)

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    sql= f'''
        INSERT INTO tokens
        VALUES ({user_id},'{hashed_token}','{hashed_cookie_token}')
    '''

    try:##if this fails it means we didnt generate a unique set of tokens
        cur.execute(sql)
    except:##so try again
        token, cookie_token = create_token(user_id)
    finally:
        cur.close()
        conn.commit()
        conn.close()

    return token,cookie_token

def token_to_user_id(token,cookie_token):
    token = hash_data(token)
    cookie_token = hash_data(cookie_token)

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    sql= f'''
        SELECT FK_user_id FROM tokens 
        WHERE user_token='{token}' AND cookie_token='{cookie_token}'
    '''

    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()

    if result:
        return result[0][0]
    
    return False

def get_designs(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    sql= f'''
        SELECT design_id,COUNT(attempts.FK_design_id),MIN(attempts.time) FROM designs 
        LEFT JOIN attempts ON attempts.FK_design_id=design_id
        WHERE FK_user_id='{user_id}'
        ORDER BY edited_on DESC
    '''

    cur.execute(sql)
    result = cur.fetchall()

    

    data = []
    for i in range(len(result)):
        sql= f'''
            SELECT x,y FROM design_pattern 
            WHERE FK_design_id='{result[i][0]}'
        '''

        cur.execute(sql)
        pattern = cur.fetchall()

        time = int(result[i][2])
        mins = str(time // 60)
        seconds = str(time % 60)

        if len(seconds) == 1:
            seconds = '0'+seconds

        data.append({
            'design_id':result[i][0],
            'attempts':result[i][1],
            'time':str(mins)+':'+str(seconds),
            'pattern':pattern
        })

    cur.close()
    conn.close()

    return data
    
    