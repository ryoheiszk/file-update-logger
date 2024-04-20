# 概要

特定のディレクトリ以下、ファイルが作成・編集・削除された履歴をExcelに書き出すシステム。
(雑な実装につき変な制約は多い)

# 使い方

1. ログを出力したいフォルダをデスクトップ等に作成し、`src/settings.ini`にパスを記載する。その他項目も調整する。
2.  `main.exe`を起動して放置する。

- プログラムを閉じたり、PCをシャットダウンしたりしない。
- Windowsの仮想デスクトップ機能を使うと便利。
- クラウドストレージの場合、常にオフラインに同期する設定が必要。

3. ログをチェックしたいときに、`logtxt2excel.exe`を実行する。 
4. 出力されたExcelを使用する。なお、一度出力されたログはテキストファイルから削除されるため、常に最新のログのみExcelに表示されている。


フォルダ構造の例

```
file-update-logger
  L main.exe
  Llogtxt2excel.exe
  L src
    L settings.ini
    L exclude_pattern.txt

logs
  L log.txt
  L log_20240403-115430.xlsx

監視対象フォルダ
  L フォルダA
  L フォルダB
```

# 環境構築

```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

まずはログフォルダをデスクトップなどに作る。
settings.iniを編集する。

# 実行方法

必ず、ルートで実行する。src内に入るなどしない。(→実装に由来)

監視開始

```
python src/main.py
```

未保存のログをExcelに書き出し

```
python src/logtxt2excel.py
```

# 実行ファイルの作り方

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

#  `src/exclude_patterns.txt`の編集方法

正規表現でマッチする文字列が含まれる場合、監視から除外される。

特定のファイルを除外したい場合 (以下は既定値)

```
~\$
\.tmp$
desktop.ini
```

特定のフォルダ以下を除外したい場合

```
フォルダA\\フォルダB
```
