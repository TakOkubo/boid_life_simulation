import pandas as pd

class CsvUtil:
	"""
	CSV読み書きUtil
	"""
	@staticmethod
	def read_csv(file_path):
		"""CSVファイルを読み込み、DataFrameとして返す"""
		try:
			data = pd.read_csv(file_path)
		except FileNotFoundError:
			print(f"File {file_path} not found.")
			data = pd.DataFrame()  # 空のDataFrameを返す
		return data

	@staticmethod
	def write_csv(file_path, data):
		"""DataFrameのデータをCSVファイルに書き込む"""
		try:
			data.to_csv(file_path, index=False)
		except Exception as e:
			print(f"An error occurred while writing to {file_path}: {e}")

	@staticmethod
	def append_to_csv(file_path, row):
		"""CSVファイルの最後に行を追加する"""
		try:
			# 既存のデータを読み込み、新しい行を追加して再度保存
			data = pd.read_csv(file_path)
			new_row = pd.DataFrame([row])
			data = pd.concat([data, new_row], ignore_index=True)
			data.to_csv(file_path, index=False)
		except FileNotFoundError:
			# ファイルが存在しない場合は新しいファイルとして書き込む
			new_row = pd.DataFrame([row])
			new_row.to_csv(file_path, index=False)
		except Exception as e:
			print(f"An error occurred while appending to {file_path}: {e}")
