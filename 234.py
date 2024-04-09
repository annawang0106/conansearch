import os
import re
import json
import chardet

# 三個目錄的列表
target_folders = ['/home/kali/Desktop/conansearch_test/lib1/', '/home/kali/Desktop/conansearch_test/lib2/', '/home/kali/Desktop/conansearch_test/lib3/', '/home/kali/Desktop/conansearch_test/lib4/']

# 遍歷每個目錄
for i, target_folder in enumerate(target_folders, 1):
    output_dict = {}  # 用於儲存結果的字典

    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)

            if 'configure' in file or 'Makefile' in file:
                file_content = []  # 用 list 儲存第三方 lib
                with open(file_path, 'rb') as f:  # 以二進位模式打開文件
                    result = chardet.detect(f.read())  # 檢測字符編碼
                encoding = result['encoding']
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    lines = f.readlines()
                    for line in lines:  # 讀取檔案內容
                        match_soname = re.search(r'-soname', line)
                        match_gcc_shared = re.search(r'gcc -shared', line)
                        match_ar_c = re.search(r'ar c', line)

                        if match_soname:
                            value_soname = line.strip()
                            if value_soname not in file_content:
                                file_content.append(value_soname)
                        elif match_gcc_shared:
                            value_gcc = line.strip()
                            if value_gcc not in file_content:
                                file_content.append(value_gcc)
                        elif match_ar_c:
                            value_ar = line.strip()
                            if value_ar not in file_content:
                                file_content.append(value_ar)

                # 將結果添加到 output_dict 中，使用檔案路徑作為 key
                if file_content:
                    output_dict[file_path] = file_content

    # 將每個目錄的結果寫入對應的 JSON 檔案
    json_filename = f'lib_{i}.json'
    with open(json_filename, 'w', encoding='utf-8') as file:
        json.dump(output_dict, file, ensure_ascii=False, indent=4)
    print(f"結果已保存到 {json_filename}")