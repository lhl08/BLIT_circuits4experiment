import drawsvg as draw
from numpy import array

class CoilMaker:

    def GenerateCoil(name):
        d = draw.Drawing(200, 200, origin='center', display = False)
        p = draw.Path(stroke_width = 0.202, stroke = 'black', fill_opacity = "0")
        coil_circuit = CoilMaker()
        coil_circuit.makeCoil(p)
        d.append(p)
        d.save_svg(name + ".svg")

    def makeCoil(self, path):
        '''
        scale limit : 9cm * 9cm (360 * 360)
        '''
        path.M(-110, 0)
        path.L(-110, 10)
        path.L(-120, 10)
        path.L(-120, 0)
        path.L(-90, 0)
        self.stitchCoil(path, 25, [-90, -90], [6, 6], [3, 3], 2)
        path.L(-87, 0)
        path.L(-30, 0)
        path.L(-30, 10)
        path.L(-40, 10)
        path.L(-40, 00)


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
    CoilMaker.GenerateCoil("coil_dis3_25")