import numpy as np

class Distance:
	def __init__(self, bird_id, near_bird_id, distance):
		self.bird_id = bird_id
		self.near_bird_id = near_bird_id
		self.distance = distance

	# ベクトル間の距離を格納するdistanceモデルを生成
	def distances_of_vectors(bird_list):
		distance_list = []

		for bird_i in bird_list:
			distance_list.append(Distance(bird_i.bird_id, bird_i.bird_id, 0))
			for bird_j in bird_list:
				if bird_i.bird_id < bird_j.bird_id:
					# ふたつのベクトルの距離を求める。
					distance = np.linalg.norm(np.subtract(bird_i.position, bird_j.position))
					# Distanceモデルに求めた距離を格納する。
					distance_list.append(Distance(bird_i.bird_id, bird_j.bird_id, distance))
					distance_list.append(Distance(bird_j.bird_id, bird_i.bird_id, distance))
		return distance_list