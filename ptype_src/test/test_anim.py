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
""" Test Animation Module. """

import pygame
from .. import resman
from .. import res_def_constrman
from .. import anim
from .. import ptype

# ###############################################################################
# Main
# ###############################################################################
class TestAnim:
    """ Test Animation Module """

    def __init__(self, width, height, path):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption('AnimTest')
        self.background = (10,10,50)
        self.quit_flag = False

        # create resource manager and load tiles
        self.resman = resman.ResourceManager(path)
        self.resman.load_tiles("/resources/construct.png", res_def_constrman.resDef, colorkey = -1)

        # create animation
        self.anim1 = anim.AnimCyc(self.resman, [0,1,2,3,4,5,6,7,8], 5)
        self.anim2 = anim.AnimCyc(self.resman, [9, 10, 11, 12, 13, 14], 5)
        self.anim3 = anim.AnimCyc(self.resman, range(15, 23), 5)
        self.anim4 = anim.AnimCyc(self.resman, range(23, 31), 5)
        self.anim5 = anim.AnimCyc(self.resman, range(31, 39), 5)

    def display(self):
        """ Draw scene on the surface. """
        self.surface.fill(self.background)
        self.resman.draw(self.surface, 0, 100, 100)
        self.anim1.draw(self.surface, 150, 150)
        self.anim2.draw(self.surface, 200, 150)

        self.resman.draw(self.surface, 39, 100, 200)
        self.resman.draw(self.surface, 39, 200, 200)
        self.resman.draw(self.surface, 39, 300, 200)

        self.anim3.draw(self.surface, 100, 200)
        self.anim4.draw(self.surface, 200, 200)
        self.anim5.draw(self.surface, 300, 200)

    def run(self):
        """ Create a pygame surface until it is closed. """

        self.display()
        pygame.display.flip()

        # Initialize clock
        clock = pygame.time.Clock()

        while not self.quit_flag:
            clock.tick(60)
            #clock.tick(15)
            self.quit_flag = ptype.check_for_quit()
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pass
                    elif event.key == pygame.K_0:
                        pass
                    elif event.key == pygame.K_1:
                        pass
                    elif event.key == pygame.K_2:
                        pass
                    elif event.key == pygame.K_3:
                        pass

            self.anim1.tick()
            self.anim2.tick()
            self.anim3.tick()
            self.anim4.tick()
            self.anim5.tick()
            self.display()
            pygame.display.flip()
