#从迭代器库中调用cycle方法 来控制鸟的动作
#音效和数字图片及背景来源网络 bird图片为自己绘制
from itertools import cycle
import random
import sys
import pygame
from pygame.locals import *
#屏幕长宽 也是背景图片的尺寸
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
# 游戏状态
ANIMATION	= 0
RUNNING		= 1
GAMEOVER	= 2

pygame.init()
pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load("assets/pictures/bird.png")
pygame.display.set_icon(icon)
#设置游戏窗口
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#取背景图,抠掉边缘转换
background_day = pygame.image.load('assets/pictures/background-day.png').convert_alpha()
background_night = pygame.image.load('assets/pictures/background-night.png').convert_alpha()
#加载鸟照片
bird = [pygame.image.load('assets/pictures/bird.png').convert_alpha()]




# 地面图
ground = pygame.image.load('assets/pictures/base.png').convert_alpha()
# 开场动画
message = pygame.image.load('assets/pictures/message.png').convert_alpha()
# 柱子的图片 采用翻转
pipe_down = pygame.image.load('assets/pictures/pipe.png').convert_alpha()
pipe_up = pygame.transform.rotate(pipe_down, 180)
best = pygame.image.load("assets/pictures/best.png").convert_alpha()
# 取声音
sound_wing 	= pygame.mixer.Sound('assets/audio/wing.wav')
sound_hit 	= pygame.mixer.Sound('assets/audio/hit.wav')
sound_point = pygame.mixer.Sound('assets/audio/score.wav')
sound_die 	= pygame.mixer.Sound('assets/audio/die.wav')
# 取game over文本
text_game_over = pygame.image.load('assets/pictures/text_game_over.png').convert_alpha()
# 加载数字图片 从零到九
number = [
			pygame.image.load('assets/pictures/0.png').convert_alpha(),
			pygame.image.load('assets/pictures/1.png').convert_alpha(),
			pygame.image.load('assets/pictures/2.png').convert_alpha(),
			pygame.image.load('assets/pictures/3.png').convert_alpha(),
			pygame.image.load('assets/pictures/4.png').convert_alpha(),
			pygame.image.load('assets/pictures/5.png').convert_alpha(),
			pygame.image.load('assets/pictures/6.png').convert_alpha(),
			pygame.image.load('assets/pictures/7.png').convert_alpha(),
			pygame.image.load('assets/pictures/8.png').convert_alpha(),
			pygame.image.load('assets/pictures/9.png').convert_alpha()
]
#加载restart
restart = pygame.image.load("assets/pictures/restart.png")
def showScore(score):
	# 拆分数字
	scoreDigits = [int(x) for x in list(str(score))]
	# 计算数字总宽度
	totalWidth = 0
	for i in scoreDigits:
		totalWidth += number[i].get_width()
	# 居中摆放
	score_x_position = (SCREEN_WIDTH - totalWidth)//2
	score_y_position = int(0.1 * SCREEN_HEIGHT)
	# 刷新屏幕
	for digit in scoreDigits:
		SCREEN.blit(number[digit], (score_x_position, score_y_position))
		score_x_position += number[digit].get_width()
def showbestScore(score):
	# 拆分数字
	scoreDigits = [int(x) for x in list(str(score))]
	# 计算数字总宽度
	totalWidth = 0
	for i in scoreDigits:
		totalWidth += number[i].get_width()
	bestscore_x_position = (SCREEN_WIDTH - totalWidth) // 2 - 60
	bestscore_y_position = int(0.2 * SCREEN_HEIGHT) - 20
	SCREEN.blit(best,(bestscore_x_position,bestscore_y_position))
	# 居中摆放
	score_x_position = (SCREEN_WIDTH - totalWidth)//2 + 40
	score_y_position = int(0.2 * SCREEN_HEIGHT)
	# 刷新屏幕
	for digit in scoreDigits:
		SCREEN.blit(number[digit], (score_x_position, score_y_position))
		score_x_position += number[digit].get_width()


def main():

	file1 = open("assets/score.txt", 'r')
	max_score = int(file1.readline())

	# 创建帧率实例
	FPS = pygame.time.Clock()
	wing_position = 0
	# 迭代器 小鸟上下抖动 
	bird_shake_iter = cycle([0,1,2,3,4,3,2,1,0,-1,-2,-3,-4,-3,-2,-1])

	
	bird_position = int(0.5 * SCREEN_HEIGHT)		# 小鸟起始高度
	bird_x_position = int(0.2*SCREEN_WIDTH)			# 小鸟水平位置
	ground_position = int(0.8 * SCREEN_HEIGHT- bird[0].get_height()) # 地面高度

	fps_count = 0			# 帧数处理
	key_down = 0			# 按键按下
	gravity = 1 			# 重力大小
	down_velocity = 0 		# 下降速度
	head_direction = 0		# 鸟头方向
	game_state	= ANIMATION 	# 游戏状态
	pipe_move_distance = SCREEN_WIDTH*4//3 + pipe_down.get_width()#管子需要移动的距离
	pipe_gap = 150 			# 管空隙大小
	pipe2_gap = 150 			# 管2空隙大小
	pipe_x_position = SCREEN_WIDTH 	# 柱子水平位置
	pipe_down_position = 0	# 下柱子管口位置
	pipe2_x_position = pipe_move_distance 	# 柱子水平位置
	pipe2_up_position = 0
	pipe2_down_position = 0	# 下柱子管口位置
	score = 0				# 得分
	ground_x_position = 0	# 地面水平位置
	bird_actual_position = 0# 小鸟实际高度


	while RUNNING:

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			# 获取键盘
			if event.type == KEYDOWN and event.key == K_SPACE:
				if game_state == ANIMATION:
					game_state = RUNNING
					down_velocity = 0 	# 下降速度
					head_direction = 0	# 鸟头方向
					fps_count = 0		# 帧数处理
					score = 0			# 得分
					pipe_x_position = SCREEN_WIDTH 	# 柱子水平位置
					pipe2_x_position = pipe_move_distance 	# 柱子水平位置

				if game_state == RUNNING:
					key_down = 6
					sound_wing.play()
				if game_state == GAMEOVER:
					# 小鸟落地后游戏才能重新开始
					if bird_actual_position == ground_position:
						game_state = ANIMATION
						bird_position = int(0.5 * SCREEN_HEIGHT)		# 小鸟起始高度




		# 刷新背景
		if (score // 15)%2 == 0:
			SCREEN.blit(background_day, (0, 0))
		else :
			SCREEN.blit(background_night,(0,0))



		if game_state == ANIMATION:
			fps_count += 1
			SCREEN.blit(message,(SCREEN_WIDTH/2-message.get_width()/2, 0.1* SCREEN_HEIGHT))
			# 草地动起来
			ground_x_position = -1*((fps_count*4)%(ground.get_width()-SCREEN_WIDTH))
			SCREEN.blit(ground, (ground_x_position,int(0.8 * SCREEN_HEIGHT)))
			# 小鸟上下抖动
			bird_shake = next(bird_shake_iter)
			# 小鸟动起来
			bird_actual_position = bird_position+bird_shake
			SCREEN.blit(bird[0], (bird_x_position, bird_actual_position))
		if game_state == RUNNING:
			# 帧数处理
			fps_count += 1
			if True:
				# 柱子动起来
				if pipe_x_position == SCREEN_WIDTH:
					pipe_down_position	= random.randrange(int(0.3 * SCREEN_HEIGHT),int(0.7 * SCREEN_HEIGHT), 10)
					pipe_gap	= random.randrange(100,151, 10)
				pipe_up_position	= pipe_down_position - pipe_gap - pipe_up.get_height()
				pipe_x_position		= SCREEN_WIDTH-(fps_count*4)%pipe_move_distance
				SCREEN.blit(pipe_down, (pipe_x_position,pipe_down_position))
				SCREEN.blit(pipe_up, (pipe_x_position,pipe_up_position))
			if fps_count*4 > pipe_move_distance//2:

				# 第二个柱子动起来 同屏最多出现两个柱子 所有属性第一个柱子相同
				if pipe2_x_position == pipe_move_distance:
					pipe2_down_position	= random.randrange(int(0.3 * SCREEN_HEIGHT),int(0.7 * SCREEN_HEIGHT), 10)
					pipe2_gap	= random.randrange(100,151, 10)
				pipe2_up_position	= pipe2_down_position - pipe2_gap - pipe_up.get_height()
				pipe2_x_position	= pipe_move_distance-pipe_down.get_width()-(fps_count*4-pipe_move_distance//3)%pipe_move_distance
				SCREEN.blit(pipe_down, (pipe2_x_position,pipe2_down_position))
				SCREEN.blit(pipe_up, (pipe2_x_position,pipe2_up_position))

			# 草地动起来
			ground_x_position = -1*((fps_count*4)%(ground.get_width()-SCREEN_WIDTH))
			SCREEN.blit(ground, (ground_x_position,int(0.8 * SCREEN_HEIGHT)))
			# 小鸟上下抖动
			bird_shake = next(bird_shake_iter)
			# 小鸟受重力下落, 空格按下则上升
			if key_down:
				# 刷新的过程需要key_down递减之0 用几帧画面完成 有动态效果
				key_down -= 1
				bird_position -= 6
				bird_position = max(0, bird_position)		# 边界检测
				down_velocity = 0
				head_direction += 6
				head_direction = min(24, head_direction)	# 边界检测
			else:
				down_velocity += gravity
				bird_position += down_velocity
				bird_position = min(bird_position, ground_position)# 边界检测
				head_direction -= 3
				head_direction = max(-42, head_direction)	# 边界检测


			# 调整头的方向
			bird_head = pygame.transform.rotate(bird[wing_position], head_direction)
			# 小鸟动起来
			bird_actual_position = bird_position+bird_shake
			SCREEN.blit(bird_head, (bird_x_position, bird_actual_position))
			# 检测撞地
			if bird_position == ground_position:
				game_state = GAMEOVER
				sound_hit.play()

			# 检测撞柱子
			# 小鸟水平位置在柱子管水平宽度内
			if bird_x_position+bird[0].get_width() > pipe_x_position and \
				bird_x_position < pipe_x_position+pipe_down.get_width():
				# 小鸟高度比下管道低或比上管道高
				if bird_actual_position+bird[0].get_height() > pipe_down_position or \
					bird_actual_position < pipe_down_position - pipe_gap:
					game_state = GAMEOVER
					sound_hit.play()
					sound_die.play()
			# 小鸟水平位置在柱子2管水平宽度内
			if bird_x_position+bird[0].get_width() > pipe2_x_position and \
				bird_x_position < pipe2_x_position+pipe_down.get_width():
				# 小鸟高度比下管道低或比上管道高
				if bird_actual_position+bird[0].get_height() > pipe2_down_position or \
					bird_actual_position < pipe2_down_position - pipe2_gap:
					game_state = GAMEOVER
					sound_hit.play()
					sound_die.play()

			# 小鸟飞过管道后壁刷新得分
			if abs(bird_x_position - (pipe_x_position+pipe_down.get_width() ) ) < 3 or\
				abs(bird_x_position - (pipe2_x_position+pipe_down.get_width() ) ) < 3:
				sound_point.play()
				score += 1
			showScore(score)


		if game_state == GAMEOVER:
			# 改变图片方向 向下移动并播放对应音效
			bird_head = pygame.transform.rotate(bird[wing_position], -90)
			SCREEN.blit(pipe_down, (pipe_x_position,pipe_down_position))
			SCREEN.blit(pipe_up, (pipe_x_position,pipe_up_position))
			SCREEN.blit(pipe_down, (pipe2_x_position,pipe2_down_position))
			SCREEN.blit(pipe_up, (pipe2_x_position,pipe2_up_position))
			SCREEN.blit(ground, (ground_x_position,int(0.8 * SCREEN_HEIGHT)))
			bird_actual_position += 10
			bird_actual_position = min(ground_position, bird_actual_position)
			SCREEN.blit(bird_head, (bird_x_position, bird_actual_position))
			showScore(score)
			if score > max_score:
				file1.close()
				max_score = score
				file2 = open("assets/score.txt",'w')
				file2.write(str(score))
				file2.close()
			showbestScore(max_score)
			restart_x_position = SCREEN_WIDTH/2 - 90
			restart_y_position = SCREEN_HEIGHT/2 - 150
			SCREEN.blit(restart,(restart_x_position,restart_y_position))
			# 小鸟落地后游戏才能重新开始 
			if bird_actual_position == ground_position:
				SCREEN.blit(text_game_over, (SCREEN_WIDTH/2-text_game_over.get_width()/2, 0.4*SCREEN_HEIGHT))

		# 图片刷新
		pygame.display.update()
		# 设置帧率30帧
		FPS.tick(30)

if __name__ == "__main__":
	main()
 
