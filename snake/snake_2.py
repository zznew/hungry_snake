import random, pygame, sys
from pygame.locals import *


snake_speed = 25                    # 贪吃蛇的爬行速度
Window_Width = 800                  # 窗口宽度
Window_Height = 600                 # 窗口高度
Cell_Size = 20                      # 格子大小
assert Window_Width % Cell_Size == 0, "Window width must be a multiple of cell size."
assert Window_Height % Cell_Size == 0, "Window height must be a multiple of cell size."
Cell_W = int(Window_Width / Cell_Size)      # 计算横排格子数
Cell_H = int(Window_Height / Cell_Size)     # 计算竖排格子数

# 定义各种颜色
#         R    G    B
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (0, 155, 0)
dark_gray = (40, 40, 40)
yellow = (255, 255, 0)
dark_red = (150, 0, 0)
blue = (0, 0, 255)
dark_blue = (0, 0, 150)
BGCOLOR = black

# 定义各种“动作”
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
HEAD = 0


def main():
    # 游戏初始化
    global SNAKE_SPEED_CLOCK, DISPLAYSURF, BASICFONT,sound
    pygame.init()
    # 插入背景音乐
    pygame.mixer.init()
    sound = pygame.mixer.music.load('River_Flows_in_you.mp3')
    pygame.mixer.music.play()

    SNAKE_SPEED_CLOCK = pygame.time.Clock()                                   # 创立时钟对象
    DISPLAYSURF = pygame.display.set_mode((Window_Width, Window_Height))    # 创建游戏窗口
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)                    # 设置显示字体和字号
    pygame.display.set_caption('Wormy')                                     # 游戏名称

    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # 随机确定游戏对象开始时的位置
    startx = random.randint(5, Cell_W - 6)
    starty = random.randint(5, Cell_H - 6)

    # 贪吃蛇在游戏开始时有三节，使用元素为字典的列表表示
    wormCoords = [{'x': startx, 'y': starty},{'x': startx - 1, 'y': starty},{'x': startx - 2, 'y': starty}]

    # 游戏对象默认向右运动
    direction = RIGHT

    # 随机确定“苹果”的位置
    apple = getRandomLocation()

    # 定义游戏对象（贪吃蛇）的操作方式
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # 处理游戏结束的两种情况
        # 出界
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == Cell_W or wormCoords[HEAD]['y'] == -1 or \
                wormCoords[HEAD]['y'] == Cell_H:
            pygame.mixer.music.stop()
            return

        # 形成闭环
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                pygame.mixer.music.stop()
                return

        # 如果苹果被吃掉，重新确定苹果的位置
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation()
        else:
            del wormCoords[-1]     # 删去贪吃蛇的“尾巴”
        # 模拟贪吃蛇的运动
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'],'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'],'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)

        # 将游戏背景填充为黑色
        DISPLAYSURF.fill(BGCOLOR)

        drawWorm(wormCoords)                    # 绘制贪吃蛇
        drawApple(apple)                        # 绘制“苹果”
        drawScore(10*(len(wormCoords) - 3))     # 计算并显示得分
        pygame.display.update()                 # 刷新游戏界面
        SNAKE_SPEED_CLOCK.tick(snake_speed)

# 显示提示信息，提示玩家
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play(ESC for escape).', True, white)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (Window_Width - 360, Window_Height - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

# 检测用户是否按键
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:             # 如果检测到大于0次的退出时间，退出游戏
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        pygame.mixer.music.load("River_Flows_in_you.mp3")
        pygame.mixer.music.play()
        return None
    if keyUpEvents[0].key == K_ESCAPE:              # 如果按下”ESC“键，退出游戏
        terminate()
    return keyUpEvents[0].key


def pause():
    if(event.key == K_SPACE):
        os.pause()


# 退出游戏
def terminate():
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


# 获取随机位置（尽量避免位置过于偏僻）
def getRandomLocation():
    return {'x': random.randint(5, Cell_W - 5), 'y': random.randint(5, Cell_H - 5)}


# 展示游戏结束的画面
def showGameOverScreen():
    Game_Over_Font=pygame.font.Font("freesansbold.ttf", 100)
    Game_Surface = Game_Over_Font.render("Game", True, white)
    Over_Surface = Game_Over_Font.render("Over", True, white)
    Game_Rect = Game_Surface.get_rect()
    Over_Rect = Game_Surface.get_rect()
    Game_Rect.midtop = (225, 200)
    Over_Rect.midtop = (575, 200)
    DISPLAYSURF.blit(Game_Surface, Game_Rect)
    DISPLAYSURF.blit(Over_Surface, Over_Rect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)               # 设置暂停时间，避免玩家误操作
    checkForKeyPress()                  # 检测玩家是否按键
    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

# 在游戏屏幕上显示得分
def drawScore(score):
    scoreSurf = BASICFONT.render("Score: {}".format(score), True, white)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (Window_Width - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

# 绘制贪吃蛇
def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * Cell_Size
        y = coord['y'] * Cell_Size
        wormSegmentRect = pygame.Rect(x, y, Cell_Size, Cell_Size)
        pygame.draw.rect(DISPLAYSURF, dark_green, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, Cell_Size - 8, Cell_Size - 8)
        pygame.draw.rect(DISPLAYSURF, green, wormInnerSegmentRect)

# 绘制“苹果”
def drawApple(coord):
    x = coord['x'] * Cell_Size
    y = coord['y'] * Cell_Size
    appleRect = pygame.Rect(x, y, Cell_Size, Cell_Size)
    pygame.draw.rect(DISPLAYSURF, red, appleRect)


if __name__=="__main__":
    try:
        main()
    except SystemExit:
        pass
