from datetime import datetime
from sportsipy.ncaab.boxscore import Boxscores

# Pulls all games between and including November 11, 2017 and November 12,
# 2017
games = Boxscores(datetime(2017, 11, 11), datetime(2017, 11, 12))
# Prints a dictionary of all results from November 11, 2017 and November 12,
# 2017
print(games.games)