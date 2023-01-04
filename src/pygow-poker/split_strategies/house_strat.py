from common import get_outcome, subtract_hand

## there are so many house rules for setting hands so I will be using this guide I found
## https://www.stonesgamblinghall.com/portfolio-item/face-up-pai-gow-poker/


def house_strat(hand: list):
    split = {
        "high": {},
        "low": {},
    }
    high_hand = []
    low_hand = []

    ## deconstruct outcome
    OUTCOME = get_outcome(hand)
    HAND = OUTCOME["hand"]
    RANK = OUTCOME["rank"]
    RANK_POINTS = OUTCOME["rank_points"]
    HAS_JOKER = OUTCOME["has_joker"]
    HIGH_CARD_ORDER = OUTCOME["high_card_order"]
    MULTIPLES = OUTCOME["multiples"]
    MULTIPLES_KEYS = OUTCOME["multiples_keys"]
    STRAIGHTS = OUTCOME["straights"]
    FLUSHES = OUTCOME["flushes"]
    STRAIGHT_FLUSHES = OUTCOME["straight_flushes"]
    SEVEN_CARD_STRAIGHT_FLUSH = OUTCOME["seven_card_straight_flush"]

    ## helper function in case of two pair; returns tuple of hands
    def two_pair_strat():
        high_hand = []
        low_hand = []
        if int(MULTIPLES_KEYS[1]) >= 12:  ##if high pair are As, Ks, or Qs then split
            low_hand = MULTIPLES[MULTIPLES_KEYS[0]]
            high_hand = subtract_hand(HAND, low_hand)
        elif (
            11 >= int(MULTIPLES_KEYS[1]) >= 9
        ):  ##if high pair are Js, 10s, or 9s - has A high keep together; else split
            if HIGH_CARD_ORDER[-1][:2] == "14" or HIGH_CARD_ORDER[-1] == "JKR":
                low_hand = [HIGH_CARD_ORDER[-2], HIGH_CARD_ORDER[-1]]
                high_hand = subtract_hand(HAND, low_hand)
            else:
                low_hand = MULTIPLES[MULTIPLES_KEYS[0]]
                high_hand = subtract_hand(HAND, low_hand)
        elif (
            8 >= int(MULTIPLES_KEYS[1]) >= 6
        ):  ##if high pair are 8s, 7s, or 6s - has K or higher keep together; else split
            if (
                HIGH_CARD_ORDER[-1][:2] == "13"
                or HIGH_CARD_ORDER[-1][:2] == "14"
                or HIGH_CARD_ORDER[-1] == "JKR"
            ):
                low_hand = [HIGH_CARD_ORDER[-2], HIGH_CARD_ORDER[-1]]
                high_hand = subtract_hand(HAND, low_hand)
            else:
                low_hand = MULTIPLES[MULTIPLES_KEYS[0]]
                high_hand = subtract_hand(HAND, low_hand)
        elif (
            5 >= int(MULTIPLES_KEYS[1]) >= 3
        ):  ##if high pair are 5s, 4s, or 3s - has Q or higher keep together; else split
            if (
                HIGH_CARD_ORDER[-1][:2] == "12"
                or HIGH_CARD_ORDER[-1][:2] == "13"
                or HIGH_CARD_ORDER[-1][:2] == "14"
                or HIGH_CARD_ORDER[-1] == "JKR"
            ):
                low_hand = [HIGH_CARD_ORDER[-2], HIGH_CARD_ORDER[-1]]
                high_hand = subtract_hand(HAND, low_hand)
            else:
                low_hand = MULTIPLES[MULTIPLES_KEYS[0]]
                high_hand = subtract_hand(HAND, low_hand)
        return high_hand, low_hand

    ## helper function in case of straight, flush, or straight flush; takes outcome type as list and rank string and returns tuple of hands
    def get_best_low_hand(type: list):
        low_hand = []
        if STRAIGHT_FLUSHES:
            for i, h in enumerate(STRAIGHT_FLUSHES):
                if i == 0:
                    low_hand = subtract_hand(HAND, h)
                elif (
                    get_outcome(subtract_hand(HAND, h))["rank_points"]
                    > get_outcome(low_hand)["rank_points"]
                ):
                    low_hand = subtract_hand(HAND, h)
            for i, h in enumerate(FLUSHES):
                if (
                    get_outcome(subtract_hand(HAND, h))["rank_points"]
                    > get_outcome(low_hand)["rank_points"]
                ):
                    low_hand = subtract_hand(HAND, h)
            for i, h in enumerate(STRAIGHTS):
                if (
                    get_outcome(subtract_hand(HAND, h))["rank_points"]
                    > get_outcome(low_hand)["rank_points"]
                ):
                    low_hand = subtract_hand(HAND, h)
        else:
            for i, h in enumerate(type):
                if i == 0:
                    low_hand = subtract_hand(HAND, h)
                elif (
                    get_outcome(subtract_hand(HAND, h))["rank_points"]
                    > get_outcome(low_hand)["rank_points"]
                ):
                    low_hand = subtract_hand(HAND, h)
        return low_hand

    def straight_flush_strat(type: list):
        high_hand = []
        low_hand = []
        if not MULTIPLES_KEYS:  ##no pair - keep type; highest possible hand in low hand
            low_hand = get_best_low_hand(type)
            high_hand = subtract_hand(HAND, low_hand)
        elif (
            len(MULTIPLES_KEYS) == 1 and len(MULTIPLES[MULTIPLES_KEYS[0]]) == 2
        ):  ##one pair - keep type; highest possible hand in low hand
            low_hand = get_best_low_hand(type)
            high_hand = subtract_hand(HAND, low_hand)
        elif (
            len(MULTIPLES_KEYS) == 2
            and (len(MULTIPLES[MULTIPLES_KEYS[0]]) == 3
            or len(MULTIPLES[MULTIPLES_KEYS[1]]) == 3)
        ):  ## Full house containing ace(s) and a joker presumably like in ['02s', '04d', '04s', '05s', '14h', '14s', 'JKR']
            high_hand, low_hand = full_house_strat()
        elif (
            len(MULTIPLES_KEYS) == 2
            and len(MULTIPLES[MULTIPLES_KEYS[0]]) == 2
            and len(MULTIPLES[MULTIPLES_KEYS[1]]) == 2
        ):  ##two pair - keep type with pair in low hand; else two pair strategy
            low_hand = get_best_low_hand(type)
            if get_outcome(low_hand)["rank"] == "Pair":
                high_hand = subtract_hand(HAND, low_hand)
            else:
                return two_pair_strat()
        elif (
            len(MULTIPLES_KEYS) == 1 and len(MULTIPLES[MULTIPLES_KEYS[0]]) in (3, 4)
        ):  ##three-of-a-kind or four-of-a-kind - keep type with pair or A in low hand
            low_hand = get_best_low_hand(type)
            high_hand = subtract_hand(HAND, low_hand)
        elif (
            len(MULTIPLES_KEYS) == 3
            and len(MULTIPLES[MULTIPLES_KEYS[0]])
            == len(MULTIPLES[MULTIPLES_KEYS[1]])
            == len(MULTIPLES[MULTIPLES_KEYS[2]])
            == 2
        ):  ## three pair - highest pair in low hand
            low_hand = MULTIPLES[MULTIPLES_KEYS[2]]  ##highest pair in low hand
            high_hand = subtract_hand(HAND, low_hand)
        return high_hand, low_hand

    def full_house_strat():
        if (
            len(MULTIPLES_KEYS) == 2
            and len(MULTIPLES[MULTIPLES_KEYS[0]])
            == len(MULTIPLES[MULTIPLES_KEYS[1]])
            == 3
        ):  ##two of three-of-a-kind - pair from highest three-of-a-kind in low hand
            low_hand = MULTIPLES[MULTIPLES_KEYS[1]][-2:]
            high_hand = subtract_hand(HAND, low_hand)
        else:  ##highest pair in low hand
            for key in list(reversed(MULTIPLES_KEYS)):
                if len(MULTIPLES[key]) == 2:
                    low_hand = MULTIPLES[key]
                    high_hand = subtract_hand(HAND, low_hand)
                    break
        return high_hand, low_hand

    if RANK == "Five Aces":  ## five aces
        low_hand = [
            MULTIPLES["14"][0],
            MULTIPLES["14"][1],
        ]  ##play pair of As in low hand
        high_hand = subtract_hand(HAND, low_hand)

    elif RANK == "Four-of-a-kind":  ## four of a kind
        if len(MULTIPLES_KEYS) > 1:  ## with pair or three-of-a-kind - pair in low hand
            for key in MULTIPLES_KEYS:
                if len(MULTIPLES[key]) < 4:
                    low_hand = MULTIPLES[key][-2:]
                    high_hand = subtract_hand(HAND, low_hand)
                    break
        elif int(MULTIPLES_KEYS[0]) >= 12:  ## As, Ks, or Qs split
            low_hand = MULTIPLES[MULTIPLES_KEYS[0]][:2]
            high_hand = subtract_hand(HAND, low_hand)
        elif (
            11 >= int(MULTIPLES_KEYS[0]) >= 9
        ):  ## Js, 10s, or 9s - has K or higher keep together; else split
            if (
                HIGH_CARD_ORDER[-1][:2] == "13"
                or HIGH_CARD_ORDER[-1][:2] == "14"
                or HIGH_CARD_ORDER[-1] == "JKR"
            ):
                low_hand = [HIGH_CARD_ORDER[-2], HIGH_CARD_ORDER[-1]]
                high_hand = subtract_hand(HAND, low_hand)
            else:
                low_hand = MULTIPLES[MULTIPLES_KEYS[0]][:2]
                high_hand = subtract_hand(HAND, low_hand)
        elif (
            8 >= int(MULTIPLES_KEYS[0]) >= 6
        ):  ## 8s, 7s, 6s - has Q or higher keep together; else split
            if (
                HIGH_CARD_ORDER[-1][:2] == "12"
                or HIGH_CARD_ORDER[-1][:2] == "13"
                or HIGH_CARD_ORDER[-1][:2] == "14"
                or HIGH_CARD_ORDER[-1] == "JKR"
            ):
                low_hand = [HIGH_CARD_ORDER[-2], HIGH_CARD_ORDER[-1]]
                high_hand = subtract_hand(HAND, low_hand)
            else:
                low_hand = MULTIPLES[MULTIPLES_KEYS[0]][:2]
                high_hand = subtract_hand(HAND, low_hand)
        elif 5 >= int(MULTIPLES_KEYS[0]) >= 2:  ## 5s, 4s, 3s, 2s - always keep together
            low_hand = [HIGH_CARD_ORDER[-2], HIGH_CARD_ORDER[-1]]
            high_hand = subtract_hand(HAND, low_hand)

    elif (
        RANK == "Full House"
    ):  ## full house with or without straight, flush, or straight flush
        high_hand, low_hand = full_house_strat()

    elif STRAIGHT_FLUSHES:
        high_hand = straight_flush_strat(STRAIGHT_FLUSHES)[0]
        low_hand = straight_flush_strat(STRAIGHT_FLUSHES)[1]

    elif FLUSHES:
        high_hand = straight_flush_strat(FLUSHES)[0]
        low_hand = straight_flush_strat(FLUSHES)[1]

    elif STRAIGHTS:
        high_hand = straight_flush_strat(STRAIGHTS)[0]
        low_hand = straight_flush_strat(STRAIGHTS)[1]

    elif (
        len(MULTIPLES_KEYS) == 3
        and len(MULTIPLES[MULTIPLES_KEYS[0]])
        == len(MULTIPLES[MULTIPLES_KEYS[1]])
        == len(MULTIPLES[MULTIPLES_KEYS[2]])
        == 2
    ):  ## three pair without straight, flush, or straight flush
        low_hand = MULTIPLES[MULTIPLES_KEYS[2]]  ##highest pair in low hand
        high_hand = subtract_hand(HAND, low_hand)

    elif RANK == "Three-of-a-kind":  ## three-of-a-kind
        if (
            MULTIPLES_KEYS[0] == "14"
        ):  ##always play together unless cards are A, then split 2 in high and 1 and low
            low_hand = [
                HIGH_CARD_ORDER[-1],
                MULTIPLES[MULTIPLES_KEYS[0]][0],
            ]  ##highest pair in low hand
            high_hand = subtract_hand(HAND, low_hand)
        else:
            low_hand = [
                HIGH_CARD_ORDER[-1],
                HIGH_CARD_ORDER[-2],
            ]  ##highest pair in low hand
            high_hand = subtract_hand(HAND, low_hand)

    elif RANK == "Two Pair":  ## two pair
        high_hand = two_pair_strat()[0]
        low_hand = two_pair_strat()[1]

    elif RANK == "Pair":  ## one pair
        low_hand = [HIGH_CARD_ORDER[-2], HIGH_CARD_ORDER[-1]]
        high_hand = subtract_hand(HAND, low_hand)

    elif RANK_POINTS < 100:  ## no pair
        try:
            low_hand = [HIGH_CARD_ORDER[-3], HIGH_CARD_ORDER[-2]]
            high_hand = subtract_hand(HAND, low_hand)
        except:
            print(hand)

    ## Return and error handling
    if not high_hand or not low_hand:
        print("Error: null hand found", f"high_hand:{high_hand}", f"low_hand{low_hand}")
        print(HAND)
        split = {
            "high": {},
            "low": {},
        }
    elif get_outcome(high_hand)["rank_points"] < get_outcome(low_hand)["rank_points"]:
        print("Error: low hand is higher than high hand", split)
        print(HAND)
        split = {
            "high": {},
            "low": {},
        }
    else:
        split = {
            "high": get_outcome(high_hand),
            "low": get_outcome(low_hand),
        }
    return split
