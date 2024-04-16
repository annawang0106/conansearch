import os
import re
import json
import chardet
import pandas as pd

# 目標資料夾路徑
target_folder = '/home/uadmin/conansearch_test/lib1'

# 創建一個空字典來儲存結果
output_list = []

# 遍历目標資料夾中的每個檔案
for root, dirs, files in os.walk(target_folder):
    if 'tests' in dirs:
        dirs.remove('tests')
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
                    match_ar_a = re.search(r'ar qc .*/lib(\w+)\.a', line)
                    match_ar_so = re.search(r'ar qc .*/lib(\w+)\.so', line)
                    match_soname_a = re.search(r'-soname,lib(\w+)\.a', line)
                    match_soname_so = re.search(r'-soname,lib(\w+)\.so', line)
                    #match_so = re.search(r'ar lib(\w+)\.so', line)
                    #match_a = re.search(r'lib(\w+)\.a', line)
                    if match_ar_a:
                        if line.strip() not in file_content:
                            file_content.append(line.strip())

                        value_ar_a = match_ar_a.group(1)
                        if value_ar_a not in file_content_filename:
                            file_content_filename.append(value_ar_a)

                    if match_ar_so:
                        if line.strip() not in file_content:
                            file_content.append(line.strip())

                        value_ar_so = match_ar_so.group(1)
                        if value_ar_so not in file_content_filename:
                            file_content_filename.append(value_ar_so)

                    if match_soname_a:
                        if line.strip() not in file_content:
                            file_content.append(line.strip())

                        value_soname_a = match_soname_a.group(1)
                        if value_soname_a not in file_content_filename:
                            file_content_filename.append(value_soname_a)

                    if match_soname_so:
                        if line.strip() not in file_content:
                            file_content.append(line.strip())

                        value_soname_so = match_soname_so.group(1)
                        if value_soname_so not in file_content_filename:
                            file_content_filename.append(value_soname_so)

                    if 'CMakeLists.txt' in file:
                        match_add_library = re.search(r'add_library\s*\(([^)]+)\)', line)
                        if match_add_library:
                            if line.strip() not in file_content_CM:
                                file_content_CM.append(line.strip())
                            
                            if 'INTERFACE' not in line and 'ALIAS' not in line and '$' not in line:
                                library_name = match_add_library.group(1).split()[0]
                                file_content_filename.append(library_name.strip())

            # 获取目标文件夹下一层的所有文件夹名称
            subdirs = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]

            # 如果有找到任何內容，將結果添加到 output_dict 中，使用檔案路徑作為 key
            if file_content or file_content_CM or file_content_filename:
                rel_path = os.path.relpath(root, target_folder)
                
                arr = rel_path.split('/')
                lib_name = arr[0]
                arr1 = lib_name.split('-')
                lib_name1 = arr1[0]
                pair = {"lib": lib_name1, "filename": file_content_filename}
                
                # 檢查這對（lib，libname）是否已存在於output_list中
                if pair not in output_list:
                    output_list.append(pair)

# 將結果保存為 JSON 檔案
json_filename = 'output.json'
with open(json_filename, 'w', encoding='utf-8') as file:
    json.dump(output_list, file, ensure_ascii=False, indent=4)

print(f"結果已保存到 {json_filename}")
