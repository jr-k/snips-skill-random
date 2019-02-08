#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import random

def action_wrapper(hermes, intentMessage):
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
        result_sentence = "Désolé je n'ai pas compris."

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("jierka:chooseRandomNumber", action_wrapper) \
.start()
