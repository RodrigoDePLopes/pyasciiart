"""
Core rendering module for the ASCII art engine.
"""

import time

class AsciiRenderer:
    def __init__(self, width, height, char_map=None):
        """
        Initializes the renderer with a given width, height, and character map.

        Args:
            width (int): The width of the rendering canvas in characters.
            height (int): The height of the rendering canvas in characters.
            char_map (list, optional): A list of characters to use for rendering, 
                                       ordered from darkest to brightest. 
                                       Defaults to a simple grayscale map.
        """
        self.width = width
        self.height = height
        # Buffer will store tuples of (character, color_code)
        # Initialize with space character and default color (e.g., None or -1 for no specific color)
        self.buffer = [[(' ', -1) for _ in range(width)] for _ in range(height)]
        if char_map is None:
            self.char_map = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']
        else:
            self.char_map = char_map

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

    def clear_buffer(self):
        """
        Clears the rendering buffer, filling it with space characters and default color.
        """
        self.buffer = [[(' ', -1) for _ in range(self.width)] for _ in range(self.height)]

# Example usage (can be moved to main.py later)
if __name__ == '__main__':
    # A simple test: a fading square
    renderer = AsciiRenderer(width=40, height=20)
    
    for i in range(10):
        frame = [[0 for _ in range(40)] for _ in range(20)] # Black background
        intensity = int((i / 9) * 255) # Fading intensity
        
        # Draw a square
        for r in range(5, 15):
            for c in range(10, 30):
                frame[r][c] = intensity
        
        renderer.load_frame(frame)
        renderer.render()
        time.sleep(0.2)

    print("Animation finished.")