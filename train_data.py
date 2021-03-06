
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.converters import load_data
import os
import shutil

#Path to save the model
SAVE_PATH = './models/trained/'

#load the training data
training_data = load_data('E:/chat_demo_updated/Data/rasa_data.json')
#Train the model
config =RasaNLUConfig('E:/chat_demo_updated/Data/config_spacy.json')
trainer = Trainer(config)
train_data=trainer.train(training_data)

model_directory = trainer.persist('./models/')
# Returns the directory the model is stored in


if os.path.exists(SAVE_PATH): # removed old model if exists
    shutil.rmtree(SAVE_PATH)
    print('{} is removed to save the new model.'.format(SAVE_PATH))

os.rename(model_directory, SAVE_PATH) # rename new model to SAVE_PATH

print('done. model saved @ {}'.format(SAVE_PATH))



