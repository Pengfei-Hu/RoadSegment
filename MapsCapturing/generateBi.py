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
     
    def genetare_google_bi(self, img_path):
        min_area = -1
        if '_16_' in img_path:
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路中间
                (252, 252, 253), # 白色道路两边
                (253, 226, 147), # 深黄色背景
                (255, 240, 156), # 深黄色背景
                (248, 172, 5), # 深黄色边缘
                (253, 218, 124), # 深黄色边缘
                (250, 192, 56),
                (250, 211, 119)
            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=40)
                bi_img = bi_img | road_map
            bi_img = bi_img.astype(np.int) * 255

            # background颜色
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [
                (232, 234, 237), # 灰色背景
                (254, 232, 180), # 黄色框
                (255, 233, 177), # 黄色框
                (255, 233, 173),
                (254, 235, 179),
                (254, 232, 172),
                (254, 234, 179)
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
                (249, 230, 188) 
            ]
            for road_color in road_color_rgb_lst_strict:
                road_map = roughly_equal_bool(img, road_color, diff_limit=5)
                final_map_bool = final_map_bool | road_map 
            final_map_bool = final_map_bool & legal_mask

            final_map = final_map_bool.astype(np.uint8)
            # 过滤小面积白色
            contours, hierarchy = cv2.findContours(final_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    cv2.drawContours(final_map, contour, contourIdx=-1, color=0, thickness=-1)
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
            #
            img_ = img.copy()
            img[final_map == 255] = (0, 0, 255)
            road_mask = (final_map == 255)
            color_img = (road_mask[:, :, None] * img_).astype(np.uint8)
            # cv2.imwrite(img_path.replace('.png', '_color_vis.png'), color_img)
            cv2.imwrite(img_path.replace('.png', '_bi.png'), final_map)
            # cv2.imwrite(img_path.replace('.png', '_vis.png'), img)    
        elif '_17_' in img_path:
            
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路中间
                (252, 252, 253), # 白色道路两边
                (253, 226, 147), # 深黄色背景
                (255, 240, 156), # 深黄色背景
                (248, 172, 5), # 深黄色边缘
                (253, 218, 124), # 深黄色边缘
                (250, 192, 56),
                (250, 211, 119)
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
                (254, 232, 180), # 黄色框
                (255, 233, 177), # 黄色框
                (255, 233, 173),
                (254, 235, 179),
                (254, 232, 172),
                (254, 234, 179)
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
                (249, 230, 188) 
            ]
            for road_color in road_color_rgb_lst_strict:
                road_map = roughly_equal_bool(img, road_color, diff_limit=5)
                final_map_bool = final_map_bool | road_map 
            final_map_bool = final_map_bool & legal_mask




            final_map = final_map_bool.astype(np.uint8)
            # 过滤小面积白色
            contours, hierarchy = cv2.findContours(final_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    cv2.drawContours(final_map, contour, contourIdx=-1, color=0, thickness=-1)
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
            #
            img_ = img.copy()
            img[final_map == 255] = (0, 0, 255)
            road_mask = (final_map == 255)
            color_img = (road_mask[:, :, None] * img_).astype(np.uint8)
            # cv2.imwrite(img_path.replace('.png', '_color_vis.png'), color_img)
            cv2.imwrite(img_path.replace('.png', '_bi.png'), final_map)
            # cv2.imwrite(img_path.replace('.png', '_vis.png'), img)            
        elif '_18_' in img_path:
            
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路中间
                (252, 252, 253), # 白色道路两边
                (253, 226, 147), # 深黄色背景
                (255, 240, 156), # 深黄色背景
                (248, 172, 5), # 深黄色边缘
                (253, 218, 124), # 深黄色边缘
                (250, 192, 56),
                (250, 211, 119)
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
                (254, 232, 180), # 黄色框
                (255, 233, 177), # 黄色框
                (255, 233, 173),
                (254, 235, 179),
                (254, 232, 172),
                (254, 234, 179),
                (255, 237, 184),
                (253, 234, 178),
                (255, 229, 165),
                (253, 231, 167),
                (254, 236, 186),
                
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
                (249, 230, 188) 
            ]
            for road_color in road_color_rgb_lst_strict:
                road_map = roughly_equal_bool(img, road_color, diff_limit=5)
                final_map_bool = final_map_bool | road_map 
            final_map_bool = final_map_bool & legal_mask




            final_map = final_map_bool.astype(np.uint8)
            # 过滤小面积白色
            contours, hierarchy = cv2.findContours(final_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    cv2.drawContours(final_map, contour, contourIdx=-1, color=0, thickness=-1)
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
            #
            img_ = img.copy()
            img[final_map == 255] = (0, 0, 255)
            road_mask = (final_map == 255)
            color_img = (road_mask[:, :, None] * img_).astype(np.uint8)
            # cv2.imwrite(img_path.replace('.png', '_color_vis.png'), color_img)
            cv2.imwrite(img_path.replace('.png', '_bi.png'), final_map)
            # cv2.imwrite(img_path.replace('.png', '_vis.png'), img)               
        elif '_15_' in img_path:
            
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路中间
                (252, 252, 253), # 白色道路两边
                (253, 226, 147), # 深黄色背景
                (255, 240, 156), # 深黄色背景
                (248, 172, 5), # 深黄色边缘
                (253, 218, 124), # 深黄色边缘
                (250, 192, 56),
                (250, 211, 119),
                (249, 192, 63),
                (244, 198, 91),
                
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
                (249, 171, 0)
            ]
            for road_color in road_color_rgb_lst_strict:
                road_map = roughly_equal_bool(img, road_color, diff_limit=5)
                final_map_bool = final_map_bool | road_map 
            final_map_bool = final_map_bool & legal_mask




            final_map = final_map_bool.astype(np.uint8)
            # 过滤小面积白色
            contours, hierarchy = cv2.findContours(final_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    cv2.drawContours(final_map, contour, contourIdx=-1, color=0, thickness=-1)
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
            #
            img_ = img.copy()
            img[final_map == 255] = (0, 0, 255)
            road_mask = (final_map == 255)
            color_img = (road_mask[:, :, None] * img_).astype(np.uint8)
            # cv2.imwrite(img_path.replace('.png', '_color_vis.png'), color_img)
            cv2.imwrite(img_path.replace('.png', '_bi.png'), final_map)
            # cv2.imwrite(img_path.replace('.png', '_vis.png'), img)    
        elif '_14_' in img_path:
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路中间
                (252, 252, 253),  # 白色道路两边
                
                # (241, 242, 243),
                # (249, 250, 251),
                (253, 226, 147), # 深黄色背景
                (255, 240, 156), # 深黄色背景
                (248, 172, 5), # 深黄色边缘
                (253, 218, 124), # 深黄色边缘 
                (225, 225, 225), # 深灰色道路 7.2892782,80.623465-14-18_18_189779_125750.png         

            ]
            for road_color in road_color_rgb_lst:
                road_map = roughly_equal_bool(img, road_color, diff_limit=40)
                bi_img = bi_img | road_map
            bi_img = bi_img.astype(np.int) * 255

            # background颜色
            bi_img_bg = np.zeros(img.shape[:2], dtype=np.bool)
            bg_color_rgb_lst = [
                # 只有最常见的：
                (232, 234, 237), # 灰色背景
                (254, 232, 180), # 黄色框
                (255, 233, 177), # 黄色框
                (255, 229, 165),
                (255, 237, 185),
                (254, 236, 186)
                # 详细的：
                # (248, 249, 250), # 灰色背景
                # (241, 243, 244), # 深灰色小房子
                # (240, 244, 244), # 深灰色小房子
                # (225, 226, 229), # 深灰色小房子边缘
                # (229, 233, 233), # 深灰色小房子边缘
                # (225, 225, 229), # 深灰色小房子边缘
                # (237, 237, 237), # 深灰色小房子边缘
                # (236, 236, 236), # 深灰色小房子边缘
                # (228, 232, 232), # 深灰色小房子边缘
                # (255, 251, 240), # 浅黄色背景
                # (251, 232, 168), # 浅黄色边缘
                # (251, 240, 210), # 浅黄色边缘
                # (156, 192, 249), # 河流背景
                # (205, 221, 250), # 河流边缘
                # (162, 215, 177), # 绿色虚线
                # (167, 206, 180), # 绿色虚线边缘
            ]
            for bg_color in bg_color_rgb_lst:
                bg_map = roughly_equal_bool(img, bg_color, diff_limit=5)
                bi_img_bg = bi_img_bg | bg_map
            bi_img_bg = ~bi_img_bg
            bi_img_bg = bi_img_bg.astype(np.int) * 255


            final_map = (bi_img_bg.astype(np.bool) & bi_img.astype(np.bool)).astype(np.uint8)

            # 过滤小面积白色
            contours, hierarchy = cv2.findContours(final_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 15:
                    cv2.drawContours(final_map, contour, contourIdx=-1, color=0, thickness=-1)
            final_map = final_map.astype(np.int) * 255
            img[final_map == 255] = (0, 0, 255)
            cv2.imwrite(img_path.replace('.png', '_bi.png'), final_map)

    def genetare_osm_bi(self, img_path):
        min_area = -1
        if '_16_' in img_path:
            
              
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路中间
                (236, 236, 236),
                (234, 234, 234),
                (248, 248, 186), # 黄色道路
                # (213, 213, 155),
                (249, 214, 170), # 肉色
                # (211, 175, 124),
                (148, 212, 148), # 绿色
                (221, 159, 159), # 粉色
                (205, 204, 203), # 灰色
                (204, 204, 204)
                
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
                (204, 204, 204),
                (224, 194, 189), # 粉色边缘不要
                (222, 187, 186),
                (222, 198, 167), # 橙色边缘
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




            final_map = final_map_bool.astype(np.uint8)
            # 过滤小面积白色
            contours, hierarchy = cv2.findContours(final_map, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    cv2.drawContours(final_map, contour, contourIdx=-1, color=0, thickness=-1)
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
        elif '_17_' in img_path:
            
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路中间
                (236, 236, 236),
                (234, 234, 234),
                (248, 248, 186), # 黄色道路
                # (213, 213, 155),
                (249, 214, 170), # 肉色
                # (211, 175, 124),
                (148, 212, 148), # 绿色
                (221, 159, 159), # 粉色
                (205, 204, 203), # 灰色
                (204, 204, 204)
                
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
                (213, 209, 205)
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




            final_map = final_map_bool.astype(np.uint8)
            # 过滤小面积白色
            contours, hierarchy = cv2.findContours(final_map, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    cv2.drawContours(final_map, contour, contourIdx=-1, color=0, thickness=-1)
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
               
        elif '_15_' in img_path:
            
            img = cv2.imread(img_path)
            bi_img = np.zeros(img.shape[:2], dtype=np.bool)
            # road颜色
            road_color_rgb_lst = [
                (255, 255, 255), # 白色道路中间
                (236, 236, 236),
                (234, 234, 234),
                (248, 248, 186), # 黄色道路
                # (213, 213, 155),
                (249, 214, 170), # 肉色
                # (211, 175, 124),
                (148, 212, 148), # 绿色
                (221, 159, 159), # 粉色
                (205, 204, 203), # 灰色
                (204, 204, 204)
                
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




            final_map = final_map_bool.astype(np.uint8)
            # 过滤小面积白色
            contours, hierarchy = cv2.findContours(final_map, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area:
                    cv2.drawContours(final_map, contour, contourIdx=-1, color=0, thickness=-1)
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
            #
            img_ = img.copy()
            img[final_map == 255] = (0, 0, 255)
            road_mask = (final_map == 255)
            color_img = (road_mask[:, :, None] * img_).astype(np.uint8)
            # cv2.imwrite(img_path.replace('.png', '_color_vis.png'), color_img)
            kernel = np.ones((2, 2), dtype=np.uint8)
            final_map = cv2.morphologyEx(final_map.astype(np.uint8), cv2.MORPH_OPEN, kernel, 1)
            cv2.imwrite(img_path.replace('.png', '_bi.png'), final_map)

if __name__ == "__main__":
    bi = BiSystem()
    img_path = ('vis/6.0559339,80.1944874_15_whole_google.png')
    bi.genetare_osm_bi(img_path)
    bi_img_path = img_path.replace('.png', '_bi.png')               
    print(bi_img_path)
