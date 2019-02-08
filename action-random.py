#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import random

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class RandomRoulette(object):

    def __init__(self):
        self.start_blocking()

    def setChooseRandomNumberIntentCallback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        item = u"none"

        if intent_message.slots.random_method:
            item = intent_message.slots.random_method.first().value

        if item == u"monnaie":
            coin_random = random.randrange(0, 1)
            if coin_random == 0:
                result_sentence = u"Le résultat est Pile"
            else:
                result_sentence = u"Le résultat est face"
        elif item == u"dé":
            dice_random = random.randrange(1, 6)
            result_sentence = u"Le dé tombe sur le numéro {number} ".format(number=dice_random)
        elif item == u"nombre":
            number_random = random.randrange(0, 1000)
            result_sentence = u"Le nombre aléatoire généré est {number} .".format(number=number_random)
        else:
            result_sentence = u"Désolé je n'ai pas compris."

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, result_sentence, "")

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):

        intent_name = intent_message.intent.intent_name
        if ':' in intent_name:
            intent_name = intent_name.split(":")[1]
        if intent_name == 'chooseRandomNumber':
            self.setChooseRandomNumberIntentCallback(hermes, intent_message)

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    RandomRoulette()