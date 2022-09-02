###############
## Game Configs
###############

NAME = 'Face Up Pai Gow Poker'

TABLE_MIN = 15

TABLE_MAX = 5000

COMMISSION = 0 ## percentage

## Payouts - ints are multipliers and strings are currency amounts
ACE_HIGH_PAYOUT = {
	'Dealer A High No Joker': 5,
	'Dealer A High with Joker': 15,
	'Dealer and Player A High': 40
}

FORTUNE_BONUS_PAYOUT = {
	'Straight': 2,
	'Three-of-a-kind': 3,
	'Flush': 4,
	'Full House': 5,
	'Four-of-a-kind': 25,
	'Straight Flush': 50,
	'Royal Flush': 150,
	'Five Aces': 400,
	'7 Card Straight Flush with Joker': 1000,
	'Royal Flush Plus Royal Match': 2000,
	'7 Card Straight Flush, No Joker': 5000
}

PROGRESSIVE_BONUS_PAYOUT = { ## typically just a $1 bet
	'Full House': 4,
	'Four-of-a-kind': 75,
	'Straight Flush': 100,
	'Royal Flush': 500,
	'Five Aces': '25000.00',
	'7 Card Straight Flush with Joker': '150000.00',
	'Royal Flush Plus Royal Match': '750000.00',
	'7 Card Straight Flush, No Joker': '1500000.00'
}

###############
## Game Logic
###############