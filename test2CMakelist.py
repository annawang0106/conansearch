import os
import re
import json
import chardet
import pandas as pd

# 目標資料夾路徑
target_folder = '/home/kali/Desktop/conansearch_test/lib/'

# 創建一個空字典來儲存結果
output_list = []

# 遍历目標資料夾中的每個檔案
for root, dirs, files in os.walk(target_folder):
    for file in files:
        file_path = os.path.join(root, file)

        if 'link.txt' in file or 'CMakeLists.txt' in file: #or 'Makefile' in file or 'CMakeLists.txt' in file : #or 'configure' in file:
            file_content = []  # 儲存第三方 lib 的列表
            file_content_CM = []
            file_content_filename = []
            with open(file_path, 'rb') as f:  # 以二進位模式打開文件
                result = chardet.detect(f.read())  # 檢測字符編碼
            encoding = result['encoding']
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                lines = f.readlines()
                for line in lines:  # 讀取檔案內容
                    match_so = re.search(r'lib(\w+)\.so', line)
                    match_a = re.search(r'lib(\w+)\.a', line)
                    if match_so:
                        if line.strip() not in file_content:
                            file_content.append(line.strip())

                        value_so = match_so.group(0)
                        if value_so not in file_content_filename:
                            file_content_filename.append(value_so)

                    if match_a:
                        if line.strip() not in file_content:
                            file_content.append(line.strip())

                        value_a = match_a.group(0)
                        if value_a not in file_content_filename:
                            file_content_filename.append(value_a)

                    if 'CMakeLists.txt' in file:
                        match_add_library = re.search(r'add_library\s*\(([^)]+)\)', line)
                        if match_add_library:
                            if line.strip() not in file_content_CM:
                                file_content_CM.append(line.strip())
                            
                            if 'INTERFACE' not in line and 'ALIAS' not in line and '$' not in line:
                                library_name = match_add_library.group(1).split()[0]
                                file_content_filename.append(library_name.strip())

            # 获取目标文件夹下一层的路径
            for dir in dirs:
                subfolder_path = os.path.join(root, dir)
                rel_path = os.path.relpath(subfolder_path, target_folder)
                arr = rel_path.split('/')
                lib_name = arr[0]
                arr1 = lib_name.split('-')
                lib_name1 = arr1[0]
                output_list.append({"lib": lib_name1})

            # 如果有找到任何內容，將結果添加到 output_dict 中，使用檔案路徑作為 key


# 將結果保存為 xlsx 檔案
df = pd.DataFrame(output_list)

excel_filename = 'lib_output2.xlsx'
df.to_excel(excel_filename, index=False)

print(f"結果已保存到 {excel_filename}")
