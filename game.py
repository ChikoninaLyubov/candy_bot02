max_total = 150
total = max_total
game = False

def set_total(num: int):
  global max_total
  max_total = num


def get_total():
  global total
  return total

def take_candies(take: int):
  global total
  total -= take

def check_game():
  global game
  return game

def new_game():
  global game
  global total
  if game:
    game = False
  else:
    game = True
    total = max_total