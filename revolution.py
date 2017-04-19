# Python object-oriented game called "Revolution"
# Japanese game for any number of players
# execution of the game

import numpy as np
from classes_revolution import Match, Game, Player, Deck, Table, Discard, Card
import itertools, random, time 

### GLOBALS ###

GAME_MODE = "allhuman"
GAME_MODE = "onehuman"
GAME_MODE = "allrandom"
t0 = time.time()

### Helper Functions ### 

def get_human_cards(cards):
    human_card = Card()
    human_cards = human_card.tuples2cards(cards)
    return human_cards

def choose(moves_lst, active_player, mode = GAME_MODE):
    if GAME_MODE == "onehuman":
        return choose_0_human_vs_random(moves_lst, active_player)
    elif GAME_MODE == "allhuman":
        return choose_action(moves_lst, mode = "human")
    elif GAME_MODE == "allrandom":
        return choose_action(moves_lst, mode = "random")
    else:
        print("GAME_MODE unknown")

def choose_0_human_vs_random(moves_lst, active_player):
    if active_player == 0:
        print("human action")
        return choose_action(moves_lst, mode="human")
    else:
        print("random computer action:")
        return choose_action(moves_lst, mode="random")

def choose_action(moves_lst, mode="human"):
    """Choice of action from a list of possible moves
    """
    if mode == "human":
        i = 0
        for move in moves_lst:
            print("Enter ", i, " to select ", get_human_cards(move))
            i +=1
        human_choice = input("Enter number: ")
        try:
            if 0 <= int(human_choice) <= len(moves_lst):
                return moves_lst[int(human_choice)]
        except:
            pass
            return np.array([])

        return move
    elif mode == "random":
        move = random.choice(moves_lst)
        return move
    elif mode == "ml":
        print("ML not yet implemented")
    else:
        print("Mode not known. Modes are 'human', 'random' and 'ml'")



# initiate Match
# define game mode
# define number of players
# define sequence of players

current_match = Match(4, 100)

# initiate Players
player_lst = []
for seat in range(0, current_match.n_players):
    player = Player(seat)
    player_lst.append(player)

# initiate empty Table

table = Table()

# initiate empty Discard

discard_pile = Discard()

# repeat until total number of games is reached
while current_match.games_total !=  current_match.n_games_played:

    # initiate Game #
    #################
    print("Game " + str(current_match.n_games_played + 1) + " is starting!")

    current_game = Game(current_match.n_players)

    # create deck with size according to the number of players

    new_deck = Deck()


    # shuffle deck
    shuffled_deck = new_deck.shuffle()

    # distribute cards to hands of players, remaining cards are discarded (face-down)
    deck_size = shuffled_deck.shape[0]
    cards_per_player = deck_size // current_match.n_players # integer division
    remaining_cards = deck_size - cards_per_player * current_match.n_players 

        # update Players
    i = 0
    for player in player_lst:
        j = i + cards_per_player
        player.new_hand(shuffled_deck[i:j])
        i = j

        # update Discard
    discard_pile.update(shuffled_deck[j:])



    # Exchange of cards between players

    #example rank #
    current_match.player_ranking = np.array([0,1,3,2])
    ##

    if str(current_match.player_ranking) == "":
        pass
    else:
        first_place, second_place, second_to_last_place, last_place = current_match.player_ranking[[0,1,-2,-1]]
        first_hand = player_lst[first_place].hand
        second_hand = player_lst[second_place].hand
        second_to_last_hand = player_lst[second_to_last_place].hand
        last_hand = player_lst[last_place].hand

        # first player and last player
        first_arg = np.argsort(first_hand[:,1])
        first_cards = np.copy(first_hand[first_arg[:2]]) # two worst cards

        last_arg = np.argsort(last_hand[:,1])
        last_cards = np.copy(last_hand[last_arg[-2:]]) # two best cards

        # swap cards
        first_hand[first_arg[:2]] = last_cards
        last_hand[last_arg[-2:]] = first_cards
        #print("first and last swapped cards:", first_cards, last_cards)

        # second player and second-to-last player
        second_arg = np.argsort(second_hand[:,1])
        second_card = np.copy(second_hand[second_arg[:1]]) # worst card

        second_to_last_arg = np.argsort(second_to_last_hand[:,1])
        second_to_last_card = np.copy(second_to_last_hand[second_to_last_arg[-1:]]) # best card

        # swap cards
        second_hand[second_arg[:1]] = second_to_last_card
        second_to_last_hand[second_to_last_arg[-1:]] = second_card
        #print("second and second to last swapped cards:", 
        #    second_card, second_to_last_card)



    # (small action required) # currently ignored

    # update Player (has automatically taken place due to referencing numpy array)

    # define starting player (first game random, otherwise last player begins) ? check with rules ?!?
    if current_match.n_games_played == 0:
        starting_player = player_lst[current_game.starting_player]
    else:
        starting_player = player_lst[current_match.player_ranking[-1]]

    current_ranking = []    # list of players in sequence of having finished
    active_player_seating = starting_player.seating
    active_player = player_lst[active_player_seating]

    ### Start of turns ###
    #####################

    # repeat until game is over
    while len(current_ranking) !=  current_match.n_players:

        print("##### Turn of Player " + str(active_player_seating) + " #####")

    # Check possible moves
    # includes suite lock, doubles, triples, quadruples, revolution, straight

        active_hand = active_player.hand
        print("Active Hand")
        print(get_human_cards(active_hand))
        #print(active_hand)

        arg = np.argsort(active_hand[:,1])
        active_hand = active_hand[arg]
        diff = active_hand - np.insert(active_hand[:-1], 0, active_hand[0], axis = 0)

        # split into same value pools
        split_hand = np.split(active_hand, np.argwhere(diff[:,1] != 0.0).flatten()[0:])

        # calculate possible moves:
        
        # 1) Single, Double, Triple, ...
        possible_sames = [np.array([])]
        for same_value in split_hand:
            index_lst = list(itertools.product([False, True], repeat=same_value.shape[0]))
            #print("product list", index_lst)
            index_array = np.array(index_lst)

            for indices in index_array:
                move = same_value[indices,:]
                #print(move)
                if str(move) != "[]":
                    possible_sames.append(move)
        #print("possible moves Single, Double, Triple, ...", possible_sames)
        
        # 2) Straights
        # remove duplicates (cards with same suite and value)
        b = np.ascontiguousarray(active_hand).view(np.dtype((np.void, active_hand.dtype.itemsize * active_hand.shape[1])))
        _, idx = np.unique(b, return_index=True)
        uniques = active_hand[idx]

        # split into same suite pools

        arg = np.argsort(uniques[:,0])
        active_unique_hand = uniques[arg]
        diff = active_unique_hand - np.insert(active_unique_hand[:-1], 0, active_unique_hand[0], axis = 0)
        split_hand = np.split(active_unique_hand, np.argwhere(diff[:,0] != 0.0).flatten()[0:])

        # find neighbouring values
        possible_straights = []

        for same_suite in split_hand:
            #print(same_suite.shape[0])
            if same_suite.shape[0] >= 3:

                arg = np.argsort(same_suite[:,1])
                same_suite = same_suite[arg]
                diff = same_suite - np.insert(same_suite[:-1], 0, same_suite[0] -1, axis = 0)

                #print("same suite cards:", same_suite)

                split_suite = np.split(same_suite, np.argwhere(diff[:,1] != 1.0).flatten()[0:])
                #print("split suite")
                #print(split_suite)
                for straight in split_suite:
                    if straight.shape[0] >= 3:

                        # calculate possible moves:
                        # Straight
                        index_lst = list(itertools.product([False, True], repeat=straight.shape[0]))
                        #print("product list", index_lst)
                        index_array = np.array(index_lst)

                        for indices in index_array:
                            move = straight[indices,:]
                            if move.shape[0] >= 3: 
                                diff = move - np.insert(move[:-1], 0, move[0] -1, axis = 0)
                                #print("same suite cards:", same_suite)
                                if np.all(diff[:,1] == 1):                              
                                    possible_straights.append(move)
        #print("possible straight moves", possible_straights)

        # unite moves
        possible_moves = possible_sames + possible_straights

        ### INFO SECTION ###
        print("is table empty?", table.is_empty)
        print("active player", active_player_seating)
        print("is straight?", table.is_straight)
        print("is revolution?", current_game.is_rev_switch)
        print("is jack switch?", table.is_jack_switch)
        print("is suite lock?", table.is_suite_lock)
        print("top player", table.top_player)
        print("top cards", get_human_cards(table.top_cards))
        #####################

        # check which of the possible moves are allowed considering the table
        if table.is_empty == True:
            possible_moves = possible_moves
        # if table is not empty
        else:
            # straight
            if table.is_straight == True:
                print("Straight")
                possible_moves = possible_straights
            # single, double, triple, ...
            else:
                possible_moves = possible_sames

            # number of cards on top
            tmp_moves = []
            for move in possible_moves:
                if move.shape[0] == table.top_cards.shape[0]:
                    tmp_moves.append(move)
            possible_moves = tmp_moves
            #print("moves with correct number of cards:", possible_moves)

            # check equality of suite with top cards if necessary
            if table.is_suite_lock:
                tmp_moves = []
                for move in possible_moves:

                    arg = np.argsort(move[:,0])
                    move = move[arg]
                    arg = np.argsort(table.top_cards[:,0])
                    table.top_cards = table.top_cards[arg]
                    if np.all(move[:,0] == table.top_cards[:,0]):
                        tmp_moves.append(move)  
                possible_moves = tmp_moves
                #print("Suite lock moves possible:")
                #print(possible_moves)

            # check wether the possible moves have a higher value
            tmp_moves = []
            for move in possible_moves:
                move_max = np.max(move[:,1])
                top_cards_max = np.max(table.top_cards[:,1])
                # if greater than 0, then move is possible
                difference = move_max - top_cards_max
                if table.is_jack_switch != current_game.is_rev_switch:
                    #print("Reverse order")
                    difference = - difference
                else:
                    #print("Normal order")
                    pass
                    # -13 for only 3 can top joker, joker can go under 3
                if difference > 0 or difference == -13:
                    tmp_moves.append(move)

            possible_moves = tmp_moves

            # append "Pass"
            possible_moves.append(np.array([]))
            #print("Moves possible:")
            #print(possible_moves)

    ## Action of players ##
    #######################
    # Action: Choose move or pass
        print("ACTION!")
        move = choose(possible_moves, active_player_seating)

        #print("ACTION DONE")
        print("It has been chosen to play ", get_human_cards(move))

        

    # update Player
        # remove cards from hand
        if len(move) > 0:
            for card in move:
                arg = np.argmin(np.any(active_hand[:] != card, axis = 1))
                # all true
                all_but_one = np.any(active_hand[:] != 42, axis = 1)
                # except first appearance of card
                all_but_one[arg] = False
                active_hand = active_hand[all_but_one]
                #active_hand = active_hand[np.any(active_hand[:] != card, axis = 1)]
                active_player.hand = active_hand
    # update Game

        current_game.update(active_player_seating, move)

    # update Table

        # add top cards
        if len(move) > 0:
            # check suite lock condition
            if table.is_empty == True:
                table.is_empty == False
            elif table.is_suite_lock == False and len(move) > 1: 
                arg = np.argsort(move[:,0])
                move = move[arg]
                arg = np.argsort(table.top_cards[:,0])
                table.top_cards = table.top_cards[arg]
                if np.all(move[:,0] == table.top_cards[:,0]):
                    table.is_suite_lock == True

            table.update(active_player_seating, move,)

            # check straight condition
            if table.is_straight == False and len(move) >=3:
                arg = np.argsort(move[:,1])
                move = move[arg]
                diff = move - np.insert(move[:-1], 0, move[0] -1, axis = 0)
                if np.all(diff[:,1] == 1):
                    table.is_straight = True


    ### Special cards and revolution ###
    # if revolution is played
        # update Game
            if len(move) >= 4:
                current_game.is_rev_switch = not current_game.is_rev_switch
    # if 10 is played:
            # discard one card for every 10
            for boolean in table.top_cards[:,1] == 7:
                # the last card can't be discarded
                if boolean and active_player.hand.shape[0] > 1:        
            # Action: Choose card in Hand
                    print("Please discard a card")
                    discard_card_list = []
                    for card in active_hand:
                        discard_card_list.append([card])

                    discarded_card = choose(discard_card_list, active_player_seating)
                    #discarded_card = choose(active_hand, active_player_seating)
                    print("Player discarded:", get_human_cards(discarded_card))
    ## End of Action ##
    ###################
            # update Player 
                    active_hand = active_hand[np.any(active_hand[:] != discarded_card, axis = 1)]
                    active_player.hand = active_hand

            # update Discard
                    discard_pile.update(discarded_card)

    # if Jack is played:
            if np.any(table.top_cards[:,1] == 8):
        # update Table
                table.is_jack_switch = not table.is_jack_switch

    # if 8 is played:
            if np.any(table.top_cards[:,1] == 5):
        # update Table
                table.clear(discard_pile)
                current_game.update()
        # update Game (starting player)
                if len(active_hand) > 0:
                    current_game.starting_player = active_player
                    # active player may play again
                    continue
    ###

    ### Updating the game status ###
    # check if Hand of one Player is empty
            if len(active_player.hand) == 0:
                print("player finished", active_player_seating)
                current_ranking.append(active_player_seating)


        # repeat until all passed
        elif len(move) == 0:
            # check if all passed including player with top cards
            # empty the Table, player who played the last cards becomes active player
            if table.top_player == active_player_seating:
                print("empty table for player:", active_player_seating)
                # update Table
                table.clear(discard_pile)
                current_game.update()
                continue
            # check now wether the player is already done
            while table.top_player in current_ranking:
                table.top_player +=1
                if table.top_player == current_match.n_players:
                    table.top_player = 0

        while True:
            # next player's turn
            active_player_seating += + 1
            if active_player_seating == current_match.n_players:
                active_player_seating = 0
            active_player = player_lst[active_player_seating]
            # exclude finished players
            if active_player_seating in current_ranking:
                print("skip player", active_player_seating)
                continue
            else:
                break

        # repeat until one Player is left
        if len(current_ranking) ==  current_match.n_players- 1:
            print("Game has ended.")
            print("Last player:", active_player_seating)
            current_ranking.append(active_player_seating)
            print("Game ranking:", current_ranking)
            break
    ###

    # end of game - update

    # Table
    table.clear(discard_pile)

    # Game

    current_game.end()

    # Match

    current_match.update(current_ranking, current_game.game_history)

    # Players

    for player in player_lst:
        player.clear()

    # update Discard

    discard_pile.clear()

    # End of Game #
    ###############
    print("Game " + str(current_match.n_games_played) + " completed")

    # repeat Game until total number of games is reached

# End of Match #
################
print("Match has ended!")

# Anounce ranking and winner
print("Ranking:", current_match.rank_history)

# display match stats
#print("Match history", current_match.match_history)

all_rankings = np.array(current_match.rank_history)
first_places = np.bincount(all_rankings[:,0])
total_ranking = np.flipud(np.argsort(first_places))
winner = np.where(first_places[:] == np.max(first_places[:]))

#winner = np.argmax(first_places)
print("Total ranking: " + str(total_ranking))
print("The winner is player:", str(winner))


# FINALISE #
t1 = time.time()

print("Total run time:", t1-t0)





















