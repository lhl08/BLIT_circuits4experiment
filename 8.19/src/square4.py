import argparse
import drawsvg as draw
from numpy import array, sqrt, pi, log
from math import floor, ceil

class SimpleMaker:

    ## 比例尺：20 对应 0.5，40 对应 1

    def GenerateSimple(name, wire_length, size = 0):
        d = draw.Drawing(200,200,origin = 'center', displayInline = False)
        p = draw.Path(stroke_width=0.202, stroke='black', fill_opacity="0")

        simple_circuit = SimpleMaker(size)
        simple_circuit.makeSimple(p,wire_length)
        d.append(p)
        d.save_svg(name+".svg")

    def __init__(self,size = 0):

        self.size = size
        # self.line_width = 0.202
        self.line_width = 0.6
        self.spacing = 10
        self.pixel_scale = 3.77
        self.minimum_stitch_length = 2 * self.pixel_scale

    def makeSimple(self, path, wire_length, reverse=False):
        reverseF = -1 if reverse else 1
        if self.size > 0:
            #40单位对应1cm
            path.M(-80,-80)
            path.L(-80,80)
            path.L(80,80)
            path.L(80,-80)
            path.L(-80,-80)

        else:
            raise Exception("size must be >0")



    def drawStitches(self, p, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        length = sqrt((dx ** 2) + (dy ** 2))
        stittches = length/self.minimum_stitch_length

        for i in range (1, floor(stittches)):
            p.L (x1 + dx/stittches*i, y1 + dy/stittches*i)
        p.L(x2,y2)

if __name__=="__main__":
    SimpleMaker.GenerateSimple("square_4", -8, 10)

