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

""" Constructions (Buildings) Module. """
import random

from . import anim
from . import resman
from . import res_def_constrman

TY_OUT = 11
TX_OUT = 8

# Animation definitions
# frameList = list of frames (indexes in res_def_constrman.py)
# ticks = number of ticks per frame
ANIM_DEF = [ #  (   frameList, ticks)
                (range( 0,  6), 3),      # 0 | shot-hit animation
                (range( 6, 14), 3),      # 1 | explosion1 animation
                (range(14, 22), 3),      # 2 | explosion2 animation
                (range(22, 30), 3),      # 3 | explosion3 animation
            ]

# Constructs definitions
# img0 = Image index (in res_def_constrman.py) for a whole building
# img1 = Image index (in res_def_constrman.py) for a destroyed building
# exp  = Animation index (in res_def_constrman.py) for a destroyed building
# life = Building's life
CONSTR_DEF = [# (img0, img1, exp, life)
                (  30,   31,   3,  100),
                (  32,   33,   3,  100),
                (  34,   35,   1,  100),
                (  36,   37,   2,   10),
                (  38,   39,   2,   50),
        ]

class Constr:
    """ Construct

    c_def = Construct definition (img0, img1, expIdx)
    """
    def __init__(self, master, row, col, c_def):
        self.master = master
        self.row = row
        self.col = col
        self.img0 = c_def[0]
        self.img1 = c_def[1]
        self.exp_idx = c_def[2]
        self.y_pos = row * 64
        self.x_pos = col * 64
        self.life = c_def[3]
        self.exp_anim = None     # explosion animation
        self.hit_anim = None     # hit animation
        self.hit_x = 0

    def draw(self, surface):
        """ draw construct (whole or destroyed) """
        if self.life > 0:
            surface.blit(self.img0, (self.x_pos, self.y_pos - 64))
        else:
            surface.blit(self.img1, (self.x_pos, self.y_pos - 64))
        # draw explosion animation if required
        if self.exp_anim is not None:
            self.exp_anim.draw(surface, self.x_pos, self.y_pos - 64)
        # draw hit animation if required
        if self.hit_anim is not None:
            self.hit_anim.draw(surface, self.hit_x - 16, self.y_pos - 32)

    def tick(self, offset_y):
        """ Construct tick, to be called every cycle """
        self.y_pos = (self.row * 64) + offset_y
        # construct explosion animation tick
        if self.exp_anim is not None:
            self.exp_anim.tick()
            # If animation ended, destroy it
            if self.exp_anim.finish:
                self.exp_anim = None
        # construct hit animation tick
        if self.hit_anim is not None:
            self.hit_anim.tick()
            # If animation ended, destroy it
            if self.hit_anim.finish:
                self.hit_anim = None

    def check_hit(self, shot):
        """ Check if the construct is hit """
        if self.life > 0:
            if (shot.y_pos >= (self.y_pos - 64)) and (shot.y_pos <= self.y_pos):
                if (shot.x_pos >= self.x_pos) and (shot.x_pos <= (self.x_pos + 64)):
                    # reduce the life of construct
                    self.life -= 25
                    # create hit animation
                    self.hit_anim = self.master.get_hit_anim()
                    self.hit_x = shot.x_pos
                    # if destroyed, create explosion animatoin
                    if self.life <= 0:
                        self.exp_anim = self.master.get_exp_anim(self.exp_idx)
                    return True
        return False

class ConstrManager:
    """ Constructs Manager """

    def __init__(self, path, shot_list):
        """ Init Constructs Manager """
        self.path = path
        self.constr_def = []     # Constructs definitions
        self.constr_dsp = []     # Constructs currently displayed
        self.shot_list = shot_list
        self.resman = resman.ResourceManager(path)

    def load_constr(self, filename):
        """ Load all construct resources from image file """
        self.resman.load_tiles(filename, res_def_constrman.resDef, colorkey=-1)
        for c_def in CONSTR_DEF:
            # Construct definition object (img0, img1, expIdx, life)
            c_def_obj = (self.resman.img_list[c_def[0]], self.resman.img_list[c_def[1]], \
                c_def[2], c_def[3])
            self.constr_def.append(c_def_obj)

    def get_exp_anim(self, exp_idx):
        """ Create and get explosion animation for the construct """
        anim_def = ANIM_DEF[exp_idx]
        return anim.AnimOnce(self.resman, anim_def[0], anim_def[1])

    def get_hit_anim(self):
        """ Create and get hit animation for the construct """
        return anim.AnimOnce(self.resman, ANIM_DEF[0][0], ANIM_DEF[0][1])

    def draw(self, surface):
        """ Draw all constructs """
        for constr in self.constr_dsp:
            constr.draw(surface)

    def tick(self, offset_y):
        """ Tick method, to be called every cycle """
        for constr in self.constr_dsp:
            constr.tick(offset_y)

    def add(self, y_pos, x_pos):
        """ add new construct for position y, x """
        rand_constr = random.randint(0, len(CONSTR_DEF) - 1)
        constr = Constr(self, y_pos, x_pos, self.constr_def[rand_constr])
        self.constr_dsp.append(constr)
        print("add ", y_pos, x_pos, len(self.constr_dsp))

    def scroll(self):
        """ scroll all constructs with one position down """
        for constr in self.constr_dsp:
            constr.row += 1
            constr.y = constr.row * 64
        for idx, constr in enumerate(self.constr_dsp):
            if constr.row >= TY_OUT:
                del self.constr_dsp[idx]
                print("delete ", len(self.constr_dsp))

    def check_shots(self):
        """ Check shots for all constructs """
        for constr in self.constr_dsp:
            for idx, shot in enumerate(self.shot_list):
                if constr.check_hit(shot):
                    # If construct hit, delete shot
                    del self.shot_list[idx]
                    break

        # delete all dead constructs
        #for idx, c in enumerate(self.constrDsp):
        #    if(c.life <= 0):
        #        del self.constrDsp[idx]
        #        print("delete hit")
