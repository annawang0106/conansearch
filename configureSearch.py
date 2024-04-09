import os
import json
import pandas as pd

# 設定目標目錄列表
target_folders = ['/home/kali/Desktop/conansearch_test/lib/']

# 遍歷每個目錄
for i, target_folder in enumerate(target_folders, 1):
    output_dict = {}  # 用於儲存結果的字典

    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)

            # 精確比對文件名是否為 'configure'
            if file == 'configure':
                output_dict[file_path] = 'File Found'

    # 將每個目錄的結果轉換為 DataFrame
    df = pd.DataFrame(list(output_dict.items()), columns=['Path', 'Status'])

    # 將 DataFrame 寫入 Excel 檔案
    excel_filename = f'configureFind_{i}.xlsx'
    df.to_excel(excel_filename, index=False, encoding='utf-8')
    
    print(f"結果已保存到 {excel_filename}")
