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

#ANNaNaS imports
from pymunk import Vec2d
import ANNaNaS.population

#
import objects

# Temp


window = pyglet.window.Window(1200, 800)
pyglet.gl.glClearColor(0.7, 0.7, 0.7, 1)







#client_population:ANNaNaS.population.Population = ANNaNaS.population.Population(1, input_size=1, hidden_size=tuple([0]), output_size=1, isHallow=True)
#
#inputsize:int = None
#hiddensize:tuple = None
#outputsize:int = None
#
#max_attempts = 10 # amount of attempts a mastermind can make before being considered dead
#max_dif_pegs = 6 # numbers simulate the diffirent colours of pegs
#max_pegs = 4 # how many pegs have to be guessed
#
#amount_attempts = 0 # amount of attempts done

attempt_list = [] # Memory of previous attempts [attempt_o]

attempt = 0 # doubles as selected_index_attempt

selected_index_peg = 0
selected_index_colour = 0

@window.event
def on_key_release(symbol, modifiers):
    global selected_index_peg
    global selected_index_colour
    global attempt

    selected_index_attempt = attempt

    pegs_list[selected_index_peg, selected_index_attempt].isSelected = False
    colours_list[selected_index_colour].isSelected = False

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

    pegs_list[selected_index_peg, selected_index_attempt].isSelected=True
    colours_list[selected_index_colour].isSelected=True

    if symbol == pygkey.SPACE:
        print("Space")
        pegs_list[selected_index_peg, selected_index_attempt].change_state(objects.peg_index_to_state(selected_index_colour+1) )





@window.event
def on_draw():
    window.clear()

    frame.draw()

    for i in range(10):
        for j in range(4):
            pegs_list[j, i].draw()

    for i in range(10):
        for j in range(4):
            indicator_list[j, i].draw()

    for i in range(4):
        solution_pegs[i].draw()

    for i in range(6):
        colours_list[i].draw()
    return







if __name__ == '__main__':
    frame_x = 240
    frame_y = 180
    # 150, 200, * 10
    # Frame 1 loc start = 200, 150
    # Creating objects structure

    frame = objects.Frame(Vec2d(200, 150))

    colours_list = np.ndarray([6], dtype=objects.Peg)

    for key, i in zip( objects.peg_colour_dict.keys(), range(6)):
        colours_list[i] = objects.Peg(Vec2d(frame_x + 200 + 30 * i, frame_y - 60))
        colours_list[i].change_state(key)

    colours_list[0].isSelected = True

    pegs_list = np.ndarray([4,10], dtype=objects.Peg)

    for i in range(10):
        for j in range(4):
            pegs_list[j,i] =  objects.Peg(Vec2d(frame_x + 50 * i, frame_y + 30 * j))

    pegs_list[0,0].isSelected = True

    indicator_list = np.ndarray([4, 10], dtype=objects.Indicator)

    for i in range(10):
        for j in range(0, 4, 2):
            indicator_list[j,i] =  objects.Indicator(Vec2d(frame_x + 50 * i - 9, frame_y + 30 * 4 + 9 * j))
            if (4 % 2) == 0:
                indicator_list[j+1,i] =  objects.Indicator(Vec2d(frame_x + 50 * i + 9, frame_y + 30 * 4 + 9 * j))

    solution_pegs = np.array([objects.Peg(Vec2d(frame_x + 50 * 11, frame_y + 30 * j)) for j in range(4)], dtype=objects.Peg)


    # randomizing all pegs as a test

    solution_nums = np.random.randint(1, 7, 4)

    for i in range(4):
        solution_pegs[i].change_state(objects.peg_index_to_state(solution_nums[i]))
        print(objects.peg_index_to_state(solution_nums[i]))


    #for i in range(10):
    #    for j in range(4):
    #        pegs_list[j,i].change_state(objects.peg_index_to_state(np.random.randint(1,7)))


    pyglet.app.run()

    print("Stopping main.py|Main")




