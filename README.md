# pymolplugin
Directory of pymol plugins

PyMOL 2.3.0の中の `/Applications/PyMOL.app/Contents/share/pymol/data/startup/` に入ってるプラグイン集です。オープンソース版PyMOLはこれらのプラグインがデフォルトで入っていないので、APBS GUIを始めとしたこれらのプラグインを使うためには、手動でインストール操作をしてあげる必要があります。

```
# オープンソース版PyMOLとapbs, pdb2pqrプログラムのインストール
brew tap brewsci/bio
brew install pymol apbspdb2pqr
# PyMOL 2.3.0の場合は /usr/local/Cellar/pymol/2.3.0/libexec/lib/python3.7/site-packages/pmg_tk/startup のディレクトリに、このリポジトリのpymolpluginのすべてファイルをコピーしてあげれば良い
# pymolpluginディレクトリをダウンロード
cd ~
git clone https://github.com/YoshitakaMo/pymolplugin.git
# ファイルをオープンソース版PyMOLのプラグインディレクトリに追加
cp -rp ~/pymolplugin/* /usr/local/Cellar/pymol/2.3.0/libexec/lib/python3.7/site-packages/pmg_tk/startup
# ここでPyMOLを立ち上げてみて、プラグインがインストールされていればOK
# インストールできたら~/pymolpluginディレクトリは削除してOK
# rm -rf ~/pymolplugin
```