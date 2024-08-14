import pygame
import random
import time
from model.bird import Bird
from model.distance import Distance
from model.food import Food
from component.bird.bird_csv_component import BirdCsvComponent

# CSVファイルへの書き込みはするか？
IS_WRITE_CSV = True
# 遺伝的アルゴリズムを利用するか？
IS_USE_GA = True

# 群れの総数
BIRD_NUM = 100

# 餌の総数
FOOD_NUM = 20
# 餌の生まれる総数
BORN_FOOD_NUM = 10
# 餌の下限
MIN_FOOD_NUM = 10
# 餌が生まれる確率
BORN_FOOD_PROB = 50

# -----------------------------------------
# 初期パラメータを指定する場合のパラメータ群
# 遺伝的アルゴリズムを利用する場合(IS_USE_GA = Trueの場合)は以下は利用しません。
# -----------------------------------------
# 動きの速さ
BIRD_SPEED = 20
# 集合ルール
POWER_OF_COHERE = 0.1
RADIUS_OF_COHERE = 200
# 分離ルール
POWER_OF_SEPARATE = 0.1
RADIUS_OF_SEPARATE = 25
# 整列ルール
POWER_OF_ALIGN = 0.1
RADIUS_OF_ALIGN = 100
# 食事ルール
POWER_OF_FOOD = 0.1
RADIUS_OF_FOOD = 300
# 繁殖ルール
RADIUS_OF_BORN = 100
# HP
HEALTH_POINT = 1000
# 寿命
LIFESPAN_POINT = 1000
#
# -----------------------------------------
#

# メイン実行
def main():
	pygame.init()
	# 画面サイズの設定
	width, height = 800, 600
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Boid Simulation")

	# 鳥の総数の初期化
	bird_num = BIRD_NUM

	# 体力が尽きた鳥の総数
	health_point_over_number = 0
	# 寿命が尽きた鳥の総数
	lifespan_over_number = 0
	# 生まれた鳥の総数
	born_number = 0

	# 鳥の生成
	bird_list = []
	last_index = bird_num - 1
	for i in range(bird_num):
		if IS_USE_GA:
			# 初期パラメータをランダムで生成します。
			bird_list.append(Bird(
				bird_id=i,
				width=width,
				height=height
			))
		else:
			# 初期パラメータを指定して生成します。
			bird_list.append(Bird(
				bird_id=i, 
				width=width, 
				height=height,
				speed_param=BIRD_SPEED,
				cohere_param=(POWER_OF_COHERE, RADIUS_OF_COHERE),
				separate_param=(POWER_OF_SEPARATE, RADIUS_OF_SEPARATE),
				align_param=(POWER_OF_ALIGN, RADIUS_OF_ALIGN),
				born_param=(1, RADIUS_OF_BORN),
				food_param=(POWER_OF_FOOD, RADIUS_OF_FOOD),
				health_point=random.randint(500, HEALTH_POINT),
				lifespan=random.randint(200, LIFESPAN_POINT)))
	
	birdCsvComponent = BirdCsvComponent(bird_list=bird_list)
	if IS_WRITE_CSV:
		# CSVファイルの書き込み
		birdCsvComponent.write_csv()
		print("CSVファイルへの書き込みを行います。")

	# 餌の生成
	food_list = []
	for i in range(FOOD_NUM):
		food_list.append(Food(random.uniform(0, width) ,random.uniform(0, height)))

	clock = pygame.time.Clock()

	# 実行
	while True:
		# 死亡予定の鳥のリスト
		over_bird_list = []

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		# ２匹の鳥同士の距離と方向
		distances_list = Distance.distances_of_vectors(bird_list)
		# それぞれの鳥の動き
		for bird in bird_list:
			# 寿命を消費する
			bird.lifespan -= 1
			# 死んだ鳥の中に、対象の鳥がいるかチェックする
			targets_in_over_bird_list = [over_bird for over_bird in over_bird_list if bird.bird_id == over_bird.bird_id]
			if bird.lifespan > 0:
				# 集合
				bird.cohere(bird_list, distances_list)
				# 分離
				bird.separate(bird_list, distances_list)
				# 整列
				bird.align(bird_list, distances_list)
				# 餌の探索
				bird.cohere_food(food_list)
				# 行動
				bird.move()
				# 食事
				bird.eat_food(food_list, bird_list, distances_list)

				# 鳥の体力がなくなると死亡する
				if bird.health_point <= 0 and len(targets_in_over_bird_list) <= 0:
					print("health point over: %s" % bird.bird_id)
					over_bird_list.append(bird)
					health_point_over_number += 1
				else:
					# 鳥の繁殖
					child_bird = bird.born(last_index, bird_list, distances_list, IS_USE_GA)
					if child_bird is not None:
						if IS_WRITE_CSV:
							birdCsvComponent.append_to_csv(child_bird)
						last_index = child_bird.bird_id
						born_number += 1
			else:
				if len(targets_in_over_bird_list) <= 0:
					# 寿命がなくなると死亡する
					print('lifespan over')
					over_bird_list.append(bird)
					lifespan_over_number += 1

		screen.fill((0, 0, 0))

		# 鳥を描画する
		for bird in bird_list:
			bird.display(screen)
		
		# 餌を描画する
		for food in food_list:
			food.display(screen)

		# 死んだ鳥を削除する
		for over_bird in over_bird_list:
			bird_list = [bird for bird in bird_list if not bird.bird_id == over_bird.bird_id]

		# 食べられた餌の数
		eaten_food_num = 0
		# 食べられた餌を削除する
		for food in food_list:
			if food.eaten:
				food_list.remove(food)
				eaten_food_num += 1

		# ランダムで餌を生む
		if len(bird_list) > 0:
			# 餌が食べられ一定確率を超えた場合、または餌が下限を切った場合、餌が生まれる。
			if (eaten_food_num > 0 and random.randint(0, 100) > BORN_FOOD_PROB) or len(food_list) < MIN_FOOD_NUM:
				for i in range(BORN_FOOD_NUM):
					food_list.append(Food(random.uniform(0, width) ,random.uniform(0, height)))
		else:
			print("鳥が絶滅しましたので、プログラムを終了します。")
			pygame.quit()
			break

		# 画面に設定を表示
		display_rendered_text(
			screen, 
			bird_list, 
			food_list,
			lifespan_over_number,
			health_point_over_number,
			born_number)

		pygame.display.flip()
		clock.tick(30)

# 画面に設定を表示する
def display_rendered_text(
		screen, 
		bird_list, 
		food_list, 
		lifespan_over_number,
		health_point_over_number,
		born_number):
	font = pygame.font.Font(None, 15)
	text_lines = [
		"bird number: %s" % len(bird_list),
		"food number: %s" % len(food_list),
		"lifespan over: %s" % lifespan_over_number,
		"health point over: %s" % health_point_over_number,
		"born: %s" % born_number
	]
	rendered_lines = [font.render(line, True, (255, 255, 255)) for line in text_lines]
	text_position = (10, 10)
	for rendered_line in rendered_lines:
		screen.blit(rendered_line, text_position)
		text_position =(text_position[0], text_position[1] + rendered_line.get_height())

if __name__ == '__main__':
	main()