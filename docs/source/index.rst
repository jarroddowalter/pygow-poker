.. pygow-poker documentation master file, created by
   sphinx-quickstart on Thu Aug 25 21:02:48 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pygow-poker
===========

Simulate or play Pai Gow Poker!

Game Rules
----------

Pai Gow Poker is an engaging table game inspired by the Chinese domino game Pai Gow. It is played with a 53 card deck (standard 52 cards + one joker) with the players trying to beat the dealer. After bets are made, 7 cards are dealt to each participant where they need to be split into a 5 card "high" poker hand and a 2 card "low" poker hand. `Standard poker rankings <https://www.poker.org/poker-hands-ranking-chart/>`_ apply when setting the cards where the single joker acts as a wild when completing a straight or a flush otherwise it acts as an ace. **The high hand must beat the low hand** when setting the cards. Once all hands are set and revealed, three possible outcomes can occur:

1. Both player hands beat both dealer hands results in a win (doubles bet)
2. Both dealer hands beat both player hands results in a loss (lose bet)
3. The player beats one dealer hand and loses the other results in a push (tie, no bet loss)

`Visit here <https://wizardofodds.com/games/pai-gow-poker/>`_ for a more in-depth explanation of the rules, strategies, and variants of Pai Gow Poker.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
	
   installation.md
   development.md
   data-types.md
   license
