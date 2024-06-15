from otree.api import *


doc = """
Your app description
"""

import random
import pandas as pd
import numpy as np

#df = pd.read_excel('_static/stage2_two_workers.xlsx', keep_default_na = False, engine = 'openpyxl')

df = pd.read_excel('_static/workersets_stage2.xlsx', keep_default_na=False, engine='openpyxl')
df["score"] = df["task"].astype(float)
df["signal"] = df["evaluation1"].astype(str)
df["evaluator_color"] = df["eval1_color"].astype(str)

random.seed(1)


class C(BaseConstants):
    NAME_IN_URL = 'evaluations'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10 #also change in creating session!
    NUM_WORKERS = 2
    minwage = 0
    maxwage = 10
    endowment = 10
    check_task_answer = True
    check_worker_answer = True
    check_middlemanager_answer = True
    check_payment_task_answer = True
    budget = 10
    bonus_payment = cu(2)
    bonus_payment_stage1 = cu(0.1)
    conversion_rate = 10
    EXAMPLE_RAVENS = 'global/inductive_10.jpg'
    EXAMPLE_SOLUTION = 'E'
    MAX_SCORE = 10


class Subsession(BaseSubsession):
    pass

def select_profiles(df):
    unique_pairs = df['pair'].unique()
    sampled_pairs = np.random.choice(unique_pairs, size=10, replace=False)
    sampled_df = df[df['pair'].isin(sampled_pairs)]
    # Shuffle within each pair
    shuffled_sampled_df = sampled_df.groupby('pair').apply(lambda x: x.sample(frac=1)).reset_index(drop=True)
    # Sort by pair to keep pairs together
    shuffled_sampled_df = shuffled_sampled_df.sort_values(by='pair').reset_index(drop=True)
    return shuffled_sampled_df


#def select_profiles(df):
#    green_sample =  df[df['color'] == 'green'].sample(10)
#    orange_sample =  df[df['color'] == 'orange'].sample(10)
#    pairs = []
#    for i in range(C.NUM_ROUNDS):
#        pair = pd.DataFrame([green_sample.iloc[i], orange_sample.iloc[i]])
#        pairs.append(pair.sample(frac=1).reset_index(drop=True))  # Shuffle within the pair
#    # Combine all pairs into one DataFrame
#    result_df = pd.concat(pairs).reset_index(drop=True)
#    print("RESULT DF", result_df)
#    return result_df


def creating_session(subsession: Subsession):
    import itertools
    treatment = itertools.cycle(['full_certainty',
                                 #'medium_certainty',
                                 'uncertainty',
                                 'strategic_uncertainty'])
    for p in subsession.get_players():
        if subsession.round_number == 1: 
            p.participant.profiles = []
            selected_profiles_df = select_profiles(df)
            profiles = selected_profiles_df.to_dict(orient='records')
            p.participant.profiles = profiles
            if 'treatment' in subsession.session.config:
                p.participant.treatment = subsession.session.config['treatment']
            else:
                p.participant.treatment = next(treatment)
            p.treatment = p.participant.treatment
            p.participant.group = random.choice(["Green"])
            #p.participant.order_beliefs = random.choice(["Green", "Orange"])


      
class Group(BaseGroup):
    pass


class Player(BasePlayer):
    offer1 = models.StringField()
    offer2 = models.StringField()
    group1 = models.StringField()
    group2 = models.StringField()
    score1 = models.FloatField()
    score2 = models.FloatField()
    signal1 = models.StringField()
    signal2 = models.StringField()
    treatment = models.StringField()
    
    check_task = models.BooleanField()
    check_payment_task = models.BooleanField()
    check_worker = models.BooleanField()
    check_middlemanager = models.BooleanField()
    check_group = models.StringField(blank=True)
    
    check_task_correct = models.BooleanField()
    check_payment_task_correct = models.BooleanField()
    check_worker_correct = models.BooleanField()
    check_middlemanager_correct = models.BooleanField()
    check_group_correct = models.BooleanField()

    decision = models.StringField()
    reveal = models.IntegerField(blank=True, initial=0 )

    def list_control_answers(player):
        if player.check_task == C.check_task_answer:
            player.check_task_correct = True
        else:
            player.check_task_correct = False
        if player.check_payment_task == C.check_payment_task_answer:
            player.check_payment_task_correct = True
        else:
            player.check_payment_task_correct = False
        if player.check_worker == C.check_worker_answer:
            player.check_worker_correct = True
        else:
            player.check_worker_correct = False
        if player.check_middlemanager == C.check_middlemanager_answer:
            player.check_middlemanager_correct = True
        else:
            player.check_middlemanager_correct = False
        if player.check_group == player.participant.group:
            player.check_group_correct = True
        else:
            player.check_group_correct = False
        
        player.participant.control_answers = [player.check_task_correct,
                                              player.check_payment_task_correct,
                                              player.check_worker_correct,
                                              player.check_middlemanager_correct,
                                              player.check_group_correct,
                                              ]
        return player.participant.control_answers.count(True) != 5


# PAGES
'''
class Background(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {'image_path_example': C.EXAMPLE_RAVENS}
'''

class Groups(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Background(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Instructions(Page):
    @staticmethod
    def vars_for_template(player:Player):
        participant = player.participant
        return {
            'treatment' : participant.treatment,
        }
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
class Check(Page):
    form_model = 'player'
    form_fields = ['check_task', 'check_payment_task', 'check_worker', 'check_middlemanager', 'check_group', ]
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Error(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return player.list_control_answers()
        else:
            False    

class Ready(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return player.list_control_answers() == False
        else:
            False  

'''
class Evaluations_example(Page):
    form_model = 'player'
    form_fields = [
        'offer1', 'offer2', 'group1', 'group2', 'score1', 'score2', 'signal1', 'signal2', 'reveal_example',
                   ]

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        # print("PROFILES IN VARS FOR TEMPLATE", participant.profiles)
        profile1 = participant.profiles[player.round_number-1][0]
        profile2 = participant.profiles[player.round_number][0]
        group1 = profile1["color"]
        group2 = profile2["color"]
        profile_id1 = profile1["prolificid"]
        profile_id2 = profile2["prolificid"]
        score1 = int(profile1["task"])
        score2 = int(profile2["task"])
        eval_color1 = profile1["evaluator_color"]
        eval_color2 = profile2["evaluator_color"]
        signal1 = int(profile1["signal"])
        signal2 = int(profile2["signal"])
        return {
            'profile1': profile1,
            'profile2': profile2,
            'profile_id1': profile_id1,
            'profile_id2': profile_id2,
            'group1': group1,
            'group2': group2,
            'score1': score1,
            'score2': score2,
            'eval_color1': eval_color1,
            'eval_color2': eval_color2,
            'signal1': signal1,
            'signal2': signal2,
            'treatment': participant.treatment,
        }

    @staticmethod
    def js_vars(player: Player):
        profile1 = player.participant.profiles[player.round_number-1][0]
        profile2 = player.participant.profiles[player.round_number][0]
        profile1['score'] = int(profile1['score'])
        profile2['score'] = int(profile2['score'])
        profile1['signal'] = int(profile1['signal'])
        profile2['signal'] = int(profile2['signal'])
        # random.seed(player.round_number + C.NUM_ROUNDS * (player.id_in_group - 1))  # not sure yet
        return dict(
            profile1=profile1,
            profile2=profile2,
        )
'''


class Evaluations(Page):
    form_model = 'player'
    form_fields = [        
        'decision', 'offer1', 'offer2', 'group1', 'group2', 'score1', 'score2', 'signal1', 'signal2', 'reveal'
                   ]

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        # print("PROFILES IN VARS FOR TEMPLATE", participant.profiles)
        profile1 = participant.profiles[player.round_number + player.round_number-2]
        profile2 = participant.profiles[player.round_number + player.round_number-1]
        group1 = profile1["color"]
        group2 = profile2["color"]
        profile_id1 = profile1["prolificid"]
        profile_id2 = profile2["prolificid"]
        score1 = int(profile1["task"])
        score2 = int(profile2["task"])
        eval_color1 = profile1["evaluator_color"]
        eval_color2 = profile2["evaluator_color"]
        signal1 = profile1["signal"]
        signal2 = profile2["signal"]
        return {
            'profile1': profile1,
            'profile2': profile2,
            'profile_id1': profile_id1,
            'profile_id2': profile_id2,
            'group1': group1,
            'group2': group2,
            'score1': score1,
            'score2': score2,
            'eval_color1': eval_color1,
            'eval_color2': eval_color2,
            'signal1': signal1,
            'signal2': signal2,
            'treatment': participant.treatment,
            'reveal': player.reveal,
            'i1' : '<input name="decision" type="radio" id="d1" value="' + profile_id1 + '"' +' onclick="enablenextbutton()"/>',
            'i2' : '<input name="decision" type="radio" id="d2" value="' + profile_id2 + '"' +' onclick="enablenextbutton()"/>',
            'round_number': player.round_number,
        }

    @staticmethod
    def js_vars(player: Player):
        profile1 = player.participant.profiles[player.round_number + player.round_number-2]
        profile2 = player.participant.profiles[player.round_number + player.round_number-1]
        profile1['score'] = int(profile1['score'])
        profile2['score'] = int(profile2['score'])
        profile1['signal'] = profile1['signal']
        profile2['signal'] = profile2['signal']
        # random.seed(player.round_number + C.NUM_ROUNDS * (player.id_in_group - 1))  # not sure yet
        return dict(
            profile1=profile1,
            profile2=profile2,
        )


page_sequence = [
                #
                 Groups,
                 Background,
                 Instructions, 
                 #Evaluations_example,
                 Check, 
                 Error, 
                 Ready,
                 Evaluations,
                 ] # EvaluationsBudget # Evaluations

