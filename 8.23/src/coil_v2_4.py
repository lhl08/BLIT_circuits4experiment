#!/usr/bin/python
import argparse
import drawsvg as draw
from numpy import array, sqrt, pi, log
from math import floor, ceil

ALIGN_BOTTOM = 0
ALIGN_TOP = 1


PIXEL_SCALE = 8.93 # customize it per computer

SIZE_0603_IN_PIXEL = 1.6 * PIXEL_SCALE
SIZE_0402_IN_PIXEL = 1 * PIXEL_SCALE
#
#  Embroidery coil maker, import to inkscape to generate pes file
#**** Size unit is mm and inductance is uH
class CoilMaker:

    ## static function to generate a coil with a transmission line directly
    def GenerateCoil(name, transmission_line_length, inductance, size = 0, reverse = False, intergrated_r = False, intergrated_c = False):
        coilMaker = CoilMaker(inductance * (10 ** -6), size)
        d = draw.Drawing(200, 200, origin='center', displayInline=False)
        p = draw.Path(stroke_width=0.202, stroke='black', fill_opacity ="0")
        coilMaker.makeCoil(p, transmission_line_length, intergrated_r, intergrated_c,
                    reverse) 

        d.append(p)
        d.save_svg(name + ".svg")  # Save to file


    def __init__(self, inductance, size = 0):

        self.inductance = inductance
        self.size = size
        self.line_width = 0.202
        self.spacing = 0.5
        self.relative_permeability = 1  # 相对磁导率，单位长度上的电感
  
        self.minimum_stitch_length = 0.5 
        # self.n_turns = self.calculateNTurns()
        self.n_turns = 11
        print("nTurns:", self.n_turns)
        # self.d_in = self.spacing if self.size == 0 else self.size - (self.spacing + self.line_width) * self.n_turns * 2
        self.d_in = self.spacing
        self.d_out = self.size if self.size > 0 else self.d_in + (self.spacing + self.line_width) * self.n_turns * 2
        print("din:", self.d_in)
        print("dout:", self.d_out)

    ## calculate the number of turns, based on (optional) dout and target inductance.
    def calculateNTurns(self): 
        best_n, l_diff = 0, 100

        if self.size > 0:
            ### binary search to find the  number of turns given the inductance
            min_n = 1
            max_n = 50
            while min_n < max_n:
                n = (min_n + max_n) // 2
                d_in = self.size - (self.spacing + self.line_width) * n * 2
                print("n chosen in binary search: ", n)
                if d_in < 0:
                    max_n = n - 1
                    continue
                d_out = self.size
                l = CoilMaker.getSingleInductance(d_in, d_out, n, self.relative_permeability)
                print("single inductance: ", l)
                if l <= self.inductance:
                    min_n = n + 1
                else:
                    max_n = n - 1
                if abs(l - self.inductance) < l_diff:
                    l_diff = abs(l - self.inductance)
                    best_n = n
        else:
            ### binary search to find the number of turns for the smallest inductor
            min_n = 1
            max_n = 50
            while min_n < max_n:
                n = (min_n + max_n) // 2
                d_in = self.spacing
                d_out = d_in + (self.spacing + self.line_width) * n * 2
                l = CoilMaker.getSingleInductance(d_in, d_out, n, self.relative_permeability)
                if l <= self.inductance:
                    min_n = n + 1
                else:
                    max_n = n - 1
                if abs(l - self.inductance) < l_diff:
                    l_diff = abs(l - self.inductance)
                    best_n = n
        return best_n

    # Stitch Coil and Transmission line
    def makeCoil(self, path, transmission_line_length, integrated_r = False, integrated_c = False, reverse = False):
        
        reverseF = -1 if reverse else 1
        path.M(95, 0)
        coil_location = array([(transmission_line_length)*reverseF*PIXEL_SCALE, 0])
        spacing = array([self.spacing*PIXEL_SCALE, self.spacing*PIXEL_SCALE])
        print("line_width: ", self.line_width * PIXEL_SCALE)
        spacing[0] = 4
        spacing[1] = 4
        print("spacing: ", spacing[0])
        print("width: ", self.line_width * PIXEL_SCALE)
        print("inner: ", self.d_in * PIXEL_SCALE)
        # din = array([self.d_in*PIXEL_SCALE, self.d_in*PIXEL_SCALE]) 
        din = array([80, 80])
        print("coil_location: ", coil_location)
        self.stitchConnectionNode(path, [0, coil_location[1]], ALIGN_BOTTOM)
        if integrated_r:
            smd_r_location = (5*PIXEL_SCALE+SIZE_0603_IN_PIXEL)
            path.L(coil_location[0] - reverseF * smd_r_location, coil_location[1])  
            self.stitchConnectionNode(path, [coil_location[0] - reverseF * smd_r_location, coil_location[1]], ALIGN_BOTTOM)  
            path.L(coil_location[0] - reverseF * (smd_r_location-SIZE_0603_IN_PIXEL), coil_location[1]) 
            self.stitchConnectionNode(path, [coil_location[0] - reverseF * (smd_r_location-SIZE_0603_IN_PIXEL), coil_location[1]], ALIGN_BOTTOM)  
        
        if integrated_c:
            smd_c_location = (1 + PIXEL_SCALE+SIZE_0603_IN_PIXEL)
            path.L(coil_location[0] - reverseF * smd_c_location, coil_location[1])  
            self.stitchConnectionNode(path, [coil_location[0] - reverseF * smd_c_location, coil_location[1]], ALIGN_BOTTOM)  
            path.L(coil_location[0] - reverseF * (smd_c_location-SIZE_0603_IN_PIXEL), coil_location[1]) 
            self.stitchConnectionNode(path, [coil_location[0] - reverseF * (smd_c_location-SIZE_0603_IN_PIXEL), coil_location[1]], ALIGN_BOTTOM)  

        centers = array([coil_location[0] + (self.d_out/2)*reverseF*PIXEL_SCALE, coil_location[1]])
        path.L(centers[0], centers[1])
        self.stitchCoil(path, centers, din, spacing, reverse)
        path.L(0, centers[1] - spacing[1])
        self.stitchConnectionNode(path, [0, centers[1] - spacing[1]], ALIGN_TOP)
        print("single inductance: ", CoilMaker.getSingleInductance(self.d_in, self.d_out, self.n_turns, self.relative_permeability))

    # Stitch Connection Node
    def stitchConnectionNode(self, p, location, alignment = 0): 
 
        self.last_point = location
        size_in_pixel = 1  * PIXEL_SCALE
        if alignment == ALIGN_BOTTOM:
            self.drawStitches(p, location[0] + size_in_pixel/2, location[1])
            print(self.last_point)
            self.drawStitches(p, location[0] + size_in_pixel/2, location[1] + size_in_pixel)
            print(self.last_point)
            self.drawStitches(p, location[0] - size_in_pixel/2, location[1] + size_in_pixel)
            self.drawStitches(p, location[0] - size_in_pixel/2, location[1])
            self.drawStitches(p, location[0], location[1])
        else:
            self.drawStitches(p, location[0] + size_in_pixel/2, location[1])
            self.drawStitches(p, location[0] + size_in_pixel/2, location[1] - size_in_pixel)
            self.drawStitches(p, location[0] - size_in_pixel/2, location[1] - size_in_pixel)
            self.drawStitches(p, location[0] - size_in_pixel/2, location[1])
            self.drawStitches(p, location[0], location[1]) 
        return p

    # Stitch Coil
    def stitchCoil(self, p, centers, din, spacing, reverse = False): 
        next_top_left_corner = array([centers[0]-din[0]/2, centers[1]-din[1]/2])
        next_bot_right_corner = array([centers[0]+din[0]/2, centers[1]+din[0]/2])
        print("top, left corneer: ", next_top_left_corner)
        print("bottom, right corner: ", next_bot_right_corner)
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

    def getSingleInductance(d_in, d_out, n, rp): 
        C1 = 1.27
        C2 = 2.07
        C3 = 0.18
        C4 = 0.13
        N = n
        diaAvg = (10**-3 * (d_in + d_out) / 2)
        permeability = 4*pi*10**(-7) * rp
        fillratio = ( d_out - d_in)/( d_out + d_in)
        L = ((permeability *  N**2 *diaAvg* C1)/2) * (log(C2/fillratio) + C3*fillratio + C4* fillratio**2)
        return L

    def getDoubleInductance(d_in, d_out, n, rp, thickness):
        N = n
        X = thickness
        A = 0.184
        B = -0.525
        C = 1.038
        D = 1.001
        KC = (N**2)/( (A*X**3 + B*X**2 + C*X + D) * ( (1.67*N**2 -5.84*N +65)* 0.64) )
        L12 = CoilMaker.getSingleInductance(d_in, d_out, n, rp)
        Ltot = 2*L12 + 2*KC * L12
        return Ltot



if __name__=="__main__":
    CoilMaker.GenerateCoil("coil_v2_4", 2, 30, 25,reverse= True, intergrated_c= False, intergrated_r=False)


    