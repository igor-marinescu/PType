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
""" Utils

Source from:
http://www.petercollingridge.co.uk/tutorials/3d/pygame/basic-transformations/

Source from:
https://stackoverflow.com/questions/47492663/how-can-i-determine-if-a-point-is-inside-a-certain-parallelogram-in-python/47508665
"""

def is_point_inside_parallelogram(parallelg, point):
    """ Check if point is inside of a parallelogram
        parallelog - definition of paralelogram as a list of 4 tulpes(xy-points)
                        [(ax, ay), (bx, by), (cx, cy), (dx, dy)]
        point - definition of a xy-point in a tulpe (px, py)
        returns True if point is inside parallelogram else False """

    # 3 points from parallelogram are required to check
    if len(parallelg) < 4:
        return False

    inside = False
    x_b = parallelg[0][0] - parallelg[1][0]
    y_b = parallelg[0][1] - parallelg[1][1]
    x_c = parallelg[2][0] - parallelg[1][0]
    y_c = parallelg[2][1] - parallelg[1][1]
    x_p = point[0] - parallelg[1][0]
    y_p = point[1] - parallelg[1][1]
    ddd = (x_b * y_c) - (y_b * x_c)
    if ddd != 0:
        oned = 1.0 / ddd
        bbb = ((x_p * y_c) - (x_c * y_p)) * oned
        ccc = ((x_b * y_p) - (x_p * y_b)) * oned
        inside = (bbb >= 0) & (ccc >= 0) & (bbb <= 1) & (ccc <= 1)
    return inside

def is_point_inside_rect(rect_point0, rect_point1, point):
    """ Check if point is inside of a rectangle
        rect_point0 - tulpe (x0, y0) contains the x and y coordinates of the upper-left corner
        rect_point1 - tulpe (x1, y1) contains the x and y coordinates of the right-bottom corner
        returns True if point is inside of rectangle or False if otherwise """
    if (point[0] >= rect_point0[0]) and (point[0] <= rect_point1[0]) and \
        (point[1] >= rect_point0[1]) and (point[1] <= rect_point1[1]):
        return True
    return False
