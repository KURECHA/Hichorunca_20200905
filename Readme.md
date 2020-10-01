# アプリ名
　入っちょるんか〜
  
# 機能
買い物の時に持参したマイバックに入るかどうかを判別してくれる。  
マイバックを持ってないときやマイバックに全て入らないとき、L、Sサイズのレジ袋がそれぞれ何枚必要かを教えてくれる。  
  
# 工夫した点
カゴの容量をwebカメラで算出する際にエッジ検出と平滑化フィルタを用いて算出した点  
<img alt="edge_image" src=static/image/frame_canny_in_item.jpg>  
  
UIの配色を山口県の特色を生かしたオレンジと緑に統一した点  

  
# 役割分担
## フロントエンド
takoyaki_hiro：UIのテンプレートとプレゼンテーションを担当<br>
w034ff：Flaskを用いてフロントエンドとバックエンド（python）の連携を担当<br>
## バックエンド
みっちゃ：カゴの検知するためのYOLOの学習、容量検出アルゴリズム<br>
ヨチモンジ：容量検出アルゴリズム、レジ部袋の必要枚数の算出<br>
  
# 使用技術
- html
- javascript
- bootstrap
- Flask
- pytorch (YOLO[^1])
- opencv (canny, median filter)

  


<p> 2020年9月5日にopenhacku vol.2で発表した作品です </p>

[^1]: https://github.com/ultralytics/yolov5.git
