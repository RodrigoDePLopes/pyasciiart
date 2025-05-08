"""
Flappy Bird游戏实现，使用ASCII渲染器显示。
使用pgzero风格的API。
"""
import time
import random
import ascii_renderer as ar

# --- 游戏配置 ---
WIDTH = 100
HEIGHT = 25
TITLE = "Flappy Bird ASCII"
FPS = 30  # 渲染帧率，可以设置得更高以获得更流畅的画面
GAME_SPEED = 10  # 游戏逻辑更新速度，保持不变以维持原有游戏速度

# --- 游戏状态 ---
bird_y = HEIGHT // 2
bird_x = 10
gravity = 0.4
velocity = 0
pipes = []
score = 0
game_over = False
last_pipe_time = None

# --- 按键处理 ---
def on_key_press(key):
    global velocity, game_over
    if game_over:
        return
    if key == b' ':
        velocity = -1.5

# --- 游戏逻辑更新函数 ---
def update(dt):
    global bird_y, velocity, game_over, last_pipe_time, score, pipes
    if game_over:
        return
    # 更新小鸟位置
    velocity += gravity
    bird_y += velocity
    # 边界检查
    if bird_y < 0:
        bird_y = 0
        velocity = 0
    elif bird_y >= HEIGHT:
        game_over = True
        return
    # 生成新管道
    if last_pipe_time is None:
        last_pipe_time = time.time()
    current_time = time.time()
    min_spawn_interval = 1.5
    base_spawn_rate = 0.15 - score * 0.001
    pipe_spawn_rate = max(0.05, base_spawn_rate)
    if current_time - last_pipe_time > min_spawn_interval and random.random() < pipe_spawn_rate:
        min_gap = max(5, 15 - score // 5)
        max_gap = min(HEIGHT - 5, HEIGHT - 15 + score // 5)
        if min_gap >= max_gap:
            min_gap = 5
            max_gap = HEIGHT - 5
        gap_pos = random.randint(min_gap, max_gap)
        gap_size = max(15 - score // 3, 5)
        pipes.append({
            'x': WIDTH - 1,
            'gap_pos': gap_pos,
            'gap_size': gap_size
        })
        last_pipe_time = current_time
    # 更新管道位置
    for pipe in pipes:
        pipe['x'] -= 1
    # 移除屏幕外的管道
    pipes = [pipe for pipe in pipes if pipe['x'] > -5]
    # 碰撞检测
    for pipe in pipes:
        if pipe['x'] <= bird_x < pipe['x'] + 3:
            if not (pipe['gap_pos'] <= bird_y < pipe['gap_pos'] + pipe['gap_size']):
                game_over = True
                return
        if pipe['x'] == bird_x - 1:
            score += 1

# --- 绘制函数 ---
def draw(screen):
    frame = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for x in range(WIDTH):
        frame[0][x] = (100, 130)
        frame[HEIGHT-1][x] = (100, 130)
    if 0 <= bird_y < HEIGHT:
        frame[int(bird_y)][bird_x] = (255, 3)
    for pipe in pipes:
        x = pipe['x']
        gap_pos = pipe['gap_pos']
        gap_size = pipe['gap_size']
        for y in range(HEIGHT):
            if y < gap_pos or y >= gap_pos + gap_size:
                if 0 <= x < WIDTH:
                    frame[y][x] = (200, 2)
                    if x + 1 < WIDTH:
                        frame[y][x+1] = (200, 2)
                    if x + 2 < WIDTH:
                        frame[y][x+2] = (200, 2)
    screen.load_frame(frame)
    if game_over:
        game_over_text = "GAME OVER"
        screen.draw_text(WIDTH // 2 - len(game_over_text) // 2, HEIGHT // 2, game_over_text, color_code=1)
        score_text = f"Final Score: {score}"
        screen.draw_text(WIDTH // 2 - len(score_text) // 2, HEIGHT // 2 + 1, score_text, color_code=3)
    else:
        score_text = f"Score: {score}"
        screen.draw_text(1, 1, score_text, color_code=7)

# --- 启动游戏 ---
if __name__ == "__main__":
    ar.go(width=WIDTH, height=HEIGHT, title=TITLE, target_fps=FPS, game_speed=GAME_SPEED)