from aiogram import types
from loader import dp
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
import game
import random
import text
total = 150
new_game = False

@dp.message_handler(commands=['start','старт'])
async def mes_start(massage: types.Message):
    print('Вам пришло сообщение')

@dp.message_handler(commands=['help'])
async def mes_help(massage: types.Message):
    await massage.answer('Бог поможет')
    
# @dp.message_handler(commands=['new_game'])
# async def mes_new(massage: types.Message):
    # global new_game
    # new_game = True
    # await massage.answer('Игра началась')  


# @dp.message_handler(commands=['set'])
# async def mes_set(massage:types.Message):
    # global total
    # global new_game
    # count = massage.text.split()[1]
    # if  not new_game:
        # if count.isdigit():
            # total = int(count)
            # await massage.answer(f'Конфет теперь будет {count}')
        # else:
            # await massage.answer(f'{massage.from_user.first_name} напишите цифрами')
    # else:
        # await massage.answer(f'{massage.from_user.first_name} нельзя менять праила во время игры')



# @dp.message_handler()
# async def mes_all(massage: types.Message):
    # global total
    # global new_game
    # if new_game:
       
        # if massage.text.isdigit():
            # total -= int(massage.text)
            # await massage.answer(f'{massage.from_user.first_name} взял(а) {massage.text} конфет.'
                                #  f'на столе осталось {total}')
           
        # if total <=0:
        #    await massage.answer(f'Урааа!{massage.from_user.first_name} ты победил(а)')
        #    new_game = False
    # else:
        # await massage.answer(f'{massage.from_user.first_name} взял(а) {massage.text} конфет.'
                                #  f'на столе осталось {total}')
        # @dp.message_handler(commands=['start'])
        # async def on_start(message: Message):
            # await message.answer(text=f'{message.from_user.first_name},{text.greeting}')


# @dp.message_handler(commands=['menu'])
# async def show_menu(message: Message):
    # name = message.from_user.full_name
    # await message.answer(f'{name}{text.menu}')

# @dp.message_handler(commands=['set'])
# async def set_total(message: Message):
#   if not game.check_game():
    # count = message.text.split()
    # if len(count) >1 and count[1].isdigit():
    #   game.set_total(int(count[1]))
    #   await message.answer(f'Конфет теперь будет {count}')
    # else:
    #   await message.answer(f'{message.from_user.first_name} вводите цифры, не печатайте ерунду')
#   else:
    # await message.answer(f'{message.from_user.first_name} правила не соблюдаете, за дураков нас держите')

# против бота
@dp.message_handler(commands='new_game')
async def start_new_game(message: Message):
  game.new_game()
  if game.check_game():
    toss = random.choice([False, True])
    if toss: 
      await player_turn(message)
    else:
      await bot_turn(message)


async def player_turn(message: Message):
  await message.answer(f'{message.from_user.first_name} {text.step}')

@dp.message_handler()
async def take(message: Message):
  name = message.from_user.first_name
  if game.check_game():
    if message.text.isdigit():
      take = int(message.text)
      total = game.get_total()
      if (0 < take < 29) and take <= total :
        game.take_candies(take)
        if await check_win(message, take,'player'):
          return
        await message.answer(f'Достойный соперник {name} берет {take} {text.take_people} '
                             f'{int(game.get_total())} {text.robot}')
        await bot_turn(message)
      else:
        if total <= 28:
          await message.answer(text.error_total(total))
        else:
          await message.answer(text.error)
    else:
      pass


async def bot_turn(message):
  total = game.get_total()
  if 28 >= total:
    take = total
  else:
    if total % 29 == 0:
      take = random.randint(1, 28)
    else:
      take = total % 29
   # take = random.randint(1, 28)
  game.take_candies(take)
  if await check_win(message, take,'Бот'):
    return
  await message.answer(text.take_bot(take, int(game.get_total())))
  await player_turn(message)

async def check_win(message, take: int, player: str):
  if game.get_total() == 0:
    if player == 'player':
      await message.answer(f'{message.from_user.first_name} {text.win_people}')
    else:
      await message.answer(text.win_bot)
    game.new_game()
    return True
  else:
    return False

           
        


     