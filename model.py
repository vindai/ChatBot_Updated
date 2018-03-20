from rasa_nlu.model import Interpreter ,Metadata
from rasa_nlu.config import RasaNLUConfig

config =RasaNLUConfig('E:/Chatbot_techfetch/config/config_spacy.json')

metadata = Metadata.load('./models/trained')

interpreter = Interpreter.load(metadata, config)
