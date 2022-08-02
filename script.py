from array import array
import random
from rich import print
from rich.console import Console

console = Console()

DECK = [
'02h', '02d', '02s', '02c',
'03h', '03d', '03s', '03c',
'04h', '04d', '04s', '04c',
'05h', '05d', '05s', '05c',
'06h', '06d', '06s', '06c',
'07h', '07d', '07s', '07c',
'08h', '08d', '08s', '08c',
'09h', '09d', '09s', '09c',
'10h', '10d', '10s', '10c',
'11h', '11d', '11s', '11c',
'12h', '12d', '12s', '12c',
'13h', '13d', '13s', '13c',
'14h', '14d', '14s', '14c',
'JKR'
]

SUIT_ORDER = ['d', 'h', 'c', 's']

test_hand = ['03c', '05h', '06c', '07c', '08h', '09c', '11c']

def format_card(card:str): ## returns formatted card string
	converted_card = ''

	match card[:2]: ## convert num
		case '02':
			converted_card = '2'
		case '03':
			converted_card = '3'
		case '04':
			converted_card = '4'
		case '05':
			converted_card = '5'
		case '06':
			converted_card = '6'
		case '07':
			converted_card = '7'
		case '08':
			converted_card = '8'
		case '09':
			converted_card = '9'
		case '10':
			converted_card = '10'
		case '11':
			converted_card = 'J'
		case '12':
			converted_card = 'Q'
		case '13':
			converted_card = 'K'
		case '14':
			converted_card = 'A'
		case 'JK':
			converted_card = 'JKR'
	
	match card[-1]: ## convert suit
		case 'h':
			converted_card = converted_card + '♥'
		case 'd':
			converted_card = converted_card + '♦'
		case 's':
			converted_card = converted_card + '♠'
		case 'c':
			converted_card = converted_card + '♣'

	return converted_card

def format_deck(deck:list): ## returns formated list
	converted_deck = []

	for card in deck:
		converted_deck.append(format_card(card))

	return converted_deck

def sort_hand(hand:list): ## takes preformatted hand
	global SUIT_ORDER
	hand.sort()

	def get_card_suit_order(card:str): ## returns index of suit order
		for i, item in enumerate(SUIT_ORDER):
			if card == "JKR":
				return 4
			elif card[-1] == item:
				return i

	i = 0
	while i < len(hand):
		if hand[i][:2] == hand[i-1][:2] and get_card_suit_order(hand[i]) < get_card_suit_order(hand[i-1]):
			hand.insert(i-1, hand.pop(i))
			i = 0
		else:
			i += 1
	
	return hand

def read_hand(hand:list): ## returns outcome as a dict
	outcome = {
		'hand': hand,
		'rank': '',
		'rank_points': 0,
		'has_joker': False,
		'high_card_order': [],
		'multiples': {},
		'multiples_keys': [],
		'flush': [],
		'straight': [],
		'straight_flush': []
	}
	hand = sort_hand(hand)

	## count num and suits
	num_count = {}
	suit_count = {}

	for card in hand:
		if card == "JKR":
			outcome['has_joker'] = True
		else:
			if num_count.get(card[:2], False): 
				num_count[card[:2]] += 1
			else:
				num_count[card[:2]] = 1
			if suit_count.get(card[-1], False):
				suit_count[card[-1]] += 1
			else:
				suit_count[card[-1]] = 1

	## get high card order
	for key, val in num_count.items():
		if key != '14':
			if val == 1:
				for card in hand:
					if card[:2] == key:
						outcome['high_card_order'].append(card)
		elif val == 1 or (outcome['has_joker'] and val == 0):
			for card in hand:
				if card[:2] == key or card == 'JKR':
					outcome['high_card_order'].append(card)
	

	## get multiples
	for key, val in num_count.items():
		if key != '14':
			if val > 1:
				outcome['multiples'][key] = []
				for card in hand:
					if card[:2] == key:
						outcome['multiples'][key].append(card)
		elif val > 1 or (outcome['has_joker'] and val > 0):
			outcome['multiples'][key] = []
			for card in hand:
				if card[:2] == key or card == 'JKR':
					outcome['multiples'][key].append(card)

	outcome['multiples_keys'] = list(outcome['multiples'].keys())

	## get flush
	for key, val in suit_count.items():
		if val >= 5 or (val == 4 and outcome['has_joker']):
			for card in hand:
				if card[-1] == key or card == 'JKR':
					outcome['flush'].append(card)

	## get straight
	hand_reversed = list(reversed(hand))
	for i, card in enumerate(hand_reversed):
		if i == 0:
			outcome['straight'].append(card)
		elif card[:2] == '14':
			if not outcome['straight'] or outcome['straight'][0] == 'JKR':
				outcome['straight'] = [card]
			elif outcome['straight'][-1][:2] == '14' and outcome['flush'] and card[-1] == outcome['flush'][0][-1]: ##if flush and multiples put suit in straight
				outcome['straight'] = [card]
		elif hand_reversed[i-1] != 'JKR' and int(card[:2]) == int(hand_reversed[i-1][:2]) - 1:
			outcome['straight'].append(card)
		elif hand_reversed[i-1] != 'JKR' and outcome['has_joker'] and int(card[:2]) == int(hand_reversed[i-1][:2]) - 2:
			if 'JKR' in outcome['straight']:
				outcome['straight'] = outcome['straight'][outcome['straight'].index('JKR')+1:]
			outcome['straight'].extend(['JKR', card])
		elif outcome['straight'][-1] != 'JKR' and int(card[:2]) == int(outcome['straight'][-1][:2]):
			if outcome['flush'] and card[-1] == outcome['flush'][0][-1]:
				outcome['straight'].pop(-1)
				outcome['straight'].append(card)
			else:
				if len(outcome['straight']) >= 5:
					break
		else:
			if len(outcome['straight']) >= 5:
				break
			else:
				if outcome['has_joker']:
					outcome['straight'] = ['JKR', card]
				else:
					outcome['straight'] = [card]

	if outcome['has_joker'] and 'JKR' not in outcome['straight']: ## add low JKR
		outcome['straight'].append('JKR')
	
	low_ace = '' ## check low Ace
	for card in hand_reversed:
		if card[:2] == '14':
			low_ace = card
			if outcome['flush']:
				if card[-1] == outcome['flush'][0][-1]:
					break
				else:
					continue
			else:
				break
	if outcome['straight'][-1][:2] == '02' and low_ace:
		outcome['straight'].append(low_ace)
	elif 'JKR' in outcome['straight'] and outcome['straight'][-1][:2] == '03' and low_ace:
		if len(outcome['straight']) < 5:
			outcome['straight'] = outcome['straight'][outcome['straight'].index('JKR')+1:]
			outcome['straight'].extend(['JKR', low_ace])
		elif len(outcome['straight']) == 6:
			outcome['straight'] = outcome['straight'][outcome['straight'].index('JKR')+1:]
			outcome['straight'].extend(['JKR', low_ace])

	if len(outcome['straight']) <  5:
		outcome['straight'] = []
	else:
		outcome['straight'] = list(reversed(outcome['straight']))

	## get straight flush
	if outcome['straight'] and outcome['flush']:
		used_joker = False
		for card in outcome['straight']:
			if card[-1] == outcome['flush'][0][-1]:
				outcome['straight_flush'].append(card)
			elif card == 'JKR' and not used_joker:
					outcome['straight_flush'].append(card)
					used_joker = True
			elif 'JKR' in outcome['straight'] and not used_joker:
					outcome['straight_flush'].append('JKR')
					used_joker = True
			else:
				break

		if outcome['straight_flush'] and outcome['straight_flush'][-1] == 'JKR' and outcome['straight_flush'][0][:2] == '02': ##orders for highest straight flush rank A-2-3-4-5 with joker
			outcome['straight_flush'].insert(0, outcome['straight_flush'][-1])
			del outcome['straight_flush'][-1]

		if len(outcome['straight_flush']) <  5:
			outcome['straight_flush'] = []

	#### Score Hand ####

	## 7 Card Straight Flush, No Joker		30000 + 1-8 straight rank (8-9-10-J-Q-K-A highest)
	if len(outcome['straight_flush']) == 7 and not outcome['has_joker']:
		outcome['rank'] = '7 Card Straight Flush, No Joker'
		if outcome['straight_flush'][0][:2] == '14':
			outcome['rank_points'] = 30001
		else:
			outcome['rank_points'] = 30000 + int(outcome['straight_flush'][0][:2])
		return outcome

	## Royal Flush Plus Royal Match			20000 + 1-2 royal match rank (A-K > K-Q of same suite/no joker)
	r_flush = []
	r_match = []
	if outcome['straight_flush'] and (outcome['straight_flush'][-5][:2] == '10' or (outcome['straight_flush'][-5] == 'JKR' and outcome['straight_flush'][-4][:2] == '11')):
		r_flush = [outcome['straight_flush'][-5], outcome['straight_flush'][-4], outcome['straight_flush'][-3], outcome['straight_flush'][-2], outcome['straight_flush'][-1]]
		for card in hand:
			if card not in r_flush:
				r_match.append(card)
		if r_match[0][-1] == r_match[1][-1] and r_match[0][:2] == '13' and r_match[1][:2] == '14':
			outcome['rank'] = 'Royal Flush Plus Royal Match'
			outcome['rank_points'] = 20000 + 2
			return outcome
		if r_match[0][-1] == r_match[1][-1] and r_match[0][:2] == '12' and r_match[1][:2] == '13':
			outcome['rank'] = 'Royal Flush Plus Royal Match'
			outcome['rank_points'] = 20000 + 1
			return outcome

	## 7 Card Straight Flush with Joker		10000 + 1-8 straight rank (8-9-10-J-Q-K-A highest)
	if len(outcome['straight_flush']) == 7:
		outcome['rank'] = '7 Card Straight Flush with Joker'
		if outcome['straight_flush'][0][:2] == '14':
			outcome['rank_points'] = 30000 + 1
		elif outcome['straight_flush'][0] == 'JKR' and outcome['straight_flush'][0][:2] == '09':
			outcome['rank_points'] = 30000 + 8
		else:
			outcome['rank_points'] = 30000 + int(outcome['straight_flush'][0][:2])
		return outcome

	## Five Aces							9000
	if '14' in outcome['multiples'] and outcome['multiples']['14'] == 5:
		outcome['rank'] = 'Five Aces'
		outcome['rank_points'] = 9000
		return outcome

	## Royal Flush							8000
	if outcome['straight_flush'] and (outcome['straight_flush'][-5][:2] == '10' or (outcome['straight_flush'][-5] == 'JKR' and outcome['straight_flush'][-4][:2] == '11')):
		outcome['rank'] = 'Royal Flush'
		outcome['rank_points'] = 8000
		return outcome

	## Straight Flush						7000 + 2-10 straight rank (A-2-3-4-5 highest)
	if outcome['straight_flush']:
		outcome['rank'] = 'Straight Flush'
		if outcome['straight_flush'][0][:2] == '14' or outcome['straight_flush'][0] == 'JKR':
			outcome['rank_points'] = 7000 + 10
		else:
			outcome['rank_points'] = 7000 + int(outcome['straight_flush'][-5][:2])
		return outcome

	## Four-of-a-kind						6000 + 2-14 card val
	for key in outcome['multiples_keys']:
		if len(outcome['multiples'][key]) == 4:
			outcome['rank'] = 'Four-of-a-kind'
			outcome['rank_points'] = 6000 + int(key)
			return outcome

	## Full House							5000 + 2-14 three-of-a-kind card val
	three_key = ''
	two_key = ''
	for key in outcome['multiples_keys']:
		if len(outcome['multiples'][key]) == 3:
			three_key = key
		elif len(outcome['multiples'][key]) == 2:
			two_key = key
	if three_key and two_key:
		outcome['rank'] = 'Full House'
		outcome['rank_points'] = 5000 + int(three_key)
		return outcome

	## Flush								4000 + 6-14 highest card in flush val
	if outcome['flush']:
		outcome['rank'] = 'Flush'
		if outcome['flush'][-1] == 'JKR':
			outcome['rank_points'] = 7000 + 140
		else:
			outcome['rank_points'] = 7000 + int(outcome['flush'][-1][:2])*10
		return outcome

	## Straight								3000 + 1-10 straight rank (10-J-Q-K-A highest)
	if outcome['straight']:
		outcome['rank'] = 'Straight'
		if outcome['straight'][-5][:2] == '14' or (outcome['straight'][-5] == 'JKR' and outcome['straight'][-4][:2] == '02'):
			outcome['rank_points'] = 3000 + 1
		elif outcome['straight'][-5] == 'JKR' and outcome['straight'][-1][:2] == '14':
			outcome['rank_points'] = 3000 + 10
		else:
			outcome['rank_points'] = 3000 + int(outcome['straight'][-5][:2])
		return outcome

	## Three-of-a-kind						2000 + 2-14 card val
	if len(outcome['multiples_keys']) == 1 and len(outcome['multiples'][outcome['multiples_keys'][0]]) == 3:
		outcome['rank'] = 'Three-of-a-kind'
		outcome['rank_points'] = 2000 + int(outcome['multiples_keys'][0])
		return outcome

	## Two Pair								1000 + 2-14 high pair card val
	if len(outcome['multiples_keys']) >= 2 and len(outcome['multiples'][outcome['multiples_keys'][-1]]) == 2 and len(outcome['multiples'][outcome['multiples_keys'][-2]]) == 2:
		outcome['rank'] = 'Two Pair'
		outcome['rank_points'] = 1000 + int(outcome['multiples_keys'][-1])
		return outcome

	## Pair									100 + 2-14 card val
	if len(outcome['multiples_keys']) == 1 and len(outcome['multiples'][outcome['multiples_keys'][0]]) == 2:
		outcome['rank'] = 'Pair'
		outcome['rank_points'] = 100 + int(outcome['multiples_keys'][0])
		return outcome

	## High									2-14 card val
	if outcome['high_card_order']:
		if outcome['high_card_order'][-1] == 'JKR' or outcome['high_card_order'][-1][:2] == '14':
			outcome['rank'] = 'A High'
		elif outcome['high_card_order'][-1][:2] == '13':
			outcome['rank'] = 'K High'
		elif outcome['high_card_order'][-1][:2] == '12':
			outcome['rank'] = 'Q High'
		elif outcome['high_card_order'][-1][:2] == '11':
			outcome['rank'] = 'J High'
		else:
			outcome['rank'] = str(int(outcome['high_card_order'][-1][:2])) + ' High'
		if outcome['high_card_order'][-1] == 'JKR':
			outcome['rank_points'] = 14
		else:
			outcome['rank_points'] = int(outcome['high_card_order'][-1][:2])
		return outcome

def house_strat(hand:list):
	return
	
def strat_split(hand:list, strat): ## takes 7 card hand list and strat function and returns a split dict
	split = {
		'high': {},
		'low': {},
	}
	high_hand = []
	low_hand = []

	if len(hand) != 7:
		print('strat_split error: hand not 7 cards')
		return

	outcome = read_hand(hand)

	split = {
		'high': read_hand(high_hand),
		'low': read_hand(low_hand),
	}

	return split

def custom_split(high_hand:list, low_hand:list): ## takes a high hand list and a low hand list and returns a split dict
	split = {
		'high_hand': [],
		'high_outcome': '',
		'high_points': 0,
		'low_hand': [],
		'low_outcome': '',
		'low_points': 0
	}

	## check if high hand is 5 cards, low hand is 2 cards
	## check if outcome of 5 card hand is better than outcome of 2 card hand

	## use outcome of 7 cards to determine split

	## move correct cards to split dict

	##	get outcomes of both hands

	return split

def determine_winner(player_split:dict, dealer_split:dict):
	if player_split['high_points'] > dealer_split['high_points'] and player_split['low_points'] > dealer_split['low_points']:
		return 'player wins'
	elif player_split['high_points'] > dealer_split['high_points'] or player_split['low_points'] > dealer_split['low_points']:
		return 'push'
	else:
		return 'dealer wins'


player_hand = dealer_hand = [] 
split_player_hands = split_dealer_hands = [[],[]] ##[H, L]

def deal_game():
	global player_hand, dealer_hand

	##shuffle
	game_deck = DECK.copy()
	random.shuffle(game_deck)

	##deal
	player_hand = game_deck[:7]
	del game_deck[:7]
	dealer_hand = game_deck[:7]
	del game_deck[:7]

def print_game_hands():
	print("Dealer: ", end='')
	pretty_print_hand(dealer_hand)
	print()
	print("Player: ", end='')
	pretty_print_hand(player_hand)

def pretty_print_hand(hand: array):
	for i, card in enumerate(hand):
		if card[-1] == "♠" or card[-1] == "♣":
			console.print(" " + card + " ", style="black on white b", end='')
		elif card[-1] == "♥" or card[-1] == "♦":
			console.print(" " + card + " ", style="red on white b", end='')
		elif card == "JKR":
			console.print(" " + card + " ", style="black on white b", end='')\
		
		if len(hand) != i+1:
			console.print(" ", end='')
		else:
			console.print()

deal_game()
print(sort_hand(player_hand))
print(read_hand(player_hand))

##Functions for house strategy and player strategy should take a hand (array of strings) and return split hands (array of two arrays of strings; first being the high hand and second being the low hand). House strategy is set while player strategy can take dealer cards into account if face-up variant.

##Script for player betting strategy. Should have global variables that track chips and progress and functions for logic.

##Interface with game logic script.

##Simulate games and export to excel spreadsheet

##Game variant scripts. Template variables and functions for gameplay, payouts, bonus bets, house strategies, etc.

##Build front end