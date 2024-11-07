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
""" Resource Manager Module. """

import os.path
import pygame

def load_image(name, colorkey=None, colorkeypos=None):
    """ Load image """
    fullname = os.path.join('', name)
    try:
        img_surface = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message) from message

    img_surface = img_surface.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = img_surface.get_at((0, 0))
        img_surface.set_colorkey(colorkey, pygame.RLEACCEL)
    elif colorkeypos is not None:
        colorkey = img_surface.get_at(colorkeypos)
        img_surface.set_colorkey(colorkey, pygame.RLEACCEL)

    return img_surface, img_surface.get_rect()

class ResourceManager:
    """ Resource Manager """

    def __init__(self, path):
        """ Init resource manager """
        self.img_list = []
        self.path = path

    def load_tiles(self, filename, res_def, colorkey = None, colorkeypos = None):
        """ Load all tiles in a list """
        img_text, _ = load_image(self.path + filename, colorkey, colorkeypos)

        # extract images from texture image based on resource definition (resDef)
        for r_def in res_def:
            src = r_def[0]
            size = r_def[1]
            surf = pygame.Surface(size)
            surf.blit(img_text, (0, 0), (src[0], src[1], size[0], size[1]))
            surf.set_colorkey((0, 0, 0))
            self.img_list.append(surf)

    def draw(self, surface, index, x_pos, y_pos, area = None, special_flags = 0):
        """ Draw image """
        surface.blit(self.img_list[index], (x_pos, y_pos), area, special_flags)
