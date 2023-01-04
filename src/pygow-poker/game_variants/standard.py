import common

###############
## Game Configs
###############

NAME = 'Standard Pai Gow Poker'
TABLE_MIN = 15
TABLE_MAX = 5000
COMMISSION = 0.05 ## percentage
HOUSE_SPLIT_STRATEGY = ''
PLAYER_SPLIT_STRATEGY = ''
BETTING_STRATEGY = ''

###############
## Game Functions
###############

def determine_bet():
	##import strategy
	return

def determine_winner(player_split:dict, dealer_split:dict): ## returns result
	if player_split['high']['rank_points'] > dealer_split['high']['rank_points'] and player_split['low']['rank_points'] > dealer_split['low']['rank_points']:
		return 'Player Wins'
	elif player_split['high']['rank_points'] > dealer_split['high']['rank_points'] or player_split['low']['rank_points'] > dealer_split['low']['rank_points']:
		return 'Push'
	else:
		return 'Dealer Wins'

def determine_winnings(bet:dict, result:str):
	winnings = {
		'ante': 0,
	}

	## ante
	if result == 'Player Wins':
		winnings['ante'] = bet['ante'] * 2 - (bet['ante'] * 2 * COMMISSION)
	elif result == 'Dealer Wins':
		winnings['ante'] = 0
	else: ## push
		winnings['ante'] = bet['ante']

	return winnings

###############
## Game Logic
###############

game = {
	'player_start_bank': 1000,
	'bet': bet,
	'player_hand': player_seven_card_hand,
	'player_split': player_split,
	'dealer_hand': dealer_seven_card_hand,
	'dealer_split': dealer_split,
	'result': 'Player Wins',
	'winnings': winnings,
	'player_end_bank': 1100
}

##Player Bets
##Deal Cards
##Player Splits Cards
##Dealer Splits Cards
##Determine Result and Winnings