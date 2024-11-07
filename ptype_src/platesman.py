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
""" Plates Manager Module. """
#-------------------------------------------------------------------------------
# Plates:
# Plate is a 64x64 pixels image. The "ground" is randomly composed by Plates.
# Beside image, a Plate contains also a definition, which allows the algorithm
# to decide how to connect the Plates beetwen them.
#
# Plate definition is a (U,R,B,L) tuple, where every element is the definition
# of the corresponding edge:
#       U=Upper edge, R=Right edge, B=Bottom edge, L=Left edge:
#
#   U=0 +---+---+   U=1 +---+---+   U=2 +---+---+   U=3 +---+---+
#       | 0 | 0 |       | 1 | 0 |       | 0 | 1 |       | 1 | 1 |
#       +---+---+       +---+---+       +---+---+       +---+---+
#       | * | * |       | * | * |       | * | * |       | * | * |
#       +---+---+       +---+---+       +---+---+       +---+---+
#
#   R=0 +---+---+   R=1 +---+---+   R=2 +---+---+   R=3 +---+---+
#       | * | 0 |       | * | 1 |       | * | 0 |       | * | 1 |
#       +---+---+       +---+---+       +---+---+       +---+---+
#       | * | 0 |       | * | 0 |       | * | 1 |       | * | 1 |
#       +---+---+       +---+---+       +---+---+       +---+---+
#
#   B=0 +---+---+   B=1 +---+---+   B=2 +---+---+   B=3 +---+---+
#       | * | * |       | * | * |       | * | * |       | * | * |
#       +---+---+       +---+---+       +---+---+       +---+---+
#       | 0 | 0 |       | 1 | 0 |       | 0 | 1 |       | 1 | 1 |
#       +---+---+       +---+---+       +---+---+       +---+---+
#
#   L=0 +---+---+   L=1 +---+---+   L=2 +---+---+   L=3 +---+---+
#       | 0 | * |       | 1 | * |       | 0 | * |       | 1 | 0 |
#       +---+---+       +---+---+       +---+---+       +---+---+
#       | 0 | * |       | 0 | * |       | 1 | * |       | 1 | 0 |
#       +---+---+       +---+---+       +---+---+       +---+---+
# Example:
#   A Plate with definition (2,3,3,2) is a Plate which looks like:
#   +---+---+
#   | 0 | 1 |
#   +---+---+
#   | 1 | 1 |
#   +---+---+
#
# Two Plates can be connected if they have the same opposite edges:
#   connected vertical:     Plate1.U == Plate2.B
#   connected hotizontal:   Plate1.R == Plate2.L
#
# Example, the following two Plates can be connected horizontal:
#                  (U,R,B,L)         (U,R,B,L)
#           Plate1=(2,3,3,2), Plate2=(1,2,3,3)
#
#                  +---+---+         +---+---+
#                  | 0 | 1 |  <----- | 1 | 0 |
#                  +---+---+         +---+---+
#                  | 1 | 1 |  <----- | 1 | 1 |
#                  +---+---+         +---+---+
#
# The definitions for all Plates are stored in a list, where every element
# is a Plate defined by a (U,R,B,L) tuple:
#
#   platesDef = [ (U0,R0,B0,L0), (U1,R1,B1,L1), (U2,R2,B2,L2), ... ]
#                 |<- plate0 ->|<-- plate1 -->|<-- plate2 -->| ...
#
#-------------------------------------------------------------------------------
# Match Matrix Left-Bottom:
# Every element in this 2D list is a list of PlatesIndex that have L and B
# definition corresponding to element's position in Match Matrix.
#  ------+---+---+---+---+
#  ^   0 |   |   |   |   |
#  |   --+---+---+---+---+  Example, if:
#  |   1 |   |   |   | <--- matchMatrixLB[1][3] = [34, 57, 123]
#  L   --+---+---+---+---+  then: all Plates with indexes 34, 57 and 123 (in platesDef)
#  |   2 |   |   |   |   |  have L=1 and B=3:
#  |   --+---+---+---+---+                      (U,R,B,L)
#  v   3 |   |   |   |   |       platesDef[ 34]=(*,*,3,1)
#  ------+---+---+---+---+       platesDef[ 57]=(*,*,3,1)
#        | 0 | 1 | 2 | 3 |       platesDef[123]=(*,*,3,1)
#        |<------B------>|
#
# The Match-Matrix is used when a Plate with coresponding L and B definitions
# must be randomly choosen. Instead of iterating randomly in Plates definition's
# list until we (randomly) find a Plate with a specific L and B.
# Using Match-Matrix we already have the list of all Plates that have L and B.
# And we just choose randomly an element from this list.
#-------------------------------------------------------------------------------

import os.path
import random
import pygame

TY_OUT = 11
TX_OUT = 8

class PlatesManager:
    """ Plates Manager """

    def __init__(self, path, constr_man):
        """ Init Plates Manager """
        self.path = path

        self.plates_def = []     # Plates Definitions
        self.plates_img = []     # Plates Images
        self.disp_idx = [[0    for x in range(TX_OUT)] for y in range(TY_OUT)]
        self.disp_img = [[None for x in range(TX_OUT)] for y in range(TY_OUT)]
        self.match_matrix_lb = [[[] for x in range(4)] for y in range(4)]

        self.scroll_cnt = 0
        self.offset_y = 0
        self.constr_man = constr_man

    def load_plates(self, filename):
        """ Load all plates from image file, decode them and append to existing list """

        # open image
        fullname = os.path.join('', self.path + filename)
        try:
            img_surface = pygame.image.load(fullname)
        except pygame.error as message:
            print('Cannot load image:', fullname)
            raise SystemExit(message) from message

        img_surface = img_surface.convert()
        #img_rect = imgSurface.get_rect()

        # get reference colorkey (point 0, 0)
        ref_colorkey = img_surface.get_at((0, 0))
        img_surface.set_colorkey(ref_colorkey, pygame.RLEACCEL)

        # How many full 64x64 Plates are in the image
        ty_cnt = 10 #int(imgRect[3]/64)
        tx_cnt = 6 #int(imgRect[2]/64)

        # Extract every 64x64 Plate from image
        for j in range(ty_cnt):
            for i in range(tx_cnt):

                # Plate image
                surf = pygame.Surface((64, 64))
                surf.blit(img_surface, (0, 0), ((i * 64), (j * 64), 64, 64))
                back_colorkey = (0, 0, 0)
                surf.set_colorkey(back_colorkey)
                self.plates_img.append(surf)

                # Plate [U, R, B, L, Sum] definitions
                plate = [0, 0, 0, 0, 0]
                p_sum = 0
                # Check the corners (top-left, top-right, bottom-right, bottom-left)
                # and automatically detect the plate's definitions
                # (if the corner has or not a background color)
                if surf.get_at((1, 1)) != back_colorkey:
                    plate[0] += 1  # Up += 1
                    plate[3] += 1  # Left += 1
                    p_sum += 1
                if surf.get_at((62, 1)) != back_colorkey:
                    plate[0] += 2  # Up += 2
                    plate[1] += 1  # Right += 1
                    p_sum += 1
                if surf.get_at((1, 62)) != back_colorkey:
                    plate[2] += 1  # Bottom += 1
                    plate[3] += 2  # Left += 2
                    p_sum += 1
                if surf.get_at((62, 62)) != back_colorkey:
                    plate[1] += 2  # Right += 2
                    plate[2] += 2  # Bottom += 2
                    p_sum += 1
                plate[4] = p_sum
                self.plates_def.append(tuple(plate))
                p_idx = len(self.plates_def) - 1

                # Insert Plate Index in Match Matrix L-B ([Left=3][Bottom=2])
                self.match_matrix_lb[plate[3]][plate[2]].append(p_idx)

                # Artificially increase the number of "full" plates
                # by insering more similare plates in the matchMatrix
                # which increases the probability of the "full" plates
                if p_sum == 4:#4
                    p_sum = 8
                    while p_sum > 0:
                        self.match_matrix_lb[plate[3]][plate[2]].append(p_idx)
                        p_sum -= 1

    def generate_line(self, y_pos):
        """ Generate one line of Plates """

        lval = None
        for i in range(0, TX_OUT):
            bval = 0

            # If not the last line, get the plate from next line
            if y_pos < (TY_OUT - 1):
                plate = self.plates_def[self.disp_idx[y_pos + 1][i]]
                # Get Up-Side of the bottom-plate
                bval = plate[0] # 0=Up

            if i > 0:
                # Get left plate
                plate = self.plates_def[self.disp_idx[y_pos][i - 1]]
                # Get Right side of the left-plate
                lval = plate[1] #1=Right
            else:
                # In case this is the first column
                # get a random value for R that matches bottom-plate
                while lval is None:
                    mat = self.match_matrix_lb[random.randint(0, 3)][bval]
                    if len(mat) > 0:
                        p_idx = mat[random.randint(0, len(mat) - 1)]
                        plate = self.plates_def[p_idx]
                        lval = plate[3] #3=Left

            mat = self.match_matrix_lb[lval][bval]
            if len(mat) > 0:
                p_idx = mat[random.randint(0, len(mat) - 1)]
                self.disp_idx[y_pos][i] = p_idx
                self.disp_img[y_pos][i] = self.plates_img[p_idx]
                # If it is a full plate (pSum == 4) place a construct on it
                plate = self.plates_def[p_idx]
                if (plate[4] == 4) and (random.randint(0, 2) == 0):
                    self.constr_man.add(y_pos, i)
            else:
                print("!!!!!")

    def generate(self):
        """ Generate a new Ground from Plates """
        for j in range(TY_OUT - 1, -1, -1):
            self.generate_line(j)

    def generate_empty(self):
        """ Generate a new empty Ground """
        for j in range(TY_OUT - 1, -1, -1):
            for i in range(0, TX_OUT):
                mat = self.match_matrix_lb[0][0]
                p_idx = mat[0]
                self.disp_idx[j][i] = p_idx
                self.disp_img[j][i] = self.plates_img[p_idx]

    def scroll(self):
        """ Scroll all Plates with one line down
            (the last line is lost, the first line is newly generated) """
        # Scroll all plates with one position down
        for j in range(TY_OUT - 1, 0, -1):
            for i in range(TX_OUT):
                self.disp_idx[j][i] = self.disp_idx[j - 1][i]
                self.disp_img[j][i] = self.disp_img[j - 1][i]
        # Scroll constructs
        self.constr_man.scroll()
        # Generate new top line
        self.generate_line(0)

    def print_plates(self):
        """ Print plates info """
        for plate in self.plates_def:
            print(plate)
        #for jl in self.matchMatrixLB:
        #    for il in jl:
        #        print(il)

    def draw(self, surface):
        """ Draw plates """
        for j in range(TY_OUT):
            for i in range(TX_OUT):
                img = self.disp_img[j][i]
                if img is not None:
                    surface.blit(img, ((i * 64), self.offset_y + (j * 64) - 64))
        self.constr_man.draw(surface)

    def tick(self):
        """ Tick method, to be caled every cycle """
        self.offset_y += 1
        if self.offset_y >= 64:
            self.offset_y = 0
            self.scroll()
        else:
            self.constr_man.tick(self.offset_y)
