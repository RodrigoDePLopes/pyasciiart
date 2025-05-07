"""
Flappy Bird游戏实现，使用ASCII渲染器显示。
"""
import time
import random
import msvcrt
from ascii_renderer import AsciiRenderer

class FlappyBird:
    def __init__(self, width=100, height=25):
        self.renderer = AsciiRenderer(width, height)
        self.width = width
        self.height = height
        self.bird_y = height // 2
        self.bird_x = 10
        self.gravity = 0.4
        self.velocity = 0
        self.pipes = []
        self.score = 0
        self.game_over = False
        
    def handle_input(self):
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b' ':
                self.velocity = -1.5
    
    def update(self):
        # 更新小鸟位置
        self.velocity += self.gravity
        self.bird_y += self.velocity
        
        # 边界检查
        if self.bird_y < 0:
            self.bird_y = 0
            self.velocity = 0
        elif self.bird_y >= self.height:
            self.game_over = True
        
        # 生成新管道
        if not hasattr(self, 'last_pipe_time'):
            self.last_pipe_time = time.time()
            
        current_time = time.time()
        min_spawn_interval = 1.5  # 最小生成间隔
        
        # 初始生成率较高，随分数增加而降低
        base_spawn_rate = 0.15 - self.score * 0.001
        pipe_spawn_rate = max(0.05, base_spawn_rate)
        
        # 检查冷却时间和随机生成
        if current_time - self.last_pipe_time > min_spawn_interval and random.random() < pipe_spawn_rate:
            # 管道间隙位置基于分数变化，但保持在一定范围内
            # 确保随机数范围始终有效
            min_gap = max(5, 15 - self.score // 5)
            max_gap = min(self.height - 5, self.height - 15 + self.score // 5)
            if min_gap >= max_gap:
                min_gap = 5
                max_gap = self.height - 5
            gap_pos = random.randint(min_gap, max_gap)
            # 间隙大小随分数递减，但最小保持为5
            gap_size = max(15 - self.score // 3, 5)
            self.pipes.append({
                'x': self.width - 1,
                'gap_pos': gap_pos,
                'gap_size': gap_size
            })
            self.last_pipe_time = current_time
        
        # 更新管道位置
        for pipe in self.pipes:
            pipe['x'] -= 1
        
        # 移除屏幕外的管道
        self.pipes = [pipe for pipe in self.pipes if pipe['x'] > -5]
        
        # 碰撞检测
        for pipe in self.pipes:
            if pipe['x'] <= self.bird_x < pipe['x'] + 3:
                if not (pipe['gap_pos'] <= self.bird_y < pipe['gap_pos'] + pipe['gap_size']):
                    self.game_over = True
            
            # 计分
            if pipe['x'] == self.bird_x - 1:
                self.score += 1
    
    def render(self):
        # 创建空白画布
        frame = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        # 绘制天花板和地板
        for x in range(self.width):
            frame[0][x] = (100, 130)  # 天花板亮度(棕色)
            frame[self.height-1][x] = (100, 130)  # 地板亮度(棕色)
        
        # 绘制小鸟
        if 0 <= self.bird_y < self.height:
            frame[int(self.bird_y)][self.bird_x] = (255, 3)  # 使用最大亮度(黄色)
        
        # 绘制管道
        for pipe in self.pipes:
            x = pipe['x']
            gap_pos = pipe['gap_pos']
            gap_size = pipe['gap_size']
            
            for y in range(self.height):
                if y < gap_pos or y >= gap_pos + gap_size:
                    if 0 <= x < self.width:
                        frame[y][x] = (200, 2)  # 管道亮度(绿色)
                        if x + 1 < self.width:
                            frame[y][x+1] = (200, 2)
                        if x + 2 < self.width:
                            frame[y][x+2] = (200, 2)
        
        # 加载到渲染器
        self.renderer.load_frame(frame)
        self.renderer.render()
        
        # 显示分数
        print(f"Score: {self.score}")
        
    def run(self):
        while not self.game_over:
            self.handle_input()
            self.update()
            self.render()
            time.sleep(0.1)
        
        print(f"Game Over! Final Score: {self.score}")

if __name__ == "__main__":
    game = FlappyBird()
    game.run()