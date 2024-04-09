import json

# 載入 lib.json 中的資料
with open('lib2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 使用字典來建立映射關係，以 libname 為 key，lib 為 value
mapping = {}
for item in data:
    lib = item['lib']
    libnames = item['libname']
    for libname in libnames:
        mapping[libname] = lib

# 定義函式來查找對應的 lib
def find_lib(linname):
    if linname in mapping:
        return mapping[linname]
    else:
        return "找不到相對應的 lib"

# 測試程式
linname = input("輸入 linname：")
result = find_lib(linname)
print("對應的 lib 為：", result)
