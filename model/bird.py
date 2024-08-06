import pygame
import random
import numpy as np

RANGE_OF_DIRECTIONS = [0, 360]
BIRD_COLORS = [
	'#FFA5CC',  # pink
	'#80FF25',  # green
	'#A0D4FF',  # skyblue
]
BIRD_SPEED = 20

# 集合ルール
POWER_OF_COHERE = 1000
RADIUS_OF_COHERE = 300
# 分離ルール
POWER_OF_SEPARATE = 1000
RADIUS_OF_SEPARATE = 300
# 整列ルール
POWER_OF_ALIGN = 1000
RADIUS_OF_ALIGN = 300

# 繁殖ルール
RADIUS_OF_BORN = 300

# 食事ルール
POWER_OF_FOOD = 1000
RADIUS_OF_FOOD = 300

# HP
HEALTH_POINT = 500
# 寿命の最大値
LIFESPAN_POINT = 1000

# 突然変異ルール
MUTATION_RATE = 0.01
MUTATION_POWER_RATE = 2
MUTATION_RADIUS_RATE = 2

class Bird:
	def __init__(self,
			bird_id,
			width,
			height,
			parent_bird_ids= None,
			type_id=None,
			speed_param = None,
			cohere_param = None,
			separate_param = None,
			align_param = None,
			food_param = None,
			born_param = None,
			position = None,
			health_point = HEALTH_POINT,
			generation_id = None
	):
		self.bird_id = bird_id
		self.width = width
		self.height = height
		self.parent_bird_ids = parent_bird_ids if parent_bird_ids is not None else []
		self.generation_id = generation_id if generation_id is not None else 1
		# 初期値
		self.speed_param = speed_param if speed_param is not None else random.randint(0, BIRD_SPEED)
		self.cohere_param = cohere_param if cohere_param is not None else (random.uniform(0, POWER_OF_COHERE), random.randint(0, RADIUS_OF_COHERE))
		self.separate_param = separate_param if separate_param is not None else (random.uniform(0, POWER_OF_SEPARATE), random.randint(0, RADIUS_OF_SEPARATE))
		self.align_param = align_param if align_param is not None else (random.uniform(0, POWER_OF_ALIGN), random.randint(0, RADIUS_OF_ALIGN))
		self.born_param = born_param if born_param is not None else (1, random.randint(0,RADIUS_OF_BORN))
		self.food_param = food_param if food_param is not None else (random.uniform(0, POWER_OF_FOOD), random.randint(0, RADIUS_OF_FOOD))
		# ランダムな初期の角度
		self.direction = random.uniform(
			np.radians(RANGE_OF_DIRECTIONS[0]),
			np.radians(RANGE_OF_DIRECTIONS[1])
		)
		# 位置と進行方向ベクトル
		self.position = position if position is not None else np.array([random.uniform(0, width), random.uniform(0, height)])
		self.velocity = np.array([np.cos(self.direction), np.sin(self.direction)])
		# 加速度ベクトル
		self.acceleration = np.array([0, 0])
		self.acceleration_to_cohere = np.array([0, 0])
		self.acceleration_to_separate = np.array([0, 0])
		self.acceleration_to_align = np.array([0, 0])
		self.acceleration_to_food = np.array([0, 0])
		# 近くで餌を見つけた
		self.search_food = False
		# 鳥のHP
		self.health_point = health_point
		self.radius = self.health_point / 100.0
		# 鳥の寿命
		self.lifespan = random.randint(200, LIFESPAN_POINT)
		# 鳥の形状
		self.polygon = np.array([(20, 0), (0, 5), (0, -5)])
		self.type_id = type_id if type_id else self.bird_id % 3
		self.color = BIRD_COLORS[self.type_id]

	def move(self):
		# 体力を消費する
		self.health_point -= self.speed_param

		# 加速度ベクトルを求める。
		self.acceleration = (
			self.acceleration_to_cohere 
			+ self.acceleration_to_separate 
			+ self.acceleration_to_align 
			+ self.acceleration_to_food
			)
		
		# 加速度ベクトルと速度ベクトルの和から進行方向を求める。
		vector = self.velocity + self.acceleration
		if np.linalg.norm(vector) != 0:
			self.velocity = self.speed_param * (vector) / np.linalg.norm(vector)
			self.direction = np.arctan2(self.velocity[1], self.velocity[0])
			self.position += self.velocity
		
		# 鳥が壁にぶつかったら反対側に通り抜ける
		if self.position[0] > self.width or self.position[0] < 0:
			self.position[0] = np.abs(self.position[0] - self.width)
		if self.position[1] > self.height or self.position[1] < 0:
			self.position[1] = np.abs(self.position[1] - self.height)

	# 集合ルール
	def cohere(self, bird_list, distance_l):
		# 力と角度
		power, radius = self.cohere_param

		# 近くの群れを抽出
		near_birds = self.get_near_bird_list(bird_list, distance_l, radius, True)
		if len(near_birds) > 0 :
			# 近くの群れの重心ベクトル
			center_of_near = np.mean(np.array([bird.position for bird in near_birds]))
			# 自分と群れの重心ベクトルの差
			vector = np.subtract(center_of_near, self.position)
			if np.linalg.norm(vector) != 0:
				# 群れの重心ベクトルに向かうように加速度を計算
				self.acceleration_to_cohere = power * (vector/np.square(np.linalg.norm(vector))) # 2次元世界なので、逆1乗則にします
		else:
			self.acceleration_to_cohere = np.array([0,0])
	
	# 分離ルール
	def separate(self, bird_list, distance_l):
		# 力と角度
		power, radius = self.separate_param

		# 近くの群れを抽出
		near_birds = self.get_near_bird_list(bird_list, distance_l, radius, False)
		if len(near_birds) > 0 :
			# 近くの群れの重心ベクトル
			center_of_near = np.mean(np.array([bird.position for bird in near_birds]))
			# 自分と群れの重心ベクトルの差
			vector = np.subtract(center_of_near, self.position)
			if np.linalg.norm(vector) != 0:
				# 群れの重心ベクトルから離れるように加速度を計算
				self.acceleration_to_separate = - power * (vector/np.square(np.linalg.norm(vector))) # 2次元世界なので、逆1乗則にします
		else:
			self.acceleration_to_separate = np.array([0,0])

	# 整列ルール
	def align(self, bird_list, distance_l):
		# 力と角度
		power, radius = self.align_param

		# 近くの群れを抽出
		near_birds = self.get_near_bird_list(bird_list, distance_l, radius, True)
		if len(near_birds) > 0 :
			# 群れの進行方向を求める
			vector = np.sum([bird.velocity for bird in near_birds], axis=0)
			if np.linalg.norm(vector) != 0:
				# 自分が群れの進行方向になるように加速度を計算
				self.acceleration_to_align = power * (vector/np.square(np.linalg.norm(vector))) # 2次元世界なので、逆1乗則にします
		else:
			self.acceleration_to_align = np.array([0,0])
	
	# 鳥の繁殖ルール
	def born(self, last_index, bird_list, distance_l):
		power, radius = self.born_param

		near_birds = self.get_near_bird_list(bird_list, distance_l, radius, True)
		near_birds_without_parent = [bird for bird in near_birds if self.bird_id not in bird.parent_bird_ids]

		child_bird = None
		if self.health_point > 500 and len(near_birds_without_parent) > 0:
			# HPが最も高い鳥を選択する
			pair_bird = max(near_birds_without_parent, key=lambda bird: bird.health_point)
			pair_bird_index = next((i for i in range(len(bird_list)) if bird_list[i].bird_id == pair_bird.bird_id), -1)

			if pair_bird.health_point < 500 or pair_bird_index == -1:
				return None
			
			# 両親のhealth_pointを減らす
			self.health_point -= 200
			pair_bird.health_point -=200

			# 交叉と突然変異による子供のパラメータ生成
			def blend_param(param1, param2):
				return (param1[0] + param2[0]) / 2 , round((param1[1] + param2[1]) / 2)  
			
			def mutate_param(param):
				if random.uniform(0, 1) <= MUTATION_RATE:
					print("occur mutation")
					return (random.uniform(0, param[0] * MUTATION_POWER_RATE), random.randint(0, param[1] * MUTATION_RADIUS_RATE))

				return param
			
			child_speed_param = int((self.speed_param + pair_bird.speed_param) /2)
			child_cohere_param = mutate_param(blend_param(self.cohere_param, pair_bird.cohere_param))
			child_separate_param = mutate_param(blend_param(self.separate_param, pair_bird.separate_param))
			child_align_param = mutate_param(blend_param(self.align_param, pair_bird.align_param))
			child_food_param = mutate_param(blend_param(self.food_param, pair_bird.food_param))
			child_born_param = mutate_param(blend_param(self.born_param, pair_bird.born_param))
			# 子供の初期位置
			child_position = np.array([random.uniform(0, self.width), random.uniform(0, self.height)])
			# 子供の世代数
			child_generation_id = max(self.generation_id, pair_bird.generation_id) + 1

			child_bird = Bird(
				bird_id=last_index + 1,
				width=self.width,
				height=self.height,
				parent_bird_ids=[self.bird_id, pair_bird.bird_id],
				speed_param=child_speed_param,
				cohere_param=child_cohere_param,
				separate_param=child_separate_param,
				align_param=child_align_param,
				born_param=child_born_param,
				food_param=child_food_param,
				position=child_position,
				generation_id=child_generation_id
			)
			bird_list.append(child_bird)
			bird_list[pair_bird_index] = pair_bird
			print("child born")

		self.radius = self.health_point / 100.0
		return child_bird
	
	# 餌を追いかける
	def cohere_food(self, food_list):
		# 力と角度
		power, radius = self.food_param
		# 自分の位置
		x = self.position[0]
		y = self.position[1]

		# 鳥の近くにある餌を取得する。
		near_food = [food for food in food_list
			if np.linalg.norm(np.array([food.x, food.y]) - np.array([x, y])) < radius
				and not food.eaten
		]

		if len(near_food) > 0 :
			self.search_food = True
			# 最も近い餌を選択する
			most_near_food = min(near_food, key=lambda food: np.linalg.norm(np.array([food.x, food.y]) - np.array([x, y])))
			near_food_position = np.array([most_near_food.x, most_near_food.y])

			# 自分と餌の位置の差
			vector = np.subtract(near_food_position, self.position)
			if np.linalg.norm(vector) != 0:
				# 餌に向かうように加速度を計算
				self.acceleration_to_food = power * (vector/np.square(np.linalg.norm(vector))) # 2次元世界なので、逆1乗則にします
		else:
			self.search_food = False
			self.acceleration_to_food = np.array([0,0])
	
	# 食事ルール
	def eat_food(self, food_list, bird_list, distance_l):
		# 餌を食べる
		x = self.position[0]
		y = self.position[1]

		# 鳥の近くにある餌を取得する。
		near_food_index = [
			index for index in range(len(food_list))
			if (np.abs(food_list[index].x - x) < food_list[index].food_radius 
	   			and np.abs(food_list[index].y -y) < food_list[index].food_radius)
				and not food_list[index].eaten
		]

		# 餌がある場合、食べる。
		if len(near_food_index) > 0:
			self.health_point += food_list[near_food_index[0]].food_power
			food_list[near_food_index[0]].eaten = True

	# 近くの鳥の抽出
	def get_near_bird_list(self, bird_list, distance_l, radius, is_only_same_color):
		near_birds = []

		# 同じ色の鳥のみを抽出するかどうか
		if is_only_same_color:
			for d in distance_l:
				if d.bird_id == self.bird_id and 0 < d.distance < radius:
					near_bird = next((bird for bird in bird_list if bird.bird_id == d.near_bird_id), None)
					if self.color == near_bird.color:
						near_birds.append(near_bird)
		else:
			for d in distance_l:
				if d.bird_id == self.bird_id and 0 < d.distance < radius:
					near_bird = next((bird for bird in bird_list if bird.bird_id == d.near_bird_id), None)
					near_birds.append(near_bird)

		return near_birds

	def display(self, screen):		
		# 回転行列を形成
		rotation_matrix = np.array([[np.cos(self.direction), -np.sin(self.direction)],
									[np.sin(self.direction), np.cos(self.direction)]])
		# 頭を進行方向にするように回転させる。
		rotated_polygon = np.dot(self.polygon, rotation_matrix.T) + self.position
		pygame.draw.polygon(screen, self.color, rotated_polygon, 0)