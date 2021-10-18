import os
import numpy as np
import cv2
from functools import reduce

from numpy.lib.type_check import imag


def roughly_equal_bool(img, rgb, diff_limit=150):
    bgr = rgb[::-1]
    h, w, _ = img.shape
    bool_map_lst = []
    for bgr_i in range(3):
        img_i = img[:, :, bgr_i]
        color_i = bgr[bgr_i]
        legal_bool = (np.abs(img_i - color_i) < diff_limit)
        bool_map_lst.append(legal_bool)
    bool_map = reduce(lambda x, y:x & y, bool_map_lst)
    return bool_map

class BiSystem:

    def generate_bing_bi(self, img_path):
        min_area = 32
        if '-16-' in img_path:
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路
                (248, 248, 248),
                (242, 242, 243),
                (241, 241, 241),
                (255, 246, 169), # 黄色道路
                (255, 245, 167),
                (246, 218, 110),
                (254, 244, 165),
                (252, 235, 146),
                (251, 232, 140),
                (246, 217, 109),
                (245, 223, 140),
                (249, 228, 132),
                (249, 225, 127),
                (244, 226, 157),
                (241, 223, 156),
                (246, 220, 122),
                (245, 219, 123),
                (244, 223, 142),
                (245, 218, 115),
                (245, 222, 138),
                (248, 243, 232), # 淡黄色道路
                (240, 236, 226),
                (252, 250, 215),
                (229, 210, 138),
                (253, 249, 215),
                (252, 250, 215),
                (237, 234, 225),
                (234, 230, 222),
                (236, 232, 222),
                (234, 230, 222),
                (221, 219, 213),
                (253, 250, 225),
                (245, 227, 162),
                (255, 201, 136), # 橙色道路 map\bing\25.110471486223332,55.17333984375_16_whole_bing.png
                (250, 238, 118),
                (248, 208, 100),
                (250, 229, 112),
                (248, 208, 99),
                (247, 210, 108),
                (249, 236, 120),
                (247, 208, 100),
                (248, 220, 107),
                (247, 219, 106),
                (234, 213, 135),
                (242, 219, 127),
                (246, 217, 110),
                (229, 210, 137), # 橙色箭头
                (252, 248, 209)
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=10)
                bi_img = bi_img | road_map
            # road颜色strict
            road_color_rgb_lst = [
                (227, 227, 228), # 灰色边缘
                (218, 218, 219),
                (217, 217, 219),
                (227, 227, 227),
                
                (223, 223, 224),
                (218, 216, 210),
                (228, 227, 223),
                (217, 215, 209),
                (240, 227, 179), # 橙色边缘
                (231, 213, 147),
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=5)
                bi_img = bi_img | road_map
            road_color_rgb_lst = [
                (224, 224, 224), # 灰色箭头
                (216, 216, 216),
                (215, 215, 215),
                (214, 214, 214),
                (238, 238, 239),
                (237, 237, 238),
                (207, 207, 207),
                (232, 232, 233),
                (217, 217, 217),
                (235, 221, 158), # 橙色箭头
                (233, 215, 149),
                (240, 229, 174),
                (224, 224, 226),
                (216, 216, 218),
                (234, 234, 235), # 灰色边缘
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=1)
                bi_img = bi_img | road_map    


            bi_img = bi_img.astype(np.int) * 255

            # background颜色
            # 
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [
                (241, 241, 241), # 灰色背景
                (229, 241, 206), # 绿色背景
                (156, 227, 249), # 蓝色背景
            ]
            for bg_color in bg_color_rgb_lst:
                bg_map = roughly_equal_bool(img, bg_color, diff_limit=3)
                bi_img_bg = bi_img_bg | bg_map
            bi_img_bg = ~bi_img_bg
            bi_img_bg = bi_img_bg.astype(np.int) * 255


            final_map = (bi_img_bg.astype(np.bool) & bi_img.astype(np.bool)).astype(np.uint8)
            final_map_bool = final_map.astype(np.bool)

            # 补充白色道路的灰色边。diff_limit设置为较小值。同时只允许原来白色部分四周被补充
            up_down_left_down = (1, 1, 1, 1)
            legal_mask_up = np.pad(final_map_bool, ((up_down_left_down[0], 0), (0, 0)), 'constant', constant_values=0)[:-up_down_left_down[0], :].astype(np.bool)
            legal_mask_down = np.pad(final_map_bool, ((0, up_down_left_down[1]), (0, 0)), 'constant', constant_values=0)[up_down_left_down[1]:, :].astype(np.bool)
            legal_mask_left = np.pad(final_map_bool, ((0, 0), (up_down_left_down[2], 0)), 'constant', constant_values=0)[:, :-up_down_left_down[2]].astype(np.bool)
            legal_mask_right = np.pad(final_map_bool, ((0, 0), (0, up_down_left_down[3])), 'constant', constant_values=0)[:, up_down_left_down[3]:].astype(np.bool)
            legal_mask = final_map_bool | legal_mask_up | legal_mask_down | legal_mask_left | legal_mask_right
            road_color_rgb_lst_strict = [
                # (227, 227, 228),
            ]
            for road_color in road_color_rgb_lst_strict:
                road_map = roughly_equal_bool(img, road_color, diff_limit=5)
                final_map_bool = final_map_bool | road_map 
            final_map_bool = final_map_bool & legal_mask

            # 增加background颜色：分割两条相邻道路
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [

            ]
            for bg_color in bg_color_rgb_lst:
                bg_map = roughly_equal_bool(img, bg_color, diff_limit=1)
                bi_img_bg = bi_img_bg | bg_map
            bi_img_bg = ~bi_img_bg
            bi_img_bg = bi_img_bg.astype(np.int) * 255
            final_map = (bi_img_bg.astype(np.bool) & final_map_bool.astype(np.bool)).astype(np.uint8)
            final_map_bool = final_map.astype(np.bool)

            # 罕见的道路颜色
            do_lst = [

            ]
            do = False
            for do_name in do_lst:
                if do_name in img_path:
                    do = True
            if do:
                road_color_rgb_lst_strict = [

                ]
                for road_color in road_color_rgb_lst_strict:
                    road_map = roughly_equal_bool(img, road_color, diff_limit=1)
                    final_map_bool = final_map_bool | road_map 
                final_map_bool = final_map_bool
            final_map =  final_map_bool.astype(np.int) * 255
        
            
            # 去黑点
            ignore_black_lst = [

            ]
            ignore = False
            for ignore_name in ignore_black_lst:
                if ignore_name in img_path:
                    ignore = True
            if not ignore:
                final_map_mask = (final_map / 255).astype(np.int)
                up = np.pad(final_map_mask, ((1, 0), (0, 0)), 'constant', constant_values=0)[:-1, :]
                down = np.pad(final_map_mask, ((0, 1), (0, 0)), 'constant', constant_values=0)[1:, :]
                left = np.pad(final_map_mask, ((0, 0), (1, 0)), 'constant', constant_values=0)[:, :-1]
                right = np.pad(final_map_mask, ((0, 0), (0, 1)), 'constant', constant_values=0)[:, 1:]
                left_up = np.pad(final_map_mask, ((1, 0), (1, 0)), 'constant', constant_values=0)[:-1, :-1] # 处理左上方块
                left_down = np.pad(final_map_mask, ((0, 1), (1, 0)), 'constant', constant_values=0)[1:, :-1]
                right_up = np.pad(final_map_mask, ((1, 0), (0, 1)), 'constant', constant_values=0)[:-1, 1:]
                right_down = np.pad(final_map_mask, ((0, 1), (0, 1)), 'constant', constant_values=0)[1:, 1:]
                sum_map = up + down + left + right + left_up + left_down + right_down + right_up
                black2white_mask = sum_map > 4
                self_black_map = final_map_mask.astype(np.bool)
                black2white_mask = (black2white_mask & ~self_black_map) | self_black_map
                after_map = black2white_mask.astype(np.int) * 255
                final_map = after_map

                # final_map_mask = (final_map / 255).astype(np.int)
                # up = np.pad(final_map_mask, ((1, 0), (0, 0)), 'constant', constant_values=0)[:-1, :]
                # down = np.pad(final_map_mask, ((0, 1), (0, 0)), 'constant', constant_values=0)[1:, :]
                # left = np.pad(final_map_mask, ((0, 0), (1, 0)), 'constant', constant_values=0)[:, :-1]
                # right = np.pad(final_map_mask, ((0, 0), (0, 1)), 'constant', constant_values=0)[:, 1:]
                # left_up = np.pad(final_map_mask, ((1, 0), (1, 0)), 'constant', constant_values=0)[:-1, :-1] # 处理左上方块
                # left_down = np.pad(final_map_mask, ((0, 1), (1, 0)), 'constant', constant_values=0)[1:, :-1]
                # right_up = np.pad(final_map_mask, ((1, 0), (0, 1)), 'constant', constant_values=0)[:-1, 1:]
                # right_down = np.pad(final_map_mask, ((0, 1), (0, 1)), 'constant', constant_values=0)[1:, 1:]
                # sum_map = up + down + left + right + left_up + left_down + right_down + right_up
                # black2white_mask = sum_map > 5
                # self_black_map = final_map_mask.astype(np.bool)
                # black2white_mask = (black2white_mask & ~self_black_map) | self_black_map
                # after_map = black2white_mask.astype(np.int) * 255
                # final_map = after_map
            # 去白点
                final_map_mask = (final_map / 255).astype(np.int)
                up = np.pad(final_map_mask, ((1, 0), (0, 0)), 'constant', constant_values=0)[:-1, :]
                down = np.pad(final_map_mask, ((0, 1), (0, 0)), 'constant', constant_values=0)[1:, :]
                left = np.pad(final_map_mask, ((0, 0), (1, 0)), 'constant', constant_values=0)[:, :-1]
                right = np.pad(final_map_mask, ((0, 0), (0, 1)), 'constant', constant_values=0)[:, 1:]
                left_up = np.pad(final_map_mask, ((1, 0), (1, 0)), 'constant', constant_values=0)[:-1, :-1] # 处理左上方块
                left_down = np.pad(final_map_mask, ((0, 1), (1, 0)), 'constant', constant_values=0)[1:, :-1]
                right_up = np.pad(final_map_mask, ((1, 0), (0, 1)), 'constant', constant_values=0)[:-1, 1:]
                right_down = np.pad(final_map_mask, ((0, 1), (0, 1)), 'constant', constant_values=0)[1:, 1:]
                sum_map = up + down + left + right + left_up + left_down + right_down + right_up
                black2white_mask = sum_map > 2
                self_black_map = final_map_mask.astype(np.bool)
                black2white_mask = black2white_mask & self_black_map
                after_map = black2white_mask.astype(np.int) * 255
                final_map = after_map

            # 过滤小面积白色
            final_map = (final_map / 255).astype(np.uint8)
            contours, hierarchy = cv2.findContours(final_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    cv2.drawContours(final_map, contour, contourIdx=-1, color=0, thickness=-1)
            final_map = final_map.astype(np.int) * 255

            # 过滤小面积黑色
            final_map_temp = (~(final_map / 255).astype(np.bool)).astype(np.uint8)
            contours, hierarchy = cv2.findContours(final_map_temp, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    cv2.drawContours(final_map_temp, contour, contourIdx=-1, color=0, thickness=-1)
            final_map = ~final_map_temp.astype(np.bool)
            final_map = final_map.astype(np.int) * 255

            # 去黑点
            final_map_mask = (final_map / 255).astype(np.int)
            up = np.pad(final_map_mask, ((1, 0), (0, 0)), 'constant', constant_values=0)[:-1, :]
            down = np.pad(final_map_mask, ((0, 1), (0, 0)), 'constant', constant_values=0)[1:, :]
            left = np.pad(final_map_mask, ((0, 0), (1, 0)), 'constant', constant_values=0)[:, :-1]
            right = np.pad(final_map_mask, ((0, 0), (0, 1)), 'constant', constant_values=0)[:, 1:]
            left_up = np.pad(final_map_mask, ((1, 0), (1, 0)), 'constant', constant_values=0)[:-1, :-1] # 处理左上方块
            left_down = np.pad(final_map_mask, ((0, 1), (1, 0)), 'constant', constant_values=0)[1:, :-1]
            right_up = np.pad(final_map_mask, ((1, 0), (0, 1)), 'constant', constant_values=0)[:-1, 1:]
            right_down = np.pad(final_map_mask, ((0, 1), (0, 1)), 'constant', constant_values=0)[1:, 1:]
            sum_map = up + down + left + right + left_up + left_down + right_down + right_up
            black2white_mask = sum_map > 4
            self_black_map = final_map_mask.astype(np.bool)
            black2white_mask = (black2white_mask & ~self_black_map) | self_black_map
            after_map = black2white_mask.astype(np.int) * 255
            final_map = after_map  

            img_ = img.copy()
            img[final_map == 255] = (0, 0, 255)
            road_mask = (final_map == 255)
            color_img = (road_mask[:, :, None] * img_).astype(np.uint8)
            # cv2.imwrite(img_path.replace('.png', '_color_vis.png'), color_img)
            cv2.imwrite(img_path.replace('.png', '_bi.png'), final_map)
            # cv2.imwrite(img_path.replace('.png', '_vis.png'), img)            
     
    def genetare_google_bi(self, img_path):
        min_area = -1
        if '-16-' in img_path:
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路中间
                (241, 243, 244),
                (252, 252, 253), # 白色道路两边
                (240, 244, 244),
                (253, 226, 147), # 深黄色背景
                (255, 240, 156), # 深黄色背景
                (248, 172, 5), # 深黄色边缘
                (253, 218, 124), # 深黄色边缘
                (250, 192, 56),
                (250, 211, 119),
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=40)
                bi_img = bi_img | road_map


            bi_img = bi_img.astype(np.int) * 255

            # background颜色
            # 
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [
                (232, 234, 237), # 灰色背景
                (249, 249, 249),
                
                (254, 232, 180), # 黄色框
                (255, 233, 177), # 黄色框
                (255, 233, 173),
                (254, 235, 179),
                (254, 232, 172),
                (254, 234, 179),
            ]
            for bg_color in bg_color_rgb_lst:
                bg_map = roughly_equal_bool(img, bg_color, diff_limit=5)
                bi_img_bg = bi_img_bg | bg_map
            bi_img_bg = ~bi_img_bg
            bi_img_bg = bi_img_bg.astype(np.int) * 255


            final_map = (bi_img_bg.astype(np.bool) & bi_img.astype(np.bool)).astype(np.uint8)
            final_map_bool = final_map.astype(np.bool)

            # 补充白色道路的灰色边。diff_limit设置为较小值。同时只允许原来白色部分四周被补充
            up_down_left_down = (2, 2, 2, 2)
            legal_mask_up = np.pad(final_map_bool, ((up_down_left_down[0], 0), (0, 0)), 'constant', constant_values=0)[:-up_down_left_down[0], :].astype(np.bool)
            legal_mask_down = np.pad(final_map_bool, ((0, up_down_left_down[1]), (0, 0)), 'constant', constant_values=0)[up_down_left_down[1]:, :].astype(np.bool)
            legal_mask_left = np.pad(final_map_bool, ((0, 0), (up_down_left_down[2], 0)), 'constant', constant_values=0)[:, :-up_down_left_down[2]].astype(np.bool)
            legal_mask_right = np.pad(final_map_bool, ((0, 0), (0, up_down_left_down[3])), 'constant', constant_values=0)[:, up_down_left_down[3]:].astype(np.bool)
            legal_mask = final_map_bool | legal_mask_up | legal_mask_down | legal_mask_left | legal_mask_right
            road_color_rgb_lst_strict = [
                (216, 220, 224),  # 白色道路两边
                (224, 228, 232),
                (228, 232, 232),
                (224, 228, 232),
                (224, 224, 228),
                (236, 236, 240),
                (232, 236, 236),
                (234, 234, 237),
                (222, 226, 230),
                (218, 218, 222),
                (230, 230, 234),
                (221, 225, 229),
                (229, 229, 233),
                (241, 243, 244),
                (249, 186, 48), # 橙色道路边缘
                (249, 201, 94),
                (249, 230, 188),
                (247, 216, 135),
                (247, 212, 115),
                (247, 208, 99),
                (244, 226, 171),
                (248, 210, 115),
                (244, 211, 109),
                (244, 219, 153),
                (248, 207, 105)
                
            ]
            for road_color in road_color_rgb_lst_strict:
                road_map = roughly_equal_bool(img, road_color, diff_limit=5)
                final_map_bool = final_map_bool | road_map 
            final_map_bool = final_map_bool & legal_mask

            # 增加background颜色：分割两条相邻道路
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [
                (242, 243, 244),
                (248, 249, 250)
            ]
            for bg_color in bg_color_rgb_lst:
                bg_map = roughly_equal_bool(img, bg_color, diff_limit=1)
                bi_img_bg = bi_img_bg | bg_map
            bi_img_bg = ~bi_img_bg
            bi_img_bg = bi_img_bg.astype(np.int) * 255
            final_map = (bi_img_bg.astype(np.bool) & final_map_bool.astype(np.bool)).astype(np.uint8)
            final_map_bool = final_map.astype(np.bool)

            # 罕见的道路颜色
            do_lst = [
                '24.9760994936954,55.1568603515625',
                '24.89640226655871,67.137451171875',
                '24.63203814959688,46.8017578125',
                
            ]
            do = False
            for do_name in do_lst:
                if do_name in img_path:
                    do = True
            if do:
                road_color_rgb_lst_strict = [
                    (241, 243, 244), # 灰色的道路
                    (237, 241, 241),
                    (225, 225, 229),
                    (233, 233, 237),
                    (221, 221, 225),
                    (226, 226, 230),
                    (227, 227, 227),
                    (236, 236, 236),
                    (224, 224, 228),
                    (242, 241, 240),
                    # (234, 238, 238), # 白点
                    (222, 222, 226),
                    (218, 218, 222),
                    (218, 222, 226),
                    (230, 230, 234),

                ]
                for road_color in road_color_rgb_lst_strict:
                    road_map = roughly_equal_bool(img, road_color, diff_limit=1)
                    final_map_bool = final_map_bool | road_map 
                final_map_bool = final_map_bool

            # 罕见的道路颜色
            do_lst = [
                '24.891419479211137,55.0689697265625'
            ]
            do = False
            for do_name in do_lst:
                if do_name in img_path:
                    do = True
            if do:
                road_color_rgb_lst_strict = [
                    (241, 243, 244), # 灰色的道路
                    (228, 232, 232),
                    (224, 224, 228),
                    (220, 220, 224),
                    (236, 236, 236),
                    (220, 220, 224),
                    
                ]
                for road_color in road_color_rgb_lst_strict:
                    road_map = roughly_equal_bool(img, road_color, diff_limit=1)
                    final_map_bool = final_map_bool | road_map 
                final_map_bool = final_map_bool                
            
            # 过滤小面积白色
            final_map = final_map_bool.astype(np.uint8)
            contours, hierarchy = cv2.findContours(final_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    cv2.drawContours(final_map, contour, contourIdx=-1, color=0, thickness=-1)
            final_map = final_map.astype(np.int) * 255
            
            # 去黑点
            ignore_black_lst = [
                '24.6370313535095,46.82373046875',
                '24.6370313535095,46.8951416015625',
                '24.39713301739104,54.51416015625',
            ]
            ignore = False
            for ignore_name in ignore_black_lst:
                if ignore_name in img_path:
                    ignore = True
            if not ignore:
                final_map_mask = (final_map / 255).astype(np.int)
                up = np.pad(final_map_mask, ((1, 0), (0, 0)), 'constant', constant_values=0)[:-1, :]
                down = np.pad(final_map_mask, ((0, 1), (0, 0)), 'constant', constant_values=0)[1:, :]
                left = np.pad(final_map_mask, ((0, 0), (1, 0)), 'constant', constant_values=0)[:, :-1]
                right = np.pad(final_map_mask, ((0, 0), (0, 1)), 'constant', constant_values=0)[:, 1:]
                left_up = np.pad(final_map_mask, ((1, 0), (1, 0)), 'constant', constant_values=0)[:-1, :-1] # 处理左上方块
                left_down = np.pad(final_map_mask, ((0, 1), (1, 0)), 'constant', constant_values=0)[1:, :-1]
                right_up = np.pad(final_map_mask, ((1, 0), (0, 1)), 'constant', constant_values=0)[:-1, 1:]
                right_down = np.pad(final_map_mask, ((0, 1), (0, 1)), 'constant', constant_values=0)[1:, 1:]
                sum_map = up + down + left + right + left_up + left_down + right_down + right_up
                black2white_mask = sum_map > 4
                self_black_map = final_map_mask.astype(np.bool)
                black2white_mask = (black2white_mask & ~self_black_map) | self_black_map
                after_map = black2white_mask.astype(np.int) * 255
                final_map = after_map
            # 去白点
                final_map_mask = (final_map / 255).astype(np.int)
                up = np.pad(final_map_mask, ((1, 0), (0, 0)), 'constant', constant_values=0)[:-1, :]
                down = np.pad(final_map_mask, ((0, 1), (0, 0)), 'constant', constant_values=0)[1:, :]
                left = np.pad(final_map_mask, ((0, 0), (1, 0)), 'constant', constant_values=0)[:, :-1]
                right = np.pad(final_map_mask, ((0, 0), (0, 1)), 'constant', constant_values=0)[:, 1:]
                left_up = np.pad(final_map_mask, ((1, 0), (1, 0)), 'constant', constant_values=0)[:-1, :-1] # 处理左上方块
                left_down = np.pad(final_map_mask, ((0, 1), (1, 0)), 'constant', constant_values=0)[1:, :-1]
                right_up = np.pad(final_map_mask, ((1, 0), (0, 1)), 'constant', constant_values=0)[:-1, 1:]
                right_down = np.pad(final_map_mask, ((0, 1), (0, 1)), 'constant', constant_values=0)[1:, 1:]
                sum_map = up + down + left + right + left_up + left_down + right_down + right_up
                black2white_mask = sum_map > 2
                self_black_map = final_map_mask.astype(np.bool)
                black2white_mask = black2white_mask & self_black_map
                after_map = black2white_mask.astype(np.int) * 255
                final_map = after_map
            img_ = img.copy()
            img[final_map == 255] = (0, 0, 255)
            road_mask = (final_map == 255)
            color_img = (road_mask[:, :, None] * img_).astype(np.uint8)
            # cv2.imwrite(img_path.replace('.png', '_color_vis.png'), color_img)
            cv2.imwrite(img_path.replace('.png', '_bi.png'), final_map)
            # cv2.imwrite(img_path.replace('.png', '_vis.png'), img)          

    def genetare_osm_bi(self, img_path):
        min_area = 16
        if '-16-' in img_path:
            
              
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路中间
                (236, 236, 236),
                (234, 234, 234),
                (248, 248, 186), # 黄色道路
                (236, 199, 152),
                # (213, 213, 155),
                (249, 214, 170), # 肉色
                (221, 159, 159),
                (131, 122, 202),
                # (211, 175, 124),
                (148, 212, 148), # 绿色
                (221, 159, 159), # 粉色
                (205, 204, 203), # 灰色
                (204, 204, 204),
                (109, 113, 213), # 蓝色箭头
                (115, 115, 210),
                (109, 112, 213),
                (113, 116, 212),
                (116, 130, 202),
                (108, 112, 213),
                (124, 119, 206),
                (115, 116, 209),
                (113, 115, 211),
                (112, 114, 212),
                (204, 204, 204), # 深灰色路

            ]
            for road_color in road_color_rgb_lst:
                limit = 40
                if road_color in [(148, 212, 148), (205, 204, 203), (204, 204, 204), (236, 236, 236)]:
                    limit = 10
                road_map = roughly_equal_bool(img, road_color, diff_limit=limit)
                bi_img = bi_img | road_map


            bi_img = bi_img.astype(np.int) * 255

            # background颜色
            # 
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [
                (210, 210, 210), # 白色道路边缘的灰色
                (207, 208, 206),
                (205, 206, 205),
                (236, 236, 236),
                (212, 209, 206),
                (212, 211, 208),
                (206, 205, 203),
                (234, 234, 234),
                (244, 241, 236),
                (247, 245, 241),
                (213, 209, 205),
                (205, 204, 203),
                (224, 194, 189), # 粉色边缘不要
                (222, 187, 186),
                (222, 198, 167), # 橙色边缘
                (0, 0, 0), # 月亮图标

            ]
            for bg_color in bg_color_rgb_lst:
                bg_map = roughly_equal_bool(img, bg_color, diff_limit=5)
                bi_img_bg = bi_img_bg | bg_map
            bi_img_bg = ~bi_img_bg
            bi_img_bg = bi_img_bg.astype(np.int) * 255


            final_map = (bi_img_bg.astype(np.bool) & bi_img.astype(np.bool)).astype(np.uint8)
            final_map_bool = final_map.astype(np.bool)

            # 补充白色道路的灰色边。diff_limit设置为较小值。同时只允许原来白色部分四周被补充
            up_down_left_down = (2, 2, 2, 2)
            legal_mask_up = np.pad(final_map_bool, ((up_down_left_down[0], 0), (0, 0)), 'constant', constant_values=0)[:-up_down_left_down[0], :].astype(np.bool)
            legal_mask_down = np.pad(final_map_bool, ((0, up_down_left_down[1]), (0, 0)), 'constant', constant_values=0)[up_down_left_down[1]:, :].astype(np.bool)
            legal_mask_left = np.pad(final_map_bool, ((0, 0), (up_down_left_down[2], 0)), 'constant', constant_values=0)[:, :-up_down_left_down[2]].astype(np.bool)
            legal_mask_right = np.pad(final_map_bool, ((0, 0), (0, up_down_left_down[3])), 'constant', constant_values=0)[:, up_down_left_down[3]:].astype(np.bool)
            legal_mask = final_map_bool | legal_mask_up | legal_mask_down | legal_mask_left | legal_mask_right
            road_color_rgb_lst_strict = [

            ]
            for road_color in road_color_rgb_lst_strict:
                road_map = roughly_equal_bool(img, road_color, diff_limit=5)
                final_map_bool = final_map_bool | road_map 
            final_map_bool = final_map_bool & legal_mask



            # 过滤小面积白色
            final_map = final_map_bool.astype(np.uint8)
            # contours, hierarchy = cv2.findContours(final_map, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            # for contour in contours:
            #     area = cv2.contourArea(contour)
            #     if area < min_area:
            #         cv2.drawContours(final_map, contour, contourIdx=-1, color=0, thickness=-1)
            final_map = final_map.astype(np.int) * 255
            
            # 去黑点
            final_map_mask = (final_map / 255).astype(np.int)
            up = np.pad(final_map_mask, ((1, 0), (0, 0)), 'constant', constant_values=0)[:-1, :]
            down = np.pad(final_map_mask, ((0, 1), (0, 0)), 'constant', constant_values=0)[1:, :]
            left = np.pad(final_map_mask, ((0, 0), (1, 0)), 'constant', constant_values=0)[:, :-1]
            right = np.pad(final_map_mask, ((0, 0), (0, 1)), 'constant', constant_values=0)[:, 1:]
            left_up = np.pad(final_map_mask, ((1, 0), (1, 0)), 'constant', constant_values=0)[:-1, :-1] # 处理左上方块
            left_down = np.pad(final_map_mask, ((0, 1), (1, 0)), 'constant', constant_values=0)[1:, :-1]
            right_up = np.pad(final_map_mask, ((1, 0), (0, 1)), 'constant', constant_values=0)[:-1, 1:]
            right_down = np.pad(final_map_mask, ((0, 1), (0, 1)), 'constant', constant_values=0)[1:, 1:]
            sum_map = up + down + left + right + left_up + left_down + right_down + right_up
            black2white_mask = sum_map > 4
            self_black_map = final_map_mask.astype(np.bool)
            black2white_mask = (black2white_mask & ~self_black_map) | self_black_map
            after_map = black2white_mask.astype(np.int) * 255
            final_map = after_map

            final_map_mask = (final_map / 255).astype(np.int)
            up = np.pad(final_map_mask, ((1, 0), (0, 0)), 'constant', constant_values=0)[:-1, :]
            down = np.pad(final_map_mask, ((0, 1), (0, 0)), 'constant', constant_values=0)[1:, :]
            left = np.pad(final_map_mask, ((0, 0), (1, 0)), 'constant', constant_values=0)[:, :-1]
            right = np.pad(final_map_mask, ((0, 0), (0, 1)), 'constant', constant_values=0)[:, 1:]
            left_up = np.pad(final_map_mask, ((1, 0), (1, 0)), 'constant', constant_values=0)[:-1, :-1] # 处理左上方块
            left_down = np.pad(final_map_mask, ((0, 1), (1, 0)), 'constant', constant_values=0)[1:, :-1]
            right_up = np.pad(final_map_mask, ((1, 0), (0, 1)), 'constant', constant_values=0)[:-1, 1:]
            right_down = np.pad(final_map_mask, ((0, 1), (0, 1)), 'constant', constant_values=0)[1:, 1:]
            sum_map = up + down + left + right + left_up + left_down + right_down + right_up
            black2white_mask = sum_map > 4
            self_black_map = final_map_mask.astype(np.bool)
            black2white_mask = (black2white_mask & ~self_black_map) | self_black_map
            after_map = black2white_mask.astype(np.int) * 255
            final_map = after_map

            final_map_mask = (final_map / 255).astype(np.int)
            up = np.pad(final_map_mask, ((1, 0), (0, 0)), 'constant', constant_values=0)[:-1, :]
            down = np.pad(final_map_mask, ((0, 1), (0, 0)), 'constant', constant_values=0)[1:, :]
            left = np.pad(final_map_mask, ((0, 0), (1, 0)), 'constant', constant_values=0)[:, :-1]
            right = np.pad(final_map_mask, ((0, 0), (0, 1)), 'constant', constant_values=0)[:, 1:]
            left_up = np.pad(final_map_mask, ((1, 0), (1, 0)), 'constant', constant_values=0)[:-1, :-1] # 处理左上方块
            left_down = np.pad(final_map_mask, ((0, 1), (1, 0)), 'constant', constant_values=0)[1:, :-1]
            right_up = np.pad(final_map_mask, ((1, 0), (0, 1)), 'constant', constant_values=0)[:-1, 1:]
            right_down = np.pad(final_map_mask, ((0, 1), (0, 1)), 'constant', constant_values=0)[1:, 1:]
            sum_map = up + down + left + right + left_up + left_down + right_down + right_up
            black2white_mask = sum_map > 4
            self_black_map = final_map_mask.astype(np.bool)
            black2white_mask = (black2white_mask & ~self_black_map) | self_black_map
            after_map = black2white_mask.astype(np.int) * 255
            final_map = after_map            
            
            # 过滤小面积白色
            final_map = (final_map / 255).astype(np.uint8)
            contours, hierarchy = cv2.findContours(final_map, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    cv2.drawContours(final_map, contour, contourIdx=-1, color=0, thickness=-1)
            final_map = (final_map * 255).astype(np.uint8)
            #
            img_ = img.copy()
            img[final_map == 255] = (0, 0, 255)
            road_mask = (final_map == 255)
            color_img = (road_mask[:, :, None] * img_).astype(np.uint8)
            # cv2.imwrite(img_path.replace('.png', '_color_vis.png'), color_img)
            kernel = np.ones((2, 2), dtype=np.uint8)
            final_map = cv2.morphologyEx(final_map.astype(np.uint8), cv2.MORPH_OPEN, kernel, 1)
            cv2.imwrite(img_path.replace('.png', '_bi.png'), final_map)
            # cv2.imwrite(img_path.replace('.png', '_vis.png'), img)  
