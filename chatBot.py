from flask import request
from model import interpreter
from state_flow import getstate
import redis
import json
import re
import datetime
from flask import Flask,session
import data_base
app = Flask(__name__)
redis_store= redis.StrictRedis("localhost")
expiry_seconds = 600
global jobs_id
status=''
candidate_id=''.join(datetime.datetime.now().strftime('%H:%M:%S')+'@example.com')
# candidate_id='17:42:47@example.com'
@app.route('/chat', methods=['POST', 'GET'])
def send_response():
    if request.method == 'GET':
        jobs_id=request.args.get('jobs_id')
        usertype = request.args.get('usertype')
        Sessionid = request.args.get('Sessionid')
        Transid = request.args.get('Transid')
        user_question = request.args.get('msg')
        date = request.args.get('date')
        Sessionid = re.sub('"', '', Sessionid)
        if redis_store.get(Sessionid +':question') == None:
            redis_store.set(Sessionid +':question',"0")
            redis_store.set(Sessionid +':prev_intent', " ")
        if user_question:
            user_question=unicode(user_question)
            response = interpreter.parse(user_question.lower())
            #get the intent name from the dictionary
            key = response['intent']['name']
            current_date=str(datetime.datetime.now())
            #Checks if the entity list is empty or not
            if not response['entities']:
                entity_name=None
                entity_value=None
            else:
                entity_name = response['entities'][0]['entity']
                entity_value=response['entities'][0]['value']
            #Checks the status of the candidate whether it is old or new
            candidate_status=data_base.check_candidateid(candidate_id)
            #Stores the candidate status in redis
            if candidate_status==False:
                status='new candidate'
                redis_store.set(Sessionid,'new candidate')
                response_state = getstate(key, jobs_id, Sessionid,status)
            elif candidate_status==True and (redis_store.get(Sessionid)!=None):
                status = 'new candidate'
                response_state = getstate(key, jobs_id, Sessionid,status)
            else:
               status='old candidate'
               response_state = getstate(key, jobs_id, Sessionid,status,entity_value,candidate_id)
               #data_base.insert_db(jobs_id,candidate_id,response_state,user_question,entity_name,entity_value,current_date)
            dic_to_user = {
                'jobs_id': jobs_id,
                'usertype': usertype,
                'Sessionid': Sessionid,
                'Transid': Transid,
                'msg': user_question,
                'response': response_state,
                'date': current_date
            }
            return json.dumps(dic_to_user)

@app.route('/flushall')
def flush_redis():
    redis_store.flushdb()
    return "Success"

if __name__ == '__main__':
    app.run(debug=True)
