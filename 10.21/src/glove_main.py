import drawsvg as draw
from numpy import array

class GloveMaker:

    def GenerateGlove(name):
        d = draw.Drawing(200, 200, origin='center', displayInline = False)
        p = draw.Path(stroke_width = 0.202, stroke = 'black', fill_opacity = "0")
        glove_circuit = GloveMaker()
        glove_circuit.makeGlove(p)
        d.append(p)
        d.save_svg(name + ".svg")

    def makeGlove(self, path):
        '''
        The Scale Limit: 9cm * 9cm (360 * 360)
        '''
        # Main Line 
        ## node1
        path.M(40, -160)
        path.L(40, -170)
        path.L(30, -170)
        path.L(30, -160)
        ## node2
        path.L(120, -160)
        path.L(120, -170)
        path.L(110, -170)
        path.L(110, -160)
        path.L(160, -160)
        ## node3
        path.L(160, 16)
        path.L(170, 16)
        path.L(170, 6)
        path.L(160, 6)
        path.L(160, 20)
        path.L(0, 20)
        ## phone coil
        self.stitchCoil(path, 10, [0, 90], [40, 40], [4, 4], 4)
        path.L(-4, 16)
        path.L(140, 16)
        ## node4
        path.L(140, 6)
        path.L(130, 6)
        path.L(130, 16)
        path.L(140, 16)
        path.L(140, -140)
        ## node5
        path.L(110, -140)
        path.L(110, -130)
        path.L(120, -130)
        path.L(120, -140)
        path.L(60, -140)
        path.L(60, -110)
        path.L(60, -120)
        path.L(50, -120)
        path.L(50, -110)
        path.L(60, -110)

        # Middle Finger
        path.M(-60, -120)
        path.L(-50, -120)
        path.L(-50, -110)
        path.L(-60, -110)
        path.L(-60, -160)
        path.L(10, -160)
        path.L(10, -170)
        path.L(0, -170)
        path.L(0, -160)
        
        # Index Finger
        ## part1
        path.M(115, -140)
        path.L(115, -60)
        path.L(50, -60)
        path.L(50, -70)
        path.L(60, -70)
        path.L(60, -60)
        ## part2
        path.M(-60, -60)
        path.L(-60, -70)
        path.L(-50, -70)
        path.L(-50, -60)
        path.L(-180, -60)
        path.L(-180, -90)
        path.L(80, -90)
        path.L(80, -180)
        path.L(90, -180)
        path.L(90, -170)
        path.L(80, -170)

        # Thumb Coil
        ## part1
        path.M(140, 11)
        path.L(-180, 11)
        path.L(-180, -24)
        path.L(-50, -24)
        path.L(-50, -34)
        path.L(-60, -34)
        path.L(-60, -24)
        ## part2
        path.M(60, -24)
        path.L(60, -34)
        path.L(50, -34)
        path.L(50, -24)
        path.L(180, -24)
        path.L(180, -14)
        path.L(170, -14)
        path.L(170, -24)
        
    def stitchCoil(self, path, n_turns, centers, din, spacing, direction):
        '''
        direction: 1 for left, 2 for up, 3 for right, 4 for down
        '''
        next_top_left_corner = array([centers[0] - din[0]/2, centers[1] - din[1]/2])
        next_bot_right_corner = array([centers[0] + din[0]/2, centers[1] + din[1]/2])
        path.L(centers[0], centers[1])

        if direction == 1:
            path.L(next_top_left_corner[0], centers[1])
            for turn in range(0, n_turns + 1):
                path.L(next_top_left_corner[0], next_top_left_corner[1])
                path.L(next_bot_right_corner[0], next_top_left_corner[1])
                if turn == n_turns:
                    path.L(next_bot_right_corner[0], centers[1] - spacing[1])
                else:
                    path.L(next_bot_right_corner[0], next_bot_right_corner[1])
                    path.L(next_top_left_corner[0] - spacing[0], next_bot_right_corner[1])
                next_top_left_corner -= spacing
                next_bot_right_corner += spacing
        elif direction == 2:
            path.L(centers[0], next_top_left_corner[1])
            for turn in range(0, n_turns + 1):
                path.L(next_bot_right_corner[0], next_top_left_corner[1])
                path.L(next_bot_right_corner[0], next_bot_right_corner[1])
                if turn == n_turns:
                    path.L(centers[0] + spacing[0], next_bot_right_corner[1])
                else:
                    path.L(next_top_left_corner[0], next_bot_right_corner[1])
                    path.L(next_top_left_corner[0], next_top_left_corner[1] - spacing[1])
                next_top_left_corner -= spacing
                next_bot_right_corner += spacing
        elif direction == 3:
            path.L(next_bot_right_corner[0], centers[1])
            for turn in range(0, n_turns + 1):
                path.L(next_bot_right_corner[0], next_bot_right_corner[1])
                path.L(next_top_left_corner[0], next_bot_right_corner[1])
                if turn == n_turns:
                    path.L(next_top_left_corner[0], centers[1] + spacing[1])
                else:
                    path.L(next_top_left_corner[0], next_top_left_corner[1])
                    path.L(next_bot_right_corner[0] + spacing[0], next_top_left_corner[1])
                next_top_left_corner -= spacing
                next_bot_right_corner += spacing
        else:
            path.L(centers[0], next_bot_right_corner[1])
            for turn in range(0, n_turns + 1):
                path.L(next_top_left_corner[0], next_bot_right_corner[1])
                path.L(next_top_left_corner[0], next_top_left_corner[1])
                if turn == n_turns:
                    path.L(centers[0] - spacing[0], next_top_left_corner[1])
                else:
                    path.L(next_bot_right_corner[0], next_top_left_corner[1])
                    path.L(next_bot_right_corner[0], next_bot_right_corner[1] + spacing[1])
                next_top_left_corner -= spacing
                next_bot_right_corner += spacing

if __name__=="__main__":
    GloveMaker.GenerateGlove("glove_main")