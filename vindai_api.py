import requests
import json
import re
import redis as redis_store

def Fetch_JobQuestions(jobid,clientid = "VAccess20171",clientname = "ChatBotAccess") :
    try:
        print(jobid)
        jobid = re.sub('"', '', jobid)
        url = 'http://vind.ai/getjobpreqdetails.asmx/getJobDetails?clientid='+ clientid + '&clientname=' + clientname + '&jobid=' + jobid
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


def Fetch_Question(preq,question_number,total_question):
    try:
       #Compared the question_number with the TotalPreQQuestions
         while int(question_number) <= int(total_question) :
            for every_preq in preq:
                   if str(every_preq.get("PreQid")) == str(question_number):
                        print(question_number)
                        return every_preq.get("PreQQuestion")
         else:

            return "Thank you! We will get back to you soon... I can help you if you have any other questions."


    except:

        print("Unable to get prequalified question for this job ")

