import os
import re
import json
import chardet

target_folder = '/home/kali/Desktop/conansearch_test/lib/'

# 检查是否存在 CMakeLists.txt 中的 $，如果存在，则执行 cmake 命令
for root, dirs, files in os.walk(target_folder):
    for file in files:
        file_path = os.path.join(root, file)
        if 'CMakeLists.txt' in file:
            with open(file_path, 'r') as f:
                content = f.read()
                if '$' in content:
                    os.makedirs(os.path.join(root, 'buildCMake'), exist_ok=True)
                    os.chdir(os.path.join(root, 'buildCMake'))
                    os.system('cmake ..')
                    break  # 只需执行一次即可，所以找到后中断循环