# This file is part of the Ptype distribution.
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
""" Ship Module """
import math
from . import anim

#-------------------------------------------------------------------------------
class Shot:
    """ Definition of a shot """

    def __init__(self, x_pos, y_pos, speed_x, speed_y, damage):
        """ Init Shot """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.damage = damage

#-------------------------------------------------------------------------------
class Weap:
    """ Definition of a weapon """

    def __init__(self, anim_weap, off_x):
        """ Init weapon """
        self.anim = anim_weap
        self.off_x = off_x

    def tick(self):
        """ Tick method,  must be called every cycle """
        self.anim.tick()

    def draw(self, surface, x_pos, y_pos):
        """ Draw weapon """
        self.anim.draw(surface, x_pos + self.off_x[self.anim.frame_idx], y_pos)

    def get_off_x(self):
        """ return offset of weapon on axis X,
            it depends how ship is tilt, left or right """
        return self.off_x[self.anim.frame_idx]

    def shoot(self, shot_list, x_pos, y_pos):
        """ Weapon schot (virtual) """

#-------------------------------------------------------------------------------
# pylint: disable=line-too-long
WEAP_DEF_LIST = [
#|<---   Animation Frame List    ---->|<------------  Offset X  ------------>|<--- Shots Definitions (list od shots) ---
#| Index in ResMan of every animation | X offset relative to Ship for every  | Every element is a shot definition:
#| frame. Linked to Ship Animation    | tilt-animation frame.                | ((xOff, yOff), (speedX, speedY), damage)
#| (must be the same length)          | (see anatomy.png)                    |
( [28, 27, 26, 25, 24, 30, 31, 32, 33], [ 15, 21, 24, 27, 30, 27, 24, 21, 15], [((32, 32),(0,-5), 3), ((32, 58),(0,5), 3)]),     # WeapR1
( [28, 27, 26, 25, 24, 30, 31, 32, 33], [-15,-21,-24,-27,-30,-27,-24,-21,-15], [((32, 32),(0,-5), 3), ((32, 32),(-3,-3), 3), ((32, 32),(-2,-4), 3)])      # WeapL1
]
# pylint: enable=line-too-long
#-------------------------------------------------------------------------------
class Weap1(Weap):
    """ Definition of a weapon """

    def __init__(self, resman, anim_ship, weap_def):
        """ Init Weapon1 """
        self.weap_def = weap_def
        self.shot_def = weap_def[2]
        anim_weap = anim.AnimTiltLink(resman, weap_def[0], anim_ship)
        Weap.__init__(self, anim_weap, weap_def[1])

    def shoot(self, shot_list, x_pos, y_pos):
        """ Weapon1 shoot """
        for shoot in self.shot_def:
            off_xy = shoot[0]
            speed_xy = shoot[1]
            shot_list.append(Shot(x_pos + self.get_off_x() + off_xy[0], y_pos + off_xy[1],
                speed_xy[0], speed_xy[1], shoot[2]))

#-------------------------------------------------------------------------------
class Ship:
    """ Definition of a Ship """

    def __init__(self, res_man, pos):
        """ Ship Init """
        self.resman = res_man
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.move_acc = 1    # move acceleratinq
        self.old_ctrl = 0    # old control (detect direction change)

        self.anim_fire = anim.AnimCyc(res_man, [0, 1, 2, 3, 4, 5, 6, 7, 8], 3)
        self.anim_ship = anim.AnimTilt(res_man, [18, 17, 16, 15, 14, 20, 21, 22, 23], 2)

        self.weapon_l = Weap1(res_man, self.anim_ship, WEAP_DEF_LIST[1])
        self.weapon_r = Weap1(res_man, self.anim_ship, WEAP_DEF_LIST[0])
        self.weapon = 0

        self.sphere_a = 0
        self.sphere_x = 0
        self.sphere_y = 0

    def anim_tick(self):
        """ Animation tick """
        self.anim_fire.tick()
        self.anim_ship.tick()
        self.weapon_r.tick()
        self.weapon_l.tick()

        self.sphere_a += 0.05
        self.sphere_x = 16 + int(64.0 * math.cos(self.sphere_a))
        self.sphere_y = 32 + int(64.0 * math.sin(self.sphere_a))

    def move(self, control):
        """ Ship move """
        if self.old_ctrl != control:
            self.move_acc = 1
        elif (control != 0) and (self.move_acc < 5):
            self.move_acc += 1
        self.old_ctrl = control

        if control & 1:
            self.anim_ship.tilt_dir = -1
            if self.x_pos > 0:
                self.x_pos -= self.move_acc
        elif control & 2:
            self.anim_ship.tilt_dir = 1
            if self.x_pos < 500:
                self.x_pos += self.move_acc
        else:
            self.anim_ship.tilt_dir = 0

        if control & 4:
            if self.y_pos > 0:
                self.y_pos -= self.move_acc
        elif control & 8:
            if self.y_pos < 1000:
                self.y_pos += self.move_acc

    def draw(self, surface):
        """ Draw Ship, Weapons and Fire """
        # The order of displaying the ship and weapons is important
        # Tilt to Right?
        if self.anim_ship.frame_idx <= self.anim_ship.ini_idx:
            if self.weapon & 1:
                self.weapon_l.draw(surface, self.x_pos, self.y_pos)
            self.anim_ship.draw(surface, self.x_pos, self.y_pos)
            if self.weapon & 2:
                self.weapon_r.draw(surface, self.x_pos, self.y_pos)
        # Tilt to Left?
        else:
            if self.weapon & 2:
                self.weapon_r.draw(surface, self.x_pos, self.y_pos)
            self.anim_ship.draw(surface, self.x_pos, self.y_pos)
            if self.weapon & 1:
                self.weapon_l.draw(surface, self.x_pos, self.y_pos)
        # Fire
        self.anim_fire.draw(surface, self.x_pos + 16, self.y_pos + 64)
        self.resman.draw(surface, 9, self.x_pos + self.sphere_x, self.y_pos + self.sphere_y)

    def set_weapon(self, weapon):
        """ Set weapon """
        self.weapon = weapon

    def shoot(self, shot_list):
        """ Add shoot to shot-list """
        # add main (ship) shot
        shot_list.append(Shot(self.x_pos + 32, self.y_pos, 0, -4, damage = 4))
        # add weapon 1 shot
        if self.weapon & 1:
            self.weapon_l.shoot(shot_list, self.x_pos, self.y_pos)
        # add weapon 2 shot
        if self.weapon & 2:
            self.weapon_r.shoot(shot_list, self.x_pos, self.y_pos)
        # add sphere schoot
        shot_list.append(Shot(self.x_pos + self.sphere_x + 16,
            self.y_pos + self.sphere_y + 16, 0, -5, damage = 2))
