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
""" Test Backtiles Module. """

import pygame

from .. import resman
from .. import res_def_backtiles
from .. import backtiles
from .. import ptype

# ###############################################################################
# Main
# ###############################################################################
class TestBacktiles:
    """ Test Backtiles Module """

    def __init__(self, width, height, path):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Test')
        self.quit_flag = False

        # create resource manager and load tiles
        self.resman = resman.ResourceManager(path)
        self.resman.load_tiles('/resources/stars.png', res_def_backtiles.resDef)

        self.b_tiles = backtiles.BackTiles(self.resman)

    def display(self):
        """ Display Method """
        self.b_tiles.display(self.surface)

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
            self.quit_flag = ptype.check_for_quit()
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        self.b_tiles.offset_y = 0
                        self.b_tiles.generate_back()
                        self.b_tiles.copy_back_to_disp()
                        self.b_tiles.generate_back()
                    elif event.key == pygame.K_1:
                        self.b_tiles.scroll()
                    elif event.key == pygame.K_2:
                        self.b_tiles.offset_y += 8
                        if self.b_tiles.offset_y >= 64:
                            self.b_tiles.scroll()
                            self.b_tiles.offset_y = 0
                    elif event.key == pygame.K_3:
                        pass

            self.b_tiles.tick()

            self.display()
            pygame.display.flip()
