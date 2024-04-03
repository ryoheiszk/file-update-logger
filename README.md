# 使い方

1. ログを出力したいフォルダをデスクトップ等に作成し、`src/settings.ini`にパスを記載する。その他項目も調整する。
2.  `main.exe`を起動して放置する。

- プログラムを閉じたり、PCをシャットダウンしたりしない。
- Windowsの仮想デスクトップ機能を使うと便利。

3. ログをチェックしたいときに、`logtxt2excel.exe`を実行する。 
4. 出力されたExcelを使用する。なお、一度出力されたログはテキストファイルから削除されるため、常に最新のログのみExcelに表示されている。

# 環境構築

```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

まずはログフォルダをデスクトップなどに作る。
settings.iniを編集する。

実行ファイルの作り方
```
pip install nuitka
python -m nuitka --onefile --standalone src/main.py
python -m nuitka --onefile --standalone src/logtxt2excel.py
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
