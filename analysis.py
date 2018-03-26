import numpy as np
import matplotlib.pyplot as plt

class war():

    def __init__(self):
        self.deck = war.generate_deck()

    @staticmethod
    def generate_deck():
        num_cards_suit = 13
        suit = [i for i in range(1, num_cards_suit + 1)]
        return suit * 4

    @staticmethod
    def collect_cards(winner, cards, collect_method):
        if collect_method == "shuffle":
            np.random.shuffle(cards)

        return winner + cards

    @staticmethod
    def increment_card_count(p1, p2, draw_pile, turn_status):
        if turn_status == "p1 win":
            return p1 + 1 + len(draw_pile), p2 - 1
        elif turn_status == "p2 win":
            return p1 - 1, p2 + 1 + len(draw_pile)
        else:
            return p1 - 1, p2 - 1

    def play_war(self, collect_method="shuffle", get_player_stats=False):
        np.random.shuffle(self.deck)

        draw_pile = []
        turn_count = 0

        p1 = self.deck[:52 // 2]
        p2 = self.deck[52 // 2:]
        num_p1 = len(p1)
        num_p2 = len(p2)

        if get_player_stats:
            p1_stats = []
            p2_stats = []

        while num_p1 > 0 and num_p2 > 0:
            cards_in_play = [p1.pop(), p2.pop()]

            if cards_in_play[0] > cards_in_play[1]:
                p1 = war.collect_cards(p1, cards_in_play + draw_pile, collect_method)
                num_p1, num_p2 = war.increment_card_count(num_p1, num_p2, draw_pile, "p1 win")
                draw_pile = []

            elif cards_in_play[1] > cards_in_play[0]:
                p2 = war.collect_cards(p2, cards_in_play + draw_pile, collect_method)
                num_p1, num_p2 = war.increment_card_count(num_p1, num_p2, draw_pile, "p2 win")
                draw_pile = []

            else:
                draw_pile.extend(cards_in_play)
                num_p1, num_p2 = war.increment_card_count(num_p1, num_p2, draw_pile, "draw")

            if get_player_stats:
                p1_stats.append(num_p1)
                p2_stats.append(num_p2)
            else:
                turn_count += 1

        if get_player_stats:
            return p1_stats, p2_stats
        else:
            return turn_count

    def get_mean_turns(self, iterations=1000, collect_method="shuffle"):

        mean_turns = []
        for i in range(iterations):
            turns = self.play_war(collect_method)
            mean_turns.append(turns)

        return mean_turns

    def get_winner_stats(self, collect_method="shuffle"):
        p1, p2 = self.play_war(collect_method, get_player_stats=True)
        return p1 if p1[-1] != 0 else p2

    def plot_means(self, mean_1, mean_2=None):

        plt.subplot(2, 1, 1)
        plt.hist(mean_1, bins=100, label="Shuffle")
        plt.xlabel('turns')
        plt.legend()

        if mean_2 is not None:
            plt.subplot(2, 1, 2)
            plt.hist(mean_2, bins=100, label="No shuffle")
            plt.xlabel('turns')

        plt.legend()
        plt.show()

    def plot_stats(self, winner1, winner2 = None):
        plt.subplot(2, 1, 1)
        plt.plot(winner1, label="Shuffle")
        plt.xlabel('turns')
        plt.legend()

        if winner2 is not None:
            plt.subplot(2, 1, 2)
            plt.plot(winner2, label="No shuffle")
            plt.xlabel('turns')

        plt.legend()
        plt.show()

if __name__=="__main__":

    war_game = war()

    mean_shuffle = war_game.get_mean_turns()
    mean_no_shuffle = war_game.get_mean_turns(collect_method=None)

    winner_shuffle = war_game.get_winner_stats()
    winner_no_shuffle = war_game.get_winner_stats(collect_method=None)

    #war_game.plot_means(mean_shuffle, mean_no_shuffle)
    war_game.plot_stats(winner_shuffle, winner_no_shuffle)

