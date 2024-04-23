downloadlib.py   

功能:

第一段程式(23~44):

(21~26)從recipes資料夾下抓取lib的yml

(40、43)用wget指令將壓縮檔下載至lib資料夾

(31~44)同時壓縮檔上一層包資料夾名稱取至於url第四個/後的名稱(因為部分壓縮檔為亂數名稱，且url第四個/後的名稱通常為lib名稱，但還是有例外，如果是例外的就已原本壓縮檔的名稱命名。)

第二段程式(47~69):解壓縮lib資料夾底下的壓縮檔。

舊檔:libFinal.py


buildCMake.py

功能:執行cmake ..

檢查CMakeLists.txt當中如果有$(變數名稱)，則執行cmake ..，將執行結果檔案放置新建的buildCMake資料夾中，其中會產生link.txt


extract.py

功能:
找尋link.txt 中的 ar qc lib_____.a/.so 及 –soname,lib_____.a/.so的line，提取______關鍵字。

找尋CMakeLists.txt中的add_library(_____________)的line，濾掉______中包含INTERFACE、ALIAS、$的關鍵字，提取()中第一個空白前的關鍵字。
舊檔:searchMFinal.py


次要

CMakeSearch.py
查找那些lib包含CMakeLists.txt

configureSearch.py
查找那些lib包含configure

makefileSearch.py
查找那些lib包含makefileSearch
