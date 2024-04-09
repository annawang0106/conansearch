import glob
import pandas as pd
import os
import re
import json
import subprocess
import time


output_data = []

conandata_files = glob.glob('./recipes1/**/conandata.yml', recursive=True)

for file_path in conandata_files:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        match = re.search(r'https?://[^\s"]+', content)
        if match:
            url = match.group()
            output_data.append({'path': file_path, 'content': url})
            # 使用 wget 下載 HTTP
            # 提取文件名
            filename_match = re.search(r'/([^/]+)/([^/]+)/([^/]+)', url)
            if filename_match:
                file_name = filename_match.group(3)
                file_name = os.path.join(download_folder, file_name)
                subprocess.run(['wget', url, '-O', file_name])
            if filename_match:
                folderName = filename_match.group(3)
                # 新建資料夾
                folder_path = os.path.join(target_folder, folderName)
                os.makedirs(folder_path, exist_ok=True)
                # 下载文件到新資料夾
                file_name = os.path.join(folder_path, os.path.basename(url))
                subprocess.run(['wget', url, '-O', file_name])

# 設定搜尋路徑
search_path = '/home/kali/Desktop/conansearch_test/downloaded_files_1/'
# 指定解壓縮後資料存放路徑
target_folder = '/home/kali/Desktop/conansearch_test/lib1/'


# 取得所有符合條件的檔案列表
files = glob.glob(os.path.join(search_path, '*'))

# 迭代處理每個檔案
for file_path in files:
    # 檢查擴展名
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.gz':
        # 如果是 .xz,.gz, .或 .tar.xz，執行 tar xvf 指令
        subprocess.run(['tar', 'xvf', file_path, '-C', target_folder])
    elif file_extension.lower() == '.xz':
        subprocess.run(['tar', 'xvf', file_path, '-C', target_folder])
    elif file_extension.lower() == '.tar' or file_extension.lower() == '.bz2' :
        subprocess.run(['tar', 'xvf', file_path, '-C', target_folder])
    elif file_extension.lower() == '.zip':
        # 創建一個新的資料夾，使用原始檔名（不包括擴展名）作為資料夾名
        folder_name = os.path.splitext(os.path.basename(file_path))[0]
        target_folder4 = os.path.join(target_folder, folder_name)
        # 確保資料夾不存在，再建立
        if not os.path.exists(target_folder4):
            os.makedirs(target_folder4)
        # 解壓縮到新的資料夾
        subprocess.run(['unzip', '-d', target_folder4, file_path])
