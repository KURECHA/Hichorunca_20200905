import sys
import cv2
import numpy as np
import calc_shopping as cs

sys.path.append("home/hirozawa/hacku/ui_django/box_camera/yolov5")

import get_region as gr


def cap_box(bag_size=6):

	cap = cv2.VideoCapture(0)
	#動画のプロパティの設定
	cap.set(3, 800)
	cap.set(4, 600)
	sum_canny = 0
	filter_size = 7
	box_empty_edge_average = 8335246   #エッジ＋メディアン7
 
	time = 0
	box_size = 50

	eco_bag_size = bag_size

	weights_box="./weights/box_weight.pt"
	# weights_item="./weights/item_weight.pt"
	weights_item="./weights/box_weight.pt"
	conf_thre =0.5

	frame_box = []
	egg_flag = False


	while True:
		_, frame = cap.read()

		#YOLOを使ってかごの領域を検出→かごの領域を取得、
		# region = [21,219,494,578]
		region = gr.get_resion_box(frame, weights=weights_box, conf_thre=conf_thre)
		# print(region)
		print ("box_region",region)
		
		if not len(region) == 0 and min(region)>=0:
			frame_box = frame[int(region[1]-40) : int(region[3]), int(region[0]) : int(region[2])]
			
			# frame_box_center = [n//2 for n in frame_box.shape][0:2]
			# print(frame_box.shape)
			# print(frame_box_change.shape)
			
			frame_gray = cv2.cvtColor(frame_box, cv2.COLOR_BGR2GRAY)
			dst = cv2.medianBlur(frame_gray, ksize=filter_size)
			
			frame_canny = cv2.Canny(dst, 50, 150)

			# オープニング・クロージング処理(yochimonji)
			# kernel = np.ones((3, 3), np.uint8)
			# frame_opening = cv2.morphologyEx(frame_canny, cv2.MORPH_OPEN, kernel)


			# カゴに入っている商品の座標を取得して黒で塗りつぶす(元のプログラム)
			# region_item = gr.get_resion_item(frame_box, weights=weights_item, conf_thre=0.7)
			# # region_item = gr.get_resion_item(frame_box, weights=weights_item, conf_thre=0.3)
			# frame_canny_item_disable = []
			# if len(region_item) != 0 :
			# 	for reg in region_item:
			# 		frame_canny_item_disable = cv2.rectangle(frame_canny, (int(reg[0]), int(reg[1]) ), ( int(reg[2]), int(reg[3])),  (0,0,0), -1)

			# カゴに入っている商品の座標を取得して黒で塗りつぶす(yochimonji変更)
			region_item, egg_flag = gr.get_resion_item(frame_box, weights=weights_item, conf_thre=0.7)
			# print("item_region", region_item)
			frame_canny_item_disable = frame_canny.copy()
			if len(region_item) != 0 :
				for reg in region_item:
					frame_canny_item_disable = cv2.rectangle(frame_canny_item_disable, (int(reg[0]), int(reg[1]) ), ( int(reg[2]), int(reg[3])),  (0,0,0), -1)
			
			sum_canny = np.sum(frame_canny_item_disable)

			# k = cv2.waitKey(1000)
			time += 1

			
			if time >= 1:
				break
		else:
			time = 0
	# print("i")

	# print("sum_canny:", sum_canny)

	# cv2.imshow('box', cv2.resize(frame_box, (600, 400)))
	# k = cv2.waitKey(5000)
	# cv2.imshow('change', cv2.resize(frame_box_change, (600, 400)))
	# k = cv2.waitKey(10000)
	# cv2.imshow('box', cv2.resize(frame_box, (600, 400)))
	# k = cv2.waitKey(3000)
	# cv2.imshow('box_edge', cv2.resize(frame_canny, (600, 400)))
	# k = cv2.waitKey(3000)
	# cv2.imshow('', cv2.resize(frame_canny_item_disable, (600, 400)))
	# k = cv2.waitKey(3000)

	# 買った商品の量を算出
	item_size = cs.calc_item_size(frame_canny_item_disable)



	
	# 画像保存(yochimonji)
	images_path = "./images/"
	# cv2.imwrite('frame.jpg', frame)
	# cv2.imwrite('cap_box.jpg', frame_box)
	# cv2.imwrite('frame_canny.jpg', frame_canny)
	# cv2.imwrite('frame_canny_item_disable.jpg', frame_canny_item_disable)
	# cv2.imwrite(images_path + 'frame_gray.jpg', frame_gray)
	# cv2.imwrite(images_path + 'frame_median.jpg', dst)
	# cv2.imwrite(images_path + 'frame_opening.jpg', frame_opening)

	# print("item_size:", item_size)

	ecobag_used, s_bag_num, l_bag_num = cs.calc_bags_num(item_size, eco_bag_size)

	# print("##########s_lbag", s_bag_num, l_bag_num)
	#キャプチャを終了
	cap.release()
	cv2.destroyAllWindows()

	# if item_size <= eco_bag_size:
	# 	print("エコバッグのみで大丈夫です。")
	# else:
	# 	print("レジ袋が必要です。")
	# cv2.imwrite("frame_canny_item_disable.jpg", frame_canny_item_disable)
	# print("エコバッグ容量(L)", eco_bag_size)
	print("商品容量(L)", item_size)
	# print("エコバッグ使用量(%)", ecobag_used)
	print("S, L = ", s_bag_num, l_bag_num)

	return( frame_box, ecobag_used, s_bag_num, l_bag_num, egg_flag)


# cap_box動作確認(yochimonji)
cap_box()