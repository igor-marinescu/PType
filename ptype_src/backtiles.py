""" Backtiles (Background Tiles) Module. """
# Background.
# Background consists from [TY_CNT x TX_CNT] Tiles.
# Every Tile is a 64pix x 64pix image stored in ResManager
#
#           |0           x            TX_CNT|
#    -------+---+---+---+---+---+---+---+---+-------------
#         0 |   |   |   |   |   |   |   |   |       Not displayed
#          -+---+---+---+---+---+---+---+---+-------------
#           |   |   |   |   |   |   |   |   | 1          ^
#          -+---+---+---+---+---+---+---+---+            |
#           |   |   |   |   |   |   |   |   |            |
#           |                               |            |
#         y |            ...                |       Displayed
#           |                               |            |
#           |   |   |   |   |   |   |   |   |            |
#          -+---+---+---+---+---+---+---+---+            |
#           |   |   |   |   |   |   |   |   | TY_CNT-1   v
#          -+---+---+---+---+---+---+---+---+-------------
#    TY_CNT |   |   |   |   |   |   |   |   |       Not displayed
#    -------+---+---+---+---+---+---+---+---+-------------
#
#
#            |      y=0     ,      y=1      ...  y = TY_CNT |
# backTIdx = [ [x=0..TX_CNT], [x=0..TX_CNT] ... [0..TX_CNT] ]
#
#   backTIdx[0..TY_CNT][0..TX_CNT]
#       2D list contains indexes (in ResManager) of background Tiles
#           Ex: backTImg[y][x] = 2
#               Contains the Tile from ReManager with image index 2
#
#   backTImg[0..TY_CNT][0..TX_CNT]
#       2D list contains pointers to images (in ResManager) of background Tiles
#               backTImg[y][x] = resMan.imgList[backTIdx[y][x]]
#
#   dispTImg[0..TY_CNT][0..TX_CNT]
#       2D list contains pointers to images (in ResManager) of displayed Tiles
#

import random

TX_CNT = 8
TY_CNT = 10

class BackTiles:
    """ Background """

    def __init__(self, res_man):

        self.resman = res_man

        # Create Back and Displayed Tiles
        self.backt_idx = [[0 for x in range(TX_CNT)]    for y in range(TY_CNT)]
        self.backt_img = [[None for x in range(TX_CNT)] for y in range(TY_CNT)]
        self.dispt_img = [[None for x in range(TX_CNT)] for y in range(TY_CNT)]

        # Create temp copy list
        self.back_lastl = [0 for x in range(TX_CNT)]

        # emptiness & simple stars
        self.bt0 = [0, 0, 1, 4, 13, 15, 22, 26, 27, 31, 48, 49, 50, 51, 52 ,53]
        # small asteroids
        self.bt1 = [0, 2, 3, 29, 30, 23]
        # big asteroids
        self.bt2 = [5, 8, 9, 14, 18, 19]
        # comets 2x1
        self.bt3 = [[16, 17]]
        # very big 2x2 asteroids
        self.bt4 = [[6,  7,  10, 11],
                    [20, 21, 24, 25],
                    [32, 33, 36, 37],
                    [34, 35, 38, 39],
                    [40, 41, 42, 43],
                    [44, 45, 46, 47]]

        self.generate_back()
        self.copy_back_to_disp()
        self.generate_back()

        self.scroll_cnt = 0
        self.offset_y = 0
        self.offset_div = 0

    def generate_back(self):
        """ Generate new Back Tiles backTIdx and backTImg """

        # clear old pattern
        for y_pos in range(TY_CNT):
            for x_pos in range(TX_CNT):
                self.backt_idx[y_pos][x_pos] = 0

        # place 1 very big (2x2) asteroid
        x_pos = random.randint(-1, TX_CNT - 1)
        y_pos = random.randint(0, TY_CNT - 2)
        z_idx = random.randint(0, len(self.bt4) - 1)
        if x_pos >= 0:
            self.backt_idx[y_pos    ][x_pos] = self.bt4[z_idx][0]
            self.backt_idx[y_pos + 1][x_pos] = self.bt4[z_idx][2]
        if (x_pos + 1) < TX_CNT:
            self.backt_idx[y_pos    ][x_pos + 1] = self.bt4[z_idx][1]
            self.backt_idx[y_pos + 1][x_pos + 1] = self.bt4[z_idx][3]

        # place 1 commet (2x1)
        x_pos = random.randint(0, TX_CNT - 2)
        y_pos = random.randint(0, TY_CNT - 2)
        z_idx = random.randint(0, len(self.bt3) - 1)
        if (self.backt_idx[y_pos][x_pos] == 0) and (self.backt_idx[y_pos][x_pos + 1] == 0):
            self.backt_idx[y_pos][x_pos]     = self.bt3[z_idx][0]
            self.backt_idx[y_pos][x_pos + 1] = self.bt3[z_idx][1]

        # place 3 big asteroid
        for _ in range(3):
            x_pos = random.randint(0, TX_CNT - 1)
            y_pos = random.randint(0, TY_CNT - 1)
            z_idx = random.randint(0, len(self.bt2) - 1)
            if self.backt_idx[y_pos][x_pos] == 0:
                self.backt_idx[y_pos][x_pos] = self.bt2[z_idx]

        # place 6 small asteroid
        for _ in range(6):
            x_pos = random.randint(0, TX_CNT - 1)
            y_pos = random.randint(0, TY_CNT - 1)
            z_idx = random.randint(0, len(self.bt1) - 1)
            if self.backt_idx[y_pos][x_pos] == 0:
                self.backt_idx[y_pos][x_pos] = self.bt1[z_idx]

        # fill the rest with small stars and empyness
        for y_pos in range(0, TY_CNT):
            for x_pos in range(0, TX_CNT):
                if self.backt_idx[y_pos][x_pos] == 0:
                    self.backt_idx[y_pos][x_pos] = self.bt0[random.randint(0, len(self.bt0) - 1)]

        # copy from idx to image
        for y_pos in range(TY_CNT):
            for x_pos in range(TX_CNT):
                self.backt_img[y_pos][x_pos] = self.resman.img_list[self.backt_idx[y_pos][x_pos]]

    def copy_back_to_disp(self):
        """ Copy all Back Tiles --> Display Tiles """
        for y_pos in range(0, TY_CNT):
            for x_pos in range(0, TX_CNT):
                self.dispt_img[y_pos][x_pos] = self.backt_img[y_pos][x_pos]

    def scroll(self):
        """ Scroll Back and Displayed Tiles with 1 Tile down """

        # copy last line from backTiles to temp buffer
        for x_pos in range(TX_CNT):
            self.back_lastl[x_pos] = self.backt_img[TY_CNT - 1][x_pos]

        # scroll down both: display and backTiles
        for y_pos in range(TY_CNT - 1, 0, -1):
            for x_pos in range(TX_CNT):
                self.dispt_img[y_pos][x_pos] = self.dispt_img[y_pos - 1][x_pos]
                self.backt_img[y_pos][x_pos] = self.backt_img[y_pos - 1][x_pos]

        # copy last line from backTiles at the top of display
        for x_pos in range(TX_CNT):
            self.dispt_img[0][x_pos] = self.back_lastl[x_pos]

        # backTiles buffer empty? generate new
        self.scroll_cnt += 1
        if self.scroll_cnt >= TY_CNT:
            self.generate_back()
            self.scroll_cnt = 0

    def display(self, surface):
        """ Draw all Display Tiles """
        for y_pos in range(TY_CNT):
            for x_pos in range(TX_CNT):
                surface.blit(self.dispt_img[y_pos][x_pos], ((x_pos * 64),
                    self.offset_y + (y_pos * 64) - 64))

    def tick(self):
        """ Class Tick function, must be called every cycle """
        self.offset_div += 1
        if self.offset_div > 4:
            self.offset_div = 0
            self.offset_y += 1
            if self.offset_y >= 64:
                self.scroll()
                self.offset_y = 0
