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
'JKR',
]

SUIT_ORDER = ['d', 'h', 'c', 's']

test_hand = ['JKR', '14d', '13s', '11s', '11h', '10c', '04d']

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
		'straight': [],
		'flush': [],
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

	outcome['multiples'] = dict(reversed(list(outcome['multiples'].items())))

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
			outcome['straight'] = [card]
		elif int(card[:2]) == int(hand_reversed[i-1][:2]) - 1:
			outcome['straight'].append(card)
		elif outcome['has_joker'] and int(card[:2]) == int(hand_reversed[i-1][:2]) - 2:
			if 'JKR' in outcome['straight']:
				outcome['straight'] = outcome['straight'][outcome['straight'].index('JKR'):]
			outcome['straight'].extend(['JKR', card])
		elif int(card[:2]) == int(outcome['straight'][-1][:2]):
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

		print(outcome['straight'])



	if len(outcome['straight']) <  5:
		outcome['straight'] = []
	else:
		outcome['straight'] = list(reversed(outcome['straight']))

	print(outcome)
	return outcome

	# outcome = {
	#	outcome: '',
	#	points: 
	# 	outcome_hand: [],
	# 	remainder: [] 
	# }

	## High									100 + 2-14 card val
	## Pair									200 + 2-14 card val
	## Two Pair								1000 + 20-140 + 2-14 high pair card val and low pair card val
	## Three-of-a-kind						2000 + 2-14 card val
	## Straight								3000 + 1-10 straight rank (10-J-Q-K-A highest)
	## Flush								4000 + 
	## Full House							5000 + 20-140  + 2-14 
	## Four-of-a-kind						6000 + 2-14 car val
	## Straight Flush						7000 + 1-9 straight rank (A-2-3-4-5 highest)
	## Royal Flush							8000
	## Five Aces							9000


	## 7 Card Straight Flush with Joker		10000 + 1-8 straight rank (8-9-10-J-Q-K-A highest)
	## Royal Flush Plus Royal Match			20000 + 1-2 royal match rank (A-K > K-Q of same suite/no joker)
	## 7 Card Straight Flush, No Joker		30000 + 1-8 straight rank (8-9-10-J-Q-K-A highest)

	## Remainder							

def house_strat(hand:list):
	return
	
def strat_split(hand:list, strat): ## takes 7 card hand list and strat function and returns a split dict
	split = {
		'high_hand': [],
		'high_outcome': '',
		'high_points': 0,
		'low_hand': [],
		'low_outcome': '',
		'low_points': 0
	}
	high_hand = []
	low_hand = []

	if len(hand) != 7:
		print('strat_split error: hand not 7 cards')
		return

	outcome = read_hand(hand)

	## move correct cards to split dict

	split = {
		'high_hand': high_hand,
		'high_outcome': read_hand(high_hand)['outcome'],
		'high_points': read_hand(high_hand)['points'],
		'low_hand': low_hand,
		'low_outcome': '',
		'low_points': read_hand(low_hand)['points']
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
read_hand(test_hand)

##Functions for house strategy and player strategy should take a hand (array of strings) and return split hands (array of two arrays of strings; first being the high hand and second being the low hand). House strategy is set while player strategy can take dealer cards into account if face-up variant.

##Script for player betting strategy. Should have global variables that track chips and progress and functions for logic.

##Interface with game logic script.

##Simulate games and export to excel spreadsheet

##Game variant scripts. Template variables and functions for gameplay, payouts, bonus bets, house strategies, etc.

##Build front end