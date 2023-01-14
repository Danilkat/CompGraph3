from svg_turtle import SvgTurtle
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

class LSystem:


    def __init__(self, iterations:int, segment_len:int):
        self.iterations = iterations
        self.segment_len = segment_len
        self.angle = 20.0
        self.rules = []
        self.turtle = SvgTurtle()
        self.saved_position = []
        self.saved_angle = []

        self.axiom = []
        self.rules = {}

        self.compiled = []

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
        self.position.append(self.turtle.position())
        self.saved_angle.append(self.turtle.heading())
    
    def terminalPopState(self):
        self.turtle.penup()
        self.turtle.setposition(self.position.pop())
        self.turtle.setheading(self.saved_angle.pop())
        self.turtle.pendown()

    def parse_str(self, input_lines):
        self.axiom = ProductionRule(input_lines.pop(0), self.commands).commands
        self.angle = float(input_lines.pop())
        self.rules = {}
        for line in input_lines:
            rule_buff = ProductionRule(line, self.commands)
            self.rules[rule_buff.letter] = rule_buff.commands
        return self

    def compile(self):
        self.compiled = self.axiom
        for i in range(self.iterations):
            self.compiled = self.compile_iteration(self.compiled)
        return self

    def compile_iteration(self, input):
        output = []
        for letter in input:
            if letter in self.rules:
                output += self.rules[letter]
            else:
                output.append(letter)
        return output

    def run(self):
        for command in self.compiled:
            if command in self.commands:
                self.commands[command]()
            else:
                self.terminalForward()


class ProductionRule:

    def __init__(self, rule_str, parent_commands: dict):

        self.commands = []
        self.letter = ""
        self.parse(rule_str, parent_commands)
        pass

    def parse(self, rule_str, parent_commands):
        if self.commands != []:
            return self.commands
        rule_str = rule_str.split(" ")
        self.letter = rule_str.pop(0)
        rule_str.pop(0)
        for letter in rule_str[0]:
            if letter in parent_commands:
                self.commands.append(parent_commands[letter])
            else:
                self.commands.append(letter)
        return self.commands
        
def main():
    file = open("data.txt", "r")
    lines = file.readlines()
    file.close()
    lsyst = LSystem(5, 1).parse_str(lines).compile()
    lsyst.run()
    name = "output.svg"
    lsyst.turtle.save_as(name)
    drawing = svg2rlg(name)
    renderPM.drawToFile(drawing, "output.png", fmt="PNG")



if __name__ == '__main__':
  main()