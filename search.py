import os
import re
import json
import chardet

# 三個目錄的列表
target_folders = '/home/kali/Desktop/conansearch_test/lib/'

# 遍歷每個目錄
for i, target_folder in enumerate(target_folders, 1):
    output_dict = {}  # 用於儲存結果的字典

    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)

            if 'configure' in file: #or 'Makefile' in file:
                file_content = []  # 用 list 儲存第三方 lib
                with open(file_path, 'rb') as f:  # 以二進位模式打開文件
                    result = chardet.detect(f.read())  # 檢測字符編碼
                encoding = result['encoding']
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    lines = f.readlines()
                    for line in lines:  # 讀取檔案內容
                        match_so = re.search(r'lib(\w+)\.so', line)
                        match_a = re.search(r'lib(\w+)\.a', line)
                        #match_soname = re.search(r'soname', line)
                        #match_gcc_shared = re.search(r'gcc*-shared', line)
                        #match_ar_c = re.search(r'ar c', line)
                        if match_so:
                            value_so = match_so.group(0)
                            if value_so not in file_content:
                                file_content.append(value_so)
                        elif match_a not in file_content:
                            value_a = match_a.group(0)
                            if value_a not in file_content:
                                file_content.append(value_a)
                        #elif match_soname not in file_content:
                            #file_content.append(line.strip())
                        #elif match_gcc_shared:
                            #file_content.append(line.strip())
                        #elif match_gcc_shared or match_ar_c:
                            #file_content.append(line.strip())
                        #if match_so or match_a or match_soname:
                            #file_content.append(line.strip())

                # 將結果添加到 output_dict 中，使用檔案路徑作為 key
                if file_content:
                    output_dict[file_path] = file_content

    # 將每個目錄的結果寫入對應的JSON檔案
    json_filename = f'lib.json'
    with open(json_filename, 'w', encoding='utf-8') as file:
        json.dump(output_dict, file, ensure_ascii=False, indent=4)
    print(f"結果已保存到 {json_filename}")
