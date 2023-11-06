from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mini_ultimatum_game'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1

    endowment = cu(200)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def set_payoffs(self):
        player1 = self.get_player_by_id(1)
        player2 = self.get_player_by_id(2)
        player3 = self.get_player_by_id(3)

        if player3.punish:
            player1.payoff = cu(0)
            player2.payoff = cu(0)
        else:
            player1.payoff = C.endowment - player1.amount_sent
            player2.payoff = player1.amount_sent


class Player(BasePlayer):
    amount_sent = models.CurrencyField(min=0, max=C.endowment)
    punish = models.BooleanField()
    capital_city = models.StringField(choices=['Kisumu', 'Nairobi', 'Mombasa'])
    sum = models.IntegerField()
    population = models.IntegerField()

    # validation for the sum field
    def sum_error_message(self, sum):
        if sum != 29:
            return 'The sum of 14 and 15 is 29, not {}'.format(sum)


# PAGES
class Player1Page(Page):
    form_model = 'player'
    form_fields = ['amount_sent']

    def is_displayed(self):
        return self.player.id_in_group == 1

class Player3Page(Page):
    form_model = 'player'
    form_fields = ['punish']

    def is_displayed(self):
        return self.player.id_in_group == 3

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

class Results(Page):
    pass

class ExitSurvey(Page):
    form_model = 'player'
    form_fields = ['capital_city', 'sum', 'population']

page_sequence = [Player1Page, Player3Page, ResultsWaitPage, Results, ExitSurvey]
