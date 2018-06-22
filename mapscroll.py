"""Roguelike map scrolling tutorial."""
from bearlibterminal import terminal
import noise

MAP_WIDTH = 256
MAP_HEIGHT = 256

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

class World:
    """Game world object"""
    def __init__(self):
        # Initialize an empty MAP_WIDTH x MAP_HEIGHT array
        # Use simplex noise to generate outdoor terrain.
        self.terrain_data = [
            [noise.snoise2(x / 16, y / 16, octaves=3)
             for x in range(MAP_WIDTH)]
            for y in range(MAP_HEIGHT)]
        self.player_x = 40
        self.player_y = 20

    def draw_terrain(self, map_x, map_y, screen_x, screen_y):
        """Draw terrain at map_x, map_y to the terminal at screen_x, screen_y"""
        if map_x >= 0 and map_y >= 0 and map_x < MAP_WIDTH and map_y < MAP_HEIGHT:
            num = self.terrain_data[map_y][map_x]
        else:
            num = -1
        if num == -1:
            # Outside the map
            terminal.puts(screen_x, screen_y, ' ')
        elif num < -0.2:
            # Water
            terminal.color(terminal.color_from_name('blue'))
            terminal.puts(screen_x, screen_y, '~')
        elif num < 0.5:
            # Grass
            terminal.color(terminal.color_from_name('green'))
            terminal.puts(screen_x, screen_y, '.')
        else:
            # Mountains
            terminal.color(terminal.color_from_name('gray'))
            terminal.puts(screen_x, screen_y, '^')

    def draw_player(self):
        terminal.color(terminal.color_from_name('white'))
        terminal.puts(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, '@')

    def to_map_x(self, screen_x):
        """Convert screen x coordinate to map x coordinate"""
        return screen_x + self.player_x - SCREEN_WIDTH // 2

    def to_map_y(self, screen_y):
        """Convert screen y coordinate to map y coordinate"""
        return screen_y + self.player_y - SCREEN_HEIGHT // 2

    def draw_world(self):
        for screen_y in range(SCREEN_HEIGHT):
            for screen_x in range(SCREEN_WIDTH):
                self.draw_terrain(
                    self.to_map_x(screen_x), self.to_map_y(screen_y), screen_x, screen_y)
        self.draw_player()

    def move_player(self, dx, dy):
        """Move player by vector (dx, dy).

        The player can't move beyond the map boundaries"""
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        if new_x >= 0 and new_y >= 0 and new_x < MAP_WIDTH and new_y < MAP_HEIGHT:
            self.player_x = new_x
            self.player_y = new_y

def setup_terminal():
    terminal.open()
    terminal.set("window: title='Map demo', size=80x50; font: square.ttf, size=16")

def main():
    """Main function"""
    setup_terminal()
    world = World()

    # Main loop
    while True:
        world.draw_world()
        terminal.refresh()

        input = terminal.read()

        if input == terminal.TK_UP:
            world.move_player(0, -1)
        if input == terminal.TK_DOWN:
            world.move_player(0, 1)
        if input == terminal.TK_LEFT:
            world.move_player(-1, 0)
        if input == terminal.TK_RIGHT:
            world.move_player(1, 0)

        if input == terminal.TK_CLOSE or input == terminal.TK_ESCAPE:
            break

    # Clean up
    terminal.close()

if __name__ == '__main__':
    main()
