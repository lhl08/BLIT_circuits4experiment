import argparse
import drawscg as draw
from numpy import array, sqrt, pi, log
from math import floor, ceil

PIXEL_SCALE = 8.93 # customize it per computer
ALIGN_TOP = 1
ALIGN_BOTTOM = 0

class CoilMaker:

    def GenerateCoil(name, n_turns, transmission_line_length, size = 0):
        coilMaker = CoilMaker(n_turns, size)
        d = draw.Drawing(200, 200, origin = 'center', displayInline = False)
        p = draw.Path(stroke_width = 0.202, stroke = 'black', fill_opacity = "0")
        coilMaker.makeCoil(p, transmission_line_length)
        d.append(p)
        d.save_svg(name + ".svg")

    def __init__(self, n_turns, size = 0):
        
        self.size = size
        self.line_width = 0.202
        self.spacing = 0.5
        self.relative_permeability = 1

        self.minimum_stitch_length = 0.5
        self.n_turns = n_turns
        self.d_in = self.spacing
        self.d_out = self.size if self.size > 0 \
                else self.d_in + (self.spacing + self.line_width) * self.n_turns * 2
        
    def makeCoil(self, path, transmission_line_length, reverse):
        spacing = 4
        coil_location = array([transmission_line_length * PIXEL_SCALE, 0])
        din = self.d_in * PIXEL_SCALE
        centers = array([coil_location[0] + (self.d_out / 2) * PIXEL_SCALE, coil_location[1]])
        path.L(centers[0], centers[1])
        self.stitchCoil(path, centers, din, spacing, reverse)
        path.L(0,centers[1] - spacing[1])

    def stitchCoil(self, p, centers, din, spacing, reverse = False): 
        next_top_left_corner = array([centers[0]-din[0]/2, centers[1]-din[1]/2])
        next_bot_right_corner = array([centers[0]+din[0]/2, centers[1]+din[0]/2])
        # print("top, left corneer: ", next_top_left_corner)
        # print("bottom, right corner: ", next_bot_right_corner)
        self.last_point = centers

        for turn in range(0,self.n_turns):
            if reverse:
                self.drawStitches(p, next_top_left_corner[0], self.last_point[1]) #Right to Left
                self.drawStitches(p, next_top_left_corner[0], next_top_left_corner[1]) #Top to Bottom
                self.drawStitches(p, next_bot_right_corner[0], next_top_left_corner[1]) #Left to Right
                if turn == (self.n_turns -1):
                    self.drawStitches(p, next_bot_right_corner[0], centers[1] - spacing[1]) #Bottom to Tio
                else:
                    self.drawStitches(p, next_bot_right_corner[0], next_bot_right_corner[1])#Bottom to Tio
            else:
                self.drawStitches(p, next_bot_right_corner[0], self.last_point[1]) #Left to Right
                self.drawStitches(p, next_bot_right_corner[0], next_top_left_corner[1]) #Top to Bottom
                self.drawStitches(p, next_top_left_corner[0], next_top_left_corner[1]) #Left to Right
                if turn == (self.n_turns -1):
                    self.drawStitches(p, next_top_left_corner[0], centers[1] - spacing[1])#Bottom to Tio
                else:
                    self.drawStitches(p, next_top_left_corner[0], next_bot_right_corner[1]+spacing[1])#Bottom to Tio

            next_top_left_corner -= spacing
            next_bot_right_corner += spacing
        return p

    def drawStitches(self, p, x, y):
        dx = x - self.last_point[0]
        dy = y - self.last_point[1]
        length = sqrt((dx**2) + (dy**2))
        
        stitches = length/(self.minimum_stitch_length* PIXEL_SCALE)
        for i in range(1, floor(stitches)):
            # print(stitches)
            p.L(self.last_point[0] + dx/stitches*i, self.last_point[1] + dy/stitches*i)
        p.L(x, y)
        self.last_point = array([x, y])

