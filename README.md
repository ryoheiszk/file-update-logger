
```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

settings.iniを編集する。
main.pyを常駐させる。


実行ファイルの作り方
```
pip install nuitka
python -m nuitka --onefile --standalone src/main.py
```

settings.iniとexclude_pattern.txtとmain.exeをパックして渡す。

```
main.exe
src
  L settings.ini
  L exclude_pattern.txt
```
