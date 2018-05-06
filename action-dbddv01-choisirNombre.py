#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import random

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    """ Write the body of the function that will be executed once the intent is recognized. 
    In your scope, you have the following objects : 
    - intentMessage : an object that represents the recognized intent
    - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol. 
    - conf : a dictionary that holds the skills parameters you defined 

    Refer to the documentation for further details. 
    """ 
    item = intentMessage.slots.item_random.first().value
    if item == 'monnaie':
        coin_random = random.randrange(0, 1)
        if coin_random == 0:
            result_sentence = "Le résultat est Pile"
        else:
            result_sentence = "Le résulat est face"
    elif item == 'dé':
        dice_random = random.randrange(1, 6)
        result_sentence = "Le dé tombe sur le numéro {number} ".format(number=dice_random)
    elif item == 'nombre':
        number_random = random.randrange(0, 1000)
        result_sentence = "Le nombre aléatoire généré est {number} .".format(number=number_random)
    else:
        result_sentence = "Désolé je n'ai pas compris. "
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("dbddv01:choisirNombre", subscribe_intent_callback) \
.start()
