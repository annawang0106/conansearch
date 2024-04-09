import glob
import pandas as pd
import os
import re
import json
import subprocess
import time


output_data = []

conandata_files = glob.glob('./recipes/**/conandata.yml', recursive=True)

for file_path in conandata_files:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines:
            match = re.search(r'https?', line)
            if match:
                url = match.group(1)
                output_data.append({'path': file_path, 'url': url})
                break

# 將結果轉換為 DataFrame
df = pd.DataFrame(output_data)

# 將 DataFrame 寫入 Excel 檔案
excel_filename = 'libHttps.xlsx'
df.to_excel(excel_filename, index=False)

print(f"結果已保存到 {excel_filename}")
