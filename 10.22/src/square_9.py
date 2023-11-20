import drawsvg as draw

class SimpleMaker:
    ## 比例尺：20 对应 0.5，40 对应 1
    def GenerateSimple(name):
        d = draw.Drawing(200,200,origin = 'center', displayInline = False)
        p = draw.Path(stroke_width=0.202, stroke='black', fill_opacity="0")

        simple_circuit = SimpleMaker()
        simple_circuit.makeSimple(p)
        d.append(p)
        d.save_svg(name+".svg")

    def makeSimple(self, path):

        path.M(-180, -180)
        path.L(180, -180)
        path.L(180, 180)
        path.L(-180, 180)
        path.L(-180, -180)

if __name__=="__main__":
    SimpleMaker.GenerateSimple("square_9")

