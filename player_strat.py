from itertools import combinations
from game import read_hand, subtract_hand
from house_strat import house_strat

def player_strat(hand:list, dealer_split:dict): ## takes 7 card hand list and strat function and returns a split dict
	split = {
		'high': {},
		'low': {},
	}
	high_hand = house_strat(hand)['high']
	low_hand = house_strat(hand)['low']
	dealer_high = dealer_split['high']
	dealer_low = dealer_split['low']

	## can other variations beat dealer?
	if high_hand['rank_points'] <= dealer_high['rank_points'] or low_hand['rank_points'] <= dealer_low['rank_points']:
		possible_five_card_hands = list(combinations(hand, 5))
		for hh in possible_five_card_hands:
			lh = subtract_hand(hand, hh)
			if read_hand(hh)['rank_points'] > dealer_high['rank_points'] and read_hand(lh)['rank_points'] > dealer_low['rank_points']:
				high_hand = hh
				low_hand = lh
				break
			elif read_hand(hh)['rank_points'] > dealer_high['rank_points'] and read_hand(hh)['rank_points'] > read_hand(high_hand)['rank_points']:
				high_hand = hh
				low_hand = lh
			elif read_hand(lh)['rank_points'] > dealer_low['rank_points'] and read_hand(lh)['rank_points'] > read_hand(low_hand)['rank_points']:
				high_hand = hh
				low_hand = lh

	split = {
		'high': read_hand(high_hand),
		'low': read_hand(low_hand),
	}

	return split