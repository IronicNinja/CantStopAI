# Can't Stop AI

<img src="https://i.pinimg.com/originals/38/b1/be/38b1be0207b3e5ae30132d4820c082a5.jpg"> </img>

Can't Stop is a board game designed by Sid Sackson originally published by Parker Brothers in 1980. The game equipment consists of four dice, a board, a set of eleven markers for each player, and three neutral-colored markers. The board consists of eleven columns of spaces, one column for each of the numbers 2 through 12. The columns (respectively) have 3, 5, 7, 9, 11, 13, 11, 9, 7, 5 and 3 spaces each.[1] The number of spaces in each column roughly corresponds to the likelihood of rolling them on two dice. Rest of the information: https://en.wikipedia.org/wiki/Can't_Stop_(board_game). I currently play on https://boardgamearena.com/.

# Code Files

```bot.py``` is my current implementation of Can't Stop in pygame. It is a **Work in Progress**.

```game.py``` is the current Monte Carlo simulator. To play with this simulator, fork this Github repository and type ```python game.py``` in your terminal. Then, use ```game_stats.py``` to update the information. You mainly have to update your opponent's information since ```game.txt``` has updated information for the player. In the future, I may make this bot automatic by using OpenCV/computer vision so the bot can make moves on its own.

# Algorithms

The current algorithm deployed in ```game.py``` is **Monte Carlo Tree Search**. Essentially, the bot pretends to make a move and then will randomly simulate games to its end. Then it aggregates how many times one of the two players wins, and after simulating all (3) moves, it will play the move that gives it the highest winning probability. If you run this code, you will notice that this simulator is currently very, very risky and has some errors when it completes a column of chips (it wants to continue instead of ending which doesn't make much sense).

The algorithm that I may try in the future is more statistical and grounded, using expected values to optimize the probability of the bot winning. This shouldn't be too hard; the board can be translated into an array of probabilities (probability that from that position, you will be able to reach the end in one move) and then combining that with the fact you can make multiple moves, depending on your current chips list.
