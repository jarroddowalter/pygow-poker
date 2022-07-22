from array import array
import random
from turtle import st
from unittest import suite
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

def read_hand(hand:list): ## returns poker hand as a dict
	outcome = {}
	hand = sort_hand(hand)

	## count num and suits
	joker_state = None
	num_count = {}
	suit_count = {}

	for card in hand:
		if card == "JKR":
			joker_state = 'ace'
		else:
			if num_count.get(card[:2], False): 
				num_count[card[:2]] += 1
			else:
				num_count[card[:2]] = 1
			if suit_count.get(card[-1], False):
				suit_count[card[-1]] += 1
			else:
				suit_count[card[-1]] = 1

	## get multiples
	multiples = {}
	for key, val in num_count.items():
		if val > 1:
			multiples[key] = val

	## get straight
	straight = []

	## joker check
	## 

	## get flush
	flush = None
	for key, val in suit_count.items():
		if val >= 7 or (val == 6 and joker_state):
			flush = f'7{key}'
			if val == 6:
				joker_state = '7flush'
		elif val >= 5 or (val == 4 and joker_state):
			flush = f'5{key}'
			if val == 4:
				joker_state = '5flush'

	## get high card remainder

	print(format_deck(hand), f'joker_state = {joker_state}', f'num_count= {num_count}', f'suit_count= {suit_count}', f'multiples= {multiples}', f'straight= {straight}', f'flush= {flush}')

	return outcome

	## 2 - Ace, High, [remainder order]
	## 2 - Ace, Pair, [remainder order]
	## 2 - Ace, 2 - Ace, Two Pair, [remainder order]
	## 2 - Ace, Three-of-a-kind, [remainder order]
	## [straight order], Straight, [remainder order]
	## suit, Flush, [remainder order]
	## 2 - Ace, 2 - Ace, Full House, [remainder order]
	## 2 - Ace, Four-of-a-kind, [remainder order]
	## [straight order], suit, Straight Flush, [remainder order]
	## Royal Flush, [remainder order]
	## Five Aces, [remainder order]
	## 7 Card Straight Flush with Joker, [remainder order]
	## Royal Flush Plus Royal Match, [remainder order]
	## 7 Card Straight Flush, No Joker, [remainder order]








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
read_hand(player_hand)

##Functions for house strategy and player strategy should take a hand (array of strings) and return split hands (array of two arrays of strings; first being the high hand and second being the low hand). House strategy is set while player strategy can take dealer cards into account if face-up variant.

##Script for player betting strategy. Should have global variables that track chips and progress and functions for logic.

##Interface with game logic script.

##Simulate games and export to excel spreadsheet

##Game variant scripts. Template variables and functions for gameplay, payouts, bonus bets, house strategies, etc.

##Build front end