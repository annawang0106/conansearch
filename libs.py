import glob
import pandas as pd
import os
import re
import json
import subprocess
import time


##############################################
#               wget url
##############################################

# 指定儲存位置
download_folder = './downloaded_files/'

# 創建儲存目錄
os.makedirs(download_folder, exist_ok=True)

output_dict = {}

conandata_files = glob.glob('./recipes/**/conandata.yml', recursive=True)

for file_path in conandata_files:
    # 处理每个找到的 conandata.yml 文件
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines:
            match = re.search(r'url:\s*(.+)', line)
            if match:
                url = match.group(1)
                output_dict[file_path] = url.replace('"', '')
                break  # 找到第一个 URL 后就停止查找

# 使用 wget 下载 URL，儲存到指定目錄
for file_path, url in output_dict.items():
    file_name = os.path.join(download_folder, os.path.basename(url))
    subprocess.run(['wget', url, '-O', file_name])


##############################################
#               解壓縮、解包
##############################################

# 設定搜尋路徑
search_path = '/home/kali/Desktop/conansearch_test/downloaded_files/'
# 指定解壓縮後資料存放路徑
target_folder1 = '/home/kali/Desktop/conansearch_test/lib1/'
target_folder2 = '/home/kali/Desktop/conansearch_test/lib2/'
target_folder3 = '/home/kali/Desktop/conansearch_test/lib3/'
target_folder4 = '/home/kali/Desktop/conansearch_test/lib4/'

# 取得所有符合條件的檔案列表
files = glob.glob(os.path.join(search_path, '*'))

# 迭代處理每個檔案
for file_path in files:
    # 檢查擴展名
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.gz':
        # 如果是 .xz,.gz, .或 .tar.xz，執行 tar xvf 指令
        subprocess.run(['tar', 'xvf', file_path, '-C', target_folder1])
    elif file_extension.lower() == '.xz':
        subprocess.run(['tar', 'xvf', file_path, '-C', target_folder2])
    elif file_extension.lower() == '.tar' or file_extension.lower() == '.bz2' :
        subprocess.run(['tar', 'xvf', file_path, '-C', target_folder3])
    elif file_extension.lower() == '.zip':
        # 如果是 .zip，執行 unzip 指令
        subprocess.run(['unzip', '-d', target_folder4, file_path])






#xlsx file
#df = pd.DataFrame(list(output_dict.items()), columns=['File Path', 'URL'])

#df.to_excel('output.xlsx', index=False)

#Json file
#with open('output.json', 'w', encoding='utf-8') as json_file:
    #json.dump(output_dict, json_file, ensure_ascii=False, indent=4)