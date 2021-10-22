import os
import numpy as np
import cv2
from functools import reduce
from numpy.core.numeric import zeros_like

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
        
            min_area = 16
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路
                (251, 250, 247),
                (245, 241, 232),
                (244, 242, 238),
                (244, 242, 238),
                (240, 238, 234),
                (248, 246, 244),
                (253, 252, 250),
                (229, 220, 202), # 咖啡色边缘
                (245, 241, 232),
                (232, 225, 212),
                (233, 211, 250), # 紫色道路
                (222, 194, 233), 
                (231, 208, 247),
                (206, 171, 210),
                (208, 177, 205),
                (210, 175, 214),
                (230, 206, 245),
                (198, 157, 196),
                (195, 147, 229),
                (202, 175, 222),
                (189, 149, 208),
                (187, 148, 203),
                (203, 175, 222),
                (191, 148, 214),
                (201, 160, 200), # 紫色边缘
                (216, 184, 223),
                (182, 150, 182),
                (186, 148, 198),
                (194, 147, 226),
                (198, 157, 196),
                (198, 157, 195),
                (204, 168, 199),
                (195, 162, 212),
                (189, 155, 203),
                (188, 151, 203),
                (199, 161, 226),
                (203, 176, 222),
                (182, 151, 178),
                (196, 147, 231),
                (191, 148, 214),
                (202, 174, 222),
                (201, 174, 218),
                (189, 158, 185),
                (195, 166, 202),
                (197, 157, 195),
                (223, 208, 186),
                (182, 153, 180),
                (183, 149, 188),
                (192, 147, 220),
                (192, 147, 216),
                (255, 244, 171), # 黄色道路
                (255, 244, 171),
                (240, 220, 156),
                (229, 201, 145),
                (238, 215, 152),
                (234, 211, 154),
                (236, 212, 149),
                (255, 244, 171),
                (248, 234, 164),
                (254, 244, 170),
                (229, 201, 145), # 黄色箭头
                (229, 201, 145),
                (220, 192, 119),
                (229, 210, 153),
                (230, 200, 121),
                (230, 200, 124),
                (229, 210, 153),
                (245, 233, 192),
                (227, 199, 143),
                (230, 210, 154),
                (255, 212, 128), # 黄色边缘
                (253, 212, 129),
                (247, 220, 150),
                (255, 239, 163),
                (255, 226, 146),
                (255, 239, 163),
                (255, 236, 159),
                (255, 228, 149),
                (253, 212, 133),
                (254, 212, 128),
                (246, 224, 178),
                (250, 218, 155),
                (255, 254, 237), #　淡黄色道路
                (253, 250, 230),
                (253, 249, 226),
                (250, 242, 209),
                (254, 244, 171),
                (251, 244, 200),
                (255, 254, 237),
                (240, 221, 164),
                (234, 209, 140),
                (231, 201, 124),
                (246, 232, 191),
                (243, 225, 175),
                (248, 240, 221),
                (231, 201, 128), #　淡黄色边缘
                (229, 197, 113),
                (231, 206, 139),
                (234, 217, 173),
                (236, 222, 188),
                (233, 212, 158),
                (254, 244, 171), #　淡橙色道路
                (254, 234, 157),
                (249, 221, 167), # 淡橙色边缘
                (252, 213, 138),
                (192, 192, 196), # 铁路的黑色部分
                (214, 213, 214),
                (204, 203, 206),
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=10)
                bi_img = bi_img | road_map
            # road颜色strict
            road_color_rgb_lst = [
                (241, 235, 223), # 咖啡色边缘
                (229, 220, 201),
                (229, 219, 200),
                (227, 219, 201),
                (238, 232, 218),
                (248, 247, 244), # 与背景相近的道路
                (246, 245, 242),
                (241, 240, 236),
                (254, 253, 250),
                (253, 252, 249),
                (210, 208, 202),
                (217, 216, 210),
                (237, 236, 232),
                (209, 208, 201),
                (226, 224, 219),
                (209, 207, 201),
                (231, 230, 225),
                (217, 215, 210),
                (208, 206, 201),
                (220, 218, 213),
                (254, 253, 250),
                (225, 223, 218),
                (207, 205, 199),
                (252, 251, 247),
                (216, 214, 209),
                (254, 252, 250),
                (210, 209, 202),
                (241, 240, 236),
                (214, 212, 206),
                (230, 229, 224),
                (215, 213, 207),
                (238, 237, 233),
                (233, 232, 229),
                (237, 224, 187),
                (246, 238, 215),
                (242, 233, 205),
                (229, 214, 184),
                (216, 189, 127),
                (236, 235, 231),
                (214, 212, 206),
                (112, 108, 108), # 国界
                (146, 143, 142),
                (113, 111, 110),
                (100, 97, 97),
                (144, 141, 140),
                (222, 220, 216),
                (173, 171, 168),
                (130, 127, 126),
                (112, 108, 108),
                (211, 209, 206),
                (222, 220, 216),
                (105, 102, 102),
                (108, 105, 104),
                (120, 116, 116),
                (210, 208, 205),
                (222, 220, 216),
                (96, 93, 93),
                (202, 199, 196),
                (158, 156, 154),
                (191, 189, 186),
                (94, 91, 91),
                (138, 135, 134),
                (195, 194, 191),
                (168, 165, 163),
                (150, 148, 146),
                (179, 177, 174),
                (186, 186, 190), # 铁路
                (203, 203, 206),
                (192, 191, 195),
                (241, 239, 236),
                
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=5)
                bi_img = bi_img | road_map
            road_color_rgb_lst = [

            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=1)
                bi_img = bi_img | road_map    


            bi_img = bi_img.astype(np.int) * 255

            # background颜色
            # 
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [
                (240, 238, 234),
                (239, 238, 234),
                (234, 230, 224),
                (244, 240, 238),
                (236, 226, 211),
                (234, 230, 224),
                (233, 230, 226),
                (234, 230, 224),
                (234, 230, 224),
                (226, 223, 219)
            ]
            for bg_color in bg_color_rgb_lst:
                bg_map = roughly_equal_bool(img, bg_color, diff_limit=3)
                if bg_map.sum() / (bg_map.shape[0] * bg_map.shape[1]) < 1 / 256:
                    continue
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


            # 补充道路中的箭头。diff_limit设置为较小值。同时只允许原来白色部分四周被补充
            up_down_left_down = (3, 3, 3, 3)
            legal_mask_up = np.pad(final_map_bool, ((up_down_left_down[0], 0), (0, 0)), 'constant', constant_values=0)[:-up_down_left_down[0], :].astype(np.bool)
            legal_mask_down = np.pad(final_map_bool, ((0, up_down_left_down[1]), (0, 0)), 'constant', constant_values=0)[up_down_left_down[1]:, :].astype(np.bool)
            legal_mask_left = np.pad(final_map_bool, ((0, 0), (up_down_left_down[2], 0)), 'constant', constant_values=0)[:, :-up_down_left_down[2]].astype(np.bool)
            legal_mask_right = np.pad(final_map_bool, ((0, 0), (0, up_down_left_down[3])), 'constant', constant_values=0)[:, up_down_left_down[3]:].astype(np.bool)
            legal_mask = final_map_bool | legal_mask_up | legal_mask_down | legal_mask_left | legal_mask_right
            road_color_rgb_lst_strict = [
                (237, 214, 152), # 黄色箭头
                (249, 241, 212),
                (245, 242, 234),
                (249, 241, 212),
                (222, 205, 139),
                (248, 238, 206),
                (245, 232, 192),
                (240, 226, 184),
                (247, 241, 221),
                (219, 192, 120),
                (223, 198, 131),
                (243, 232, 198),
                (233, 226, 184),
                (229, 196, 112),
            ]
            for road_color in road_color_rgb_lst_strict:
                road_map = roughly_equal_bool(img, road_color, diff_limit=10)
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
            contours, hierarchy = cv2.findContours(final_map, cv2.RETR_TREE      , cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    cv2.fillPoly(final_map, contour, 0)
            final_map = final_map.astype(np.int) * 255

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

            # final_map = (final_map / 255).astype(np.uint8)
            # contours, hierarchy = cv2.findContours(final_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            # for contour in contours:
            #     area = cv2.contourArea(contour)
            #     if area < min_area:
            #         cv2.fillPoly(final_map, contour, 0)
            # final_map = final_map.astype(np.int) * 255     

            # final_map = (final_map / 255).astype(np.uint8)
            # contours, hierarchy = cv2.findContours(final_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            # for contour in contours:
            #     area = cv2.contourArea(contour)
            #     if area < min_area:
            #         cv2.fillPoly(final_map, contour, 0)
            # final_map = final_map.astype(np.int) * 255                     

            # 过滤小面积黑色
            final_map_temp = (~(final_map / 255).astype(np.bool)).astype(np.uint8)
            contours, hierarchy = cv2.findContours(final_map_temp, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 24:
                    cv2.drawContours(final_map_temp, contour, contourIdx=-1, color=0, thickness=-1)
            final_map = ~final_map_temp.astype(np.bool)
            final_map = final_map.astype(np.int) * 255

            ## 去黑点
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
        else:
            min_area = 32
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 254, 237), # 黄色
                (245, 233, 193),
                (251, 247, 222), # 黄色边缘
                (231, 200, 123),
                (230, 199, 119),
                (240, 220, 163),
                (233, 207, 138), 
                (216, 186, 111), # 黄色箭头
                (216, 186, 111),
                (221, 194, 125),
                (255, 255, 255), # 白色
                (210, 200, 178), # 白色箭头
                (224, 216, 197),
                (218, 210, 192),
                (232, 225, 209),
                (232, 211, 249), # 紫色
                # (224, 197, 235), # 紫色边缘
                # (202, 162, 199),
                # (216, 185, 223),
                # (201, 162, 198),
                (255, 245, 170), # 橙色
                (239, 208, 148),
                (238, 208, 149),
                (249, 232, 162),
                (247, 227, 159),
                (247, 242, 229), # 肉色
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=10)
                bi_img = bi_img | road_map
            # road颜色strict
            road_color_rgb_lst = [

            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=5)
                bi_img = bi_img | road_map
            road_color_rgb_lst = [

            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=1)
                bi_img = bi_img | road_map    


            bi_img = bi_img.astype(np.int) * 255

            # background颜色
            # 
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [

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
        zoom_level = os.path.basename(img_path).split('-')[2]    
        if zoom_level == '14':  
            min_area = -1  
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (253, 226, 147), # 黄色道路
                (249, 171, 0), # 橙色边缘
                (255, 255, 255), # 白色道路
                (245, 245, 245),
                (244, 244, 244),
                # (95, 99, 104), # 灰色国界 
                
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=40)
                bi_img = bi_img | road_map

            road_color_rgb_lst = [
                (213, 216, 219), # 灰色铁路 map_14\google_1024_14\29.430029404571762, 71.65283203125_14_whole_google.png
                
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=5)
                bi_img = bi_img | road_map                


            bi_img = bi_img.astype(np.int) * 255

            # background颜色
            # 
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [
                # (232, 234, 237)
            ]
            for bg_color in bg_color_rgb_lst:
                bg_map = roughly_equal_bool(img, bg_color, diff_limit=5)
                bi_img_bg = bi_img_bg | bg_map
            bi_img_bg = ~bi_img_bg
            bi_img_bg = bi_img_bg.astype(np.int) * 255


            final_map = (bi_img_bg.astype(np.bool) & bi_img.astype(np.bool)).astype(np.uint8)
            final_map_bool = final_map.astype(np.bool)

            # 补充白色道路的灰色边。diff_limit设置为较小值。同时只允许原来白色部分四周被补充
            up_down_left_down = (4, 4, 4, 4)
            legal_mask_up = np.pad(final_map_bool, ((up_down_left_down[0], 0), (0, 0)), 'constant', constant_values=0)[:-up_down_left_down[0], :].astype(np.bool)
            legal_mask_down = np.pad(final_map_bool, ((0, up_down_left_down[1]), (0, 0)), 'constant', constant_values=0)[up_down_left_down[1]:, :].astype(np.bool)
            legal_mask_left = np.pad(final_map_bool, ((0, 0), (up_down_left_down[2], 0)), 'constant', constant_values=0)[:, :-up_down_left_down[2]].astype(np.bool)
            legal_mask_right = np.pad(final_map_bool, ((0, 0), (0, up_down_left_down[3])), 'constant', constant_values=0)[:, up_down_left_down[3]:].astype(np.bool)
            legal_mask = final_map_bool | legal_mask_up | legal_mask_down | legal_mask_left | legal_mask_right
            road_color_rgb_lst_strict = [
                # (224, 224, 228), #　灰色边缘
                # (216, 220, 224),
                # (204, 204, 212),
                (148, 148, 156),
                (180, 184, 188),
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
        else:
            min_area = -1
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (253, 226, 147), # 橙色
                (249, 171, 0), # 橙色边缘
                (255, 255, 255), # 白色
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=40)
                bi_img = bi_img | road_map


            bi_img = bi_img.astype(np.int) * 255

            # background颜色
            # 
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [

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
        zoom_level = os.path.basename(img_path).split('-')[2]
        if zoom_level == '14':
            min_area = 16
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (254, 253, 215), # 黄色道路
                (255, 234, 187), # 橙色边缘
                (253, 235, 206),

                (255, 255, 255), # 白色道路
                (255, 233, 165), # 深黄色道路
                (251, 219, 153), # 深黄色道路边缘
                (251, 219, 152),

                (234, 233, 230), # 灰色铁路
                (237, 236, 233),
                (234, 233, 230),
                (244, 242, 238),
                (237, 236, 233),
                (224, 224, 223),
                (228, 227, 226)
               
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=40)
                bi_img = bi_img | road_map

            road_color_rgb_lst = [
                # (235, 214, 216), # 淡紫色国界
                
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=3)
                bi_img = bi_img | road_map                


            bi_img = bi_img.astype(np.int) * 255

            # background颜色
            # 
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [
                (251, 248, 243), # 淡黄色背景
                (213, 232, 235), # 蓝色海洋
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
            # black2white_mask = sum_map > 4
            # self_black_map = final_map_mask.astype(np.bool)
            # black2white_mask = (black2white_mask & ~self_black_map) | self_black_map
            # after_map = black2white_mask.astype(np.int) * 255
            # final_map = after_map

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
        else:
            min_area = 16
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路中间
                (254, 253, 215), # 黄色道路
                (253, 235, 206),
                (255, 237, 193),
                (254, 240, 205),
                (255, 233, 165), # 橙色道路
                (251, 219, 152),

            ]
            for road_color in road_color_rgb_lst:
                limit = 40
                road_map = roughly_equal_bool(img, road_color, diff_limit=limit)
                bi_img = bi_img | road_map


            bi_img = bi_img.astype(np.int) * 255

            # background颜色
            # 
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [


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