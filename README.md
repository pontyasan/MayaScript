StrechIKCreater
====

## Overview
StrechIK(精度向上バージョン)の自動生成スクリプトです。 
@9bozさんがクリカンで発表していた内容のものになります。

## 使い方
①取得ボタンからSplineIKカーブを選択。  
②伸ばす方向を指定。scaleXYZから選択してください  
③実行  
  
※コントローラーは作成されません。  
  
## 起動コマンド
    import sys
    sys.path.insert(0,r'お好みのパス')
    import CreateStrechIK
    reload(CreateStrechIK)
