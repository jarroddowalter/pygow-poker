from itertools import combinations
from common import get_outcome, subtract_hand
from split_strategies import house_strat


def player_strat(
    hand: list, dealer_split: dict
):  ## takes 7 card hand list and strat function and returns a split dict
    split = {
        "high": {},
        "low": {},
    }
    high_hand = house_strat.house_strat(hand)["high"]
    low_hand = house_strat.house_strat(hand)["low"]
    dealer_high = dealer_split["high"]
    dealer_low = dealer_split["low"]

    ## can other variations beat dealer?
    if (
        high_hand["rank_points"] <= dealer_high["rank_points"]
        or low_hand["rank_points"] <= dealer_low["rank_points"]
    ):
        possible_five_card_hands = list(combinations(hand, 5))
        for hh in possible_five_card_hands:
            lh = subtract_hand(hand, hh)
            if (
                get_outcome(hh)["rank_points"] > dealer_high["rank_points"]
                and get_outcome(lh)["rank_points"] > dealer_low["rank_points"]
                and get_outcome(hh)["rank_points"] > get_outcome(lh)["rank_points"]
            ):
                high_hand = get_outcome(hh)
                low_hand = get_outcome(lh)
                break
            elif (
                get_outcome(hh)["rank_points"] > dealer_high["rank_points"]
                and get_outcome(hh)["rank_points"] > high_hand["rank_points"]
                and get_outcome(hh)["rank_points"] > get_outcome(lh)["rank_points"]
            ):
                high_hand = get_outcome(hh)
                low_hand = get_outcome(lh)
            elif (
                get_outcome(lh)["rank_points"] > dealer_low["rank_points"]
                and get_outcome(lh)["rank_points"] > low_hand["rank_points"]
                and get_outcome(hh)["rank_points"] > get_outcome(lh)["rank_points"]
            ):
                high_hand = get_outcome(hh)
                low_hand = get_outcome(lh)

    split = {
        "high": high_hand,
        "low": low_hand,
    }

    return split
