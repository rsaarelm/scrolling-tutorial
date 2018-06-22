"""Roguelike map scrolling tutorial."""
from collections import namedtuple
from bearlibterminal import terminal
import noise

# Make an immutable class for 2-dimensional geometric vectors.
# Inherit from a named tuple to get immutability.
class Vec2(namedtuple('BaseVec', 'x, y')):
    """Two-dimensional geometric vector class"""

    # Implement basic vector ops.
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __floordiv__(self, other):
        return Vec2(self.x // other, self.y // other)

# And let's make a rectangle class too, just to make the rectangle iterations
# easier

class Rect(namedtuple('BaseRect', 'origin, size')):
    """Immutable rectangle class.

    Origin is the top left corner of the rectangle, size is the size of the rectangle.
    Both values are expected to be 2D vector like."""

    def __new__(self, origin, size):
        # Cast the arguments to Vec2 in case they're some generic tuple type.
        # The * prefix unpacks the value into a syntactical argument list.
        return super().__new__(Rect, Vec2(*origin), Vec2(*size))

    def __iter__(self):
        """Generate all the integer points contained in the rectangle."""
        for y in range(self.origin.y, self.origin.y + self.size.y):
            for x in range(self.origin.x, self.origin.x + self.size.x):
                yield Vec2(x, y)

    def __contains__(self, item):
        """Return whether a vector value is within this rectangle"""
        try:
            pos = Vec2(*item)
            return pos.x >= self.origin.x and pos.y >= self.origin.y \
                    and pos.x < self.origin.x + self.size.x \
                    and pos.y < self.origin.y + self.size.y
        except TypeError:
            return False

MAP = Rect((0, 0), (256, 256))
SCREEN = Rect((0, 0), (80, 50))

class World:
    """Game world object"""
    def __init__(self):
        # Initialize an empty MAP_WIDTH x MAP_HEIGHT array
        # Use simplex noise to generate outdoor terrain.
        self.terrain_data = [
            [noise.snoise2(x / 16, y / 16, octaves=3)
             for x in range(MAP.size.x)]
            for y in range(MAP.size.y)]
        self.player_pos = Vec2(40, 20)

    def draw_terrain(self, map_pos, screen_pos):
        """Draw terrain at map_x, map_y to the terminal at screen_x, screen_y"""
        if map_pos in MAP:
            num = self.terrain_data[map_pos.y][map_pos.x]
        else:
            num = -1
        if num == -1:
            # Outside the map
            terminal.puts(screen_pos.x, screen_pos.y, ' ')
        elif num < -0.2:
            # Water
            terminal.color(terminal.color_from_name('blue'))
            terminal.puts(screen_pos.x, screen_pos.y, '~')
        elif num < 0.5:
            # Grass
            terminal.color(terminal.color_from_name('green'))
            terminal.puts(screen_pos.x, screen_pos.y, '.')
        else:
            # Mountains
            terminal.color(terminal.color_from_name('gray'))
            terminal.puts(screen_pos.x, screen_pos.y, '^')

    def draw_player(self):
        terminal.color(terminal.color_from_name('white'))
        terminal.puts(SCREEN.size.x // 2, SCREEN.size.y // 2, '@')

    def to_map_pos(self, screen_pos):
        """Convert screen position to map position"""
        return screen_pos + self.player_pos - SCREEN.size // 2

    def draw_world(self):
        for screen_pos in SCREEN:
            self.draw_terrain(self.to_map_pos(screen_pos), screen_pos)
        self.draw_player()

    def move_player(self, delta):
        """Move player by vector delta

        The player can't move beyond the map boundaries"""
        if self.player_pos + delta in MAP:
            self.player_pos = self.player_pos + delta

def setup_terminal():
    terminal.open()
    terminal.set("window: title='Map demo', size=80x50; font: square.ttf, size=16")

# Vectors corresponding to movement keys
MOVES = {
    terminal.TK_UP: Vec2(0, -1),
    terminal.TK_DOWN: Vec2(0, 1),
    terminal.TK_LEFT: Vec2(-1, 0),
    terminal.TK_RIGHT: Vec2(1, 0),
    }

def main():
    """Main function"""
    setup_terminal()
    world = World()

    # Main loop
    while True:
        world.draw_world()
        terminal.refresh()

        input = terminal.read()

        if input in MOVES:
            world.move_player(MOVES[input])

        if input == terminal.TK_CLOSE or input == terminal.TK_ESCAPE:
            break

    # Clean up
    terminal.close()

if __name__ == '__main__':
    main()
