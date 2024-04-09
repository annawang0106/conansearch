import os

for root, dirs, files in os.walk("/home/kali/Desktop/conansearch_test/lib1/"):
    for f in files:
        print(os.path.join(root, f))


import os
import subprocess

for root, dirs, files in os.walk("/home/kali/Desktop/conansearch_test/lib1/"):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        folder_path = os.path.dirname(file_path)  # 取得檔案的資料夾路徑
        # 檢查擴展名
        _, file_extension = os.path.splitext(file_name)
        
        if file_extension.lower() == '.gz':
            # 如果是 .gz, .xz, .tar.xz，執行 tar xvf 指令
            subprocess.run(['tar', 'xvf', file_path, '-C', folder_path])
        elif file_extension.lower() == '.xz':
            subprocess.run(['tar', 'xvf', file_path, '-C', folder_path])
        elif file_extension.lower() == '.tar' or file_extension.lower() == '.bz2':
            subprocess.run(['tar', 'xvf', file_path, '-C', folder_path])
        elif file_extension.lower() == '.zip':
            # 創建一個新的資料夾，使用原始檔名（不包括擴展名）作為資料夾名
            folder_name = os.path.splitext(file_name)[0]
            target_folder4 = os.path.join(folder_path, folder_name)
            # 確保資料夾不存在，再建立
            if not os.path.exists(target_folder4):
                os.makedirs(target_folder4)
            # 解壓縮到新的資料夾
            subprocess.run(['unzip', '-d', target_folder4, file_path])
