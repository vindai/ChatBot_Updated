from vindai_api import Fetch_Question, Fetch_JobQuestions
import redis
import random

# opening redis connection here
redis_store = redis.StrictRedis("localhost")
expiry_seconds = 600
list_intents = []
previous_query=[]
def getstate(key, job_id, Sessionid,*vartuple):
    #gets the prequalify question number from Redis
    question_no = redis_store.get(Sessionid + ':question')
    # gets the previous intent number from Redis
    prev_intent = redis_store.get(Sessionid + ':prev_intent')
    list_intents.append(prev_intent)
    preq_flag=redis_store.get(Sessionid + ':flag')
    current_question = int(question_no) + 1
    print(key)

    if (key == "greet_intent") and (prev_intent == " ") and (preq_flag == " "):
        redis_store.set(Sessionid + ':prev_intent', str(key))
        greet_list = ['Welcome!!  Are you ready to chat?', 'Hello!! Would you like to chat?',
                      'Hi welcome!! Do you wanna chat?',
                      'Hello I would like you to take you through a list of Pre-qualification questions for this job. Are you ready ?',
                      'Welcome Buddy!! Shall We begin our Chat?', 'Welcome!! Do you want me to chat?']
        # Returns the Random response for the intent
        return ''.join(random.sample(greet_list, 1))

    if key == "end_intent" and (preq_flag == " "):
        redis_store.set(Sessionid + ':prev_intent', str(key))
        end_list = ['Thanks for your time with me. Good Luck with your Job search !!',
                    'Nice to chat with you.All the best!!', 'Thank you. Good Luck !!',
                    'Well, it was great catching up with you.Best of Luck!!',
                    'It\'s been nice speaking with you.Good Luck !!']
        return ''.join(random.sample(end_list, 1))


    if key == "misc_intent" and (preq_flag == " "):
        redis_store.set(Sessionid + ':prev_intent', str(key))
        misc_list = ['Cool', 'My Pleasure', 'That\'s fine']
        return ''.join(random.sample(misc_list, 1))


    if key == "job_query_intent" and (preq_flag == " "):
        if "end_intent" not in list_intents:
            redis_store.set(Sessionid + ':prev_intent', str(key))
            job_query = ['You can refer our website vind.ai for further details',
                         'You can check our website vind.ai for more details on this or other similar jobs',
                         'Please visit our website vind.ai to know more about Job details']
            return ''.join(random.sample(job_query, 1))
        else:
            return "We had a good chat !! let's catchup someother time"


    if key == "payrate_query_intent" and (preq_flag == " "):
        if "end_intent" not in list_intents:
            redis_store.set(Sessionid + ':prev_intent', str(key))
            payrate_query = ['Please discuss with the client manager on payrate or salary info',
                             'You can contact the Client Manager to know more about payrate details',
                             'Please feel free to ask the Client Manager for payrate related queries']
            return ''.join(random.sample(payrate_query, 1))
        else:
            return "We had a good chat !! let's catchup someother time"


    if (key == "travel_query_intent") and (preq_flag == " "):
        if ("end_intent" not in list_intents):
            redis_store.set(Sessionid + ':prev_intent', str(key))
            travel_query = ['We are ready to pay high if you are willing to travel/relocate.',
                            'We provide travel/relocation benefits for Candidates',
                            'We cover travel/relocation benefits but advise you to stay up-to-date on company  policies and costs covered for reimbursement']
            return ''.join(random.sample(travel_query, 1))
        else:
            return "We had a good chat !! let's catchup someother time"


    if key == "followup_query_intent" and (preq_flag == " "):
        if ("end_intent" not in list_intents):
            redis_store.set(Sessionid + ':prev_intent', str(key))
            followup_query = ['You can get in touch with Recruiter for more details or next steps',
                              'Feel free to Contact Recruiter for further details',
                              'Catch up Recruiter for further details']
            return ''.join(random.sample(followup_query, 1))


    if key == "visa_query_intent" and (preq_flag == " "):
        redis_store.set(Sessionid + ':prev_intent', str(key))
        visa_list = ['We will let you know about visa related details after having a discussion with our manager',
                     'You will be intimated as soon as possible about visa details']
        return ''.join(random.sample(visa_list, 1))


    if ((key == "positive_intent") or (key == "yes_intent") or (key == "no_intent") or (key == "negative_intent")):
        '''if ("negative_intent " not in list_intents) and ("no_intent" not in list_intents) :'''
        redis_store.set(Sessionid + ':prev_intent', str(key))
        redis_store.set(Sessionid + ':flag', "yes")
        print(redis_store.get(Sessionid + ':flag'))
        total_question, preq = Fetch_JobQuestions(jobid=job_id)
        preq_question = Fetch_Question(preq, current_question, total_question,Sessionid)
        redis_store.set(Sessionid + ':question', str(current_question))

        return preq_question

    else:
        return 'Please say yes or no or give appropriate reply for proceed further'