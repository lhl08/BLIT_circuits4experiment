#!/usr/bin/python
import argparse
import drawsvg as draw
from numpy import array, sqrt, pi, log
from math import floor, ceil

#  Embroidery capacitor maker, import to inkscape to generate pes file
#**** Size unit is mm and capacitance is pF
class CapacitorMaker:

    def GenerateInterdigitalCapacitor(name, wire_length, capacitance, size = 0):
        d = draw.Drawing(200, 200, origin='center', displayInline=False)
        p = draw.Path(stroke_width=0.202, stroke='black', fill_opacity ="0")
        
        c = CapacitorMaker(capacitance, size)
        c.makeInterdigitalCapacitor(p, wire_length)
        d.append(p)
        d.save_svg(name + ".svg")  # Save to file

    def __init__(self, capacitance, size = 0):

        self.capacitance = capacitance
        self.size = size
        self.line_width = 0.202
        self.spacing = 2
        self.relative_permeability = 1
        self.pixel_scale = 3.77
        self.minimum_stitch_length = 2 * self.pixel_scale

    def makeInterdigitalCapacitor(self, path, wire_length, reverse = False):
        reverseF = -1 if reverse else 1
        if self.size > 0:
            n = floor((self.capacitance * self.line_width / ((self.relative_permeability + 1)*self.size) - 0.1) / 0.089 + 3)
            print("estimated capacitance: ", (self.relative_permeability+1) / self.line_width * self.size * (((n-3)*.089)+.10))
            spacing = array([self.spacing*reverseF*self.pixel_scale, self.spacing*self.pixel_scale])
            # line_width = self.line_width*self.pixel_scale*reverseF
            line_width = 1.2
            spacing[0] = 7.8
            print("spacing: ", spacing[0])
            print("line width: ", line_width)
            finger_length = 120
            path.M(-89,-95)
            path.L(-89,-60)
            path.L(-99,-60)
            path.L(-99,-50)
            path.L(-89,-50)
            path.L(-89,-60)
            path.L(-60,-60)
            lastPoint = array([-60,-60])
            for i in range(1,16):
                # self.drawStitches(path, lastPoint[0], lastPoint[1],
                #                         lastPoint[0], lastPoint[1] + finger_length)
                path.L(lastPoint[0], lastPoint[1] + finger_length)
                lastPoint[1] = lastPoint[1] + finger_length
                # self.drawStitches(path, lastPoint[0], lastPoint[1],
                #                         lastPoint[0] + line_width, lastPoint[1])
                path.L(lastPoint[0] + line_width, lastPoint[1])
                lastPoint[0] = lastPoint[0] + line_width
                if i == 5 : finger_length = 80
                if i == 10 : finger_length = 40
                # self.drawStitches(path, lastPoint[0], lastPoint[1],
                #                         lastPoint[0], lastPoint[1] - finger_length)
                path.L(lastPoint[0], lastPoint[1] - finger_length)
                lastPoint[1] = lastPoint[1] - finger_length
                # self.drawStitches(path, lastPoint[0], lastPoint[1],
                #                         lastPoint[0]+ spacing[0], lastPoint[1])
                path.L(lastPoint[0] + spacing[0], lastPoint[1])
                lastPoint[0] = lastPoint[0]+ spacing[0]
            path.M(-89, 70)
            path.L(-99, 70)
            path.L(-99, 80)
            path.L(-89, 80)
            path.L(-89, 70)
            path.L(-55.5, 70)
            lastPoint = array([-55.5, 70])
            finger_length = 120
            for i in range(2,16):
                self.drawStitches(path, lastPoint[0], lastPoint[1],
                                        lastPoint[0], lastPoint[1] - finger_length)
                lastPoint[1] = lastPoint[1] - finger_length
                self.drawStitches(path, lastPoint[0], lastPoint[1],
                                        lastPoint[0] + line_width, lastPoint[1])
                lastPoint[0] = lastPoint[0] + line_width
                self.drawStitches(path, lastPoint[0], lastPoint[1],
                                        lastPoint[0], lastPoint[1] + finger_length)
                lastPoint[1] = lastPoint[1] + finger_length
                self.drawStitches(path, lastPoint[0], lastPoint[1],
                                        lastPoint[0] + spacing[0], lastPoint[1])
                lastPoint[0] = lastPoint[0] + spacing[0]
                if i == 5: finger_length = 80
                if i == 10: finger_length = 40
            
        else:
            raise Exception("size must be > 0")
        

    def drawStitches(self, p, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        length = sqrt((dx**2) + (dy**2))
        
        stitches = length/self.minimum_stitch_length

        # print("stitches", stitches)
        for i in range(1, floor(stitches)):
            
            p.L(x1 + dx/stitches*i, y1 + dy/stitches*i)
        p.L(x2, y2)

    


if __name__=="__main__":
    CapacitorMaker.GenerateInterdigitalCapacitor("c", 20, 100, 20)


    