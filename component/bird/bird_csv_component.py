import os
from util.csv_util import CsvUtil

CSV_DIRECTORY = ".\\data"
CSV_FILE_NAME = "bird_data.csv"

class BirdCsvComponent:
	"""
	鳥のデータをCSVへ読み書きするコンポーネント
	"""
	def __init__(self, bird_list):
		self.header = ["bird_id", "generation_id", "speed", "power_of_cohere", "radius_of_cohere", "power_of_separate", "radius_of_separate", "power_of_align", "radius_of_align", "power_of_food", "radius_of_food", "radius_of_born"]
		self.bird_list = bird_list

	def add_bird(self, bird):
		"""鳥をリストに追加する"""
		self.bird_list.append(bird)

	def write_csv(self):
		"""鳥のデータをCSVに書き込み"""
		# ディレクトリが存在しない場合は作成
		if not os.path.exists(CSV_DIRECTORY):
			os.makedirs(CSV_DIRECTORY)

		csvUtil = CsvUtil()
		data = []

		data.append(self.header)
		for bird in self.bird_list:
			bird_data = self.create_data(bird)
			data.append(bird_data)
		
		filePath = CSV_DIRECTORY + "\\" + CSV_FILE_NAME
		csvUtil.write_csv(filePath, data)

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
			return [
					bird.bird_id, 
					bird.generation_id, 
					bird.speed_param, 
					bird.cohere_param[0], 
					bird.cohere_param[1], 
					bird.separate_param[0], 
					bird.separate_param[1], 
					bird.align_param[0], 
					bird.align_param[1], 
					bird.food_param[0], 
					bird.food_param[1], 
					bird.born_param[1]
				]
		else:
			return []