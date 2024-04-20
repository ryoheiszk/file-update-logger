# 概要

特定のディレクトリ以下、ファイルが作成・編集・削除された履歴をExcelに書き出すシステム。
(雑な実装につき変な制約は多い)

以下について、もしマルウェア認定されてブロックされるなら、潔くPythonで実行するか、ローカルでexeをコピーするか。
今後の安定感など考えたときに、Pythonで実行しておいたほうがいいかも。

# 使い方

1. ログを出力したいフォルダをデスクトップ等に作成し、`src/settings.ini`にパスを記載する。その他項目も調整する。
2. 下記の「実行ファイルの作り方」におけるショートカット作成を自ら行う。
3. `main.exe - ショートカット`を起動して放置する。

- プログラムを閉じたり、PCをシャットダウンしたりしない。
- Windowsの仮想デスクトップ機能を使うと便利。
- クラウドストレージの場合、常にオフラインに同期する設定が必要。

3. ログをチェックしたいときに、`logtxt2excel.exe`を実行する。 
4. 出力されたExcelを使用する。なお、一度出力されたログはテキストファイルから削除されるため、常に最新のログのみExcelに表示されている。


フォルダ構造の例

```
file-update-logger
  L main.exe - ショートカット           <- 作業フォルダ書き換え済み
  L logtxt2excel.exe - ショートカット   <- 作業フォルダ書き換え済み
  L src
    L settings.ini
    L exclude_pattern.txt
  L main.dist
    L main.exe
    L ...
    L ..
    L.
  L logtxt2excel.dist
    L logtxt2excel.exe
    L ...
    L ..
    L.

logs
  L event_log.txt
  L event_log_20240403-115430.xlsx

監視対象フォルダ
  L フォルダA
  L フォルダB
  L 除外フォルダ
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

`--onefile`で作成した実行ファイルは、Windows Defenderにウイルス判定されてしまいやすいらしい。
よって、暫定的に下記の手順で実行するものとする。

1. `main.py`と`logtxt2excel.py`をExeにする。

```
python -m nuitka --standalone src/main.py
python -m nuitka --standalone src/logtxt2excel.py
```

2. 生成された`main.dist`と`logtxt2excel.dist`を、`file-update-logger-v1.x.x`のようなフォルダにコピーする。
3. `src/settings.ini`と`src/exclude_patterns.txt`もコピーする。
4. `main.dist/main.exe`のショートカットを上の階層に配置して、プロパティから作業フォルダを、その階層に設定する。
   これは、雑な実装の兼ね合いで、ルートで実行する必要があるため。
5. `logtxt2excel`の方も同様に行う。

ここで、下記のような構成になっている。

```
file-update-logger-v1.x.x
  L logtxt2excel.dist
      L logtxt2excel.exe
      L ...
      L ..
      L .
  L main.dist
      L main.exe
      L ...
      L ..
      L .
  L src
      L exclude_patterns.txt
      L settings.ini
  L logtxt2excel.exe - ショートカット    <-作業フォルダ書き換え済み
  L main.exe - ショートカット            <-作業フォルダ書き換え済み
```

6. この状態で動作テストする。
7. OKなら、ショートカットは削除して、Zipにして公開する。

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
