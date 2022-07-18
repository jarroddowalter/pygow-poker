from array import array
import random
from rich import print
from rich.console import Console

console = Console()

DECK = [
'2♥', '2♦', '2♠', '2♣',
'3♥', '3♦', '3♠', '3♣',
'4♥', '4♦', '4♠', '4♣',
'5♥', '5♦', '5♠', '5♣',
'6♥', '6♦', '6♠', '6♣',
'7♥', '7♦', '7♠', '7♣',
'8♥', '8♦', '8♠', '8♣',
'9♥', '9♦', '9♠', '9♣',
'10♥', '10♦', '10♠', '10♣',
'J♥', 'J♦', 'J♠', 'J♣',
'Q♥', 'Q♦', 'Q♠', 'Q♣',
'K♥', 'K♦', 'K♠', 'K♣',
'A♥', 'A♦', 'A♠', 'A♣',
'JKR',
]

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

def sort_hand(hand: array):
	num_order = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', 'JKR')
	suit_order = ("♦", "♥", "♣", "♠")

	def get_card_num_order(card):
		for i, item in enumerate(num_order):
			if card == "JKR":
				return 13
			elif card[0] == item[0]:
				return i
	
	def get_card_suit_order(card):
		for i, item in enumerate(suit_order):
			if card == "JKR":
				return 4
			elif card[-1] == item:
				return i
	
	temp_hand = hand
	sorted_hand = []
	has_joker = False
	suit_count = {
		'♠': 0,
		'♣': 0,
		'♥': 0,
		'♦': 0
	}
	num_count = {
		'2': 0,
		'3': 0,
		'4': 0,
		'5': 0,
		'6': 0,
		'7': 0,
		'8': 0,
		'9': 0,
		'10': 0,
		'J': 0,
		'Q': 0,
		'K': 0,
		'A': 0
	}

	##sort by order > suit > straight > flush
	
	##sort order
	for i, card in enumerate(temp_hand):
		##on first iteration just add first card to sorted_hand
		if i == 0:
			sorted_hand.append(card)
			continue

		##get order position of current card
		current_card_order = get_card_num_order(card)

		##loop through sorted hand until current_card_order < sorted_card_order then add card to sorted hand
		for j, item in enumerate(sorted_hand):
			if current_card_order < get_card_num_order(item):
				sorted_hand.insert(j, card)
				break
			elif current_card_order >= get_card_num_order(item) and j+1 == len(sorted_hand):
				sorted_hand.append(card)
				break
	
	##count num and suits
	for i, card in enumerate(temp_hand):
		if card == "JKR":
			has_joker = True
		else:
			suit_count[card[-1]] += 1
			if card[0] != '1':
				num_count[card[0]] += 1
			elif card[0] == '1':
				num_count['10'] += 1

	##sort suit
	temp_hand = sorted_hand
	# sorted_hand = []



	## for i, card in enumerate(temp_hand):
	## 	num_count[card[0]]
	
	console.print('🃏' + str(has_joker), suit_count, num_count)
	return sorted_hand
	
	
deal_game()
print_game_hands()
dealer_hand = sort_hand(dealer_hand)
player_hand = sort_hand(player_hand)
print_game_hands()

##Functions for house strategy and player strategy should take a hand (array of strings) and return split hands (array of two arrays of strings; first being the high hand and second being the low hand). House strategy is set while player strategy can take dealer cards into account if face-up variant.

##Script for player betting strategy. Should have global variables that track chips and progress and functions for logic.

##Interface with game logic script.

##Simulate games and export to excel spreadsheet

##Game variant scripts. Template variables and functions for gameplay, payouts, bonus bets, house strategies, etc.

##Build front end