import csv
import os

class CsvUtil:
    """
    CSV読み書きUtil
    """
    @staticmethod
    def read_csv(file_path):
        """CSVファイルを読み込み、リストとして返す"""
        data = []
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        return data

    @staticmethod
    def write_csv(file_path, data):
        """リストのデータをCSVファイルに書き込む"""
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)
        except Exception as e:
            print(f"An error occurred while writing to {file_path}: {e}")

    @staticmethod
    def append_to_csv(file_path, row):
        """CSVファイルの最後に行を追加する"""
        try:
            with open(file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(row)
        except Exception as e:
            print(f"An error occurred while appending to {file_path}: {e}")
