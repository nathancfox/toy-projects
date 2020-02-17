import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.colors as col

class Pattern:
    def __init__(self, name, desc, upper_left_points, cells):
        self.name = name
        self.desc = desc
        self.start_cells = {
                            'small': upper_left_points[0],
                            'medium': upper_left_points[1],
                            'large': upper_left_points[2]
                           }
        self.cells = np.array(cells)
    def generate_init_state(self, board_size):
        '''Create initial state for a given board size.

        Given a certain board size, create the list of live
        cell tuples that is used by the Board class to initialize
        the board state. Choosing a different board state causes
        a different "top-left" cell of the pattern to be used.
        This method works by combining a "top-left" cell of the
        pattern and a list of live cells, created by relative
        position to the "top-left" cell.
        
        Args:
            board_size: String from {'small', 'medium', 'large'}
                indicating a board side length of 11, 31, or 101.
        
        Returns:
            List of 2-member integer tuples that are absolute positions
            for lives cells as an initial state for the pattern on
            the given board.
        '''
        if self.start_cells[board_size] is not None:
            return self.cells + self.start_cells[board_size]
        else:
            raise Exception('Pattern too big for board!')

class PatternDict:
    def __init__(self):
        self.patterns = {}
    def add_pattern(self, pattern):
        '''Add new Pattern entry.'''
        self.patterns[pattern.name] = pattern
    def print_patterns(self):
        '''Pretty print contents.

        Creates a pretty string that displays the names
        and descriptions of all the Pattern stored in this
        PatternDict in alphabetical order.

        Returns:
            output_str: String to be printed to display contents
                of self.patterns.
        '''
        output_str = 'Patterns:\n\n'
        for k in sorted(self.patterns.keys()):
            output_str += f'\t{self.patterns[k].name}:\n'
            output_str += f'\t\t{self.patterns[k].desc}\n'
        output_str += '\n'
        return output_str

class Board:
    def __init__(self, x, y):
        self.state = np.zeros((x, y))
        self.x = x
        self.y = y
        self.next_state = np.zeros((x, y))
        self.initialized = False
    def initialize(self, live_cells):
        '''Initialize the board state with a given list of live cells.

        Args:
            live_cells: List of integer tuples or lists, each sub-list
                or sub-tuple having 2 members, where each sub-list or
                sub-tuple represent a single live cell on the board.
        '''
        for cell in live_cells:
            y, x = cell
            self.state[y, x] = 1
        self.initialized = True
    
    def count_live_neighbors(self, cell):
        '''Count live neighbors for cell.

        Given a single cell, count the number of live
        neighbors in the Moore Neighborhood, i.e. the
        8 cells directly adjacent to the given cell.
        If the given cell is on an edge, the neighbors
        are wrapped to the opposite edge.

        Args:
            cell: Integer tuple or list with 2 members, representing
                the (y, x) location of the cell whose neighbors should
                be counted, where the top left cell is (0, 0).
        
        Returns:
            live_neighbors: Integer from [0, 8] representing the number
                of live neighbors the given cell has.
        '''
        live_neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                else:
                    live_neighbors += self.state[(cell[0] + i) % self.x,
                                                 (cell[1] + j) % self.y]
        if live_neighbors < 0 or live_neighbors > 8:
            raise Exception('live_neighbors is illegal value')
        return live_neighbors
    
    def advance_one_cell(self, cell):
        '''Advance one cell one time step forward.

        self.initialize() must be called before this method.
        
        Args:
            cell: Integer tuple or list with 2 members, representing
                the (y, x) location of the cell to advance, where
                the top left cell is (0, 0).
        '''
        if not self.initialized:
            raise Exception('Initialize board first!')
        count = self.count_live_neighbors(cell)
        if count < 2 or count > 3:
            pass
        elif self.state[cell] == 1:
            self.next_state[cell] = 1
        elif count == 2:
            pass
        else:
            self.next_state[cell] = 1
    
    def advance_board(self):
        '''Advance the board one time step forward.

        Runs the Game of Life on the whole board for one
        time step, by populating a new array, then making
        the new array the current array and zeroing out the
        new array. self.initialize() must be called before
        this method.
        '''
        if not self.initialized:
            raise Exception('Initialize board first!')
        for i in range(self.x):
            for j in range(self.y):
                self.advance_one_cell((i, j))
        self.state = self.next_state
        self.next_state = np.zeros((self.x, self.y))
    
    def get_state(self):
        '''Return internal board state'''
        return self.state

def generate_patterns():
    '''Generate PatternDict of Pattern objects.

    Stores all available patterns stored as Pattern objects
    in a PatternDict object called patterns, available as
    a reference for initializing a Board object. Patterns
    should be added or removed from this method without
    perturbing the alphabetical ordering. This method should
    be called once at the beginning of a program using these
    patterns.

    Returns:
        patterns: PatternDict object holding all available Patterns.
    '''
    patterns = PatternDict()
    patterns.add_pattern(Pattern('beacon', 
                                 ('Small oscillator - Period 2'),
                                 [(3, 3), (13, 13), (48, 48)],
                                 [(0, 0), (0, 1), (1, 0), (2, 3),
                                  (3, 2), (3, 3)]))
    patterns.add_pattern(Pattern('beehive',
                                 ('Small still life'),
                                 [(4, 3), (14, 13), (49, 48)],
                                 [(0, 1), (0, 2), (1, 0), (1, 3),
                                  (2, 1), (2, 2)]))
    patterns.add_pattern(Pattern('blinker',
                                 ('Small oscillator - Period 2'),
                                 [(5, 4), (15, 14), (50, 49)],
                                 [(0, 0), (0, 1), (0, 2)]))
    patterns.add_pattern(Pattern('block',
                                 ('Small still life'),
                                 [(4, 4), (14, 14), (49, 49)],
                                 [(0, 0), (0, 1), (1, 0), (1, 1)]))
    patterns.add_pattern(Pattern('boat',
                                 ('Small still life'),
                                 [(4, 4), (14, 14), (49, 49)],
                                 [(0, 0), (0, 1), (1, 0), (1, 2),
                                  (2, 1)]))
    patterns.add_pattern(Pattern('diehard',
                                 ('Large methuselah that disappears after'
                                  '130 generations'),
                                 [None, (14, 11), (49, 46)],
                                 [(0, 6), (1, 0), (1, 1), (2, 1),
                                  (2, 5), (2, 6), (2, 7)]))
    patterns.add_pattern(Pattern('glider',
                                 ('Tiny spaceship that moves down and to'
                                  'the right indefinitely'),
                                 [(1, 1), (1, 1), (1, 1)],
                                 [(0, 1), (1, 2), (2, 0), (2, 1),
                                  (2, 2)]))
    patterns.add_pattern(Pattern('gosperglidergun',
                                 ('Large infinite that generates glider'
                                  'patterns indefinitely'),
                                 [None, None, (1, 1)],
                                 [(0, 24,), (1, 22), (1, 24), (2, 12),
                                  (2, 13), (2, 20), (2, 21), (2, 34),
                                  (2, 35), (3, 11), (3, 15), (3, 20),
                                  (3, 21), (3, 34), (3, 35), (4, 0),
                                  (4, 1), (4, 10), (4, 16), (4, 20),
                                  (4, 21), (5, 0), (5, 1), (5, 10),
                                  (5, 14), (5, 16), (5, 17), (5, 22),
                                  (5, 24), (6, 10), (6, 16), (6, 24),
                                  (7, 11), (7, 15), (8, 12), (8, 13)]))
    patterns.add_pattern(Pattern('hwss',
                                 ('Medium spaceship that moves to the'
                                  'right indefinitely'),
                                 [(2, 1), (12, 1), (47, 1)],
                                 [(0, 2), (0, 3), (1, 0), (1, 5),
                                  (2, 6), (3, 0), (3, 6), (4, 1),
                                  (4, 2), (4, 3), (4, 4), (4, 5),
                                  (4, 6)]))
    patterns.add_pattern(Pattern('loaf',
                                 ('Small still life'),
                                 [(3, 3), (13, 13), (48, 48)],
                                 [(0, 1), (0, 2), (1, 0), (1, 3),
                                  (2, 1), (2, 3), (3, 2)]))
    patterns.add_pattern(Pattern('lwss',
                                 ('Small spaceship that moves to the'
                                  'right indefinitely'),
                                 [(3, 1), (13, 1), (48, 1)],
                                 [(1, 3), (1, 4), (2, 1), (2, 2),
                                  (2, 4), (2, 5), (3, 1), (3, 2),
                                  (3, 3), (3, 4), (4, 2), (4, 3)]))
    patterns.add_pattern(Pattern('mwss',
                                 ('Medium spaceship that moves to the'
                                  'right indefinitely'),
                                 [(2, 1), (12, 1), (47, 1)],
                                 [(0, 2), (1, 0), (1, 4), (2, 5),
                                  (3, 0), (3, 5), (4, 1), (4, 2),
                                  (4, 3), (4, 4), (4, 5)]))
    patterns.add_pattern(Pattern('pentadecathlon',
                                 ('Large oscillator - Period 15'),
                                 [None, (10, 14), (45, 49)],
                                 [(0, 1), (1, 1), (2, 0), (2, 2),
                                  (3, 1), (4, 1), (5, 1), (6, 1),
                                  (7, 0), (7, 2), (8, 1), (9, 1)]))
    patterns.add_pattern(Pattern('pulsar',
                                 ('Large oscillator - Period 3'),
                                 [None, (9, 9), (44, 44)],
                                 [(0, 2), (0, 3), (0, 4), (0, 8),
                                  (0, 9), (0, 10), (2, 0), (2, 5),
                                  (2, 7), (2, 12), (3, 0), (3, 5),
                                  (3, 7), (3, 12), (4, 0), (4, 5),
                                  (4, 7), (4, 12), (5, 2), (5, 3),
                                  (5, 4), (5, 8), (5, 9), (5, 10),
                                  (7, 2), (7, 3), (7, 4), (7, 8),
                                  (7, 9), (7, 10), (8, 0), (8, 5),
                                  (8, 7), (8, 12), (9, 0), (9, 5),
                                  (9, 7), (9, 12), (10, 0), (10, 5),
                                  (10, 7), (10, 12), (12, 2), (12, 3),
                                  (12, 4), (12, 8), (12, 9), (12, 10)]))
    patterns.add_pattern(Pattern('r-pentomino',
                                 ('Large methuselah that stabilizes after'
                                  '1103 generations'),
                                 [(4, 4), (14, 14), (49, 49)],
                                 [(0, 1), (0, 2), (1, 0), (1, 1),
                                  (2, 1)]))
    patterns.add_pattern(Pattern('toad',
                                 ('Small oscillator - Period 2'),
                               [(4, 3), (14, 13), (49, 48)],
                               [(0, 1), (0, 2), (0, 3), (1, 0),
                                (1, 1), (1, 2)]))
    patterns.add_pattern(Pattern('tub',
                                 ('Small still life'),
                                 [(4, 4), (14, 14), (49, 49)],
                                 [(0, 1), (1, 0), (1, 2), (2, 1)]))
    return patterns
    
def update(n, *fargs):
    '''Updates the board and plot for the FuncAnimation method.

    Used as an argument for the FuncAnimation method that updates
    the plot by updating the Board object's state and then feeding
    the new state to the data being used for the plot.

    Args:
        n: Integer frame number. Mandatory argument that is unused here.
        *fargs: Variable number of arguments. Contains img, the object
            produced by matplotlib.pyplot.imshow() that should be updated
            for the FuncAnimation method. Also contains game, the Board
            object holding the state of the Game of Life being animated.
    '''
    img, game = fargs
    game.advance_board()
    img.set_data(game.state)

def main(print_pat, size, pattern, frames, speed):
    '''Runs a Game of Life and produces a video animation.

    Takes optional command line parameters to pick a board
    size, a starting pattern, a number of frames to play,
    and a frames-per-second encoding for the video animation.
    Then plays Conway's Game of Life on the specified board
    with the specified pattern for the specified number of
    frames. Then plots the progression of board states as
    an exported video animation called animation.mp4.

    Args:  
        size: String from {'small', 'medium', 'large'} indicating
            board size, where all boards are square and the 3
            available side lengths are 11, 31, and 101.
        pattern: String from hard-coded list of available patterns
            indicating the starting configuration of live cells.
        frames: Integer representing the number of time steps
            the Game of Life should be played for.
        speed: Integer from {1, 2, 3, 4} indicating the frames
            per second the animation should be encoded with. Options
            correspond to {2, 2.5, 3, 5}.
        
    Returns:
        Exports a video file called animation.mp4 to the current
        working directory containing a depiction of the Game of Life
        that played out.
    '''
    patt_dict = generate_patterns()
    if print_pat:
        print('\n')
        print(patt_dict.print_patterns())
        sys.exit()
    if size == 'small':
        game = Board(x = 11, y = 11)
    elif size == 'medium':
        game = Board(x = 31, y = 31)
    else:
        game = Board(x = 101, y = 101)
    init_state = patt_dict.patterns[pattern].generate_init_state(size)
    game.initialize(init_state)

    fig, ax = plt.subplots(figsize = (14, 14))
    cmap = col.ListedColormap(['white', 'black'])
    norm = col.BoundaryNorm(boundaries = [0, 1, 2], ncolors = cmap.N)
    ax.grid(which = 'major', axis = 'both', linestyle = '-',
            color = 'gray', linewidth = 0.5)
    ax.set_xticks(np.arange(-0.5, game.state.shape[1]))
    ax.set_yticks(np.arange(-0.5, game.state.shape[0]))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis = 'both', which = 'both', length = 0)
    plt.tight_layout()
    img = ax.imshow(game.state, cmap = cmap, norm = norm)

    anim = ani.FuncAnimation(fig, update, frames = frames,
                             fargs = (img, game))
    speeds = {
              1: 2,
              2: 2.5,
              3: 3,
              4: 5
             }
    anim.save('animation.mp4', fps = speeds[speed], writer = 'ffmpeg', codec = 'libx264')
    print('New movie file called "animation.mp4"')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--print_pat', action = 'store_true',
                        help = ('Print the available patterns'
                                'and exit the program.'))
    parser.add_argument('--board_size', nargs = '?', default = 'medium',
                        type = str,
                        choices = ['small', 'medium', 'large'],
                        help = ('Choose the size of the board you',
                                'want your Game of Life to be played',
                                'on. small, medium or large = size'
                                'length of 11, 31, or 101'))
    parser.add_argument('--pattern', nargs = '?', default = 'pulsar',
                        type = str,
                        choices = ['block', 'beehive', 'loaf', 'boat',
                                   'tub', 'blinker', 'toad', 'beacon',
                                   'pulsar', 'pentadecathlon', 'glider',
                                   'lwss', 'mwss', 'hwss', 'r-pentomino',
                                   'diehard', 'gosperglidergun'],
                        help = ('Choose the pattern to visualize on your',
                                'Game of Life. Note that some patterns',
                                'will not fit on small board'))
    parser.add_argument('--frames', nargs = '?', default = 30, type = int,
                        help = ('Number of frames to visualize at 5 fps.',
                                'Maximum period is 15 frames for pattern',
                                'options available.'))
    parser.add_argument('--speed', nargs = '?', default = 2, type = int,
                        choices = [1, 2, 3, 4],
                        help = ('Frames per second for the animation.',
                                'Options are 1, 2, 3, or 4, corresponding',
                                'to 2, 2.5, 3, or 5'))
    args = parser.parse_args()

    main(args.print_pat, args.board_size, args.pattern,
         args.frames, args.speed)
