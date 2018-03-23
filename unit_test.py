import requests
import  json
i = 11
job_id='3258599'
usertype='R'
candidateid=1
Sessionid='45455KI'
date='2017-12-02%2011:42:60:300'
Transid='1'
chatresponse=""
while i >10:
    user_input =  raw_input("Enter Text : ")
    payload = {'user_question': user_input}
    urls='http://127.0.0.1:5000/chat?jobs_id=' + job_id  + '&usertype=' + usertype + '&Sessionid=' + Sessionid+ '&Transid=' + Transid + '&msg=' + user_input + '&date=' + date + '&chatresponse=' + chatresponse
    print(urls)
    r = requests.get(urls)
    print(r.text)
    data=json.loads(r.text)
    chatresponse=data['response']
    print(chatresponse)