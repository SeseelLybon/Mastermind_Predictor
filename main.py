#Library imports
import numba
import numpy as np
import pyglet
import math
import sys
import Pyro4
import serpent

#Random imports
from typing import List
import pyglet.window.key as pygkey
from pymunk import Vec2d

#ANNaNaS imports
import ANNaNaS.population
import ANNaNaS.meeple

#
import objects

# Temp


window = pyglet.window.Window(1200, 800)
pyglet.gl.glClearColor(0.7, 0.7, 0.7, 1)








max_attempts = 10 # amount of attempts a mastermind can make before being considered dead
max_dif_pegs = 6 # numbers simulate the diffirent colours of pegs
max_pegs = 4 # how many pegs have to be guessed

inputsize:int = max_pegs * max_attempts * 2  # Double to count for the 'hit and blow'
hiddensize:tuple = tuple([max_pegs * max_attempts * 2, max_pegs * max_attempts, max_pegs * max_dif_pegs])
# hiddensize=tuple([60, 40, 20])
outputsize:int = max_pegs * max_dif_pegs


print("Getting meeps from pickle; crashes if there is no picklejar")
client_population:ANNaNaS.population.Population = ANNaNaS.population.Population(300, input_size=inputsize, hidden_size=hiddensize, output_size=outputsize)
client_population.unpickle_population_from_file()
print("done unpickling and setting up population")

meep: ANNaNaS.meeple.Meeple = client_population.pop[60]


attempt = 0 # doubles as selected_index_attempt
selected_index_peg = 0
selected_index_colour = 0

@window.event
def on_key_release(symbol, modifiers):
    global selected_index_peg
    global selected_index_colour
    global attempt

    selected_index_attempt = attempt

    playerBoard.pegs_list[selected_index_peg, selected_index_attempt].isSelected = False
    playerBoard.colours_list[selected_index_colour].isSelected = False

    if symbol == pygkey.UP:
        selected_index_peg+=1
        print("Up")
    elif symbol == pygkey.DOWN:
        selected_index_peg-=1
        print("Down")
    if symbol == pygkey.LEFT:
        selected_index_colour-=1
        print("Left")
    elif symbol == pygkey.RIGHT:
        selected_index_colour+=1
        print("Right")

    selected_index_peg = min(max(selected_index_peg, 0), 3)
    selected_index_colour = min(max(selected_index_colour, 0), 5)

    playerBoard.pegs_list[selected_index_peg, selected_index_attempt].isSelected=True
    playerBoard.colours_list[selected_index_colour].isSelected=True

    if symbol == pygkey.SPACE:
        print("Space")
        playerBoard.pegs_list[selected_index_peg, selected_index_attempt].change_state(objects.peg_index_to_state(selected_index_colour+1) )

    if symbol == pygkey.ENTER:
        print("Enter")

        # Test if all pegs have been filled.
        if 0 not in [objects.peg_state_to_index(playerBoard.pegs_list[peg, selected_index_attempt].state) for peg in range(4)]:
            # Check how incorrect the player is
            playerBoard.pegs_list[selected_index_peg, selected_index_attempt].isSelected = False

            result = check_attempt([objects.peg_state_to_index(playerBoard.pegs_list[peg, selected_index_attempt].state) for peg in range(4)],
                                   mastermind_solution)
            print(result)

            # Show how incorrect the player is
            for i in range(4):
                playerBoard.indicator_list[i, selected_index_attempt].change_state(objects.indicator_index_to_state(result[i]))

            # Set the input for the ANN and fire the network

            attempt_player = [objects.peg_state_to_index(playerBoard.pegs_list[peg, selected_index_attempt].state)-1 for peg in range(4)]
            ANN_input:np.array = np.array(ANNaNaS.population.sanitize_input(meep.results_list), dtype=int)
            meep.brain.set_inputs(ANN_input)
            meep.brain.fire_network()
            ANN_output = meep.brain.get_outputs()
            ANN_output = ANNaNaS.population.sanitize_output(ANN_output, 4, 6)

            print(ANN_output, attempt_player, result )
            # Show the ANN's suggestion
            for i in range(4):
                ANNBoard.pegs_list[i,attempt].change_state(objects.peg_index_to_state((ANN_output[i])))

            meep.results_list.append((attempt_player, result))
            print(meep.results_list)

            attempt += 1
            playerBoard.pegs_list[selected_index_peg, attempt].isSelected = True
            # Crashes on the 10th attempt, however, if the ANN hasn't gotten to an answer, it didn't do well in the first place.





@window.event
def on_draw():
    window.clear()

    playerBoard.draw()
    ANNBoard.draw()


def check_attempt(attempt:List[int], mastermind_solution)->List[int]:

    result:List[int] = []
    #Some code that tests the current attempt for hits (number, location) and blows (number)
    # 0 - miss
    # 1 - blow (correct number, not correct location)
    # 2 - hit (correct number, correct location)

    for i in range(len(attempt)):
        if attempt[i] == mastermind_solution[i]:
            # if the right peg is in the right place
            result.append(2)
        elif attempt[i] in mastermind_solution:
            # if the right peg is in the wrong place
            result.append(1)
        else:
            # if the wrong peg
            result.append(0)
    result.sort(reverse=True)

    # Obscufate as the player can't know which exact one is blow or hit.
    return result


def generate_mastermind_solution(t='unique'):
    global max_dif_pegs
    global max_pegs

    if t == 'unique':
        temp_rng = list(range(1, max_dif_pegs + 1))
        np.random.shuffle(temp_rng)
        mastermind_solution = temp_rng[:max_pegs]
    else:
        mastermind_solution = np.random.randint(1, max_dif_pegs+1, max_pegs)
    return mastermind_solution


if __name__ == '__main__':
    frame_pos_player = Vec2d(240, 180)
    frame_pos_ANN = Vec2d(240, 380)
    # 150, 200, * 10
    # Frame 1 loc start = 200, 150
    # Creating objects structure

    mastermind_solution = generate_mastermind_solution()

    playerBoard:objects.Board = objects.Board(frame_pos_player, mastermind_solution)
    ANNBoard:objects.Board = objects.Board(frame_pos_ANN, mastermind_solution, isAI=True)


    pyglet.app.run()

    print("Stopping main.py|Main")




