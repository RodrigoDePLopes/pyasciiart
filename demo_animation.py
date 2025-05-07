"""
Main script to demonstrate the ASCII art rendering engine.
"""
import time
import math
from ascii_renderer import AsciiRenderer
from utils import get_char_map

def create_animated_sine_wave_frames(width, height, num_frames):
    """
    Generates frames for a simple sine wave animation with color.
    """
    all_frames_data = []
    for i in range(num_frames):
        # Initialize frame_data with a default tuple (intensity, color_code)
        # Using (0, -1) for black background, no specific color
        frame_data = [[(0, -1) for _ in range(width)] for _ in range(height)]
        for x in range(width):
            sine_y_float = (math.sin(x * 0.2 + i * 0.3) + 1) / 2 * (height - 1)
            sine_y_int = int(round(sine_y_float))
            
            if 0 <= sine_y_int < height:
                intensity = 150 + int(math.sin(x * 0.1 + i * 0.2) * 105)
                intensity = max(0, min(255, intensity))
                # Simple color cycling based on frame number and x position
                # ANSI 256 colors: 16-255 are a 6x6x6 color cube. Let's pick from these.
                # Example: cycle through a range of colors (e.g., 20-50)
                color_code = 16 + ( (i + x//2) % 216 ) # Cycle through the 6x6x6 cube
                frame_data[sine_y_int][x] = (intensity, color_code)
        all_frames_data.append(frame_data)
    return all_frames_data

def create_static_gradient_frame(width, height):
    """
    Generates a single frame with a horizontal gradient and color.
    """
    # Initialize frame_data with a default tuple (intensity, color_code)
    frame_data = [[(0, -1) for _ in range(width)] for _ in range(height)]
    for r in range(height):
        for c in range(width):
            intensity = int((c / (width - 1)) * 255)
            # Assign a color based on intensity or position, e.g., a simple rainbow
            # For simplicity, let's make the gradient go from blue to green to red
            if c < width / 3:
                color_code = 21  # Blue-ish
            elif c < 2 * width / 3:
                color_code = 46  # Green-ish
            else:
                color_code = 196 # Red-ish
            frame_data[r][c] = (intensity, color_code)
    return frame_data

def create_bouncing_chars_animation_frames(width, height, num_frames, num_chars=5):
    """
    Generates frames for an animation of multiple characters bouncing within the console.
    Each character has a unique color.
    """
    import random
    all_frames_data = []

    # Initialize characters: [x, y, dx, dy, char_itself, color_code]
    # For simplicity, intensity is fixed for the character, background is 0.
    chars_data = []
    possible_chars = ['@', '#', '$', '%', '&', '*', 'O', 'X', '!', '?']
    for _ in range(num_chars):
        char_itself = random.choice(possible_chars)
        # Ensure color codes are within the 6x6x6 cube (16-251)
        # and try to make them distinct if possible, though not guaranteed for many chars.
        color = 16 + random.randint(0, 215) 
        chars_data.append([
            random.randint(1, width - 2),  # x position
            random.randint(1, height - 2), # y position
            random.choice([-1, 1]),        # dx
            random.choice([-1, 1]),        # dy
            char_itself,                   # The character to render (not used by current renderer directly, but good for logic)
            color                          # color_code
        ])

    for frame_num in range(num_frames):
        # Initialize frame_data with a default tuple (intensity, color_code)
        # Using (0, -1) for black background, no specific color
        frame_data = [[(0, -1) for _ in range(width)] for _ in range(height)]

        for i in range(num_chars):
            x, y, dx, dy, char_symbol, color_code = chars_data[i]

            # Update position
            x += dx
            y += dy

            # Bounce off walls
            if x <= 0 or x >= width - 1:
                dx = -dx
                x += dx # move back into bounds immediately
            if y <= 0 or y >= height - 1:
                dy = -dy
                y += dy # move back into bounds immediately
            
            # Ensure positions are within bounds after bounce correction
            x = max(0, min(width - 1, x))
            y = max(0, min(height - 1, y))

            # Update character data
            chars_data[i] = [x, y, dx, dy, char_symbol, color_code]

            # Draw character on the frame (intensity 255 for full brightness)
            if 0 <= y < height and 0 <= x < width:
                frame_data[y][x] = (255, color_code) # Full intensity, specific color
        
        all_frames_data.append(frame_data)
    return all_frames_data

if __name__ == '__main__':
    RENDER_WIDTH = 80
    RENDER_HEIGHT = 25

    # Initialize renderer with a detailed character map
    # renderer = AsciiRenderer(width=RENDER_WIDTH, height=RENDER_HEIGHT, char_map=get_char_map('detailed'))
    # Or use the default map from the renderer itself
    renderer = AsciiRenderer(width=RENDER_WIDTH, height=RENDER_HEIGHT, char_map=get_char_map('default'))

    # print("Rendering a static gradient...")
    # static_frame = create_static_gradient_frame(RENDER_WIDTH, RENDER_HEIGHT)
    # renderer.load_frame(static_frame)
    # renderer.render()
    # time.sleep(3) # Display for a few seconds

    # print("Starting sine wave animation...")
    # num_animation_frames = 100
    # animation_frames = create_animated_sine_wave_frames(RENDER_WIDTH, RENDER_HEIGHT, num_animation_frames)

    print("Starting bouncing characters animation...")
    num_bouncing_frames = 300 # More frames for a longer animation
    num_bouncing_chars = 7
    bouncing_frames = create_bouncing_chars_animation_frames(RENDER_WIDTH, RENDER_HEIGHT, num_bouncing_frames, num_bouncing_chars)

    try:
        for frame_data in bouncing_frames:
            renderer.load_frame(frame_data)
            renderer.render()
            time.sleep(0.07) # Adjust for animation speed
    except KeyboardInterrupt:
        print("\nAnimation stopped by user.")
    finally:
        # Clear screen and show cursor again (though renderer.render() already clears)
        # For some terminals, an explicit cursor show might be needed if ^C is messy
        print("\033[?25h") # Show cursor
        print("Animation finished or stopped.")

    # Example of how to use the example from ascii_renderer.py directly if needed
    # print("\nRunning the original fading square test from ascii_renderer.py...")
    # for i in range(10):
    #     frame = [[0 for _ in range(RENDER_WIDTH)] for _ in range(RENDER_HEIGHT)]
    #     intensity = int((i / 9) * 255)
    #     for r in range(5, RENDER_HEIGHT - 5):
    #         for c in range(10, RENDER_WIDTH - 10):
    #             frame[r][c] = intensity
    #     renderer.load_frame(frame)
    #     renderer.render()
    #     time.sleep(0.2)
    # print("Fading square test finished.")