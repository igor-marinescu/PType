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
""" Backtiles Resource Definition Module.

Resource definitions
This definition is used by res_man.py (loadTiles) when extracting tiles
from ./resources/images.png
"""
#
#       Top-left location| Tile size  |Tile | Description
#          in images.png |width,height|index|
resDef = [ #(( x0,  y0), |  (w,  h)   |     |

            #((  0,   0),    (64, 64)), #0
            ((  0, 448),    (64, 64)),  #0 (28, empty)
            (( 64,   0),    (64, 64)),
            ((128,   0),    (64, 64)),
            ((192,   0),    (64, 64)),

            ((  0,  64),    (64, 64)),  #4
            (( 64,  64),    (64, 64)),
            ((128,  64),    (64, 64)),
            ((192,  64),    (64, 64)),

            ((  0, 128),    (64, 64)),  #8
            (( 64, 128),    (64, 64)),
            ((128, 128),    (64, 64)),
            ((192, 128),    (64, 64)),

            ((  0, 192),    (64, 64)),  #12
            (( 64, 192),    (64, 64)),
            ((128, 192),    (64, 64)),
            ((192, 192),    (64, 64)),

            ((  0, 256),    (64, 64)),  #16
            (( 64, 256),    (64, 64)),
            ((128, 256),    (64, 64)),
            ((192, 256),    (64, 64)),

            ((  0, 320),    (64, 64)),  #20
            (( 64, 320),    (64, 64)),
            ((128, 320),    (64, 64)),
            ((192, 320),    (64, 64)),

            ((  0, 384),    (64, 64)),  #24
            (( 64, 384),    (64, 64)),
            ((128, 384),    (64, 64)),
            ((192, 384),    (64, 64)),

            #((  0, 448),    (64, 64)), #28
            ((  0,   0),    (64, 64)),  #28 (0)
            (( 64, 448),    (64, 64)),
            ((128, 448),    (64, 64)),
            ((192, 448),    (64, 64)),

            ((  0, 512),    (64, 64)),  #32
            (( 64, 512),    (64, 64)),
            ((128, 512),    (64, 64)),
            ((192, 512),    (64, 64)),

            ((  0, 578),    (64, 64)),  #36
            (( 64, 578),    (64, 64)),
            ((128, 578),    (64, 64)),
            ((192, 578),    (64, 64)),

            ((256,   0),    (64, 64)), #40
            ((320,   0),    (64, 64)),
            ((256,  64),    (64, 64)),
            ((320,  64),    (64, 64)),

            ((256, 128),    (64, 64)), #44
            ((320, 128),    (64, 64)),
            ((256, 192),    (64, 64)),
            ((320, 192),    (64, 64)),

            ((256, 256),    (64, 64)), #48
            ((320, 256),    (64, 64)),
            ((256, 320),    (64, 64)),
            ((320, 320),    (64, 64)),

            ((256, 384),    (64, 64)), #52
            ((320, 384),    (64, 64))
        ]
#----------------------------------------------------------------------------------------------
