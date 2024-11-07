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
""" Constructs Manager Resource Definition Module.

Resource definitions
This definition is used by res_man.py (loadTiles) when extracting tiles
from ./resources/images.png
"""

#       Top-left location| Tile size  |Tile | Description
#          in images.png |width,height|index|
resDef = [ #(( x0,  y0), |  (w,  h)   |     |

            ((  0,  96),    (32, 32)),  # 0  shot1
            (( 32,  96),    (32, 32)),  # 1  shot2
            (( 64,  96),    (32, 32)),  # 2  shot3
            ((  0, 128),    (32, 32)),  # 3  shot4
            (( 32, 128),    (32, 32)),  # 4  shot5
            (( 64, 128),    (32, 32)),  # 5  shot6

            (( 96,   0),    (64, 64)),  # 6  exp1-1
            ((160,   0),    (64, 64)),  # 7  exp1-2
            ((224,   0),    (64, 64)),  # 8  exp1-3
            ((288,   0),    (64, 64)),  # 9  exp1-4
            (( 96,  64),    (64, 64)),  # 10 exp1-5
            ((160,  64),    (64, 64)),  # 11 exp1-6
            ((224,  64),    (64, 64)),  # 12 exp1-7
            ((288,  64),    (64, 64)),  # 13 exp1-8

            (( 96, 128),    (64, 64)),  # 14 exp2-1
            ((160, 128),    (64, 64)),  # 15 exp2-2
            ((224, 128),    (64, 64)),  # 16 exp2-3
            ((288, 128),    (64, 64)),  # 17 exp2-4
            (( 96, 192),    (64, 64)),  # 18 exp2-5
            ((160, 192),    (64, 64)),  # 19 exp2-6
            ((224, 192),    (64, 64)),  # 20 exp2-7
            ((288, 192),    (64, 64)),  # 21 exp2-8

            (( 96, 256),    (64, 64)),  # 22 exp3-1
            ((160, 256),    (64, 64)),  # 23 exp3-2
            ((224, 256),    (64, 64)),  # 24 exp3-3
            ((288, 256),    (64, 64)),  # 25 exp3-4
            (( 96, 320),    (64, 64)),  # 26 exp3-5
            ((160, 320),    (64, 64)),  # 27 exp3-6
            ((224, 320),    (64, 64)),  # 28 exp3-7
            ((288, 320),    (64, 64)),  # 29 exp3-8

            (( 96, 384),    (64, 64)),  # 30 build11
            ((160, 384),    (64, 64)),  # 31 build12
            ((224, 384),    (64, 64)),  # 32 build21
            ((288, 384),    (64, 64)),  # 33 build22
            (( 96, 446),    (64, 64)),  # 34 build31
            ((160, 446),    (64, 64)),  # 35 build32
            ((224, 446),    (64, 64)),  # 36 build41
            ((288, 446),    (64, 64)),  # 37 build42
            (( 96, 512),    (64, 64)),  # 38 build51
            ((160, 512),    (64, 64)),  # 39 build52
        ]
#----------------------------------------------------------------------------------------------
