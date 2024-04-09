import os
import re
import json
import chardet
import pandas as pd


# 目標資料夾路徑
target_folder = '/home/kali/Desktop/conansearch_test/lib/'

# 創建一個空字典來儲存結果
output_list = []

# 遍歷目標資料夾中的每個檔案
for root, dirs, files in os.walk(target_folder):
    for file in files:
        file_path = os.path.join(root, file)

        if 'CMakeLists.txt' in file: #or 'configure' in file:
            file_content = []  # 儲存第三方 lib 的列表
            with open(file_path, 'rb') as f:  # 以二進位模式打開文件
                result = chardet.detect(f.read())  # 檢測字符編碼
            encoding = result['encoding']
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                lines = f.readlines()
                for line in lines:  # 讀取檔案內容
                    if 'CMakeLists.txt' in file:
                        match_add_library = re.search(r'add_library\s*\(([^)]+)\)', line)
                        
                        if match_add_library:
                            #file_content.append(line.strip())
                            if 'INTERFACE' not in line and 'ALIAS' not in line and '$' not in line:
                                library_name = match_add_library.group(1).split()[0]
                                file_content.append(library_name.strip())


            # 如果有找到任何內容，將結果添加到 output_dict 中，使用檔案路徑作為 key
            if file_content:
                rel_path = os.path.relpath(root, target_folder)
                arr = rel_path.split('/')
                lib_name = arr[0]
                arr1 = lib_name.split('-')
                lib_name1 = arr1[0]
                pair = {"lib": lib_name1, "filenam": file_content}
                # 檢查這對（lib，libname）是否已存在於output_list中
                if pair not in output_list:
                    output_list.append(pair)

# 將結果保存為 JSON 檔案
#json_filename = 'var.json'
#with open(json_filename, 'w', encoding='utf-8') as file:
    #json.dump(output_list, file, ensure_ascii=False, indent=4)

#print(f"結果已保存到 {json_filename}")

# 將結果保存為 xlsx 檔案
df = pd.DataFrame(output_list)

excel_filename = 'lib_outputCM.xlsx'
df.to_excel(excel_filename, index=False)

print(f"結果已保存到 {excel_filename}")

