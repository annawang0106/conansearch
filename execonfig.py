import os
import subprocess

# 定義 configure 文件名
configure_file_name = 'configure'

# 定義所有的 target_folder
target_folders = [
    '/home/kali/Desktop/conansearch_test/lib1/',
    '/home/kali/Desktop/conansearch_test/lib2/',
    '/home/kali/Desktop/conansearch_test/lib3/',
    '/home/kali/Desktop/conansearch_test/lib4/'
]

# 遞迴處理每個 target_folder
for target_folder in target_folders:
    # 遍历目录及其子目录
    for root, dirs, files in os.walk(target_folder):
        # 構建 configure 文件的完整路徑
        configure_path = os.path.join(root, configure_file_name)

        # 檢查 configure 文件是否存在
        if os.path.exists(configure_path):
            print(f"Found {configure_file_name} in {root}. Executing ./configure...")

            # 確保 configure 文件有執行權限
            os.chmod(configure_path, 0o755)

            # 切換到目錄，執行 configure 指令
            try:
                os.chdir(root)
                subprocess.run(['./configure'], check=True)
                print(f"./configure executed successfully in {root}.")
            except subprocess.CalledProcessError as e:
                print(f"Error executing ./configure in {root}: {e}")
