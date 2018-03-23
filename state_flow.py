from vindai_api import Fetch_Question, Fetch_JobQuestions
import redis
import random

# opening redis connection here
redis_store = redis.StrictRedis("localhost")
expiry_seconds = 600
generic_response = ['Our recruiter will call and clear you on this query.',
                    'Please feel free to call our recruiter for further queries.',
                    'Please contact our hiring manager to clarify your queries.']


def getstate(key, job_id, Sessionid, confidence_score):

    # gets the prequalify question number from Redis
    question_no = redis_store.get(Sessionid + ':question')

    # gets the previous intent number from Redis
    prev_intent = redis_store.get(Sessionid + ':prev_intent')
    preq_flag = redis_store.get(Sessionid + ':flag')
    current_question = int(question_no) + 1

    # For key is greet intent with previous no previous intent and preq flag is set as n
    if key == "greet_intent" and prev_intent == " " and preq_flag == "n":
        redis_store.set(Sessionid + ':prev_intent', str(key))
        greet_list = ['Welcome!!  Are you ready to chat?', 'Hello!! Would you like to chat?',
                      'Hi welcome!! Do you wanna chat?',
                      'Hello I would like to take you through a list of Pre-qualification questions for this job. '
                      'Are you ready ?',
                      'Welcome Buddy!! Shall We begin our Chat?', 'Welcome!! Do you want me to chat?']

        # Returns the Random response for the intent
        return ''.join(random.sample(greet_list, 1))

    # To handle the preq questions with preq flag is set as y
    if preq_flag == 'y':
        redis_store.set(Sessionid + ':prev_intent', str(key))
        total_question, preq = Fetch_JobQuestions(jobid=job_id)
        preq_question = Fetch_Question(preq, current_question, total_question, Sessionid)
        redis_store.set(Sessionid + ':question', str(current_question))
        return preq_question

    # For handling positive intent, negative intent, yes intent, no intent and greet intent after preq questions
    if (key == "positive_intent" or key == "negative_intent" or key == "yes_intent" or key == "no_intent"
            or key == "greet_intent") and preq_flag == 'n':
        return "For further queries kindly contact our Recruiter"

    # To handle end intent after the preq questions
    if key == "end_intent" and preq_flag == "n":
        redis_store.set(Sessionid + ':prev_intent', str(key))
        end_list = ['Thanks for your time with me. Good Luck with your Job search !!',
                    'Nice to chat with you.All the best!!', 'Thank you. Good Luck !!',
                    'Well, Nice talking to you.Have a Great day. Good bye!!',
                    'It\'s been nice speaking with you.Good Luck !!']
        return ''.join(random.sample(end_list, 1))

    # To handle misc intent after the preq questions
    if key == "misc_intent" and preq_flag == "n":
        redis_store.set(Sessionid + ':prev_intent', str(key))
        misc_list = ['Cool', 'My Pleasure', 'That\'s fine']
        return ''.join(random.sample(misc_list, 1))

    # To handle the job query intent after preq questions with threshold confidence score value
    if key == "job_query_intent" and preq_flag == "n":
        if confidence_score > 0.2:
            redis_store.set(Sessionid + ':prev_intent', str(key))
            job_query = ['You can refer our website http://www.techfetch.com/ for further details',
                         'You can check our website http://www.techfetch.com/ for more details on this or '
                         'other similar jobs',
                         'Please visit our website http://www.techfetch.com/ to know more about Job details']
            return ''.join(random.sample(job_query, 1))
        else:
            return ''.join(random.sample(generic_response, 1))

    # To handle the payrate query intent after preq questions with threshold confidence score value
    if key == "payrate_query_intent" and preq_flag == "n":
       if confidence_score > 0.2:
            redis_store.set(Sessionid + ':prev_intent', str(key))
            payrate_query = ['Please discuss with the client manager on payrate or salary info',
                             'You can contact the Client Manager to know more about payrate details',
                             'Please feel free to ask the Client Manager for payrate related queries']
            return ''.join(random.sample(payrate_query, 1))
       else:
           return ''.join(random.sample(generic_response, 1))

    # To handle the travel query intent after preq questions with threshold confidence score value
    if key == "travel_query_intent" and preq_flag == "n":

        if confidence_score > 0.2:
            redis_store.set(Sessionid + ':prev_intent', str(key))
            travel_query = ['For travel/relocation related queries kindly contact the Recruiter',
                            'You can contact the Recruiter to know more on travel/relocation details']
            return ''.join(random.sample(travel_query, 1))
        else:
            return ''.join(random.sample(generic_response, 1))

    # To handle the visa query intent after preq questions with threshold confidence score value
    if key == "visa_query_intent" and preq_flag == "n":
        if confidence_score > 0.2:
            redis_store.set(Sessionid + ':prev_intent', str(key))
            visa_query = ['Please feel free to ask the Client Manager for visa related queries',
                          'You can contact the Client Manager to know more about visa details']
            return ''.join(random.sample(visa_query, 1))
        else:
            return ''.join(random.sample(generic_response, 1))

    # To handle the followup query intent after preq questions with threshold confidence score value
    if key == "followup_query_intent" and preq_flag == "n":
        if confidence_score > 0.2:
            redis_store.set(Sessionid + ':prev_intent', str(key))
            followup_query = ['You can get in touch with our Recruiter for more details',
                              'Feel free to Contact the Recruiter for further details']
            return ''.join(random.sample(followup_query, 1))
        else:
            return ''.join(random.sample(generic_response, 1))
    else:
        return 'I am still training on this new update !!'
