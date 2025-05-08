"""
Core rendering module for the ASCII art engine.
"""

import time
import os
try:
    import msvcrt
except ImportError:
    msvcrt = None  # Placeholder for non-Windows systems

class AsciiRenderer:
    _instance = None  # Singleton instance for global key access

    @staticmethod
    def get_instance():
        return AsciiRenderer._instance
    def __init__(self, width, height, char_map=None, update_func=None, draw_func=None, key_press_func=None, title="ASCII Game"):
        """
        Initializes the renderer with a given width, height, character map,
        and optional update, draw, and key_press callback functions.

        Args:
            width (int): The width of the rendering canvas in characters.
            height (int): The height of the rendering canvas in characters.
            char_map (list, optional): A list of characters to use for rendering,
                                       ordered from darkest to brightest.
                                       Defaults to a simple grayscale map.
            update_func (callable, optional): A function to be called every frame
                                              to update game logic. It should
                                              accept dt (delta time) as an argument.
            draw_func (callable, optional): A function to be called every frame
                                            to draw the scene. It should accept
                                            the renderer instance (screen) as an argument.
            key_press_func (callable, optional): A function to be called when a key
                                                 is pressed. It should accept the
                                                 key (bytes) as an argument.
            title (str, optional): The title for the console window (if supported).
        """
        AsciiRenderer._instance = self
        self.width = width
        self.height = height
        self.buffer = [[(' ', -1) for _ in range(width)] for _ in range(height)]
        if char_map is None:
            self.char_map = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']
        else:
            self.char_map = char_map
        
        self.update_callback = update_func
        self.draw_callback = draw_func
        self.key_press_callback = key_press_func
        self.running = False
        self.target_fps = 30  # Default target FPS
        self.game_speed = 10  # Default game speed (logic updates per second)
        self.title = title

        # Attempt to set console title (works on Windows)
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(self.title)
        except (ImportError, AttributeError):
            pass # Silently fail if ctypes is not available or not on Windows




    def _map_intensity_to_char(self, intensity):
        """
        Maps an intensity value (0-255) to a character in the char_map.
        """
        index = int((intensity / 255) * (len(self.char_map) - 1))
        return self.char_map[index]

    def load_frame(self, frame_data):
        """
        Loads a 2D array of intensity values (0-255) into the buffer.
        The dimensions of frame_data should match the renderer's width and height.
        This is a placeholder for actual image/video frame loading.
        """
        if len(frame_data) != self.height or len(frame_data[0]) != self.width:
            raise ValueError("Frame dimensions do not match renderer dimensions.")

        for r in range(self.height):
            for c in range(self.width):
                # Expect frame_data[r][c] to be a tuple (intensity, color_code)
                # If only intensity is provided (old format), default color_code to -1
                if isinstance(frame_data[r][c], tuple) and len(frame_data[r][c]) == 2:
                    intensity, color_code = frame_data[r][c]
                else:
                    intensity = frame_data[r][c] # Assuming old format if not a tuple
                    color_code = -1 # Default: no color
                
                char = self._map_intensity_to_char(intensity)
                self.buffer[r][c] = (char, color_code)

    def render(self):
        """
        Renders the current buffer to the console.
        Uses ANSI escape codes to clear the screen and move the cursor.
        """
        # Clear screen (ANSI escape code)
        print("\033[H\033[J", end="")
        output_lines = []
        for r in range(self.height):
            line_str = ""
            for c in range(self.width):
                char, color_code = self.buffer[r][c]
                if color_code != -1 and color_code is not None: # Check for a valid color code
                    # Using 256-color mode: \033[38;5;{CODE}m for foreground
                    line_str += f"\033[38;5;{color_code}m{char}\033[0m"
                else:
                    line_str += char
            output_lines.append(line_str)
        print("\n".join(output_lines))

    def clear_buffer(self, char=' ', color_code=-1):
        """
        Clears the rendering buffer, filling it with a specified character and color.
        Args:
            char (str): The character to fill the buffer with.
            color_code (int): The color code for the character.
        """
        self.buffer = [[(char, color_code) for _ in range(self.width)] for _ in range(self.height)]

    def draw_char(self, x, y, char, color_code=-1):
        """
        Draws a single character at a specific position in the buffer.
        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.
            char (str): The character to draw.
            color_code (int): The color code for the character.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = (char, color_code)

    def draw_text(self, x, y, text, color_code=-1):
        """
        Draws a string of text at a specific position.
        Args:
            x (int): The starting x-coordinate.
            y (int): The y-coordinate.
            text (str): The string to draw.
            color_code (int): The color code for the text.
        """
        for i, char_to_draw in enumerate(text):
            if 0 <= (x + i) < self.width and 0 <= y < self.height:
                self.buffer[y][x + i] = (char_to_draw, color_code)

    def run(self):
        """
        Starts the main rendering loop.
        This will call the user-defined update and draw functions.
        Game logic updates are controlled by game_speed, while rendering is controlled by target_fps.
        """
        if not self.update_callback and not self.draw_callback:
            print("Error: No update or draw function provided to run().")
            print("Please define update(dt) and/or draw(screen) functions ")
            print("or pass them to the AsciiRenderer constructor.")
            return

        self.running = True
        last_time = time.perf_counter()
        last_update_time = last_time
        frame_duration = 1.0 / self.target_fps
        update_duration = 1.0 / self.game_speed if self.game_speed > 0 else 0
        fixed_dt = update_duration  # Fixed delta time for consistent game speed

        try:
            while self.running:
                current_time = time.perf_counter()
                frame_dt = current_time - last_time
                last_time = current_time

                # Handle input
                if msvcrt and msvcrt.kbhit():
                    key = msvcrt.getch()
                    if self.key_press_callback:
                        self.key_press_callback(key)
                
                # Update game logic at fixed intervals based on game_speed
                if self.update_callback and update_duration > 0:
                    # Check if it's time for a logic update
                    if current_time - last_update_time >= update_duration:
                        self.update_callback(fixed_dt)  # Use fixed delta time for consistent game speed
                        last_update_time = current_time
                
                # The draw callback should prepare the frame using renderer methods
                # like clear_buffer, load_frame, draw_char, draw_text etc.
                if self.draw_callback:
                    self.draw_callback(self) # Pass the renderer instance as 'screen'
                
                self.render() # Render the current state of the buffer

                # Frame rate limiting for smooth rendering
                sleep_time = frame_duration - (time.perf_counter() - current_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
        except KeyboardInterrupt:
            print("\nLoop terminated by user (KeyboardInterrupt).")
            self.running = False
        finally:
            # Attempt to show cursor again, useful if terminal gets messy
            print("\033[?25h", end="") 
            print("Exiting renderer loop.")

    def quit(self):
        """Stops the rendering loop."""
        self.running = False

# Global functions to be defined by the user (pgzero style)
# These will be assigned to the renderer instance if not passed in constructor
_update_func_global = None
_draw_func_global = None
_key_press_func_global = None # For pgzero-style key handling

def update(dt):
    if _update_func_global:
        _update_func_global(dt)

def draw(screen):
    if _draw_func_global:
        _draw_func_global(screen)

def on_key_press(key):
    """Global key press handler, to be defined by the user."""
    if _key_press_func_global:
        _key_press_func_global(key)

def go(width=80, height=25, title="ASCII Game", char_map=None, target_fps=30, game_speed=10):
    """
    Initializes and runs the ASCII renderer with globally defined update/draw functions.
    This is the main entry point for a pgzero-style application.
    """
    global _update_func_global, _draw_func_global, _key_press_func_global
    
    # Try to find user-defined update, draw, and on_key_press in the global scope
    # This is a bit hacky but mimics pgzero's magic
    main_module = __import__("__main__")
    user_update = getattr(main_module, 'update', None)
    user_draw = getattr(main_module, 'draw', None)
    user_on_key_press = getattr(main_module, 'on_key_press', None)

    # Assign to global handlers if found, so they can be called by the stubs
    if user_update:
        _update_func_global = user_update
    if user_draw:
        _draw_func_global = user_draw
    if user_on_key_press:
        _key_press_func_global = user_on_key_press

    renderer = AsciiRenderer(width, height, char_map, 
                             update_func=user_update, 
                             draw_func=user_draw, 
                             key_press_func=user_on_key_press, # Pass it here
                             title=title)
    renderer.target_fps = target_fps
    renderer.game_speed = game_speed
    renderer.run()

# Example of how to use the new API (can be in a separate main.py)
# To run this example, you would save it as, e.g., main_game.py and run it.
# It won't run directly if __name__ == '__main__' is inside ascii_renderer.py
# because the global `update` and `draw` wouldn't be correctly picked up by `go()`.

# --- main_game.py (Example) ---
# import ascii_renderer as ar
# import time
import os
try:
    import msvcrt
except ImportError:
    msvcrt = None  # Placeholder for non-Windows systems
# 
# WIDTH = 40
# HEIGHT = 20
# 
# # Game state
# box_x = 0
# box_y = 5
# box_dx = 10 # units per second
# 
# def update(dt): # dt is delta time in seconds
#     global box_x
#     box_x += box_dx * dt
#     if box_x > WIDTH - 5 or box_x < 0:
#         box_x = max(0, min(box_x, WIDTH - 5)) # clamp
#         # In a real pgzero example, you might change direction here
# 
# def draw(screen): # screen is the AsciiRenderer instance
#     screen.clear_buffer() # Clear with default space
#     # Draw a simple box
#     for i in range(5):
#         screen.draw_char(int(box_x) + i, box_y, '#', color_code=200) # Red-ish box
#     screen.draw_text(0, 0, f"Box X: {box_x:.1f}", color_code=226) # Yellow text
# 
# # To run:
# # ar.go(WIDTH, HEIGHT, title="My ASCII Game", target_fps=20)
# # This line would typically be at the end of your main_game.py file.
# --- End of main_game.py (Example) ---