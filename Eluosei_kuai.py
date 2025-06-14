
import pygame
import operator
from fangkuai import *
from random import *
from pygame.locals import *

# 定义游戏相关参数
block_size = 17  # 单个方块的高度和宽度
width = 10       # 游戏板宽度（以方块为单位）
height = 20      # 游戏板高度（以方块为单位）
framerate = 30   # 帧率控制参数，数值越大速度越慢

# 初始化 Pygame 库
pygame.init()

# 创建一个 Clock 对象用于控制帧率
clock = pygame.time.Clock()

# 设置窗口大小为 300x374 像素
screen = pygame.display.set_mode((300, 374))

# 设置定时器事件，频率为 framerate * 10 毫秒
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)

# 设置窗口标题为 "PYTRIS™"
pygame.display.set_caption("PYTRIS™")

# 定义 UI 相关变量和资源的类
class ui_variables:
    # 字体路径定义
    font_path = "./assets/fonts/OpenSans-Light.ttf"     # 常规字体路径
    font_path_b = "./assets/fonts/OpenSans-Bold.ttf"    # 粗体字体路径
    font_path_i = "./assets/fonts/Inconsolata.otf"  # 等宽字体路径

    # 加载不同大小的字体对象
    h1 = pygame.font.Font(font_path, 50)  # 大标题字体
    h2 = pygame.font.Font(font_path, 30)  # 标题字体
    h4 = pygame.font.Font(font_path, 20)  # 小标题字体
    h5 = pygame.font.Font(font_path, 13)  # 正文小字体
    h6 = pygame.font.Font(font_path, 10)  # 很小的字体

    h1_b = pygame.font.Font(font_path_b, 50)  # 粗体大标题字体
    h2_b = pygame.font.Font(font_path_b, 30)  # 粗体标题字体

    h2_i = pygame.font.Font(font_path_i, 30)  # 等宽标题字体
    h5_i = pygame.font.Font(font_path_i, 13)  # 等宽正文小字体

    # 音效加载
    click_sound = pygame.mixer.Sound("assets/sounds/LWZ_ButtonUp.wav")        # 按钮点击音效
    move_sound = pygame.mixer.Sound("assets/sounds/LWZ_PieceMoveLR.wav")      # 方块移动音效
    drop_sound = pygame.mixer.Sound("assets/sounds/LWZ_PieceHardDrop.wav")    # 快速下落音效
    single_sound = pygame.mixer.Sound("assets/sounds/LWZ_SpecialLineClearSingle.wav")  # 单行消除音效
    double_sound = pygame.mixer.Sound("assets/sounds/LWZ_SpecialLineClearDouble.wav")  # 双行消除音效
    triple_sound = pygame.mixer.Sound("assets/sounds/LWZ_SpecialLineClearTriple.wav")  # 三行消除音效
    tetris_sound = pygame.mixer.Sound("assets/sounds/LWZ_SpecialTetris.wav")          # 四行消除（Tetris）音效

    # 背景颜色定义（RGB 格式）
    black = (10, 10, 10)      # 黑色
    white = (255, 255, 255)   # 白色
    grey_1 = (26, 26, 26)     # 深灰色 1
    grey_2 = (35, 35, 35)     # 深灰色 2
    grey_3 = (55, 55, 55)     # 深灰色 3

    # 不同 Tetrimino（俄罗斯方块中的方块形状）的颜色定义
    cyan = (69, 206, 204)     # 青色 - I 形状
    blue = (64, 111, 249)     # 蓝色 - J 形状
    orange = (253, 189, 53)   # 橙色 - L 形状
    yellow = (246, 227, 90)   # 黄色 - O 形状
    green = (98, 190, 68)     # 绿色 - S 形状
    pink = (242, 64, 235)     # 粉红色 - T 形状
    red = (225, 13, 27)       # 红色 - Z 形状

    # 颜色列表，索引对应不同的方块类型或状态
    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]


# 绘制单个方块
def draw_block(x, y, color):
    """
    在指定坐标绘制一个带有边框的方块。

    参数:
    x (int): 方块左上角的x坐标。
    y (int): 方块左上角的y坐标。
    color (tuple): 用RGB元组表示的颜色值。
    """
    # 填充颜色绘制方块
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    # 绘制深灰色边框
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1  # 边框宽度为1像素
    )

# 绘制游戏主界面
def draw_board(next, hold, score, level, goal):
    """
    绘制整个游戏界面，包括侧边栏、下一个方块、持有方块、分数、等级和游戏板。

    参数:
    next (int): 下一个方块类型。
    hold (int): 当前持有的方块类型。
    score (int): 当前得分。
    level (int): 当前关卡。
    goal (int): 升级所需的目标分数。
    """
    # 填充背景色（深灰色）
    screen.fill(ui_variables.grey_1)

    # 绘制右侧侧边栏
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(204, 0, 96, 374)  # 白色区域，用于放置UI元素
    )

    # 绘制下一个方块预览
    grid_n = tetrimino.mino_map[next - 1][0]  # 获取下一个方块的形状数据

    for i in range(4):
        for j in range(4):
            dx = 220 + block_size * j
            dy = 140 + block_size * i
            if grid_n[i][j] != 0:  # 如果该位置有方块
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],  # 根据数字绘制对应颜色
                    Rect(dx, dy, block_size, block_size)
                )

    # 绘制持有方块
    grid_h = tetrimino.mino_map[hold - 1][0]  # 获取当前持有方块的形状数据

    if hold_mino != -1:  # 如果已经持有一个方块
        for i in range(4):
            for j in range(4):
                dx = 220 + block_size * j
                dy = 50 + block_size * i
                if grid_h[i][j] != 0:  # 如果该位置有方块
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],  # 绘制对应颜色
                        Rect(dx, dy, block_size, block_size)
                    )

    # 设置最大分数限制
    if score > 999999:
        score = 999999  # 防止分数过大导致显示问题

    # 渲染文本内容
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)  # "HOLD" 文本
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)  # "NEXT" 文本
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)  # "SCORE" 文本
    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)  # 当前分数
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)  # "LEVEL" 文本
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)  # 当前等级
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)  # "GOAL" 文本
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)  # 目标分数

    # 将文本绘制到屏幕上
    screen.blit(text_hold, (215, 14))       # HOLD 文本位置
    screen.blit(text_next, (215, 104))      # NEXT 文本位置
    screen.blit(text_score, (215, 194))     # SCORE 文本位置
    screen.blit(score_value, (220, 210))    # 分数数值位置
    screen.blit(text_level, (215, 254))     # LEVEL 文本位置
    screen.blit(level_value, (220, 270))    # 等级数值位置
    screen.blit(text_goal, (215, 314))      # GOAL 文本位置
    screen.blit(goal_value, (220, 330))     # 目标数值位置

    # 绘制游戏板上的所有方块
    for x in range(width):          # 遍历游戏板的列
        for y in range(height):     # 遍历游戏板的行
            dx = 17 + block_size * x
            dy = 17 + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])  # 调用draw_block绘制每个方块

# 绘制一个 Tetrimino（俄罗斯方块中的方块）
def draw_mino(x, y, mino, r):
    """
    在指定位置绘制一个 Tetrimino，并在底部绘制“幽灵方块”作为投影。

    参数:
    x (int): 方块左上角的x坐标。
    y (int): 方块左上角的y坐标。
    mino (int): 方块类型（1-7）。
    r (int): 旋转状态（0-3）。
    """
    grid = tetrimino.mino_map[mino - 1][r]  # 获取当前方块在该旋转状态下的形状矩阵

    tx, ty = x, y
    # 找到方块可以下落到的最底部位置
    while not is_bottom(tx, ty, mino, r):
        ty += 1

    # 绘制“幽灵”投影
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[tx + j][ty + i] = 8  # 使用数字8表示幽灵方块

    # 绘制实际的方块
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = grid[i][j]  # 将方块写入游戏板矩阵


# 擦除一个 Tetrimino
def erase_mino(x, y, mino, r):
    """
    从游戏板矩阵中擦除指定的 Tetrimino。

    参数:
    x (int): 方块左上角的x坐标。
    y (int): 方块左上角的y坐标。
    mino (int): 方块类型（1-7）。
    r (int): 旋转状态（0-3）。
    """
    grid = tetrimino.mino_map[mino - 1][r]  # 获取当前方块在该旋转状态下的形状矩阵

    # 擦除“幽灵”投影
    for j in range(21):
        for i in range(10):
            if matrix[i][j] == 8:
                matrix[i][j] = 0  # 清除幽灵方块

    # 擦除实际的方块
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = 0  # 清除方块


# 判断方块是否已到达底部
def is_bottom(x, y, mino, r):
    """
    判断当前方块是否已经到达底部或下方有其他方块。

    参数:
    x (int): 方块左上角的x坐标。
    y (int): 方块左上角的y坐标。
    mino (int): 方块类型（1-7）。
    r (int): 旋转状态（0-3）。

    返回:
    bool: 如果无法继续下落则返回 True，否则返回 False。
    """
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (y + i + 1) > 20:  # 超出游戏板底部边界
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
                    # 下方已经有其他方块
                    return True

    return False


# 判断方块是否已到达左侧边缘
def is_leftedge(x, y, mino, r):
    """
    判断当前方块是否已经到达左侧边缘或左侧有其他方块。

    参数:
    x (int): 方块左上角的x坐标。
    y (int): 方块左上角的y坐标。
    mino (int): 方块类型（1-7）。
    r (int): 旋转状态（0-3）。

    返回:
    bool: 如果无法继续左移则返回 True，否则返回 False。
    """
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j - 1) < 0:  # 超出游戏板左侧边界
                    return True
                elif matrix[x + j - 1][y + i] != 0:  # 左侧已经有其他方块
                    return True

    return False


# 判断方块是否已到达右侧边缘
def is_rightedge(x, y, mino, r):
    """
    判断当前方块是否已经到达右侧边缘或右侧有其他方块。

    参数:
    x (int): 方块左上角的x坐标。
    y (int): 方块左上角的y坐标。
    mino (int): 方块类型（1-7）。
    r (int): 旋转状态（0-3）。

    返回:
    bool: 如果无法继续右移则返回 True，否则返回 False。
    """
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j + 1) > 9:  # 超出游戏板右侧边界
                    return True
                elif matrix[x + j + 1][y + i] != 0:  # 右侧已经有其他方块
                    return True

    return False


# 判断是否可以向右旋转
def is_turnable_r(x, y, mino, r):
    """
    判断当前方块是否可以在当前位置向右旋转。

    参数:
    x (int): 方块左上角的x坐标。
    y (int): 方块左上角的y坐标。
    mino (int): 方块类型（1-7）。
    r (int): 当前旋转状态（0-3）。

    返回:
    bool: 如果可以旋转则返回 True，否则返回 False。
    """
    if r != 3:
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False  # 超出边界
                elif matrix[x + j][y + i] != 0:
                    return False  # 已经有其他方块

    return True


# 判断是否可以向左旋转
def is_turnable_l(x, y, mino, r):
    """
    判断当前方块是否可以在当前位置向左旋转。

    参数:
    x (int): 方块左上角的x坐标。
    y (int): 方块左上角的y坐标。
    mino (int): 方块类型（1-7）。
    r (int): 当前旋转状态（0-3）。

    返回:
    bool: 如果可以旋转则返回 True，否则返回 False。
    """
    if r != 0:
        grid = tetrimino.mino_map[mino - 1][r - 1]
    else:
        grid = tetrimino.mino_map[mino - 1][3]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False  # 超出边界
                elif matrix[x + j][y + i] != 0:
                    return False  # 已经有其他方块

    return True


# 判断新方块是否可以放置
def is_stackable(mino):
    """
    判断新生成的方块是否可以在初始位置放置。

    参数:
    mino (int): 方块类型（1-7）。

    返回:
    bool: 如果可以放置则返回 True，否则返回 False。
    """
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False  # 初始位置已有其他方块

    return True


# 初始化游戏变量
blink = False         # 控制闪烁效果的状态（用于开始/暂停界面）
start = False         # 游戏是否已经开始
pause = False         # 游戏是否处于暂停状态
done = False          # 游戏是否已经结束（窗口关闭）
game_over = False     # 是否游戏失败（方块堆到顶部）

score = 0             # 当前得分
level = 1             # 当前关卡等级
goal = level * 5      # 升级所需消除的行数目标
bottom_count = 0      # 计时器，用于控制方块自动下落
hard_drop = False     # 是否进行了硬降（即快速下落到底部）

dx, dy = 3, 0         # 当前方块在游戏板上的位置（x, y）
rotation = 0           # 当前方块的旋转状态

mino = randint(1, 7)   # 当前掉落的方块类型（1-7表示不同形状）
next_mino = randint(1, 7)  # 下一个将要掉落的方块类型

hold = False           # 是否已持有方块
hold_mino = -1         # 当前持有的方块类型（-1表示未持有）

name_location = 0      # 名字输入时的光标位置
name = [65, 65, 65]    # 默认名字的ASCII码（"AAA"）

# 从 paihangbang.txt 文件读取排行榜数据
with open('paihangbang.txt') as f:
    lines = f.readlines()
# 去除每行末尾的换行符
lines = [line.rstrip('\n') for line in open('paihangbang.txt')]

# 初始化排行榜字典
leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
# 将文件中的排行榜数据读入字典
for i in lines:
    leaders[i.split(' ')[0]] = int(i.split(' ')[1])
# 按分数对排行榜排序（从高到低）
leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

# 初始化游戏板矩阵：宽度 x (高度 + 1)，初始全为 0
# matrix[x][y] 表示游戏板上坐标为 (x, y) 的位置是否有方块
# 0 表示无方块，其他数字代表不同颜色和类型的方块
matrix = [[0 for y in range(height + 1)] for x in range(width)]

# 主循环：游戏核心控制逻辑
while not done:
    # 暂停界面
    if pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True  # 如果收到退出事件，关闭窗口
            elif event.type == USEREVENT:
                # 设置定时器，用于闪烁效果
                pygame.time.set_timer(pygame.USEREVENT, 300)
                # 绘制游戏板
                draw_board(next_mino, hold_mino, score, level, goal)

                # 渲染暂停文本
                pause_text = ui_variables.h2_b.render("PAUSED", 1, ui_variables.white)
                pause_start = ui_variables.h5.render("Press esc to continue", 1, ui_variables.white)

                # 显示暂停文本
                screen.blit(pause_text, (43, 100))
                if blink:
                    screen.blit(pause_start, (40, 160))  # 显示闪烁提示
                    blink = False
                else:
                    blink = True

                pygame.display.update()  # 更新屏幕显示

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)  # 清除当前方块（准备重绘）
                if event.key == K_ESCAPE:
                    pause = False  # 按下 ESC 键取消暂停
                    ui_variables.click_sound.play()  # 播放音效
                    pygame.time.set_timer(pygame.USEREVENT, 1)  # 恢复游戏更新频率

    # 游戏进行界面
    elif start:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True  # 收到退出事件，关闭窗口

            elif event.type == USEREVENT:
                # 控制速度：根据是否按下下方向键调整定时器间隔
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 1)  # 下落加速
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 10)  # 正常速度

                # 绘制当前方块和游戏板
                draw_mino(dx, dy, mino, rotation)
                draw_board(next_mino, hold_mino, score, level, goal)

                # 清除方块（仅在未游戏结束时执行）
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                # 方块自动下落
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1  # 向下移动一行
                else:
                    # 到达底部后创建新方块
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level  # 增加分数

                        draw_mino(dx, dy, mino, rotation)  # 确认绘制到底部
                        draw_board(next_mino, hold_mino, score, level, goal)

                        if is_stackable(next_mino):  # 判断是否可以继续放置新方块
                            mino = next_mino  # 当前方块变为下一个
                            next_mino = randint(1, 7)  # 随机生成下一个方块
                            dx, dy = 3, 0  # 重置位置
                            rotation = 0  # 重置旋转状态
                            hold = False  # 可再次 Hold
                        else:
                            start = False  # 无法继续开始新游戏
                            game_over = True  # 触发游戏结束
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1  # 计数器递增，等待生成新方块

                # 行消除逻辑
                erase_count = 0
                for j in range(21):  # 遍历每一行
                    is_full = True
                    for i in range(10):  # 检查该行是否满格
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:  # 如果该行满格
                        erase_count += 1
                        k = j
                        # 将上方所有行向下移动
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1
                # 根据消除的行数增加得分并播放对应音效
                if erase_count == 1:
                    ui_variables.single_sound.play()
                    score += 50 * level
                elif erase_count == 2:
                    ui_variables.double_sound.play()
                    score += 150 * level
                elif erase_count == 3:
                    ui_variables.triple_sound.play()
                    score += 350 * level
                elif erase_count == 4:
                    ui_variables.tetris_sound.play()
                    score += 1000 * level

                # 升级逻辑
                goal -= erase_count  # 减少剩余目标行数
                if goal < 1 and level < 15:  # 达成目标且等级未满
                    level += 1  # 提高等级
                    goal += level * 5  # 更新目标
                    framerate = int(framerate * 0.8)  # 提高速度

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)  # 按键前先清除当前方块

                # 按下 ESC 键：进入暂停界面
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True

                # 按下空格键：硬降到底部
                elif event.key == K_SPACE:
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1  # 快速下落到最底
                    hard_drop = True  # 设置硬降标志
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

                # 按下 Shift 或 C 键：Hold 功能
                elif event.key == K_RSHIFT or event.key == K_c:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:  # 第一次 Hold
                            hold_mino = mino
                            mino = next_mino
                            next_mino = randint(1, 7)
                        else:  # 已有 Hold，交换
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0  # 重置位置
                        rotation = 0  # 重置旋转
                        hold = True  # 设置已 Hold 状态
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

                # 按上键或 X 键：向右旋转
                elif event.key == K_UP or event.key == K_x:
                    if is_turnable_r(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation += 1  # 旋转角度 +1
                    # Kick 机制：尝试微调位置以完成旋转
                    elif is_turnable_r(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1

                    if rotation == 4:  # 旋转超过最大值则归零
                        rotation = 0

                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

                # 按 Z 或 Ctrl 键：向左旋转
                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation -= 1  # 旋转角度 -1
                    # Kick 机制
                    elif is_turnable_l(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1

                    if rotation == -1:  # 旋转角度归为最大值
                        rotation = 3

                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

                # 按左键：左移
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1  # x 坐标减一实现左移
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

                # 按右键：右移
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1  # x 坐标加一实现右移
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

        pygame.display.update()  # 更新整个游戏画面


        # 游戏结束界面
    elif game_over:
        # 处理事件（如按键、定时器等）
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True  # 如果点击关闭按钮，则退出游戏

            elif event.type == USEREVENT:
                # 设置定时器为300毫秒（用于闪烁效果）
                pygame.time.set_timer(pygame.USEREVENT, 300)

                # 渲染“GAME OVER”文字和提示信息
                over_text_1 = ui_variables.h2_b.render("GAME", 1, ui_variables.white)
                over_text_2 = ui_variables.h2_b.render("OVER", 1, ui_variables.white)
                over_start = ui_variables.h5.render("Press return to continue", 1, ui_variables.white)

                # 绘制游戏板（显示最终状态）
                draw_board(next_mino, hold_mino, score, level, goal)

                # 显示“GAME”和“OVER”文本
                screen.blit(over_text_1, (58, 75))
                screen.blit(over_text_2, (62, 105))

                # 渲染玩家输入的名字（每个字符单独渲染）
                name_1 = ui_variables.h2_i.render(chr(name[0]), 1, ui_variables.white)
                name_2 = ui_variables.h2_i.render(chr(name[1]), 1, ui_variables.white)
                name_3 = ui_variables.h2_i.render(chr(name[2]), 1, ui_variables.white)

                # 下划线表示当前编辑的位置
                underbar_1 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_2 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_3 = ui_variables.h2.render("_", 1, ui_variables.white)

                # 显示名字字符
                screen.blit(name_1, (65, 147))
                screen.blit(name_2, (95, 147))
                screen.blit(name_3, (125, 147))

                # 控制闪烁效果（提示按回车继续）
                if blink:
                    screen.blit(over_start, (32, 195))  # 显示提示信息
                    blink = False
                else:
                    # 根据光标位置显示下划线
                    if name_location == 0:
                        screen.blit(underbar_1, (65, 145))
                    elif name_location == 1:
                        screen.blit(underbar_2, (95, 145))
                    elif name_location == 2:
                        screen.blit(underbar_3, (125, 145))
                    blink = True

                pygame.display.update()  # 更新屏幕显示

            elif event.type == KEYDOWN:
                # 按下回车键：保存分数并重置游戏
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()  # 播放音效

                    # 将玩家名字和得分写入排行榜文件
                    outfile = open('paihangbang.txt', 'a')
                    outfile.write(chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                    outfile.close()

                    # 重置所有游戏变量
                    game_over = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65]  # 默认名字 "AAA"
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]  # 重置游戏板矩阵

                    # 重新加载排行榜数据
                    with open('paihangbang.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('paihangbang.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

                    # 恢复定时器，进入开始界面
                    pygame.time.set_timer(pygame.USEREVENT, 1)

                # 按右箭头：切换名字输入光标位置
                elif event.key == K_RIGHT:
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1)

                # 按左箭头：切换名字输入光标位置
                elif event.key == K_LEFT:
                    if name_location != 0:
                        name_location -= 1
                    else:
                        name_location = 2
                    pygame.time.set_timer(pygame.USEREVENT, 1)

                # 按上箭头：当前光标位置字符递增（A -> B -> ... -> Z）
                elif event.key == K_UP:
                    ui_variables.click_sound.play()
                    if name[name_location] != 90:  # 'Z' 的 ASCII 是 90
                        name[name_location] += 1
                    else:
                        name[name_location] = 65  # 循环回到 'A'
                    pygame.time.set_timer(pygame.USEREVENT, 1)

                # 按下箭头：当前光标位置字符递减（Z -> Y -> ... -> A）
                elif event.key == K_DOWN:
                    ui_variables.click_sound.play()
                    if name[name_location] != 65:  # 'A' 的 ASCII 是 65
                        name[name_location] -= 1
                    else:
                        name[name_location] = 90  # 循环回到 'Z'
                    pygame.time.set_timer(pygame.USEREVENT, 1)


        # 开始界面（游戏未启动时）
    else:
        # 处理事件（如退出、按键等）
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True  # 如果点击关闭按钮，则退出游戏
            elif event.type == KEYDOWN:
                # 按下空格键：开始游戏
                if event.key == K_SPACE:
                    ui_variables.click_sound.play()  # 播放点击音效
                    start = True  # 设置开始标志为 True，进入游戏主界面

        # 填充背景颜色为白色
        screen.fill(ui_variables.white)

        # 绘制灰色区域（下半部分）
        pygame.draw.rect(
            screen,
            ui_variables.grey_1,
            Rect(0, 187, 300, 187)
        )

        # 渲染标题文字
        title = ui_variables.h1.render("Eluosi", 1, ui_variables.grey_1)
        # 渲染“按空格开始”提示文字
        title_start = ui_variables.h5.render("Press space to start", 1, ui_variables.white)
        # 渲染开发者信息
        title_info = ui_variables.h6.render("Modified By LRZ_WZH_ZTX", 1, ui_variables.white)

        # 获取排行榜前三名并渲染文本
        leader_1 = ui_variables.h5_i.render('1st ' + leaders[0][0] + ' ' + str(leaders[0][1]), 1, ui_variables.grey_1)
        leader_2 = ui_variables.h5_i.render('2nd ' + leaders[1][0] + ' ' + str(leaders[1][1]), 1, ui_variables.grey_1)
        leader_3 = ui_variables.h5_i.render('3rd ' + leaders[2][0] + ' ' + str(leaders[2][1]), 1, ui_variables.grey_1)

        # 控制“按空格开始”的闪烁效果
        if blink:
            screen.blit(title_start, (92, 195))  # 显示提示信息
            blink = False
        else:
            blink = True  # 切换闪烁状态

        # 显示标题和开发者信息
        screen.blit(title, (65, 120))
        screen.blit(title_info, (40, 335))

        # 显示排行榜前三名
        screen.blit(leader_1, (10, 10))
        screen.blit(leader_2, (10, 23))
        screen.blit(leader_3, (10, 36))

        # 如果游戏尚未开始，则更新屏幕并限制帧率为 3 FPS
        if not start:
            pygame.display.update()
            clock.tick(3)

# 退出 Pygame
pygame.quit()
