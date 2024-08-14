import matplotlib.pyplot as plt
from component.bird.bird_csv_component import BirdCsvComponent


# CSVのカラムのうち、どのカラムを対象にするか
TARGET_NAME_PAIR = ('generation_id', 'radius_of_align')

# カラム名
COLUMN_DICT = {
	"generation_id": "世代",
	"speed": "速さ",
	"power_of_cohere": "集合する力",
	"radius_of_cohere": "集合範囲",
	"power_of_separate": "分離する力",
	"radius_of_separate": "分離範囲",
	"power_of_align": "整列する力",
	"radius_of_align": "整列範囲",
	"power_of_food": "餌に向かう力",
	"radius_of_food": "餌の探索範囲",
	"radius_of_born": "鳥の交配範囲"
}

#
# 分析用メソッド
# 鳥のパラメータを保存したCSVファイルを読み込み、TARGET_NAME_PAIRで設定したカラムから散布図を作成します。
# 例えば世代数（generation_id）と速さ（speed）を設定すると、
# 世代ごとの速さを表示します。
# 世代ごとに速さが最適化されるため、ある値に速さが収束していくのが散布図から読み取ることができます。
#
def analyze():
	bird_list = []
	birdCsvComponent = BirdCsvComponent(bird_list=bird_list)
	data = birdCsvComponent.read_csv()

	print(data.head())

	# 散布図を作成
	plt.figure(figsize=(10, 6))
	plt.scatter(data[TARGET_NAME_PAIR[0]], data[TARGET_NAME_PAIR[1]], alpha=0.5)
	plt.title("%sごとの%s" % (COLUMN_DICT[TARGET_NAME_PAIR[0]], COLUMN_DICT[TARGET_NAME_PAIR[1]]), fontname="MS Gothic")
	plt.xlabel(COLUMN_DICT[TARGET_NAME_PAIR[0]], fontname="MS Gothic")
	# plt.ylabel(COLUMN_DICT[TARGET_NAME_PAIR[1]], fontname="MS Gothic")
	plt.grid(True)
	plt.show()

if __name__ == '__main__':
	analyze()
