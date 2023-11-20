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
            # path.M(-95,-80)
            # path.L(-95, 0)
            # centers = array ([wire_length*reverseF*self.pixel_scale, 0])
            # spacing = array ([self.spacing*reverseF*self.pixel_scale, self.spacing*reverseF*self.pixel_scale])
            # finger_length = self.size * self.pixel_scale
            # line_width = self.line_width * self.pixel_scale * reverseF
            # path.L(-3*line_width-95, 0)
            # path.L(-3*line_width-95, 3*line_width)
            # path.L(-95, 3*line_width)
            # path.L(-95, 0)

            # ## parameters test
            # print("spacing: ", spacing)
            # print("line_width: ", line_width)
            # print("finger_length: ", finger_length)
            # ## end of test

            # path.L(centers[0], centers[1])
            # centers[1] -= finger_length
            # path.L(centers[0], centers[1])
            # lastPoint = centers

            # for i in range(0,3):
            #     self.drawStitches(path, lastPoint[0], lastPoint[1] , 
            #                             lastPoint[0] + spacing[0] , lastPoint[1] )
            #     self.drawStitches(path, lastPoint[0] + spacing[0] , lastPoint[1] , 
            #                             lastPoint[0] + spacing[0] , lastPoint[1] + finger_length )
            #     self.drawStitches(path, lastPoint[0] + spacing[0] , lastPoint[1] + finger_length , 
            #                             lastPoint[0] + spacing[0] - line_width , lastPoint[1] + finger_length )
            #     self.drawStitches(path, lastPoint[0] + spacing[0] - line_width , lastPoint[1] + finger_length , 
            #                             lastPoint[0] + spacing[0] - line_width , lastPoint[1] + finger_length + 3*line_width )
            #     self.drawStitches(path, lastPoint[0] + spacing[0] - line_width , lastPoint[1] + finger_length + 3*line_width ,
            #                             lastPoint[0] + spacing[0] + 2*line_width , lastPoint[1] + finger_length + 3*line_width )
            #     self.drawStitches(path, lastPoint[0] + spacing[0] + 2*line_width , lastPoint[1] + finger_length + 3*line_width ,
            #                             lastPoint[0] + spacing[0] + 2*line_width , lastPoint[1] + finger_length )
            #     self.drawStitches(path, lastPoint[0] + spacing[0] + 2*line_width , lastPoint[1] + finger_length ,
            #                             lastPoint[0] + spacing[0] + line_width , lastPoint[1] + finger_length )
            #     self.drawStitches(path, lastPoint[0] + spacing[0] + line_width , lastPoint[1] + finger_length ,
            #                             lastPoint[0] + spacing[0] + line_width , lastPoint[1] )
            #     lastPoint[0] += spacing[0] + line_width

            # lastPoint[1] += 3*finger_length

            # path.M(lastPoint[0], lastPoint[1])
            # for i in range(0,3):
            #     self.drawStitches(path, lastPoint[0] , lastPoint[1] ,
            #                             lastPoint[0] , lastPoint[1] - finger_length )
            #     self.drawStitches(path, lastPoint[0] , lastPoint[1] - finger_length ,
            #                             lastPoint[0] + line_width , lastPoint[1] - finger_length )
            #     self.drawStitches(path, lastPoint[0] + line_width , lastPoint[1] - finger_length ,
            #                             lastPoint[0] + line_width , lastPoint[1] - finger_length - 3*line_width )
            #     self.drawStitches(path, lastPoint[0] + line_width , lastPoint[1] - finger_length - 3*line_width ,
            #                             lastPoint[0] - 2*line_width , lastPoint[1] - finger_length - 3*line_width )
            #     self.drawStitches(path, lastPoint[0] - 2*line_width , lastPoint[1] -finger_length - 3*line_width ,
            #                             lastPoint[0] - 2*line_width , lastPoint[1] - finger_length )
            #     self.drawStitches(path, lastPoint[0] - 2*line_width , lastPoint[1] -finger_length,
            #                             lastPoint[0] - line_width , lastPoint[1] - finger_length )
            #     self.drawStitches(path, lastPoint[0] - line_width , lastPoint[1] - finger_length ,
            #                             lastPoint[0] - line_width , lastPoint[1] )
            #     self.drawStitches(path, lastPoint[0] - line_width , lastPoint[1] ,
            #                             lastPoint[0] - line_width - spacing[0] , lastPoint[1] )
            #     lastPoint[0] -= line_width + spacing[0]

            # path.L(centers[0], centers[1])
            # path.L(centers[0], centers[1] - finger_length)
            # # path.L(centers[0] - finger_length , centers[1] - finger_length)
            # path.L(-95 , centers[1] - finger_length)
            # path.L(-3*line_width-95 , centers[1] - finger_length)
            # path.L(-3*line_width-95, centers[1] - finger_length - 3*line_width)
            # path.L(-95, centers[1] - finger_length - 3*line_width)
            # path.L(-95, centers[1] - finger_length)
            
            #  # 宽度为40单位，即1cm
            # path.M(20,20)
            # path.L(20,-20)
            # path.L(-20,-20)
            # path.L(-20,20)
            # path.L(20,20)

            # 宽度为 5cm * 7cm ， 即200单位 * 280单位

            path.M(40,0)
            path.L(40,200)
            path.L(50,200)
            path.L(50,190)
            path.L(40,190)

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
    SimpleMaker.GenerateSimple("simple_line2", -8, 10)

