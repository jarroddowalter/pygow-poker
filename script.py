import random
from pygments import highlight
from rich import print
from rich.console import Console
from rich.table import Table

import game_configs
from game import DECK, format_hand, read_hand, determine_winner
from house_strat import house_strat
from player_strat import player_strat
from betting_strat import betting_strat

test_hand = ['10c', 'JKR', '12c', '13c', '14c', '12d', '13s']
player_hand = []
dealer_hand = []

def deal_game():
	global player_hand, dealer_hand

	##shuffle
	game_deck = DECK.copy()
	random.shuffle(game_deck)

	##deal
	player_hand = tuple(game_deck[:7])
	del game_deck[:7]
	dealer_hand = tuple(game_deck[:7])
	del game_deck[:7]

def pretty_hand(hand):
	hand = format_hand(hand)
	result = ''
	for card in hand:
		if card[-1] == "♠" or card[-1] == "♣":
			result += f'[black on white b] {card} [/] '
		elif card[-1] == "♥" or card[-1] == "♦":
			result += f'[red on white b] {card} [/] '
		elif card == "JKR":
			result += f'[black on white b] {card} [/] '
	return result



console = Console()
table_header = Table()

table_header.add_column('D Hand')
table_header.add_column('D High')
table_header.add_column('D High Rank')
table_header.add_column('D High Points')
table_header.add_column('D Low')
table_header.add_column('D Low Rank')
table_header.add_column('D Low Points')
table_header.add_column('P Hand')
table_header.add_column('P High')
table_header.add_column('P High Rank')
table_header.add_column('P High Points')
table_header.add_column('P Low')
table_header.add_column('P Low Rank')
table_header.add_column('P Low Points')
table_header.add_column('Outcome')

console.print(table_header)

r = 0
while r < 100:
	table_row = Table()
	deal_game()
	read_dealer_hand = read_hand(dealer_hand)
	split_dealer_hand = house_strat(dealer_hand)
	read_player_hand = read_hand(player_hand)
	split_player_hand = player_strat(player_hand, split_dealer_hand)
	table_row.add_row(
		pretty_hand(read_dealer_hand['hand']), 
		pretty_hand(split_dealer_hand['high']), 
		str(split_dealer_hand['high']['rank']), 
		str(split_dealer_hand['high']['rank_points']), 
		pretty_hand(split_dealer_hand['low']), 
		str(split_dealer_hand['low']['rank']), 
		str(split_dealer_hand['low']['rank_points']), 
		pretty_hand(read_player_hand['hand']), 
		pretty_hand(split_player_hand['high']), 
		str(split_player_hand['high']['rank']), 
		str(split_player_hand['high']['rank_points']), 
		pretty_hand(split_player_hand['low']), 
		str(split_player_hand['low']['rank']), 
		str(split_player_hand['low']['rank_points']), 
		determine_winner(split_player_hand, split_dealer_hand))
	console.print(table_row)
	r += 1


##Functions for house strategy and player strategy should take a hand (array of strings) and return split hands (array of two arrays of strings; first being the high hand and second being the low hand). House strategy is set while player strategy can take dealer cards into account if face-up variant.

##Script for player betting strategy. Should have global variables that track chips and progress and functions for logic.

##Interface with game logic script.

##Simulate games and export to excel spreadsheet

##Game variant scripts. Template variables and functions for gameplay, payouts, bonus bets, house strategies, etc.

##Build front end