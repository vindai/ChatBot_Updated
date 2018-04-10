import requests
import json
import re
import redis

redis_store = redis.StrictRedis("localhost")


def Fetch_JobQuestions(jobid,clientid = "VAccess20171",clientname = "ChatBotAccess") :
   '''

   :param jobid: jobid
   :param clientid:clientid
   :param clientname: clientname
   :return: total_question - (int) total number of preq questions, preq - list of preq questions
   '''
   try:
        jobid = re.sub('"', '', jobid)
        url = 'http://uat.techfetch.com/getjobpreqdetails.asmx/getJobDetails?clientid='+ clientid + '&clientname=' \
              + clientname + '&jobid=' + jobid
        r = requests.get(url)
        json_parsed = json.loads(r.text)

        preq = []
        for k in json_parsed.keys():
            for item in json_parsed[k]:
                preq = item['JobPreQ']
                total_question = item['TotalPreQQuestions']
        return total_question,preq
   except:
        print("Unable to access vind.ai jobdetails " + r.status_code)


def Fetch_Question(preq,question_number,total_question,Sessionid):
    '''

    :param preq: preq question
    :param question_number: number of question like 1, 2, 3
    :param total_question:  total number of preq questions

    :param Sessionid: id for the particular session
    :return: prequalification question, returns each question when called
    '''
    try:
        # Compared the question_number with the TotalPreQQuestions
        while int(question_number) <= int(total_question) :
            for every_preq in preq:
                 if str(every_preq.get("PreQid")) == str(question_number):
                      print(question_number)
                      return every_preq.get("PreQQuestion")
        else:
            redis_store.set(Sessionid + ':flag',"n")
            redis_store.set(Sessionid + ':preq_status', "preqend")
            print(redis_store.get(Sessionid + ':preq_status'))
            return "Thank you! We will get back to you soon...If you have any queries related to travel/ payrate/ job/ visa kindly leave a message."

    except Exception as e:
        print(e)
        print("Unable to get prequalified question for this job")
