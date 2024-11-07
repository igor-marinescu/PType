# This file is part of the PType distribution.
# Copyright (c) 2020 Igor Marinescu (igor.marinescu@gmail.com).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
""" PType Main Module. """

import pygame

from . import resman
from . import ship
from . import res_def_ship
from . import backtiles
from . import res_def_backtiles
from . import platesman
from . import constrman

def check_for_quit():
    """ Check if an exit-event occured """
    for event in pygame.event.get(pygame.QUIT):     # get all the QUIT events
        return True                                 # terminate if any QUIT events are present
    for event in pygame.event.get(pygame.KEYUP):    # get all the KEYUP events
        if event.key == pygame.K_ESCAPE:
            return True
        pygame.event.post(event)                    # put the other KEYUP event objects back
    return False

# ###############################################################################
# Main
# ###############################################################################
class PType:
    """ Main Class """

    def __init__(self, width, height, path):
        """ Init module """
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption('RubikQuat')
        self.background = (25,32,49)
        self.quit_flag = False

        # create Backtiles
        self.resman_back = resman.ResourceManager(path)
        self.resman_back.load_tiles('/resources/stars.png', res_def_backtiles.resDef)
        self.b_tiles = backtiles.BackTiles(self.resman_back)

        # create Ship
        self.resman_ship = resman.ResourceManager(path)
        self.resman_ship.load_tiles("/resources/images.png", res_def_ship.resDefShip, colorkey=-1)
        self.ship = ship.Ship(self.resman_ship, (200, 450))
        # create list of shots
        self.shot_list = []

        # create Constructs
        self.constrman = constrman.ConstrManager(path, self.shot_list)
        self.constrman.load_constr('/resources/construct.png')

        # create Plates
        self.platesman = platesman.PlatesManager(path, self.constrman)
        self.platesman.load_plates('/resources/plates64x64.png')
        #self.platesMan.printPlates()
        #self.platesman.generate()
        self.platesman.generate_empty()

    def display(self):
        """ Draw scene on the surface. """
        # display background
        self.surface.fill(self.background)
        self.b_tiles.display(self.surface)
        self.platesman.draw(self.surface)
        self.ship.draw(self.surface)
        self.shot_list_display()

    def run(self):
        """ Create a pygame surface until it is closed. """
        self.display()
        pygame.display.flip()

        # Initialize clock
        clock = pygame.time.Clock()

        while not self.quit_flag:

            # Computes how many miliseconds have passed since previous call
            # The argument framerate makes the function to delay to keep the game running slower.
            # ex: clock.tick(60) -> doesn't run faster than 60 frames/sec (16ms)
            clock.tick(60)
            #clock.tick(15)
            self.quit_flag = check_for_quit()
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.ship.shoot(self.shot_list)
                    elif event.key == pygame.K_0:
                        self.ship.set_weapon(0)
                    elif event.key == pygame.K_1:
                        self.ship.set_weapon(1)
                    elif event.key == pygame.K_2:
                        self.ship.set_weapon(2)
                    elif event.key == pygame.K_3:
                        self.ship.set_weapon(3)
                    elif event.key == pygame.K_4:
                        print(len(self.shot_list))
                    #if(not self.actList.execKeyDown(event.key, pygame.key.get_mods())):
                    #    pass

            control = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                control |= 1
            if keys[pygame.K_RIGHT]:
                control |= 2
            if keys[pygame.K_UP]:
                control |= 4
            if keys[pygame.K_DOWN]:
                control |= 8

            self.ship.move(control)

            self.b_tiles.tick()
            self.platesman.tick()
            self.ship.anim_tick()
            self.shot_list_tick()
            self.constrman.check_shots()
            self.display()
            pygame.display.flip()

    def shot_list_display(self):
        """ Display schots """
        for schot in self.shot_list:
            pygame.draw.circle(self.surface, (255, 130, 0),
                (schot.x_pos, schot.y_pos), schot.damage)

    def shot_list_tick(self):
        """ Ticks schots, to be called every cycle """
        for schot in self.shot_list:
            if (schot.y_pos > 0) and (schot.y_pos < self.height) and \
                (schot.x_pos > 0) and (schot.y_pos < self.width):
                schot.x_pos += schot.speed_x
                schot.y_pos += schot.speed_y
            else:
                self.shot_list.remove(schot)
