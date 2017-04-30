# Python classes for the Japanese game "Revolution"
# The following objects are needed for the game:
# Match
# Game
# Player
# Deck
# Card
# Table
# Discard

import numpy as np

# helper functions

class Match():
    """Object with information about game session
    - Total number of games
    - Number of games played
    - Winner, 2nd winner, last and 2nd-to-last of last game
    - Number of Players
    - Game mode (variations of revolution)
    - Play history of each game
    - Rank history
    """
    def __init__(self, n_players, games_total = 12, game_mode = "standard",):
        self.n_players = n_players
        self.games_total = games_total
        self.game_mode = game_mode
        self.n_games_played = 0
        self.match_history = []
        self.player_ranking = []
        self.rank_history = []
        return None

    def update(self, player_ranking, game_history,):
        """
        Update match after game
        """
        self.n_games_played += 1
        self.player_ranking = player_ranking
        self.rank_history.append(player_ranking)
        self.match_history.append(game_history)
        return None

class Game():
    """Object with game state information.
    - Starting Player
    - Cards played
    - Play history of game
    - Revolution switch
    """
    def __init__(self, n_players):
        self.is_rev_switch = False
        self.game_history = []
        self.cards_played = []
        self.starting_player = np.random.randint(0, n_players)
        return

    def update(self, active_player = "Empty table", cards = []):
        self.cards_played.append((active_player, cards))
        return

    def end(self, table_object, discard_object, player_lst):
        """Wraps up the game
        """
        self.game_history = self.cards_played
        # Table
        table_object.clear(discard_object)

        # Players
        for player in player_lst:
            player.clear()
        # update Discard
        discard_object.clear()

        # (update match)


        return self.game_history


class Player():
    """Object containing player-specific information
    - Hand
    - Rank during previous games
    - Starting hands
    """
    def __init__(self, seating):
        self.hand = None
        self.starting_hands = []
        self.seating = seating # sequencing of players
        return

    def new_hand(self, hand):
        self.hand = hand
        self.starting_hands.append(hand)
        return 

    def update(self, cards_played):
        # remove cards from self.hand =
        # YET TO BE IMPLEMENTED
        for card in cards_played:
            arg = np.argmin(np.any(self.hand[:] != card, axis = 1))
            # all true
            all_but_one = np.any(self.hand[:] != 42, axis = 1)
            # except first appearance of card
            all_but_one[arg] = False
            self.hand = self.hand[all_but_one]
        return self.hand

    def discard(self, card, discard_object):
        # update Player 
        self.hand = self.hand[np.any(self.hand[:] != card, axis = 1)]
        # update Discard
        discard_object.update(card)
        return card

    def clear(self):
        self.hand = None
        return None

    def get_ranking(self, match_object):
        player_ranking_history = match.object.rank_history[:, self.seating]

        return player_ranking_history



class Deck():
    """Deck containing card information
    - Number of cards in deck
    - Define each card value and suite in the deck on start
    """
    def __init__(self, multiplicator = 1, n_jokers = 3):
        """Creates Deck with (52 cards + jokers) * multiplicator
        """
        values = [0,1,2,3,4,5,6,7,8,9,10,11,12,] # 0 = card 3, 12 = card 2
        suite = [1,2,3,4,] # diamonds 1, hearts 2, spades 3, clubs 4
        simple_deck = np.array(np.meshgrid(suite, values,)).T.reshape(-1,2)
        deck_w_jokers = np.vstack((simple_deck, np.array([[0,13],]*n_jokers)))
        full_deck = np.tile(deck_w_jokers, (multiplicator, 1))
        self.deck = full_deck
        return None

    def shuffle(self):
        np.random.shuffle(self.deck)
        return self.deck


class Table():
    """Object containing information
    about the stack
    - Stack history
    - Jack switch
    - Top cards
    - Empty / not empty
    - Allowed combination to be played (doubles, triples, revolution, straight)
    - Suite locked / not locked
    """
    def __init__(self):
        self.is_jack_switch = False
        self.top_cards = ""
        self.is_empty = True
        self.is_suite_lock = False
        self.stack_history = []
        self.is_straight = False
        self.top_player = ""

    def update(self, seating, cards = []):
        if len(cards) >0:
            self.top_cards = cards

            self.stack_history.append(cards)
            self.is_empty = False
            self.top_player = seating
        else: 
            pass

        return self.top_cards

    def clear(self, discard_object):
        self.is_jack_switch = False
        self.top_cards = ""
        self.is_empty = True
        self.is_suite_lock = False
        self.is_straight = False
        self.top_player = ""
        # update Discard
        for cards in self.stack_history:
                discard_object.update(cards)
        self.stack_history = []


class Discard():
    """Discard pile
    face down
    """
    def __init__(self):
        self.discard_history = []

    def update(self, cards = None):
        self.discard_history.append(cards)

    def clear(self):
        self.discard_history = []
 

class Card():
    """Information about specific card
    - suite
    - value
    Maybe needed for displaying in human-readable format
    """
    def __init__(self):
        self.value_dict = {0 : 3, 1 : 4, 2 : 5, 3 : 6, 4 : 7, 5 : 8, 6 : 9,
         7 : 10, 8 : "J", 9 : "Q", 10 : "K", 11 : "A", 12 : 2, 13 : "Joker"}
        self.suite_dict = {0 : "", 1 : "c", 2: "s",
         3 : "h", 4 : "d"}
        return None

    def tuple2card(self, card_tuple):
        card = str(self.value_dict[card_tuple[1]]) + str(self.suite_dict[card_tuple[0]])
        return card

    def tuples2cards(self, card_tuple_lst):
        cards = []

        """if len(card_tuple_lst) != 0:
            if card_tuple_lst.shape[0] == 1:
                print("DUDE")
                print(card_tuple_lst)
                return ""
                #return self.tuple2card(card_tuple_lst)
        """
        for card_tuple in card_tuple_lst:
            cards.append(self.tuple2card(card_tuple))
        return cards














