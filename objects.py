


import pyglet
from pymunk import Vec2d
from typing import List
import numpy as np
from enum import Enum
from enum import auto

#Variables
image_peg = pyglet.resource.image("resources/Peg_1.png")
image_peg_empty = pyglet.resource.image("resources/Indicator_Empty.png")
image_peg_selected = pyglet.resource.image("resources/Peg_Selected.png")

image_indicator_empty = pyglet.resource.image("resources/Indicator_Empty.png")
image_indicator = pyglet.resource.image("resources/Indicator_1.png")

image_frame = pyglet.resource.image("resources/Frame.png")


image_peg_size = Vec2d(24, 24)
image_indicator_size = Vec2d(9, 9)
image_frame_size = Vec2d(669, 167)




class peg_state(Enum):
    empty = auto()
    red = auto()
    green = auto()
    blue = auto()
    magenta = auto()
    cyan = auto()
    yellow = auto()

class indicator_state(Enum):
    empty = auto() # Miss
    hit = auto()
    blow = auto()

ci = 200

peg_colour_dict:dict = {peg_state.red     :(ci, 0, 0),
                        peg_state.green   :(0,ci,0),
                        peg_state.blue    :(0,0,ci),
                        peg_state.magenta :(ci,0,ci),
                        peg_state.cyan    :(0,ci,ci),
                        peg_state.yellow  :(ci,ci,0), }

peg_image_dict:dict = {peg_state.empty   :image_peg_empty,
                       peg_state.red     :image_peg,
                       peg_state.green   :image_peg,
                       peg_state.blue    :image_peg,
                       peg_state.magenta  :image_peg,
                       peg_state.cyan    :image_peg,
                       peg_state.yellow  :image_peg,}

indicator_colour_dict:dict = {indicator_state.hit:[255,0,0],
                              indicator_state.blow:[255,255,255]}

indicator_image_dict:dict = {indicator_state.empty :image_indicator_empty,
                             indicator_state.blow  :image_indicator,
                             indicator_state.hit   :image_indicator}


class Drawable:
    def __init__(self, pos:Vec2d, dim:Vec2d, image:pyglet.resource.image):
        self.pos:Vec2d = pos
        self.dim:Vec2d = dim
        self.sprite:pyglet.sprite.Sprite = pyglet.sprite.Sprite(image, x=pos.x, y=pos.y)
        pass

    def draw(self):
        self.sprite.draw()



peg_offset = 7
class Peg(Drawable):
    def __init__(self, pos:Vec2d):
        super().__init__(pos, image_peg_size, image_peg_empty)
        self.state = peg_state.empty
        self.isSelected = False
        self.selectedSprite:pyglet.sprite.Sprite = pyglet.sprite.Sprite(image_peg_selected, x=pos.x-peg_offset, y=pos.y-peg_offset)

    def draw(self, isAI=False):
        self.sprite.draw()
        if self.isSelected and isAI == False:
            self.selectedSprite.draw()

    def change_state(self, tostate:peg_state):
        if tostate == peg_state.empty:
            self.sprite.image = peg_image_dict[peg_state.empty]
            self.sprite.update(x=self.pos.x, y=self.pos.y)
        else:
            # Change sprite to the indicator
            self.sprite.image = peg_image_dict[peg_state.red]
            # Change sprite colour
            if tostate == peg_state.red:
                self.sprite.color = peg_colour_dict[tostate]
                self.sprite.update(x=self.pos.x-peg_offset, y=self.pos.y-peg_offset)
            elif tostate == peg_state.green:
                self.sprite.color = peg_colour_dict[tostate]
                self.sprite.update(x=self.pos.x-peg_offset, y=self.pos.y-peg_offset)
            elif tostate == peg_state.blue:
                self.sprite.color = peg_colour_dict[tostate]
                self.sprite.update(x=self.pos.x-peg_offset, y=self.pos.y-peg_offset)
            elif tostate == peg_state.magenta:
                self.sprite.color = peg_colour_dict[tostate]
                self.sprite.update(x=self.pos.x-peg_offset, y=self.pos.y-peg_offset)
            elif tostate == peg_state.cyan:
                self.sprite.color = peg_colour_dict[tostate]
                self.sprite.update(x=self.pos.x-peg_offset, y=self.pos.y-peg_offset)
            elif tostate == peg_state.yellow:
                self.sprite.color = peg_colour_dict[tostate]
                self.sprite.update(x=self.pos.x-peg_offset, y=self.pos.y-peg_offset)
            else:
                raise ValueError("ValueError|Peg.change_state; state", tostate, "doesn't exist!")
        self.state = tostate



class Indicator(Drawable):
    def __init__(self, pos:Vec2d):
        super().__init__(pos, image_indicator_size, image_indicator_empty)
        self.state = indicator_state.empty

    def change_state(self, tostate:indicator_state):
        if tostate == indicator_state.empty:
            self.sprite.image = indicator_image_dict[indicator_state.empty]
        else:
            # Change sprite to the indicator
            self.sprite.image = indicator_image_dict[indicator_state.hit]
            # Change sprite colour
            if tostate == indicator_state.blow:
                self.sprite.color = indicator_colour_dict[indicator_state.blow]
            elif tostate == indicator_state.hit:
                self.sprite.color = indicator_colour_dict[indicator_state.hit]
        self.state = tostate



class Frame(Drawable):
    def __init__(self, pos:Vec2d):
        super().__init__(pos, image_frame_size, image_frame)


class Selected(Drawable):
    def __init__(self, pos:Vec2d, dim:Vec2d):
        super().__init__(pos, dim, image_peg_selected)



def peg_index_to_state(i:int)->peg_state:
    if i == 0:
        return peg_state.empty
    elif i == 1:
        return peg_state.red
    elif i == 2:
        return peg_state.green
    elif i == 3:
        return peg_state.blue
    elif i == 4:
        return peg_state.magenta
    elif i == 5:
        return peg_state.cyan
    elif i == 6:
        return peg_state.yellow
    else:
        raise ValueError("ValueError in peg_index_to_state; index was too high", i)

def peg_state_to_index(i:peg_state)->int:
    if i == peg_state.empty:
        return 0
    elif i == peg_state.red:
        return 1
    elif i == peg_state.green:
        return 2
    elif i == peg_state.blue:
        return 3
    elif i == peg_state.magenta:
        return 4
    elif i == peg_state.cyan:
        return 5
    elif i == peg_state.yellow:
        return 6
    else:
        raise ValueError("ValueError in peg_index_to_state; index was too high", i)

def indicator_index_to_state(i:int)->indicator_state:
    if i == 0:
        return indicator_state.empty
    elif i == 1:
        return indicator_state.blow
    elif i == 2:
        return indicator_state.hit




class Board:
    def __init__(self, pos:Vec2d, solution, isAI=False):

        self.frame = Frame(Vec2d(pos.x-40, pos.y-30))
        self.isAI = isAI
        self.solution = solution


        self.pegs_list = np.ndarray([4, 10], dtype=Peg)

        for i in range(10):
            for j in range(4):
                self.pegs_list[j, i] = Peg(Vec2d(pos.x + 50 * i, pos.y + 30 * j))

        self.pegs_list[0, 0].isSelected = True

        self.indicator_list = np.ndarray([4, 10], dtype=Indicator)

        for i in range(10):
            for j in range(0, 4, 2):
                self.indicator_list[j, i] = Indicator(Vec2d(pos.x + 50 * i - 9, pos.y + 30 * 4 + 9 * j))
                if (4 % 2) == 0:
                    self.indicator_list[j + 1, i] = Indicator(Vec2d(pos.x + 50 * i + 9, pos.y + 30 * 4 + 9 * j))

        # If the board belongs to the ANN, don't add the following fluff.
        if not self.isAI:
            self.colours_list = np.ndarray([6], dtype=Peg)

            for key, i in zip(peg_colour_dict.keys(), range(6)):
                self.colours_list[i] = Peg(Vec2d(pos.x + 200 + 30 * i, pos.y - 60))
                self.colours_list[i].change_state(key)

            self.colours_list[0].isSelected = True

            self.solution_pegs = np.array([Peg(Vec2d(pos.x + 50 * 11, pos.y + 30 * j)) for j in range(4)],
                                     dtype=Peg)

            # Put correct colours in for the solution_pegs
            for i in range(4):
                self.solution_pegs[i].change_state(peg_index_to_state(self.solution[i]))
                print(peg_index_to_state(self.solution[i]))



    def draw(self):
        self.frame.draw()

        for i in range(10):
           for j in range(4):
               self.pegs_list[j, i].draw(isAI=self.isAI)


        if not self.isAI:
            for i in range(10):
                for j in range(4):
                    self.indicator_list[j, i].draw()

            for i in range(4):
                self.solution_pegs[i].draw()

            for i in range(6):
                self.colours_list[i].draw()
















#if __name__ == '__main__':
#
#    window = pyglet.window.Window(1200, 800)
#    pyglet.gl.glClearColor(0.7, 0.7, 0.7, 1)
#
#
#    @window.event
#    def on_draw():
#        window.clear()
#
#        frame.draw()
#
#        for i in range(10):
#            for j in range(4):
#                pegs_list[j, i].draw()
#
#        for i in range(10):
#            for j in range(4):
#                indicator_list[j, i].draw()
#
#        for i in range(4):
#            solution_pegs[i].draw()
#        return
#
#    # 150, 200, * 10
#
#    # Frame 1 loc start = 200, 150
#
#    # Creating objects structure
#
#    frame = Frame(Vec2d(200, 150))
#
#    pegs_list = np.ndarray([4,10], dtype=Peg)
#
#    for i in range(10):
#        for j in range(4):
#            pegs_list[j,i] =  Peg( Vec2d( 240+50*i, 180+30*j ) )
#
#    indicator_list = np.ndarray([4, 10], dtype=Indicator)
#
#    for i in range(10):
#        for j in range(0, 4, 2):
#            indicator_list[j,i] =  Indicator( Vec2d( 240+50*i-9, 180+30*4+9*j ) )
#            if (4 % 2) == 0:
#                indicator_list[j+1,i] =  Indicator( Vec2d( 240+50*i+9, 180+30*4+9*j ) )
#
#    solution_pegs = np.array( [ Peg( Vec2d( 240+50*11, 180+30*j ) ) for j in range(4) ] , dtype=Peg)
#
#
#    # randomizing all pegs as a test
#
#    solution_nums = np.random.randint(1, 7, 4)
#
#    for i in range(4):
#        solution_pegs[i].change_state(peg_index_to_state(solution_nums[i]))
#        print(peg_index_to_state(solution_nums[i]))
#
#
#    pyglet.app.run()
#
#    print("Stopping drawbles.py|Main")




