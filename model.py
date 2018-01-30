from rasa_nlu.model import Interpreter ,Metadata
from rasa_nlu.config import RasaNLUConfig

config =RasaNLUConfig('C:/Users/Tilliconveli6/Desktop/New folder/ChatBot_Updated/Data/config_spacy.json')

metadata = Metadata.load('./models/trained')

interpreter = Interpreter.load(metadata, config)
#
#for testing purposes
# result=''
# while(result!='exit'):
#     user_says=raw_input("User_says> ")
#     result1=interpreter.parse(unicode(user_says))
#     # print(result1['entities'][0]['entity'])
#     print(result1)
#     result=user_says