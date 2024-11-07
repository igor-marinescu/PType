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
""" Test Plates Module. """

import pygame

from .. import ptype
from .. import platesman
from .. import constrman

# ###############################################################################
# Main
# ###############################################################################
class TestPlates:
    """ Test Plates Module """

    def __init__(self, width, height, path):
        """ Init Test Plates Module """
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Test')
        self.back_color = (10,10,50)
        self.quit_flag = False
        self.shot_list = []

        self.constrman = constrman.ConstrManager(path, self.shot_list)
        self.constrman.load_constr('/resources/plates64x64.png')

        self.platesman = platesman.PlatesManager(path, self.constrman)
        self.platesman.load_plates('/resources/plates64x64.png')
        #self.platesMan.printPlates()
        self.platesman.generate()

    def display(self):
        """ Display Method """
        self.surface.fill(self.back_color)
        self.platesman.draw(self.surface)

    def run(self):
        """ Create a pygame surface until it is closed. """

        self.display()
        pygame.display.flip()

        # Initialize clock
        clock = pygame.time.Clock()

        while not self.quit_flag:
            clock.tick(60)
            self.quit_flag = ptype.check_for_quit()
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        self.platesman.generate()
                    elif event.key == pygame.K_1:
                        self.platesman.scroll()
                    elif event.key == pygame.K_2:
                        pass
                    elif event.key == pygame.K_3:
                        pass

            self.platesman.tick()

            self.display()
            pygame.display.flip()
