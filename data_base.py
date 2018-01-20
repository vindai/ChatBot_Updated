import MySQLdb
from flask import session
#connects with Database
def get_connection():
    db = MySQLdb.connect('localhost', 'root', '', 'chat')
    cursor = db.cursor()
    return cursor,db
#inserts chat details to Database
def insert_db(jobs_id,candidate_id,bot_response,user_replies,entity_name,entity_value,date):
    cursor,db = get_connection()
    print(jobs_id,candidate_id,bot_response,user_replies,date)
    sql ="insert into chat_details (job_id,candidate_id,bot_response,user_replies,entity_name,entity_value,date) values ('%s','%s','%s','%s','%s','%s','%s')"%(jobs_id,candidate_id,bot_response,user_replies,entity_name,entity_value,date)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    db.close()
#Checks whether the candidate Id exist in database or not
def check_candidateid(new_id):
    data=[]
    cursor, db = get_connection()
    try:
        cursor.execute("select * from chat_details")
        db.commit()
        results = cursor.fetchall()
        for row in results:
            candidate_id = row[1]
            data.append(candidate_id)
        print(data)
        if new_id in data:
            status = 'old candidate'
            return status
        else:
            status = 'new candidate'
            return status
    except Exception as e:
        db.rollback()
        print(e)
    db.close()
#Checks entity and value of the candidate from the previous chat to check whether they have queried or not.
def check_old_entity(candidate_id):
    response=[]
    entity=[]
    try:
        #gets the Database connection
        cursor, db = get_connection()
        cursor.execute('select entity_name,entity_value from chat_details where candidate_id ="%s" AND entity_value!="None" AND entity_name="visa_type"' % candidate_id)
        db.commit()
        results = cursor.fetchall()
        for value in results:
                entity_value=value[1]
                entity.append(entity_value)
                cursor.execute(
                    'select user_replies from chat_details where candidate_id ="%s" AND entity_value="%s"' % (candidate_id, entity_value))
                db.commit()
                result = cursor.fetchall()
                response.append(''.join(result[0]))
        else:
            print(entity)
            return response,entity
    except Exception as e:
        db.rollback()
        print (e)




