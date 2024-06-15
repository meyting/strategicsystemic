from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'questions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label="How old are you?")
    gender = models.StringField(
        choices=[[0, 'male'], [1, 'female'], [2, 'other'], [3, 'prefer not to say']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    race = models.StringField(
        choices=["Hispanic or Latin", "Asian", "White", "Black or African American",
                 "other / prefer not to answer"],
                label='What is your ethnic group?',
        widgets=widgets.RadioSelect,
    )
    education = models.IntegerField(
        choices=[[0, 'did not graduate high school'], [1, 'High school or GED'], [2, 'began college, no degree yet'],
                 [3, 'Bachelor'], [4, 'Associate'], [5, 'Master'], [6, 'Doctoral'], [7, 'other']],
        label='What is the highest level of education you have completed?',
        widgets=widgets.RadioSelect,
    )
    gpa_highschool = models.FloatField(
        label='What is your (current/ final) high school GPA?',
        blank=True,
    )
    gpa_college = models.FloatField(
        label='What is your (current/ final) college GPA?',
        blank=True,
    )
    political_affiliation = models.IntegerField(initial=None)
    political_orientation = models.IntegerField(
        choices=[[0, 'Democrat'], [1, 'Republican']],
        label='Which direction would you prefer if you had to vote today?',
        widget=widgets.RadioSelectHorizontal(),
        blank=True,
    )
#    financial_literacy1 = models.IntegerField(
#        choices=[[1, 'more than $102'], [2, 'exactly $102'], [3, 'less than $102'], [4, 'I don`t know']],
#        label='Suppose you had $100 in a savings account and the interest rate was 2% per year. '
#              'After 5 years, how much do you think you would have in the account if you left the money to grow?',
#        widget=widgets.RadioSelect()
#    )
#    financial_literacy2 = models.IntegerField(
#        choices=[[1, 'more than before'], [2, 'less than before'], [3, 'same as before'], [4, 'I don`t know']],
#        label='Imagine that the interest rate on your savings account was 1% per year and inflation was 2% per year. '
#              'After one year, you would be able to buy...',
#        widget=widgets.RadioSelect(),
#    )
#    financial_literacy3 = models.BooleanField(
#        choices=[[False, 'False'], [True, 'True']],
#        label='Do you think that the following statement is true or false? “Buying a single company stock usually '
#              'provides a safer return than a stock mutual fund.”',
#        widgets=widgets.RadioSelect(),
#    )
    lazy = models.LongStringField(
        initial=None,
        blank=True,
        verbose_name="How did you make your decision to reveal reveal the workers' scores or not?"
    )
    purpose = models.LongStringField(initial=None,
                                     blank=True,
                                     verbose_name="What do you think this study is about?")

#    points_financial1 = models.IntegerField(initial=0)
#    points_financial2 = models.IntegerField(initial=0)
#    points_financial3 = models.IntegerField(initial=0)
#    points_financial_ges = models.IntegerField()
#    financial_literacy_est = models.IntegerField(
#        choices=[[0, '0'], [1, '1'], [2, '2'], [3, '3']],
#        label='How many of the 3 financial knowledge questions above do you think you have answered correctly?',
#        widgets=widgets.RadioSelect()
#    )


# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'race', 'education', 'gpa_highschool', 'gpa_college',
                   'political_affiliation', 'political_orientation', #'financial_literacy1',
 #                  'financial_literacy2', 'financial_literacy3', 'financial_literacy_est',
                   'lazy', 'purpose']

    @staticmethod
    def error_message(player, values):
        print('values is', values)
        if values['political_orientation'] == None and values['political_affiliation'] == 2:
            # funktioniert so halb (man muss dann pol_affiliation neu eintragen)
            return 'Please choose your political orientation if you are independent'

#    @staticmethod
#    def before_next_page(player: Player, timeout_happened):
#        player.points_financial_ges = 0
#        if player.financial_literacy1 == 1:
#            player.points_financial1 = 1
#            player.points_financial_ges += 1
#        if player.financial_literacy2 == 2:
#            player.points_financial2 = 1
#            player.points_financial_ges += 1
#        if player.financial_literacy3 == True:
#            player.points_financial1 = 1
#            player.points_financial_ges += 1


page_sequence = [Survey,
                 ]
