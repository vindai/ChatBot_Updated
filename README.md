# Chatbot_Techfetch
Data Folder : Stores input training data
config : Contains the config_spacy json file
models : Directory under which the trained model gets stored #Chatbot.py: Its an entry which gets user message from vind.ai page ,
runs it through model and returns the response #Model.py: Every time model gets loaded from this saved directory
#Stateflow.py :Determines the output message to be sent #train_data.py :It trains the rasa_nlu model for the given input json data
#vind_api.py :Module to call vind api for the given job_id and lists the preq questions #unit_test.py: internal testing module 

