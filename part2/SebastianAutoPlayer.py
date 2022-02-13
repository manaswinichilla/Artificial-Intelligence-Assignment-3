# Automatic Sebastian game player
# B551 Fall 2020
# admysore-hdeshpa-machilla
#
# Based on skeleton code by D. Crandall
#
#
# This is the file you should modify to create your new smart player.
# The main program calls this program three times for each turn.
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list
#      of dice indices that should be re-rolled.
#
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#

from SebastianState import Dice
from SebastianState import Scorecard
import random
import operator

class SebastianAutoPlayer:

    def __init__(self):
        dice = Dice()

    # calculating the score for categories that haven't been visited yet
    # and whose conditions are satisfied by the list of dice values
    def cost_function(self, diceval, not_visited):
        scorelist = {}
        counts = [diceval.count(i) for i in range(1, 7)]
        Numbers = {"primis": 1, "secundus": 2, "tertium": 3, "quartus": 4, "quintus": 5, "sextus": 6}

        for category in not_visited:
        #for the 1st 6 categories- primis, secundus, tertium, quartus, quintus, sextus
            if category in Numbers.keys():
                scorelist[category] = counts[Numbers[category] - 1] * Numbers[category]
            if category == "company":
                if sorted(diceval) == [1, 2, 3, 4, 5] or sorted(diceval) == [2, 3, 4, 5, 6]:
                    scorelist["company"] = 40
                else:
                    scorelist["company"] = 0
            if category == "prattle":
                if (len(set([1, 2, 3, 4]) - set(diceval)) == 0 or len(
                        set([2, 3, 4, 5]) - set(diceval)) == 0 or len(
                        set([3, 4, 5, 6]) - set(diceval)) == 0):
                    scorelist["prattle"] = 30
                else:
                    scorelist["prattle"] = 0
            if category == "squadron":
                if (2 in counts) and (3 in counts):
                    scorelist["squadron"] = 25
                else:
                    scorelist["squadron"] = 0
            if category == "triplex":
                if max(counts) >= 3:
                    scorelist["triplex"] = (sum(diceval))
                else:
                    scorelist["triplex"] = 0
            if category == "quadrupla":
                if max(counts) >= 4:
                    scorelist["quadrupla"] = (sum(diceval))
                else:
                    scorelist["quadrupla"] = 0
            if category == "quintuplicatam":
                if max(counts) == 5:
                    scorelist["quintuplicatam"] = 50
                else:
                    scorelist["quintuplicatam"] = 0
            if category == "pandemonium":
                scorelist["pandemonium"] = sum(diceval)

        return scorelist

    # This function gets the dice list values over all the successors
    # For each dice value in the dice list, it checks the boolean value and decides whether to reroll or not
    def get_dice_list(self, dices, reroll):
        dicelist = []
        for outcome_a in ((dices.dice[0],) if not (reroll[0]) else range(1, 7)):
            for outcome_b in ((dices.dice[1],) if not (reroll[1]) else range(1, 7)):
                for outcome_c in ((dices.dice[2],) if not (reroll[2]) else range(1, 7)):
                    for outcome_d in ((dices.dice[3],) if not (reroll[3]) else range(1, 7)):
                        for outcome_e in ((dices.dice[4],) if not (reroll[4]) else range(1, 7)):
                            newdice = [outcome_a, outcome_b, outcome_c, outcome_d, outcome_e]
                            dicelist.append(newdice)
        return dicelist

        # This function calculates the score over all the successors
        # reference-  Professor Crandall's solution code explanation for week 8's activity- 'a game of chance'
    def expectation(self, dices, reroll, not_visited):
        max_at_exp_layer = ([], 0)
        dicelist = self.get_dice_list(dices, reroll)
        # for each dice value list, we call the cost function and get the list of unvisited categories
        for dice in dicelist:
            scorelist = self.cost_function(dice, not_visited)
            # for each of these unvisited category's expected score, we calculate the probability
            for category in scorelist.keys():
                scorelist[category] = scorelist[category] / len(dicelist)
            # fetch the max from these scores
            max_expected = max(scorelist.items(), key=operator.itemgetter(0))[1]
            # to get the best seen expected score till now
            if max_expected > max_at_exp_layer[1]:
                max_at_exp_layer = (dice, max_expected)
        # return dice value list and expected score
        return max_at_exp_layer[0], max_at_exp_layer[1]

    # This is the max layer of expectiminimax
    # reference-  Professor Crandall's solution code explanation for week 8's activity- 'a game of chance'
    def max_layer(self, dice, not_visited):
        max_at_max_layer = ([], 0)
        outcome_count = 0
        # it takes on boolean values for each of the dice values in the list
        # A 'True' value for a dice indicates that it can be rerollled
        for dice_a in (True, False):
            for dice_b in (True, False):
                for dice_c in (True, False):
                    for dice_d in (True, False):
                        for dice_e in (True, False):
                            # fetch the dice value list, expected score for each possibility
                            newdiceval, exp_score = self.expectation(dice, (dice_a, dice_b, dice_c, dice_d, dice_e),not_visited)
                            outcome_count += 1
                            # to get the list of dice values with the highest score
                            if exp_score > max_at_max_layer[1]:
                                max_at_max_layer = (newdiceval, exp_score)
        # return dice value list
        return max_at_max_layer[0]

    # This function is to return a list of categories that haven't been visited
    def get_list_of_categories(self, visited):
        Categories = ["primis", "secundus", "tertium", "quartus", "quintus", "sextus", "company", "prattle",
                      "squadron", "triplex", "quadrupla", "quintuplicatam", "pandemonium"]
        not_visited = list(set(Categories) - set(visited))
        return not_visited

    def first_roll(self, dice, scorecard):
        sc = scorecard.scorecard
        # to get a list of unvisited categories
        not_visited = self.get_list_of_categories(list(sc.keys()))
        # call to max_layer
        newdiceval = self.max_layer(dice, not_visited)
        return newdiceval

    def second_roll(self, dice, scorecard):
        sc = scorecard.scorecard
        # to get a list of unvisited categories
        not_visited = self.get_list_of_categories(list(sc.keys()))
        # call to max_layer
        newdiceval = self.max_layer(dice, not_visited)
        return newdiceval

    def third_roll(self, dice, scorecard):
        sc = scorecard.scorecard
        # to get a list of unvisited categories
        not_visited = self.get_list_of_categories(list(sc.keys()))
        # call to cost_function to get the scores for all the applicable and unvisited categories
        scorelist = self.cost_function(dice.dice, not_visited)
        # return the category which had the highest score
        return max(scorelist.items(), key=operator.itemgetter(1))[0]