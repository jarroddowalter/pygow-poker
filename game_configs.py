TABLE_MIN = 15
TABLE_MAX = 5000

## Payouts
## ints are multipliers and strings are currency amounts
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

FORTUNE_ENVY_BONUS_PAYOUT = { ## in $; typically $5 or more qualifies on fortune bonus
	'Four-of-a-kind': '5.00',
	'Straight Flush': '20.00',
	'Royal Flush': '50.00',
	'Five Aces': '250.00',
	'7 Card Straight Flush with Joker': '500.00',
	'Royal Flush Plus Royal Match': '1000.00',
	'7 Card Straight Flush, No Joker': '3000.00'
}

PROGRESSIVE_BONUS_PAYOUT = { ## typically just a $1 bet
	'Full House': 4,
	'Four-of-a-kind': 75,
	'Straight Flush': 100,
	'Royal Flush': 500,
	'Five Aces': '25000.00',
	'7 Card Straight Flush with Joker': '150000.00',
	'Royal Flush Plus Royal Match': 0,
	'7 Card Straight Flush, No Joker': '150000.00'
}