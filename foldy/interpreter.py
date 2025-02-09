import random
import sys

class FoldyIP:
    """The instruction pointer in a FoldyGrid."""

    def __init__(self, parent):
        """Return a FoldyIP in grid at (0, 0) going right."""
        self.x = 0
        self.y = 0
        self.direction = 1
        self.parent = parent

    def __repr__(self):
        """Return a string representation of the FoldyIP."""
        return f'<IP at ({self.x}, {self.y}) going {self.dir_name}>'

    @property
    def dir_name(self):
        """Return the name of the direction the FoldyIP is going."""
        return ['up', 'right', 'down', 'left'][self.direction]

    @property
    def dir_grid(self):
        """Return a 2-tuple of the (dx, dy) of the IP's direction."""
        return [(0, -1), (1, 0), (0, 1), (-1, 0)][self.direction]
    
    @property
    def char_on(self):
        """Return the character the FoldyIP is on."""
        return self.parent[self.x, self.y]

    def turn(self, clockwise):
        """Turn the FoldyIP 90 degrees."""
        self.direction += 1 if clockwise else -1
        self.direction %= 4
        
    def tick(self):
        """Do the function the FoldyIP is on, then move the FoldyIP."""
        stack = self.parent.stack
        char = self.char_on
        move_amount = 1 # Changes to 2 if IP encounters skip command
        if char in (' ', None, ''): # No-op
            pass
        elif char in '0123456789': # Push number
            stack.append(int(char))
        elif char in '+-*:': # Arithmetic
            while len(stack) < 2:
                stack.insert(0, 0)
            b = stack.pop()
            a = stack.pop()
            if char == '+':
                stack.append(a + b)
            elif char == '-':
                stack.append(a - b)
            elif char == '*':
                stack.append(a * b)
            elif char == ':':
                stack.append(a // b)
        elif char in '^>v<': # Direction forcers
            self.direction = '^>v<'.index(char)
        elif char == '/': # Bouncers
            self.direction = [1, 0, 3, 2][self.direction]
        elif char == '\\':
            self.direction = [3, 2, 1, 0][self.direction]
        elif char == '|':
            self.direction = [0, 3, 2, 1][self.direction]
        elif char == '_':
            self.direction = [2, 1, 0, 3][self.direction]
        elif char == '$': # Skip if greater than 0
            if stack and stack[-1] > 0:
                move_amount = 2
        elif char == '?': # Random integer in [0, n)
            if stack:
                n = stack.pop()
                if n > 0:
                    stack.append(random.randrange(n))
        elif char in '{}': # Fold (or turn if fold mode is off)
            going_clockwise = char == '}'
            if fold_mode:
                self.parent.fold(going_clockwise)
            else:
                self.turn(going_clockwise)
        elif char == '!': # Output char
            n = stack.pop() if stack else 0
            print(chr(n % 0x110000), end='', file=self.parent.output_file)
        elif char == '.': # Output number
            n = stack.pop() if stack else 0
            print(n, end='', file=self.parent.output_file)
        elif char == ';': # Input char
            stack.append(ord(sys.stdin.read(1)))
        elif char == ',': # Input number
            line = sys.stdin.readline()
            try:
                stack.append(int(line))
            except ValueError:
                stack.append(0)
        elif char == '@': # Terminate
            raise StopIteration
        elif char == '&': # Duplicate top of stack
            if stack:
                stack.append(stack[-1])
        elif char == '~': # Pop top of stack
            if stack:
                stack.pop()
        elif char == '[': # Move top of stack to the bottom
            if stack:
                top_element = stack.pop()
                stack.insert(0, top_element)
        elif char == ']': # Move n-th item of stack to top
            if stack:
                element_number = stack.pop()
                # Account for 1-indexing
                element_number = (element_number - 1) % len(stack) + 1
                stack.append(stack.pop(-element_number))
        elif char == '#': # Toggle fold mode
            self.fold_mode = not self.fold_mode
            
        # Move the FoldyIP
        self.x += self.dir_grid[0] * move_amount
        self.x %= self.parent.width
        self.y += self.dir_grid[1] * move_amount
        self.y %= self.parent.height
        
class FoldyGrid:
    """The grid Foldy operates on."""

    def __init__(self, grid_string, output_file=sys.stdout):
        """Return a FoldyGrid formed from the code grid_string."""
        # Raise an error if unknown characters are in the code
        foldy_characters = r' 0123456789-*:<>^v/\|_$?{}!.;,@&~[]#'
        if (unknown_chars := set(grid_string) - set(foldy_characters)):
            error_text  = 'Unknown character'
            error_text += 's' if len(unknown_chars) > 1 else ''
            error_text += ' ('
            error_text += ''.join(sorted(list(unknown_chars)))
            error_text += ') found in code'
            raise SyntaxError(error_text)

        # Turn the code into a grid. [list(...)] is intentional.
        grid_string = grid_string or ' '
        self.grid = [list(grid_string)]
        self.width = len(grid_string)
        self.height = 1
        self.ip = FoldyIP(self)
        self.stack = []
        self.fold_mode = True
        self.output_file = output_file

    def __str__(self):
        """Return a string representation of the FoldyGrid."""
        grid = [[char for char in row] for row in self.grid]
        grid[self.ip.y][self.ip.x] = '\u00B7'
        return '\n'.join([' '.join(row) for row in grid])

    def __repr__(self):
        """Return a string representation of the FoldyGrid."""
        return (f'<{self.width}\u00D7{self.height} grid with '
                f'{repr(self.ip).removeprefix("<").removesuffix(">")}>')

    def __getitem__(self, pos):
        """Return the character at position pos in the grid."""
        x, y = pos
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError('FoldyGrid must be indexed by two ints')
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else: # Out of bounds
            return None

    def fold(self, clockwise):
        """Fold the code at the position of the IP either clockwise or
        counterclockwise.
        """
        # old_x/old_y is the location of the character to be folded.
        # new_x/new_y is where that character will end up.
        # old_* and new_* will keep marching one character at a time
        # until old_* goes out of bounds.
        old_x = new_x = self.ip.x
        old_y = new_y = self.ip.y
        old_direction = self.ip.dir_grid
        self.ip.turn(clockwise)
        new_direction = self.ip.dir_grid
        while True:
            old_x = old_x + old_direction[0]
            old_y = old_y + old_direction[1]
            new_x = new_x + new_direction[0]
            new_y = new_y + new_direction[1]
            current_char = self[old_x, old_y]
            if current_char is None:
                break
            self.grid[old_y][old_x] = ' '
            # If the new character position is out of bounds... redo the bounds
            if new_y < 0:
                self.grid.insert(0, [' '] * self.width)
                self.height += 1
                self.ip.y += 1
                oldY += 1
                newY += 1
            elif new_y >= self.height:
                self.grid.append([' '] * self.width)
                self.height += 1
            if new_x < 0:
                for row in range(self.height):
                    self.grid[row].insert(0, ' ')
                self.width += 1
                self.ip.x += 1
                oldX += 1
                newX += 1
            elif new_x > self.width:
                for row in range(self.height):
                    self.grid[row].append(' ')
                self.width += 1
            # Then we can place the new character down
            self.grid[new_y][new_x] = current_char

    def tick(self):
        """Run 1 tick of Foldy code. Return whether the code terminated
        on this tick.
        """
        try:
            self.ip.tick()
        except StopIteration:
            return True
        else:
            return False

    def run(self, ticks=50000):
        """Run Foldy code until it terminates or reaches ticks ticks."""
        if ticks == 0:
            while True:
                terminated = self.tick()
                if terminated:
                    break
        else:
            for i in range(ticks):
                terminated = self.tick()
                if terminated:
                    break
            else:
                raise RuntimeError(f'Foldy code did not terminate by tick {ticks}')
