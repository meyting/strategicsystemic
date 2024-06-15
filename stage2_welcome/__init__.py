from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'start'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField()
    prolific_id = models.StringField(default=str(" "))


# PAGES
class consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.prolific_id = player.participant.label


class instructions(Page):
    form_model = 'player'
    form_fields = ['prolificid']

page_sequence = [consent,
                 ]
