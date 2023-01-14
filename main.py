from svg_turtle import SvgTurtle
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import sys
import math

class LSystem:

    def __init__(self, iterations:int, segment_len:int, init_angle = 0.0):
        self.iterations = iterations
        self.segment_len = segment_len
        self.angle = 20.0
        self.init_angle = init_angle
        self.turtle = SvgTurtle()
        self.turtle.left(self.init_angle)
        self.saved_position = []
        self.saved_angle = []

        self.axiom = ""
        self.rules = {}

        self.compiled = ""

        self.commands = {
            '+': self.terminalRotateCW,
            '-': self.terminalRotateCCW,
            '[': self.terminalPushState,
            ']': self.terminalPopState
        }

    def terminalForward(self):
        self.turtle.forward(self.segment_len)
  
    def terminalRotateCW(self):
        self.turtle.right(self.angle)
    
    def terminalRotateCCW(self):
        self.turtle.left(self.angle)
    
    def terminalPushState(self):
        self.saved_position.append(self.turtle.position())
        self.saved_angle.append(self.turtle.heading())
    
    def terminalPopState(self):
        self.turtle.penup()
        self.turtle.setposition(self.saved_position.pop())
        self.turtle.setheading(self.saved_angle.pop())
        self.turtle.pendown()

    def parse_str(self, input_lines):
        self.axiom = ProductionRule(input_lines.pop(0)).commands
        self.angle = float(input_lines.pop())
        self.rules = {}
        for line in input_lines:
            rule_buff = ProductionRule(line)
            self.rules[rule_buff.letter] = rule_buff.commands
        return self

    def compile(self):
        self.compiled = self.axiom
        for i in range(self.iterations):
            print(f"compiling iteration {i} of {self.iterations}")
            self.compiled = self.compile_iteration(self.compiled)
            print(f"finished compiling iteration {i} of {self.iterations} (length = {len(self.compiled)})")
        return self

    def compile_iteration(self, input):
        output = ""
        for letter in input:
            if letter in self.rules:
                output += self.rules[letter]
            else:
                output += letter
                if letter not in self.commands.keys():
                    print(f"WARNING: unknown letter {letter}")
        return output

    def prerun(self):
        x_ll_corner = 0
        y_ll_corner = 0
        x_ur_corner = 0
        y_ur_corner = 0

        for command in self.compiled:
            if command in self.commands.keys():
                self.commands[command]()
            else:
                self.terminalForward()

            x_ll_corner, x_ur_corner, y_ll_corner, y_ur_corner = self.update_aabb(
                x_ll_corner,
                x_ur_corner,
                y_ll_corner,
                y_ur_corner
                )
        x_ll_corner = math.floor(x_ll_corner)
        y_ll_corner = math.floor(y_ll_corner)
        x_ur_corner = math.ceil(x_ur_corner)
        y_ur_corner = math.ceil(y_ur_corner)

        x_center = (x_ur_corner + x_ll_corner) / 2
        y_center = (y_ur_corner + y_ll_corner) / 2

        self.turtle = SvgTurtle(width = x_ur_corner - x_ll_corner, height = y_ur_corner - y_ll_corner)
        self.turtle.left(self.init_angle)
        self.turtle.penup()
        self.turtle.setposition(-x_center, -y_center)
        self.turtle.pendown()
        print("finished prerun")

    def run(self):
        print("start running...")
        self.prerun()
        for command in self.compiled:
            if command in self.commands.keys():
                self.commands[command]()
            else:
                self.terminalForward()
        

    def update_aabb(self, x0, x1, y0, y1, x = None, y = None):
        if x is None:
            x = self.turtle.xcor()
        if y is None:
            y = self.turtle.ycor()
        x0 = min(x0, x)
        x1 = max(x1, x)
        y0 = min(y0, y)
        y1 = max(y1, y)
        return x0, x1, y0, y1


class ProductionRule:

    def __init__(self, rule_str):

        self.commands = ""
        self.letter = ""
        self.parse(rule_str)
        pass

    def parse(self, rule_str):
        if self.commands != "":
            return self.commands
        rule_str = rule_str.split(" ")
        self.letter = rule_str.pop(0)
        rule_str.pop(0)
        self.commands = rule_str[0]
        return self.commands
        
def main(input_str, iterations, init_angle):
    file = open(input_str, "r")
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    file.close()
    lsyst = LSystem(int(iterations), 10, float(init_angle)).parse_str(lines).compile()
    lsyst.run()

    name_svg = input_str.split(".")[0] +iterations+ ".svg"
    name_png = input_str.split(".")[0] +iterations+ ".png"

    lsyst.turtle.save_as(name_svg)
    drawing = svg2rlg(name_svg)
    renderPM.drawToFile(drawing, name_png, fmt="PNG")


if __name__ == '__main__':
    main(*sys.argv[1:])