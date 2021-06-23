import os
import threading
import time
from battleship_client import BattleshipClient

from game_handling import BattleBoard

grpc_host = os.getenv('GRPC_HOST', 'localhost')
grpc_port = os.getenv('GRPC_PORT', '50051')

playing = threading.Event()
playing.set()

battleship = BattleshipClient(grpc_host=grpc_host, grpc_port=grpc_port)


@battleship.on()
def begin():
    print('Game started!')


@battleship.on()
def start_turn():
    global target_coordinates
    target, target_coordinates = enemy_board.send_attack()
    # print('Start turn')
    # s = input('Your move> ')

    battleship.attack(target)


@battleship.on()
def end_turn():
    print('End turn')


@battleship.on()
def hit():
    enemy_board.record_attack(target_coordinates, True)
    # print('You hit the target!')


@battleship.on()
def miss():
    enemy_board.record_attack(target_coordinates, False)
    # print('Aww.. You missed!')


@battleship.on()
def win():
    print('Yay! You won!')
    playing.clear()


@battleship.on()
def lose():
    print('Aww... You lost...')
    playing.clear()


@battleship.on()
def attack(vector):
    # print(f'Shot received at {vector}')
    attack_result = home_board.receive_attack(vector)

    defeated = home_board.check_defeat()

    if defeated:
        battleship.defeat()
    if attack_result:
        battleship.hit()
    else:
        battleship.miss()


target_coordinates = ()

home_board = BattleBoard()
enemy_board = BattleBoard()

home_board.set_board()

print('Waiting for the game to start...')

battleship.join()
while playing.is_set():
    time.sleep(1.0)