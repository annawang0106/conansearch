import os
import json
import pandas as pd

target_folders = ['/home/kali/Desktop/conansearch_test/lib/']
# 遍歷每個目錄
for i, target_folder in enumerate(target_folders):
    output_dict = {}  # 用於儲存結果的字典

    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)

            # 精確比對文件名是否為 'Makefile'
            if file == 'Makefile'or 'Makefile.in':
                output_dict[file_path] = 'File Found'
            

    # 將每個目錄的結果轉換為 DataFrame
    df = pd.DataFrame(list(output_dict.items()), columns=['Path', 'Status'])

    # 將 DataFrame 寫入 Excel 檔案
    excel_filename = f'MakefileFind.xlsx'
    df.to_excel(excel_filename, index=False, encoding='utf-8')
    
    print(f"結果已保存到 {excel_filename}")

import os
import json
import pandas as pd

target_folder = '/home/kali/Desktop/conansearch_test/lib/'

output_dict = {}  # 用於儲存結果的字典

# 遍歷目標目錄下的每個子目錄
for subdir in os.listdir(target_folder):
    subdir_path = os.path.join(target_folder, subdir)

    # 檢查是否為目錄
    if os.path.isdir(subdir_path):
        # 使用 os.walk 遍歷目錄中的文件
        for root, dirs, files in os.walk(subdir_path):
            for file in files:
                file_path = os.path.join(root, file)

                # 精確比對文件名是否為 'Makefile'
                if file == 'Makefile':
                    output_dict[subdir_path] = 'File Found'
                    break  # 找到第一個 Makefile 就停止查找

# 將結果轉換為 DataFrame
df = pd.DataFrame(list(output_dict.items()), columns=['Path', 'Status'])

# 將 DataFrame 寫入 Excel 檔案
excel_filename = f'MakefileFind.xlsx'
df.to_excel(excel_filename, index=False, encoding='utf-8')

print(f"結果已保存到 {excel_filename}")
