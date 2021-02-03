import random

from typing import Dict, List


class Bot(object):
    def __init__(self):
        self.name = "1702502"

    def get_bid_game_type_collection(
        self,
        current_round: int,
        bots,
        game_type: str,
        winner_pays: int,
        artists_and_values,
        round_limit: int,
        starting_budget: int,
        painting_order: List[str],
        target_collection: List[int],
        my_bot_details,
        current_painting: str,
        winner_ids: List[str],
        amounts_paid: List[int],
    ) -> int:
        """
        Defines the strategy used for "collection" type games.

        Args:
            current_round: The current round number
            bots: Information about the other bots in the game
            game_type: Either "collection" or "value"
            winner_pays: Whether the winner pays their bet or the one below
            artist_and_values: Assignment of scores for each artist
            round_limit: Total number of rounds in the game
            starting_budget: How much each bot began with
            painting_order: The order in which paintings will be auctioned
            target_collection: The type of collection required to win a collection game
            my_bot_details: Information about your bot
            current_painting: The artist for the current painting
            winner_ids: The identifiers for the winners so far
            amounts_paid: The amount paid for each painting so far

        Returns: The bid to be placed this round
        """

        my_budget = my_bot_details["budget"]
        return random.randint(0, my_budget)

    def get_bid_game_type_value(
        self,
        current_round: int,
        bots,
        game_type: str,
        winner_pays: int,
        artists_and_values: Dict[str, int],
        round_limit: int,
        starting_budget: int,
        painting_order: List[str],
        target_collection: List[int],
        my_bot_details,
        current_painting: str,
        winner_ids: List[str],
        amounts_paid: List[int],
    ) -> int:
        """
        Defines the strategy used for "value" type games.

        Args:
            current_round: The current round number
            bots: Information about the other bots in the game
            game_type: Either "collection" or "value"
            winner_pays: Whether the winner pays their bet or the one below
            artist_and_values: Assignment of scores for each artist
            round_limit: Total number of rounds in the game
            starting_budget: How much each bot began with
            painting_order: The order in which paintings will be auctioned
            target_collection: The type of collection required to win a collection game
            my_bot_details: Information about your bot
            current_painting: The artist for the current painting
            winner_ids: The identifiers for the winners so far
            amounts_paid: The amount paid for each painting so far

        Returns: The bid to be placed this round
        """
        # WRITE YOUR STRATEGY HERE FOR VALUE GAMES - MOST VALUABLE PAINTINGS WON WINS

        # Here is an example of how to get the current painting's value
        current_painting_value = artists_and_values[current_painting]
        print("The current painting's value is ", current_painting_value)

        # Here is an example of printing who won the last round
        if current_round > 1:
            who_won_last_round = winner_ids[current_round - 1]
            print("The last round was won by ", who_won_last_round)

        # Play around with printing out other variables in the function,
        # to see what kind of inputs you have to work with
        my_budget = my_bot_details["budget"]
        return random.randint(0, my_budget)
