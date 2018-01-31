from flask import request
from model import interpreter
from state_flow import getstate
import redis
import json
import re
import datetime
from flask import Flask,session

app = Flask(__name__)
redis_store= redis.StrictRedis("localhost")
expiry_seconds = 600
global jobs_id


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
            redis_store.set(Sessionid +':flag', " ")
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

            response_state = getstate(key, jobs_id, Sessionid,entity_value)
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
