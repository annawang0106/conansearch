import os
import re
import json
import subprocess
import glob

# 壓縮檔下載位置
download_folder = './downloaded_files_1/'

# 指定解壓縮後資料存放路徑
target_folder = '/home/kali/Desktop/conansearch_test/lib1/'

# 設定搜尋路徑
search_path = download_folder

# 創建儲存目錄
os.makedirs(download_folder, exist_ok=True)

output_data = []

conandata_files = glob.glob('./recipes/**/conandata.yml', recursive=True)

for file_path in conandata_files:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        match = re.search(r'https?://[^\s"]+', content)
        if match:
            url = match.group()
            output_data.append({'path': file_path, 'content': url})
            # 使用 wget 下載 HTTP
            filename_match = re.search(r'/([^/]+)/([^/]+)/([^/]+)', url)
            if filename_match:
                folderName = filename_match.group(3)
                if folderName not in ['downloads', 'repository', 'sdk', 'closer\.lua', 'gnome', 'medias', 'software', 'dist1', 'polyclipping', '1\.1', 'sources', 'naif', 'Code', 'dr_libs', 'ftp', 'frameworks', 'releases', 'cci-sources-backup', 'gnu', 'OpenGL-Registry', 'gcrypt', 'gsoap2', 'gz-math', 'gz-cmake', 'ign-tools', 'gz-utils', 'individual', 'linux', 'Little-CMS', 'archive', 'bastard', 'l', 'Attic', 'opencore-amr', 'developer', 'scm', 'mad', '1\.0', 'Downloads', 'perfmon2']:
                    # 新建資料夾
                    folder_path = os.path.join(target_folder, folderName)
                    os.makedirs(folder_path, exist_ok=True)
                    # 下载文件到新資料夾
                    file_name = os.path.join(folder_path, os.path.basename(url))
                    subprocess.run(['wget', url, '-O', file_name])
                else:
                    # 直接下载文件到目标文件夹
                    file_name = os.path.join(target_folder, os.path.basename(url))
                    subprocess.run(['wget', url, '-O', file_name])


for root, dirs, files in os.walk(target_folder):
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

 