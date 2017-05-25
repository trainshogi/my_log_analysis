# my_log_analysis
It's only for submit Fixpoint,Inc as a exam answer.

apache access logをパースするためのプログラム。
言語　　　：python3
開発環境　：Windows10
エディタ　：Atom
ライブラリ：標準ライブラリ(sys, glob, datetime)
　　　　　：apache_log_parser
入出力　　：標準入出力（コマンド）
元データ　：targetフォルダ内に保存の.txt形式ファイルがすべて対象
時間　　　：1900/01/01~2099/12/31対応
最小メモリ：不明。ファイル容量よりメモリが少なくても実行可能。

注意点
・言語：python 3
   python 2系とは異なるため、注意が必要。
   プログラムにはpython3と明示していない。
   python2で実行できるかは未確認です。
・追加ライブラリapache_log_parser
   事前に
    pip install apache-log-parser
   とし、インストールすることが必要となる。
   （参考：Apache logをparseする(2017/05/24閲覧)
   　http://tdoc.info/blog/2013/12/12/apache_log.html）
・日付入力
   期間指定の際に入力が必要となるが、フォーマットは以下の通り。
    aaaa/bb/cc dd:ee:ff
   （aaaa:年, bb:月, cc:日, dd:時, ee:分, ff:ミリ秒）
・実行方法
   main_ver3.pyとtargetが同フォルダ内にある状態で
    python main_ver3.py
   とすればよい。
・バージョン
   main_ver1.pyがメモリ管理を考慮しないプログラム、
   main_ver2.pyは進捗状況を出力しないプログラムです。
   ご参考にお願いします。
