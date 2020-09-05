import numpy as np
import cv2


# def calc_bags_num:商品とエコバックの容量から袋の枚数を計算する関数
# input item_size, eco_bag_size, s_bag_size, l_bag_size:商品、エコバッグ、S、Lサイズのレジ袋の容量(L:liter)
# output エコバッグの使用済み容量、S,Lの枚数のリスト
# eco_bag_size_used:エコバッグの使用済み容量(%)
# 商品の容量が0以下になるまで商品容量からエコバッグ及びレジ袋の容量を
# 減算する。エコバッグ→Lのレジ袋→Sのレジ袋の順で使用するものとする。
def calc_bags_num(item_size, eco_bag_size=0, s_bag_size=7, l_bag_size=17):

    eco_bag_size_used = 0
    s_bag_num = 0
    l_bag_num = 0

    if eco_bag_size > 0:
        eco_bag_size_used = (int)(item_size / eco_bag_size * 100)
        item_size -= eco_bag_size

    while item_size > 0:
        if item_size > s_bag_size:
            item_size -= l_bag_size
            l_bag_num += 1
        else:
            item_size -= s_bag_size
            s_bag_num += 1

    return (eco_bag_size_used, s_bag_num, l_bag_num)


# def calc_item_size:エッジ画像から商品のサイズ(L:liter)を計算する関数
# input frame_canny:エッジ画像(ndarray)
# input frame_canny_sum_empty:カゴが空の時のエッジの合計
# input box_size:カゴのサイズ(L:liter)
# output item_size:商品のサイズ(L:liter)
# 検出したエッジ(dot)がエッジ画像の中心から遠いほどL2ノルムをエッジに
# 乗算することで商品容量をより正確に検出する。
# 中心からの距離の時、frame_canny_sum_empty=3000000
def calc_item_size(frame_canny, frame_canny_sum_empty=7500000, box_size=50):

    frame_canny_sum = 0

    # 中心からの距離ver.
    frame_box_center = [n//2 for n in frame_canny.shape][0:2]
    max_length = np.linalg.norm(frame_box_center)
    # for i, frame_line in enumerate(frame_canny):
    #     for j, dot in enumerate(frame_line):
    #         frame_canny_sum += dot * np.linalg.norm(np.array((i,j))-frame_box_center) / max_length

    # 底面と側面をそれぞれ考慮するver. 2種類
    ratio = 0.2
    hight = frame_canny.shape[0]
    length = frame_canny.shape[1]
    bottom_region = (
        (int)(hight*ratio), (int)(hight-hight*ratio),
        (int)(length*ratio), (int)(length-length*ratio)
        )
    frame_canny_bottom = \
        frame_canny[bottom_region[0]:bottom_region[1], bottom_region[2]:bottom_region[3]]
    frame_canny_side = frame_canny.copy()
    frame_canny_side[bottom_region[0]:bottom_region[1], bottom_region[2]:bottom_region[3]] = 0
    
    # 底面と側面をかけ合わせるver.
    # frame_canny_sum = frame_canny_bottom.sum() * frame_canny_side.sum()

    # 底面と側面に別々の重みをかけて足し合わせるver.
    for i, frame_line in enumerate(frame_canny_side):
        for j, dot in enumerate(frame_line):
            frame_canny_sum += dot * (np.linalg.norm(np.array((i,j))-frame_box_center)/max_length+0.7)
    frame_canny_sum += frame_canny_bottom.sum()
    
    # cv2.imwrite("frame_canny_bottom.jpg", frame_canny_bottom)
    # cv2.imwrite("frame_canny_side.jpg", frame_canny_side)
    # print("frame_canny_sum:", frame_canny_sum)
    
    item_size = (1-frame_canny_sum/frame_canny_sum_empty)*box_size
    item_size = max(item_size, 0)
    
    return item_size


if __name__ == "__main__":
    bags_num = calc_bags_num(95, 50)
    print("bags_num:\n(エコバッグ使用済み容量(%), S枚数, L枚数) = ", bags_num)