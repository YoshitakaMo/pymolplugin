# pymolplugin
Directory of pymol plugins

PyMOL 2.5.0の中の `/Applications/PyMOL.app/Contents/share/pymol/data/startup/` に入ってるプラグイン集です。オープンソース版PyMOLはこれらのプラグインがデフォルトで入っていないので、APBS GUIを始めとしたこれらのプラグインを使うためには、手動でインストール操作をしてあげる必要があります。


```bash
# オープンソース版PyMOLとapbs, pdb2pqrプログラムのインストール
brew tap brewsci/bio
brew install pymol apbs
# pymolpluginディレクトリをダウンロード
cd ~
git clone https://github.com/YoshitakaMo/pymolplugin.git
# ファイルをオープンソース版PyMOLのプラグインディレクトリに追加
cp -rp ~/pymolplugin/* ${HOMEBREW_PREFIX}/opt/pymol/libexec/lib/python3.9/site-packages/pmg_tk/startup
# ここでPyMOLを立ち上げてみて、プラグインがインストールされていればOK
# インストールできたら~/pymolpluginディレクトリは削除してOK
# rm -rf ~/pymolplugin
```