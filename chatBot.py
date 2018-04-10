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

    # To get the Job Id,User type,Session Id,Transaction Id,User response,Date from UI
    if request.method == 'GET':
        jobs_id=request.args.get('jobs_id')
        usertype = request.args.get('usertype')
        Sessionid = request.args.get('Sessionid')
        Transid = request.args.get('Transid')
        user_question = request.args.get('msg')
        date = request.args.get('date')
        Sessionid = re.sub('"', '', Sessionid)

        # Setting the initial values for the variables stored in Redis
        if redis_store.get(Sessionid +':question') == None:
            redis_store.set(Sessionid +':question',"0")
            redis_store.set(Sessionid +':prev_intent', " ")
            redis_store.set(Sessionid +':flag', "y")
            redis_store.set(Sessionid + ':preq_status',"progress")
        if user_question:
            user_question=unicode(user_question)
            response = interpreter.parse(user_question.lower())
            # Get the intent name from the dictionary
            key = response['intent']['name']
            confidence_score= response['intent']['confidence']
            current_date=str(datetime.datetime.now())
            # Checks if the entity list is empty or not
            response_state = getstate(key, jobs_id, Sessionid,confidence_score)
            preq_status = redis_store.get(Sessionid + ':preq_status')
            dic_to_user = {
                'jobs_id': jobs_id,
                'usertype': usertype,
                'Sessionid': Sessionid,
                'Transid': Transid,
                'msg': user_question,
                'response': response_state,
                'date': current_date,
                'confidence_score': confidence_score,
                'intent_type': key,
                'preq_status': preq_status
            }
            print(response_state,preq_status)
            return json.dumps(dic_to_user)


@app.route('/flushall')
def flush_redis():
    # To clear the redis
    redis_store.flushdb()
    return "Success"


if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0',port=5201)
    app.run(debug=True)