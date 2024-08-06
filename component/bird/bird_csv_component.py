import os
import pandas as pd
from util.csv_util import CsvUtil

CSV_DIRECTORY = ".\\data"
CSV_FILE_NAME = "bird_data.csv"

class BirdCsvComponent:
	"""
	鳥のデータをCSVへ読み書きするコンポーネント
	"""
	def __init__(self, bird_list):
		self.bird_list = bird_list

	def add_bird(self, bird):
		"""鳥をリストに追加する"""
		self.bird_list.append(bird)
	
	def read_csv(self):
		"""鳥のCSVデータを読み込む"""
		csvUtil = CsvUtil()
		data = []

		filePath = CSV_DIRECTORY + "\\" + CSV_FILE_NAME
		return csvUtil.read_csv(filePath)

	def write_csv(self):
		"""鳥のデータをCSVに書き込み"""
		# ディレクトリが存在しない場合は作成
		if not os.path.exists(CSV_DIRECTORY):
			os.makedirs(CSV_DIRECTORY)

		csvUtil = CsvUtil()
		data = []
		for bird in self.bird_list:
			bird_data = self.create_data(bird)
			data.append(bird_data)

		# データをDataFrameに変換
		df = pd.DataFrame(data)

		filePath = CSV_DIRECTORY + "\\" + CSV_FILE_NAME
		csvUtil.write_csv(filePath, df)

	def append_to_csv(self, bird):
		"""新たに生まれた鳥のデータを書き込み"""
		csvUtil = CsvUtil()
		self.add_bird(bird=bird)

		bird_data = self.create_data(bird)

		filePath = CSV_DIRECTORY + "\\" + CSV_FILE_NAME
		csvUtil.append_to_csv(filePath, bird_data)
	
	def create_data(self, bird):
		"""鳥のデータを加工"""
		if bird is not None:
			return {
					'bird_id': bird.bird_id, 
					'generation_id': bird.generation_id, 
					'speed': bird.speed_param, 
					'power_of_cohere': bird.cohere_param[0], 
					'radius_of_cohere': bird.cohere_param[1], 
					'power_of_separate': bird.separate_param[0], 
					'radius_of_separate': bird.separate_param[1], 
					'power_of_align': bird.align_param[0], 
					'radius_of_align': bird.align_param[1], 
					'power_of_food': bird.food_param[0], 
					'radius_of_food': bird.food_param[1], 
					'radius_of_born': bird.born_param[1]
			}

		else:
			return {}