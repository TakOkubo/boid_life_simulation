import matplotlib.pyplot as plt
from component.bird.bird_csv_component import BirdCsvComponent

"""
CSVのカラムのうち、どのカラムを対象にするか
・bird_id 
・generation_id 
・speed 
・power_of_cohere 
・radius_of_cohere 
・power_of_separate 
・radius_of_separate 
・power_of_align 
・radius_of_align 
・power_of_food 
・radius_of_food 
・radius_of_born
"""
TARGET_NAME_PAIR = ('generation_id', 'speed')

def analyze():
	bird_list = []
	birdCsvComponent = BirdCsvComponent(bird_list=bird_list)
	data = birdCsvComponent.read_csv()

	print(data.head())

	# 散布図を作成
	plt.figure(figsize=(10, 6))
	plt.scatter(data[TARGET_NAME_PAIR[0]], data[TARGET_NAME_PAIR[1]], alpha=0.5)
	plt.xlabel(TARGET_NAME_PAIR[0])
	plt.ylabel(TARGET_NAME_PAIR[1])
	plt.grid(True)
	plt.show()

if __name__ == '__main__':
	analyze()
