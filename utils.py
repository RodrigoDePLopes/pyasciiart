"""
Utility module for the ASCII art engine.
Contains character maps and color handling logic (placeholder).
"""

# Default character map (grayscale, simple)
# Ordered from darkest to brightest perception for typical console backgrounds
DEFAULT_CHAR_MAP = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']

# More detailed character map for better grayscale representation
DETAILED_CHAR_MAP = [
    ' ', '.', ',', ':', ';', 'i', 'l', 'I', 'L', 'Y', 'V', 'X', 'K', 'W', 
    'M', 'N', '8', 'B', '&', '%', '$', '#', '@'
]

# Example of a very simple color mapping (placeholder)
# This would need to be expanded significantly for actual color support
# and would depend on the terminal's capabilities (e.g., ANSI escape codes for colors)

def get_char_map(name='default'):
    """
    Returns a predefined character map.

    Args:
        name (str): The name of the character map ('default', 'detailed').

    Returns:
        list: A list of characters for rendering.
    """
    if name == 'detailed':
        return DETAILED_CHAR_MAP
    return DEFAULT_CHAR_MAP

def get_color_code(r, g, b):
    """
    Placeholder function to get a terminal color code for an RGB value.
    This is highly dependent on the terminal and the desired color depth.
    For simplicity, this example won't implement full color.

    Args:
        r (int): Red component (0-255).
        g (int): Green component (0-255).
        b (int): Blue component (0-255).

    Returns:
        str: ANSI escape code for the color (or an empty string if not supported).
    """
    # Example for 256-color terminals (very simplified)
    # This is not a robust solution and just for demonstration
    if r == g == b: # Grayscale
        gray_index = int((r / 255) * 23) + 232 # 232-255 are grayscale
        # return f"\033[38;5;{gray_index}m"
        pass # For now, we focus on char mapping, not ANSI colors
    
    # For full color, one might use: f"\033[38;2;{r};{g};{b}m"
    # but this is not universally supported.
    return "" # No color by default

if __name__ == '__main__':
    print("Default char map:", get_char_map())
    print("Detailed char map:", get_char_map('detailed'))
    # print("Example color code (placeholder):", get_color_code(128, 128, 128))