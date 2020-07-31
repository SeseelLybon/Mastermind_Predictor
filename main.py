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

#ANNaNaS imports
from ANNaNaS.population import Population

#
import objects

# Temp
from meeple import Meeple

window = pyglet.window.Window(1200,800)
pyglet.gl.glClearColor(0.7,0.7,0.7,1)


client_population:Population = Population(1, input_size=1, hidden_size=tuple([0]), output_size=1, isHallow=True)

inputsize:int = None
hiddensize:tuple = None
outputsize:int = None

showGraph = False
skip_once = False
score = 0
best_score = 0
bestfitness = 0
lastspawnscore = 0



max_attempts = 10 # amount of attempts a mastermind can make before being considered dead
max_dif_pegs = 6 # numbers simulate the diffirent colours of pegs
max_pegs = 4 # how many pegs have to be guessed

amount_attempts = 0 # amount of attempts done


attempt_list = [] # Memory of previous attempts [attempt_o]






client_isDone = False





score_label = pyglet.text.Label('score: ' + str(score),
                  font_name='Times New Roman',
                  font_size=12,
                  x=50, y=450,
                  anchor_x='left', anchor_y='center')
score_best_label = pyglet.text.Label('best score: ',
                  font_name='Times New Roman',
                  font_size=12,
                  x=50, y=425,
                  anchor_x='left', anchor_y='center')
dinos_live_label = pyglet.text.Label("Dino's alive: ",
                   font_name='Times New Roman',
                   font_size=12,
                   x=50, y=400,
                   anchor_x='left', anchor_y='center')

@window.event
def on_draw():
    global client_population
    global window
    global score
    global lastspawnscore
    global showGraph

    window.clear()

    return

#    if client_population.bestMeeple is not None and showGraph:
#        client_population.bestMeeple.brain.updateposGFX([600, 750], [550, 500])
#        client_population.bestMeeple.brain.updateintensityGFX([2, 2,  # dinner pos
#                                                               0.5, 2, 3, 3,  # first object
#                                                               1.5])       # score
#        client_population.bestMeeple.brain.draw()
#
#    # Run the game here
#    # Move the objects/obstacles on the platform, not the dino or the platform
#    # Use the update() and isDone() function
#
#    score_label.text = 'score: ' + str(score)
#    score_label.draw()
#    score_best_label.text = 'best score: ' + str(client_population.highestScore)
#    score_best_label.draw()
#    dinos_live_label.text = "Dino's alive: " + str(client_population.countAlive()) + " of " + str(client_population.size)
#    dinos_live_label.draw()
#
#    obt.ground.draw()
#
#    client_population.drawAlife()
#
#    for obst in obstacle_drawlist:
#        obst.draw()
#    #pops.bestMeeple.draw()



#def update(dt):
#    global client_population
#    global client_isDone
#    global score
#    global bestfitness
#    global lastspawnscore
#
#    global_inputs  = []
#
#    # -----------------
#    # getting data to set the inputs of the brain
#
#
#    global_inputs += [obst_distance,
#                      obst_height,
#                      obst_x,
#                      obst_y]
#
#
#    global_inputs.append(score)
#    # -----------------
#
#    client_population.updateAlive(obstacle_drawlist, score, global_inputs)
#
#
#    if client_population.isDone():
#        print("--------------------------------------------")
#        print("All dino's are dead. Returning dino brains.")
#        print("Best score this batch:", score)
#        pyglet.clock.unschedule(update)
#        pyglet.clock.unschedule(scoreupdate)
#        client_isDone = True




def dojob(job):
    global client_population
    global client_isDone
    #global score
    #global bestfitness
    #global lastspawnscore
    #global best_score

    client_isDone = False

    print("Starting the job batch")

    # For Mastermind, a job is testing a meep against x diffirent randomized solutions.
    # Score is a function of the amount of correctly solved solutions aiming for 100%


    # unpack job (a pickle of a list of meeple brains)
    client_population = Population(len(job), input_size=inputsize, hidden_size=hiddensize, output_size=outputsize, isHallow=True)

    client_population.unpickle_population_from_list(job)

    for meep in client_population.pop:
        meep.brain.score = 0
        meep.brain.fitness = 0



    # Run test
    for runi in range(100):
        print("starting run", runi)
        # generate new solution to test all meeps against
        mastermind_solution = np.random.randint(1, max_dif_pegs, max_pegs)

        # reset meeps every run except score
        for meep in client_population.pop:
            meep: Meeple = meep
            meep.results_list = []  # whipe it's memory of attempts
            meep.epochs = max_attempts # reset the amount of times it can try
            meep.isAlive = True
            meep.isDone = False

        # run all meeps against this until pop.isDone.
        while not client_population.isDone():
            client_population.updateAlive(mastermind_solution, max_dif_pegs)

    print("--------------------------------------------")
    print("All dino's are either done or dead.")
    best_score = max([meep.brain.score for meep in client_population.pop])
    print("Best score this batch:", best_score)
    client_isDone = True















if __name__ == '__main__':
    print("hello world")