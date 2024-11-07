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
""" Animation Module, contains diverse Animation-Classes. """

#-------------------------------------------------------------------------------
class Anim:
    """ Definition of an Animation """

    def __init__(self, res_man, frame_lst, ticks_frame):
        """ resMan - resource manager
            frameLst - list of frames (indexes in resMan)
            ticksFrame - number of ticks per frame """
        self.res_man = res_man
        self.frame_lst = frame_lst
        self.ticks_frame = ticks_frame
        self.frame_idx = 0
        self.ticks_idx = 0
        # Get resource index of the frame
        self.res_idx = self.frame_lst[self.frame_idx]

    def draw(self, surface, x_pos, y_pos):
        """ Draw current frame on surface """
        self.res_man.draw(surface, self.res_idx, x_pos, y_pos)

    def tick(self):
        """ Next tick, increment tick index,
            return True if next frame to be displayed """
        self.ticks_idx += 1
        # Next frame to be displayed?
        if self.ticks_idx > self.ticks_frame:
            self.ticks_idx = 0
            return True
        return False

#-------------------------------------------------------------------------------
class AnimCyc(Anim):
    """ Definition of Cyclic-Animation """

    def __init__(self, resMan, frameLst, ticksFrame):
        """ resMan - resource manager
            frameLst - list of frames (indexes in resMan)
            ticksFrame - number of ticks per frame """
        Anim.__init__(self, resMan, frameLst, ticksFrame)

    def tick(self):
        if Anim.tick(self):
            self.frame_idx += 1
            if self.frame_idx >= len(self.frame_lst):
                self.frame_idx = 0
            # Get resource index of the frame
            self.res_idx = self.frame_lst[self.frame_idx]

#-------------------------------------------------------------------------------
class AnimOnce(Anim):
    """ Definition of Once-Animation """

    def __init__(self, resMan, frameLst, ticksFrame):
        """ resMan - resource manager
            frameLst - list of frames (indexes in resMan)
            ticksFrame - number of ticks per frame """
        Anim.__init__(self, resMan, frameLst, ticksFrame)
        self.finish = False

    def tick(self):
        if not self.finish:
            if Anim.tick(self):
                self.frame_idx += 1
                if self.frame_idx < len(self.frame_lst):
                    # Get resource index of the frame
                    self.res_idx = self.frame_lst[self.frame_idx]
                else:
                    self.finish = True

#-------------------------------------------------------------------------------
class AnimTilt(Anim):
    """ Definition of Tilt-Animation (Tilt to Left or to Right) """

    def __init__(self, resMan, frameLst, ticksFrame):
        """ resMan - resource manager
            frameLst - list of frames (indexes in resMan)
            ticksFrame - number of ticks per frame """
        Anim.__init__(self, resMan, frameLst, ticksFrame)
        self.tilt_dir = 0
        # Find the middle frame from the list, this is initial (ini) frame
        self.ini_idx = len(self.frame_lst)//2
        self.frame_idx = self.ini_idx
        # Get resource index of the frame
        self.res_idx = self.frame_lst[self.frame_idx]

    def tick(self):
        if Anim.tick(self):
            # if tilt left or right?
            if self.tilt_dir != 0:
                self.frame_idx += self.tilt_dir
                if self.frame_idx < 0:
                    self.frame_idx = 0
                elif self.frame_idx >= len(self.frame_lst):
                    self.frame_idx = len(self.frame_lst) - 1
            # if no tilt, but we are still not in the middle
            # move middle frame)
            elif self.frame_idx != self.ini_idx:
                if self.frame_idx < self.ini_idx:
                    self.frame_idx += 1
                else:
                    self.frame_idx -= 1
            # Get resource index of the frame
            self.res_idx = self.frame_lst[self.frame_idx]

#-------------------------------------------------------------------------------
class AnimTiltLink(Anim):
    """ Definition of Tilt-Linked Animation (the frame index and
        Tilt calculation is done by another AnimTilt class) """

    def __init__(self, resMan, frameLst, animTilt):
        """ resMan - resource manager
            frameLst - list of frames (indexes in resMan)
            animTilt - AnimTilt which handles frame and Tilt """
        Anim.__init__(self, resMan, frameLst, 0)
        self.anim_tilt = animTilt
        self.frame_idx = self.anim_tilt.frame_idx

    def tick(self):
        self.frame_idx = self.anim_tilt.frame_idx
        self.res_idx = self.frame_lst[self.anim_tilt.frame_idx]
    