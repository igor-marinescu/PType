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
""" Plates Resource Definition Module.

Resource definitions
This definition is used by res_man.py (loadTiles) when extracting tiles
from ./resources/images.png
"""

#       Top-left location| Tile size  |Tile | Description
#          in images.png |width,height|index|
resDef = [ #(( x0,  y0), |  (w,  h)   |     | U | L | B | R |
            ((  0,   0),    (32, 32)), #0   [ 0 | 0 | 0 | 0 ]

            (( 32,   0),    (32, 32)), #1   [ 0 | 2 | 2 | 0 ]
            (( 64,   0),    (32, 32)), #2   [ 0 | 2 | 3 | 2 ]
            (( 96,   0),    (32, 32)), #3   [ 0 | 0 | 1 | 2 ]

            (( 32,  32),    (32, 32)), #4   [ 2 | 3 | 2 | 0 ]
            (( 64,  32),    (32, 32)), #5   [ 3 | 3 | 3 | 3 ]
            (( 96,  32),    (32, 32)), #6   [ 1 | 0 | 1 | 3 ]

            (( 32,  64),    (32, 32)), #7   [ 2 | 1 | 0 | 0 ]
            (( 64,  64),    (32, 32)), #8   [ 3 | 1 | 0 | 1 ]
            (( 96,  64),    (32, 32)), #9   [ 1 | 0 | 0 | 1 ]

            (( 32,  96),    (32, 32)), #10  [ 2 | 3 | 3 | 2 ]
            (( 96,  96),    (32, 32)), #11  [ 1 | 2 | 3 | 3 ]
            (( 32, 160),    (32, 32)), #12  [ 3 | 3 | 2 | 1 ]
            (( 96, 160),    (32, 32)), #14  [ 3 | 1 | 1 | 3 ]

            (( 32, 224),    (32, 32)), #15  [ 3 | 1 | 1 | 3 ]
            (( 64, 224),    (32, 32)), #16  [ 3 | 3 | 2 | 1 ]
            (( 32, 256),    (32, 32)), #17  [ 1 | 2 | 3 | 3 ]
            (( 64, 256),    (32, 32)), #18  [ 2 | 3 | 3 | 2 ]

        ]
#----------------------------------------------------------------------------------------------
