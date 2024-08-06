import pygame
import random
from model.bird import Bird
from model.distance import Distance
from model.food import Food
from component.bird.bird_csv_component import BirdCsvComponent

# 群れの総数
BIRD_NUM = 100

# 餌の総数
FOOD_NUM = 10
# 餌の生まれる総数
BORN_FOOD_NUM = 5

# メイン実行
def main():
	pygame.init()
	# 画面サイズの設定
	width, height = 800, 600
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Boid Simulation")

	# 鳥の総数の初期化
	bird_num = BIRD_NUM

	# 鳥の生成
	bird_list = []
	last_index = bird_num - 1
	for i in range(bird_num):
		bird_list.append(Bird(i, width, height))
	
	birdCsvComponent = BirdCsvComponent(bird_list=bird_list)
	# CSVファイルの書き込み
	birdCsvComponent.write_csv()
	print("CSVファイルに書き込みました")

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
			if bird.lifespan > 0:
				# 集合
				bird.cohere(bird_list, distances_list)
				# 分離
				bird.separate(bird_list, distances_list)
				# 整列
				bird.align(bird_list, distances_list)
				# 餌を追いかける
				bird.cohere_food(food_list)
				# 行動
				bird.move()
				# 食事
				bird.eat_food(food_list, bird_list, distances_list)

				# 鳥の体力がなくなると死亡する
				if bird.health_point <= 0:
					print('health point over')
					over_bird_list.append(bird)
				else:
					# 鳥の繁殖
					child_bird = bird.born(last_index, bird_list, distances_list)
					if child_bird is not None:
						birdCsvComponent.append_to_csv(child_bird)
						last_index = child_bird.bird_id
			else:
				# 寿命がなくなると死亡する
				print('lifespan over')
				over_bird_list.append(bird)

		screen.fill((0, 0, 0))

		# 鳥を描画する
		for bird in bird_list:
			bird.display(screen)
		
		# 餌を描画する
		for food in food_list:
			food.display(screen)

		# 死んだ鳥を削除する
		for bird in over_bird_list:
			bird_list.remove(bird)
		
		# 食べられた餌の数
		eaten_food_num = 0
		# 食べられた餌を削除する
		for food in food_list:
			if food.eaten:
				food_list.remove(food)
				eaten_food_num += 1

		# ランダムで餌を生む
		if len(bird_list) > 0:
			# 餌が食べられて、一定確率で餌が生まれる。
			if eaten_food_num > 0 and random.randint(0, 100) > 50: 
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
			food_list)

		pygame.display.flip()
		clock.tick(30)

# 画面に設定を表示する
def display_rendered_text(screen, bird_list, food_list):
	font = pygame.font.Font(None, 15)
	text_lines = [
		"bird number: %s" % len(bird_list),
		"food number: %s" % len(food_list),
		# "cohesion power: %s"  % POWER_OF_COHERE,
		# "cohesion radius: %s" % RADIUS_OF_COHERE,
		# "separate power: %s" % POWER_OF_SEPARATE,
		# "separate radius: %s" % RADIUS_OF_SEPARATE,
		# "align power: %s" % POWER_OF_ALIGN,
		# "align radius: %s" % RADIUS_OF_ALIGN,
	]
	rendered_lines = [font.render(line, True, (255, 255, 255)) for line in text_lines]
	text_position = (10, 10)
	for rendered_line in rendered_lines:
		screen.blit(rendered_line, text_position)
		text_position =(text_position[0], text_position[1] + rendered_line.get_height())

if __name__ == '__main__':
	main()