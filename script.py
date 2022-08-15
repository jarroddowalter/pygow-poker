import random
from pygments import highlight
from rich import print
from rich.table import Table
from rich.console import Console
console = Console()

import game_configs
from game import DECK, format_hand, read_hand, determine_winner, add_bet, determine_winnings
import game_configs
from house_strat import house_strat
from player_strat import player_strat
from betting_strat import betting_strat

test_hand = ['10c', 'JKR', '12c', '13c', '14c', '12d', '13s']
player_hand = []
dealer_hand = []

## https://www.vegashowto.com/face-up-pai-gow
## https://massgaming.com/wp-content/uploads/RULES-Pai-Gow-Poker-8-20-18.pdf
## https://www.orangecitypoker.com/table-games/face-up-pai-gow
## https://www.liveabout.com/beating-pai-gow-poker-537016
## https://wizardofodds.com/games/pai-gow-poker/house-way/foxwoods/
## https://www.stonesgamblinghall.com/portfolio-item/face-up-pai-gow-poker/
## https://fallsviewcasinoresort.com/content/dam/fallsview/PDF/Playing/FaceUpPaiGow-HouseWays-EN.pdf

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

simulations = input('Enter Number of Simulated Games:')
simulations = int(simulations)

player_win_count = 0
dealer_win_count = 0
push_count = 0
a_high_pai_gow_count = 0
longest_loss_streak = 0
longest_loss_streak_count = 0
longest_win_streak = 0
longest_win_streak_count = 0

dealer_a_high_no_jkr = 0
dealer_a_high_jkr = 0
dp_a_high = 0

high_count = 0
a_high_count = 0
pair_count = 0
two_pair_count = 0
toak_count = 0
straight_count = 0
flush_count = 0
full_house_count = 0
foak_count = 0
sf_count = 0
rf_count = 0
five_a_count = 0
scsf_count = 0
rfrm_count = 0
scsfnj_count = 0

ante_wins = 0
ante_winnings = 0
ace_high_wins = 0
ace_high_winnings = 0
fortune_wins = 0
fortune_winnings = 0
progressive_wins = 0
progressive_winnings = 0
envy_wins = 0
envy_winnings = 0

last_bet = {}
last_rank = ''
last_outcome = ''
player_bank = game_configs.PLAYER_BANK

r = 0
while r < simulations:
	bet = betting_strat(player_bank, last_rank, last_outcome, last_bet)
	if add_bet(bet) > player_bank:
		console.print('[bold red]End Simulation: Not enough funds to play betting strategy[/bold red]')
		console.print('')
		break
	last_bet = bet
	player_bank -= add_bet(bet)

	deal_game()
	read_dealer_hand = read_hand(dealer_hand)
	read_player_hand = read_hand(player_hand)
	last_rank = read_player_hand['rank']

	# print(read_dealer_hand)
	split_dealer_hand = house_strat(dealer_hand)
	# print(read_player_hand)
	split_player_hand = player_strat(player_hand, split_dealer_hand)

	outcome = determine_winner(split_player_hand, split_dealer_hand)
	last_outcome = outcome

	winnings = determine_winnings(bet, outcome, read_player_hand['rank'], read_dealer_hand['rank'], read_dealer_hand['hand'])
	if winnings['ante'] > 0:
		ante_wins += 1
		ante_winnings += winnings['ante']
	if winnings['ace_high'] > 0:
		ace_high_wins += 1
		ace_high_winnings += winnings['ace_high']
	if winnings['fortune'] > 0:
		fortune_wins += 1
		fortune_winnings += winnings['fortune']
	if winnings['progressive'] > 0:
		progressive_wins += 1
		progressive_winnings += winnings['progressive']
	if winnings['envy'] > 0:
		envy_wins += 1
		envy_winnings += winnings['envy']
	player_bank += add_bet(winnings)
	
	table = Table() ## 9 columns

	table.add_column(f'Game {r+1}')
	table.add_column('Hand')
	table.add_column('Hand Rank')
	table.add_column('High')
	table.add_column('High Rank')
	table.add_column('High Points')
	table.add_column('Low')
	table.add_column('Low Rank')
	table.add_column('Low Points')

	table.add_row(
		'Dealer',
		pretty_hand(read_dealer_hand['hand']),
		str(read_dealer_hand['rank']), 
		pretty_hand(split_dealer_hand['high']['hand']), 
		str(split_dealer_hand['high']['rank']), 
		str(split_dealer_hand['high']['rank_points']), 
		pretty_hand(split_dealer_hand['low']['hand']), 
		str(split_dealer_hand['low']['rank']), 
		str(split_dealer_hand['low']['rank_points']))
	table.add_row(
		'Player',
		pretty_hand(read_player_hand['hand']),
		str(read_player_hand['rank']),
		pretty_hand(split_player_hand['high']['hand']), 
		str(split_player_hand['high']['rank']), 
		str(split_player_hand['high']['rank_points']), 
		pretty_hand(split_player_hand['low']['hand']), 
		str(split_player_hand['low']['rank']), 
		str(split_player_hand['low']['rank_points']))
	table.add_row(
		'Bets',
		f'Ante:{bet["ante"]}, A High:{bet["ace_high"]}, Fortune:{bet["fortune"]}, Progressive:{bet["progressive"]}',
		'Total',
		str(add_bet(bet)),
		'',
		'',
		'',
		'',
		'')
	table.add_row(
		'Outcome',
		outcome,
		'Winnings',
		str(add_bet(winnings)),
		'Player Bank',
		str(player_bank),
		'',
		'',
		'')
	
	if outcome == 'Player Wins':
		player_win_count += 1
		longest_win_streak_count += 1
		if longest_win_streak_count > longest_win_streak:
			longest_win_streak = longest_win_streak_count
		longest_loss_streak_count = 0
	elif outcome == 'Dealer Wins':
		dealer_win_count += 1
		longest_loss_streak_count += 1
		if longest_loss_streak_count > longest_loss_streak:
			longest_loss_streak = longest_loss_streak_count
		longest_win_streak_count = 0
	elif outcome == 'Push':
		push_count += 1
	elif outcome == 'Push - A High Pai Gow':
		push_count += 1
		a_high_pai_gow_count += 1

	if read_dealer_hand['rank'] == 'A High' and 'JKR' not in read_dealer_hand['hand']:
		dealer_a_high_no_jkr += 1
	elif read_dealer_hand['rank'] == 'A High' and 'JKR' in read_dealer_hand['hand']:
		dealer_a_high_jkr += 1
	elif read_dealer_hand['rank'] == 'A High' and read_player_hand['rank'] == 'A High':
		dp_a_high += 1

	if read_player_hand['rank_points'] < 100:
		high_count += 1
	elif read_player_hand['rank'] == 'Pair':
		pair_count += 1
	elif read_player_hand['rank'] == 'Two Pair':
		two_pair_count += 1
	elif read_player_hand['rank'] == 'Three-of-a-kind':
		toak_count += 1
	elif read_player_hand['rank'] == 'Straight':
		straight_count += 1
	elif read_player_hand['rank'] == 'Flush':
		flush_count += 1
	elif read_player_hand['rank'] == 'Full House':
		full_house_count += 1
	elif read_player_hand['rank'] == 'Four-of-a-kind':
		foak_count += 1
	elif read_player_hand['rank'] == 'Straight Flush':
		sf_count += 1
	elif read_player_hand['rank'] == 'Royal Flush':
		rf_count += 1
	elif read_player_hand['rank'] == 'Five Aces':
		five_a_count += 1
	elif read_player_hand['rank'] == '7 Card Straight Flush with Joker':
		scsf_count += 1
	elif read_player_hand['rank'] == 'Royal Flush Plus Royal Match':
		rfrm_count += 1
	elif read_player_hand['rank'] == '7 Card Straight Flush, No Joker':
		scsfnj_count += 1

	r += 1
	console.print(table)

console.print(f'Player Wins: {player_win_count/simulations * 100}%')
console.print(f'Dealer Wins: {dealer_win_count/simulations * 100}%')
console.print(f'Push: {push_count/simulations * 100}%')
console.print(f'A High Pai Gow: {a_high_pai_gow_count/simulations * 100}%')
console.print(f'Longest Loss Streak: {longest_loss_streak}')
console.print(f'Longest Win Streak: {longest_win_streak}')
console.print('')
console.print(f'Dealer A High, No Joker: {dealer_a_high_no_jkr/simulations * 100}%')
console.print(f'Dealer A High with Joker: {dealer_a_high_jkr/simulations * 100}%')
console.print(f'Dealer and Player A High: {dp_a_high/simulations * 100}%')
console.print('')
console.print(f'High Card: {high_count/simulations * 100}%')
console.print(f'Pair: {pair_count/simulations * 100}%')
console.print(f'Two Pair: {two_pair_count/simulations * 100}%')
console.print(f'Three-of-a-kind: {toak_count/simulations * 100}%')
console.print(f'Straight: {straight_count/simulations * 100}%')
console.print(f'Flush: {flush_count/simulations * 100}%')
console.print(f'Full House: {full_house_count/simulations * 100}%')
console.print(f'Four-of-a-kind: {foak_count/simulations * 100}%')
console.print(f'Straight Flush: {sf_count/simulations * 100}%')
console.print(f'Royal Flush: {rf_count/simulations * 100}%')
console.print(f'Five Aces: {five_a_count/simulations * 100}%')
console.print(f'7 Card Straight Flush with Joker: {scsf_count/simulations * 100}%')
console.print(f'Royal Flush Plus Royal Match: {rfrm_count/simulations * 100}%')
console.print(f'7 Card Straight Flush, No Joker: {scsfnj_count/simulations * 100}%')
console.print('')
console.print(f'Ante Wins: {ante_wins/simulations * 100}%')
console.print(f'Ante Winnings: {ante_winnings}')
console.print(f'A High Wins: {ace_high_wins/simulations * 100}%')
console.print(f'A High Winnings: {ace_high_winnings}')
console.print(f'Fortune Wins: {fortune_wins/simulations * 100}%')
console.print(f'Fortune Winnings: {fortune_winnings}')
console.print(f'Progressive Wins: {progressive_wins/simulations * 100}%')
console.print(f'Progressive Winnings: {progressive_winnings}')
console.print(f'Envy Wins: {envy_wins/simulations * 100}%')
console.print(f'Envy Winnings: {envy_winnings}')
console.print('')
console.print(f'Total Winnings: {player_bank - game_configs.PLAYER_BANK}')
console.print(f'Starting Bank: {game_configs.PLAYER_BANK}')
console.print(f'Ending Bank: {player_bank}')

##Functions for house strategy and player strategy should take a hand (array of strings) and return split hands (array of two arrays of strings; first being the high hand and second being the low hand). House strategy is set while player strategy can take dealer cards into account if face-up variant.

##Script for player betting strategy. Should have global variables that track chips and progress and functions for logic.

##Interface with game logic script.

##Simulate games and export to excel spreadsheet

##Game variant scripts. Template variables and functions for gameplay, payouts, bonus bets, house strategies, etc.

##Build front end