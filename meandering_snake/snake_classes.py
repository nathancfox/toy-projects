# Snake class definitions for meandering_snake.py
import numpy as np
import matplotlib as mpl
import matplotlib.path as mpath
import matplotlib.patches as mpatches

class SnakeSegment:
    def __init__(self, position, color='#000000', label=''):
        # Instance Variable Assignment
        self.position = self.validate_position(position)
        self.color = self.validate_hex(color)
        self.label = label
    
    def validate_position(self, position):
        position = tuple(position)
        if len(position) != 2:
            raise ValueError('position must be an iterable of length 2!')
        position_int = tuple([int(p) for p in position])
        for i in range(len(position)):
            if position[i] != position_int[i]:
                raise ValueError('position must contain two integers!')
        position = position_int
        return(position)

    def validate_hex(self, hex_string):
        if type(hex_string) is not str:
            raise ValueError('hex_string must be a string!')
        hex_format_flag = False
        hex_string = hex_string.upper()
        if len(hex_string) == 7:
            if hex_string[0] == '#':
                hex_options = ('0', '1', '2', '3', '4', '5', '6', '7',
                               '8', '9', 'A', 'B', 'C', 'D', 'E', 'F')
                new_hex_string = '#'
                for i in range(1, 7):
                    if hex_string[i] not in (hex_options):
                        hex_format_flag = True 
            else:
                hex_format_flag = True 
        else:
            hex_format_flag = True 
        if hex_format_flag:
            raise ValueError('hex_string must be in hex format! e.g. #000000')
        return(hex_string)

    def get_patches(self):
        patch_list = []
        patch_list.append(mpatches.Rectangle(xy=(self.position[0] - 1,
                                                self.position[1] - 1),
                                            width=1, height=1, fill=True,
                                            edgecolor=None, linewidth=0,
                                            facecolor=self.color,
                                            label=self.label)
                         )
        return(patch_list)

class SnakeHead(SnakeSegment):
    def __init__(self, position, direction,
                 color='#000000', eye_color='#FF0000',
                 label=''):
        SnakeSegment.__init__(self, position, color)
        self.eye_color = self.validate_hex(eye_color)
        self.direction = self.validate_direction(direction)
        self.label = label

    def validate_direction(self, direction):
        if type(direction) is not str:
            raise ValueError('direction must be a string!')
        direction = direction[0].upper()
        valid_directions = ('U', 'D', 'L', 'R')
        if direction not in valid_directions:
            raise ValueError('direction must be one of these words or an '
                             'abbreviation of these words: {\"top\", '
                             '\"bottom\", \"left\", \"right\"}. It is not '
                             'case-sensitive')
        return(direction)

    def get_patches(self):
        patch_list = [] 
        # Always start at left corner (snake's perspective,
        # then move to tip, then right corner, then close
        if self.direction == 'U':
            path_data = [
                (mpath.Path.MOVETO, (self.position[0] - 1, self.position[1] - 1)),
                (mpath.Path.LINETO, (self.position[0] - 0.5, self.position[1])),
                (mpath.Path.LINETO, (self.position[0], self.position[1] - 1)),
                (mpath.Path.CLOSEPOLY, (self.position[0] - 1, self.position[1] - 1))
            ]
        elif self.direction == 'D':
            path_data = [
                (mpath.Path.MOVETO, (self.position[0], self.position[1])),
                (mpath.Path.LINETO, (self.position[0] - 0.5, self.position[1] - 1)),
                (mpath.Path.LINETO, (self.position[0] - 1, self.position[1])),
                (mpath.Path.CLOSEPOLY, (self.position[0], self.position[1]))
            ]
        elif self.direction == 'L':
            path_data = [
                (mpath.Path.MOVETO, (self.position[0], self.position[1] - 1)),
                (mpath.Path.LINETO, (self.position[0] - 1, self.position[1] - 0.5)),
                (mpath.Path.LINETO, (self.position[0], self.position[1])),
                (mpath.Path.CLOSEPOLY, (self.position[0], self.position[1] - 1))
            ]
        elif self.direction == 'R':
            path_data = [
                (mpath.Path.MOVETO, (self.position[0] - 1, self.position[1])),
                (mpath.Path.LINETO, (self.position[0], self.position[1] - 0.5)),
                (mpath.Path.LINETO, (self.position[0] - 1, self.position[1] - 1)),
                (mpath.Path.CLOSEPOLY, (self.position[0] - 1, self.position[1]))
            ]
        else:
            raise AssertionError('self.direction wasn\'t U, D, L, or R!')
        codes, verts = zip(*path_data)
        head_path = mpath.Path(verts, codes)
        head = mpatches.PathPatch(head_path,
                                  edgecolor=None, linewidth=0,
                                  facecolor=self.color, label=self.label)
        eye_direction_offset = {
                'U': {
                    'left': (-0.65, -0.75),
                    'right': (-0.35, -0.75)
                     },
                'D': {
                    'left': (-0.35, -0.25),
                    'right': (-0.65, -0.25)
                     },
                'L': {
                    'left': (-0.25, -0.65),
                    'right': (-0.25, -0.35)
                     },
                'R': {
                    'left': (-0.75, -0.35),
                    'right': (-0.75, -0.65)
                     }
        }
        EYE_RADIUS = 0.05
        le_position = (self.position[0] + eye_direction_offset[self.direction]['left'][0],
                       self.position[1] + eye_direction_offset[self.direction]['left'][1])
        left_eye = mpatches.Circle(xy = le_position,
                                   radius = EYE_RADIUS,
                                   edgecolor=None, linewidth=0,
                                   facecolor=self.eye_color, label=self.label)
        re_position = (self.position[0] + eye_direction_offset[self.direction]['right'][0],
                       self.position[1] + eye_direction_offset[self.direction]['right'][1])
        right_eye = mpatches.Circle(xy = re_position,
                                    radius = EYE_RADIUS,
                                    edgecolor=None, linewidth=0,
                                    facecolor=self.eye_color, label=self.label)
        patch_list.append(head)
        patch_list.append(left_eye)
        patch_list.append(right_eye)
        return(patch_list)

class SnakeBodySegment(SnakeSegment):
    def __init__(self, position, color, label=''):
        SnakeSegment.__init__(self, position, color, label=label)

class Snake:
    def __init__(self, head_position, head_direction,
                 length, color='#000000', eye_color='#FF0000',
                 label=''):
        self.head = SnakeHead(head_position, head_direction,
                              color=color, eye_color=eye_color, label=label)
        self.body = []
        if self.head.direction == 'U':
            body_offset = (0, -1)
        elif self.head.direction == 'D':
            body_offset = (0, 1)
        elif self.head.direction == 'L':
            body_offset = (1, 0)
        elif self.head.direction == 'R':
            body_offset = (-1, 0)
        else:
            raise AssertionError('Snake\'s head\'s direction is not U, D, L, or R!')
        for i in range(length):
            self.body.append(SnakeBodySegment(( head_position[0] + ((i+1) * body_offset[0]),
                                                head_position[1] + ((i+1) * body_offset[1]) ),
                                              color=color, label=label))
        self.label = label

    def get_new_head_pos(self, direction):
        direction = self.head.validate_direction(direction)
        direction_offset = {
                'U': (0, 1),
                'D': (0, -1),
                'L': (-1, 0),
                'R': (1, 0)
        }
        new_head_pos = (self.head.position[0] + direction_offset[direction][0],
                        self.head.position[1] + direction_offset[direction][1])
        return(new_head_pos)

    def move_snake_one(self, direction):
        direction = self.head.validate_direction(direction)
        new_head_pos = self.get_new_head_pos(direction)
        for bs in self.body:
            if bs.position == new_head_pos:
                raise ValueError('Can\'t go that direction, a body '
                                 'segment is there!')
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].position = self.body[i - 1].position
        self.body[0].position = self.head.position
        self.head.position = new_head_pos
        self.head.direction = direction

    def get_patches(self):
        patch_list = []
        patch_list.append(self.head.get_patches())
        for bs in self.body:
            patch_list.append(bs.get_patches())
        return(patch_list)

    def draw_on_axes(self, axes):
        patches = self.get_patches()
        for patch_list in patches:
            for patch in patch_list:
                axes.add_patch(patch)

    def remove_from_axes(self, axes):
        # Have to do this awkward loop because each iteration potentially
        # removes an element from the list. So simple naive iteration
        # doesn't work.
        i = 0
        while i < len(axes.patches):
            if axes.patches[i].get_label() == self.label:
                axes.patches[i].remove()
            else:
                i += 1

    def get_label(self):
        return(self.label)

    def set_label(self, label):
        if type(label) is not str:
            raise ValueError('label must be a string!')
        self.label = label

    def set_head_color(self, color):
        self.head.color = self.head.validate_hex(color)

    def set_eye_color(self, color):
        self.head.eye_color = self.head.validate_hex(color)

    def set_body_color(self, color):
        hex = None
        try:
            color = self.body[0].validate_hex(color)
            hex = True
        except ValueError as e:
            try:
                cmap = mpl.cm.get_cmap(color)
                hex = False
            except ValueError:
                raise ValueError('color must be a hex color or a '
                                 'matplotlib colormap name!') from e
        if hex:
            for bs in self.body:
                bs.color = color
        else:
            colors = np.linspace(0, 1, len(self.body))
            for bs, c in zip(self.body, colors):
                bs.color = cmap(c)

def main():
    pass

if __name__ == '__main__':
    main()
