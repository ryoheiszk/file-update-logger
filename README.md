
```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

まずはログフォルダをデスクトップなどに作る。
settings.iniを編集する。

main.py(exe)を常駐させる。


実行ファイルの作り方
```
pip install nuitka
python -m nuitka --onefile --standalone src/main.py
```

settings.iniとexclude_pattern.txtとmain.exeをパックして渡す。
(下記の状態でリリース)

file-upload-logger_vx.x.x
```
main.exe
logtxt2excel.exe
src
  L settings.ini
  L exclude_pattern.txt
```
