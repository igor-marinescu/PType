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
""" Ship Resource Definition Module.

Resource definitions
This definition is used by res_man.py (loadTiles) when extracting tiles
from ./resources/images.png
"""

#       Top-left location| Tile size  |Tile | Description
#          in images.png |width,height|index|
resDefShip = [
           #(( x0,  y0), |  (w,  h)   |     |
            ((  0,   0),    (32, 32)),  # 0 fire1
            (( 32,   0),    (32, 32)),  # 1 fire2
            (( 64,   0),    (32, 32)),  # 2 fire3
            ((  0,  32),    (32, 32)),  # 3 fire4
            (( 32,  32),    (32, 32)),  # 4 fire5
            (( 64,  32),    (32, 32)),  # 5 fire6
            ((  0,  64),    (32, 32)),  # 6 fire7
            (( 32,  64),    (32, 32)),  # 7 fire8
            (( 64,  64),    (32, 32)),  # 8 fire9

            ((  0,  96),    (32, 32)),  # 9
            (( 32, 120),    (32, 32)),  # 10
            (( 64, 120),    (32, 32)),  # 11

            ((  0, 152),    (32, 32)),  # 12
            (( 32, 152),    (32, 32)),  # 13

            (( 96,   0),    (64, 64)),  # 14 ship1
            ((160,   0),    (64, 64)),  # 15 ship2
            ((224,   0),    (64, 64)),  # 16 ship3
            ((288,   0),    (64, 64)),  # 17 ship4
            ((352,   0),    (64, 64)),  # 18 ship5

            (( 96,  64),    (64, 64)),  # 19 ship1
            ((160,  64),    (64, 64)),  # 20 ship2
            ((224,  64),    (64, 64)),  # 21 ship3
            ((288,  64),    (64, 64)),  # 22 ship4
            ((352,  64),    (64, 64)),  # 23 ship5

            (( 96, 128),    (64, 64)),  # 24 weapon1
            ((160, 128),    (64, 64)),  # 25 weapon2
            ((224, 128),    (64, 64)),  # 26 weapon3
            ((288, 128),    (64, 64)),  # 27 weapon4
            ((352, 128),    (64, 64)),  # 28 weapon5

            (( 96, 192),    (64, 64)),  # 29 weapon1
            ((160, 192),    (64, 64)),  # 30 weapon2
            ((224, 192),    (64, 64)),  # 31 weapon3
            ((288, 192),    (64, 64)),  # 32 weapon4
            ((352, 192),    (64, 64)),  # 33 weapon5
        ]
#----------------------------------------------------------------------------------------------
