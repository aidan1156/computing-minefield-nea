import sqlite3
import hashlib
import string
import random
import datetime

import path_generation

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
        cur.close()
        conn.close()
        token, cookie_token = create_token(user_id)

    conn.commit()
    cur.close()   
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
        SELECT design_id FROM designs 
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

        sql= f'''
            SELECT COUNT(attempts.FK_design_id),MIN(attempts.time) FROM attempts 
            WHERE FK_design_id='{result[i][0]}'
        '''

        cur.execute(sql)
        stats = cur.fetchall()

        if stats[0][1] == None:
            time = ' - '
        else:
            time = int(stats[0][1])
            mins = str(time // 60)
            seconds = str(time % 60)
            if len(seconds) == 1:
                seconds = '0'+seconds
            time = mins+':'+seconds

        data.append({
            'design_id':result[i][0],
            'attempts':stats[0][0],
            'time':time,
            'pattern':pattern
        })

    cur.close()
    conn.close()

    return data
    
def get_owner_of_design(design_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    sql= f'''
        SELECT FK_user_id FROM designs 
        WHERE design_id='{design_id}'
    '''

    cur.execute(sql)
    result = cur.fetchall()

    cur.close()
    conn.close()

    return result[0][0]

def get_design(design_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    sql= f'''
        SELECT x,y FROM design_pattern
        WHERE FK_design_id='{design_id}'
    '''

    cur.execute(sql)
    result = cur.fetchall()

    cur.close()
    conn.close()

    return result

def save_design(design_id,pattern):
    design_id = int(design_id)
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    sql= f'''
        DELETE FROM design_pattern
        WHERE FK_design_id='{design_id}'
    '''

    cur.execute(sql)

    sql= f'''
        UPDATE designs
        SET edited_on = '{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        WHERE design_id='{design_id}'
    '''

    cur.execute(sql)

    if len(pattern) != 0:
        values = ''

        for i in range(len(pattern)):##generate the sql we convewrt from int back to string for sql cleaning
            values += '('+str(design_id)+','+str(int(pattern[i][0]))+','+str(int(pattern[i][1]))+')'
            if i != len(pattern) - 1:
                values += ','

        sql= f'''
            INSERT INTO design_pattern
            VALUES {values}
        '''

        cur.execute(sql)

    cur.close()
    conn.commit()
    conn.close()
    
def create_new_design(user_id,auto_generate):
    ##create a new design
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    sql= f'''
        INSERT INTO designs (FK_user_id, created_on, edited_on, auto_generated)
        VALUES ('{user_id}','{date}','{date}','{int(auto_generate)}')
    '''

    cur.execute(sql)

    sql = '''SELECT last_insert_rowid();'''
    cur.execute(sql)
    design_id = cur.fetchall()[0][0]

    cur.close()
    conn.commit()
    conn.close()

    if auto_generate:
        pattern = path_generation.generate_path()
        save_design(design_id,pattern)

    return design_id