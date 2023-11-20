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
            spacing = array([self.spacing*reverseF*self.pixel_scale, self.spacing*self.pixel_scale])
            line_width = 1
            spacing[0] = 8
            finger_length = 120
            path.M(-160, -160)
            path.L(-160, -70)
            path.L(-170, -70)
            path.L(-170, -80)
            path.L(-120, -80)
            lastPoint = array([-120, -80])
            for i in range(1,6):
                self.drawStitches(path, lastPoint[0], lastPoint[1],
                                        lastPoint[0], lastPoint[1] + finger_length)
                lastPoint[1] = lastPoint[1] + finger_length
                self.drawStitches(path, lastPoint[0], lastPoint[1],
                                        lastPoint[0] + line_width, lastPoint[1])
                lastPoint[0] = lastPoint[0] + line_width
                self.drawStitches(path, lastPoint[0], lastPoint[1],
                                        lastPoint[0], lastPoint[1] - finger_length)
                lastPoint[1] = lastPoint[1] - finger_length
                self.drawStitches(path, lastPoint[0], lastPoint[1],
                                        lastPoint[0]+ spacing[0], lastPoint[1])
                lastPoint[0] = lastPoint[0]+ spacing[0]
            path.L(lastPoint[0] + 80, lastPoint[1])
            
            path.M(-160, 50)
            path.L(-170, 50)
            path.L(-170, 60)
            path.L(-160, 60)
            path.L(-160, 50)
            path.L(-124.5, 50)
            lastPoint = array([-124.5, 50])
            finger_length = 120
            for i in range(1,6):
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
            path.L(lastPoint[0] + 80, lastPoint[1])
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
    CapacitorMaker.GenerateInterdigitalCapacitor("humidity_v2", 20, 100, 20)


    