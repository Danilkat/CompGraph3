
# Third lab on Computer Graphics subject - L-systems

This program renders L-systems in svg and png files

## Usage:
`python main.py [file_name] [n_iterations] [init_angle] [verbose]`

- file_name (mandatory, path-like) - path to the txt file with rules
- n_interations (mandatory, int) - number of recursions
- init_angle (float) - initial heading of the turtle
- verbose (string) - call standard turtle graphics window if option given, else export results to png and svg

### Examples:
```
python main.py dragon.txt 9 0.0
python main.py snowflake.txt 5 0.0
python main.py triangle.txt 5 0.0 v
python main.py triangle.txt 5 0.0 sdaf
python main.py tree.txt 5 90.0
```

### Expected result:
* dragon9.svg and dragon9.png
* dragon5.svg and dragon5.png
* opens up turtle window that draws triangle
* opens up turtle window that draws triangle
* tree5.svg and tree5.png

## Txt files' description:
- First line in a file is axiom in format `S = "axiom"`
- Last line in a file is angle number that is used by some constants
- All other lines are rules in format `"rule_name" = "rule"`


## Grammar description:
* `F` - move forward for 10 units
* `b` - move forward for 10 units without drawing a line
* `+` - turn right (CW) by given angle (last line in txt file)
* `-` - turn left (CCW) by given angle (last line in txt file)
* `[` - save turtle's current position
* `]` - go back to the turtle's last saved position
* All other english capital letters are treated like rule names