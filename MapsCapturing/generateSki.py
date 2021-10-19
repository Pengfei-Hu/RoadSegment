import cv2
import pandas as pd
from skimage import morphology
import numpy as np
import glob
from pandas import DataFrame
import os
import tqdm

map_color_width_info = {
    'google': {
        "name": ['yellow_10', 'yellow_17', 'white_5', 'white_10', 'white_20'],
        "width": [10, 17, 5, 10, 20],
        "color": ['yellow', 'yellow', 'white', 'white', 'white'],  # rgb
        "color_name": {'yellow':(255, 242, 175), 'white':(255, 255, 255)},
        "name_map": {
            'yellow_10':'free_way', 'yellow_17':'free_way', 'white_20':'trunk', 
            'white_10':'primary_roads', 'white_5':'residential_roads'
        }
    },
    'bing': {
        "name": ['orange_11', 'yellow_7', 'purple_12' 'white_4', 'white_8', 'grey_18', 'mid_white_4', 'grey_5'],
        "width": [11, 7, 12, 4, 8, 18, 4, 5],
        "color": ['orange', 'yellow', 'purple', 'white', 'white', 'grey', 'mid_white', 'grey'],  # rgb
        "color_name": {'orange':(255, 244, 171), 'yellow':(255, 254, 2379), 'white':(255, 255, 255), 'purple':(233, 211, 250), 'grey':(217, 215, 210), 'mid_white':(232, 231, 226)},
        "name_map": {
            'grey_18':'provincial_boundariy', 'grey_5':'railway', 'mid_white_4':'unclassied roads',
            'orange_11':'freeway', 'yellow_7':'freeway', 'purple':'freeway', 'white_8':'trunks', 'white_4':'primary_roads'
        }
    },
    'osm': {
        "name": ['white_4','white_10', 'white_16', 'pink', 'orange', 'yellow', 'green'],
        "width": [4, 10, 16, None, None, None, None, None],
        "color": ['white', 'white', 'white', 'pink', 'orange', 'yellow', 'green'],  # rgb
        "color_name": {'pink':(221, 159, 159), 'orange':(249, 214, 170), 'green':(148, 212, 148),
        'yellow':(248, 248, 186), 'white':(255, 255, 255)},
        "name_map": {
            'pink':'free_way', 'orange':'free_way',  'green':'free_way', 'yellow':'trunk', 
            'white_16':'trunk', 'white_10':'primary_roads', 'white_4':'residential_roads'            
        }        
    }    
}

def generate_excel(header, data, xlsx_path):
    df = DataFrame(data, columns=header)
    df.to_excel(xlsx_path, index=False)

def sum_around(skeleton_pad):
    up = np.pad(skeleton_pad, ((1, 0), (0, 0)), 'constant', constant_values=0)[:-1, :]
    down = np.pad(skeleton_pad, ((0, 1), (0, 0)), 'constant', constant_values=0)[1:, :]
    left = np.pad(skeleton_pad, ((0, 0), (1, 0)), 'constant', constant_values=0)[:, :-1]
    right = np.pad(skeleton_pad, ((0, 0), (0, 1)), 'constant', constant_values=0)[:, 1:]
    left_up = np.pad(skeleton_pad, ((1, 0), (1, 0)), 'constant', constant_values=0)[:-1, :-1] # 处理左上方块
    left_down = np.pad(skeleton_pad, ((0, 1), (1, 0)), 'constant', constant_values=0)[1:, :-1]
    right_up = np.pad(skeleton_pad, ((1, 0), (0, 1)), 'constant', constant_values=0)[:-1, 1:]
    right_down = np.pad(skeleton_pad, ((0, 1), (0, 1)), 'constant', constant_values=0)[1:, 1:]
    sum_map = up + down + left + right + left_up + left_down + right_down + right_up + skeleton_pad
    return sum_map

def skeleton_gen(img):
    img[img == 255] = 1
    print(np.unique(img))
    skeleton0 = morphology.skeletonize(img)
    skeleton = skeleton0.astype(np.uint8)*255
    return skeleton

def get_road_intersection(skeleton):
    skeleton_pad = skeleton.astype(np.int)
    sum_map = sum_around(skeleton_pad)
    node_map = (sum_map >= 4 * 255) & skeleton.astype(np.bool)
    node_map_grey = node_map.astype(np.uint8) * 255
    node_idx = np.where(node_map)
    num_nodes, labels, stats, centroids = cv2.connectedComponentsWithStats(node_map_grey, connectivity=8)
    node_center_cor_lst = []
    for node_i in range(1, num_nodes):
        node_idx = np.where(labels == node_i)
        node_pts = np.array(node_idx).T # ((y1, x1), (y2, x2)...)
        dis_lst = []
        for pt_i in range(len(node_pts)):
            pt = node_pts[pt_i]
            distance = pt - node_pts
            dis_sum = np.abs(distance).sum()
            dis_lst.append(dis_sum)
        center_i = np.array(dis_lst).argmin()
        node_center_cor_lst.append(node_pts[center_i])
    
    node_center_bgr_skeleton = cv2.cvtColor(skeleton, cv2.COLOR_GRAY2BGR)
    for node_center_cor in node_center_cor_lst: 
        node_center_bgr_skeleton[node_center_cor[0], node_center_cor[1]] = (0, 0, 255)
        cv2.circle(node_center_bgr_skeleton, tuple(reversed(node_center_cor)), 5, (0, 255, 255), 2) # cv2.circle: (x, y)
    return node_center_bgr_skeleton, node_center_cor_lst # (y, x)

def get_subroad_info(skeleton, skeleton_node_cor_lst, img, gray, mask_path):
    if skeleton_node_cor_lst != []:
        node_cor = np.array(skeleton_node_cor_lst)
        # 交点附近grey赋1，skeleton赋0
        num_ignore = 2
        node_cor_lst = [node_cor + [i, j] for i in range(-num_ignore, num_ignore) for j in range(-num_ignore, num_ignore)]
        node_cor_heavy_lst = [node_cor + [i, j] for i in range(-num_ignore, num_ignore) for j in range(-num_ignore, num_ignore)]
        node_cor_lst = [np.clip(a, 0, 255) for a in node_cor_lst]
        node_cor_heavy_lst = [np.clip(a, 0, 255) for a in node_cor_heavy_lst]
        for node_cor in node_cor_lst:
            for pt in node_cor:
                skeleton[pt[0], pt[1]] = 0
        for node_cor in node_cor_heavy_lst:
            for pt in node_cor:
                gray[pt[0], pt[1]] = 1
    else:
        num_ignore = 0                
    # cv2.imwrite('skeleton.png', skeleton)
    # cv2.imwrite('gray.png', gray * 255)
    # 连通域排序
    num_nodes, labels, stats, centroids = cv2.connectedComponentsWithStats(skeleton, connectivity=8)
    subroad_pts_lst = []
    for node_i in range(1, num_nodes):
        node_idx = np.where(labels == node_i)
        node_pts = np.array(node_idx).T # ((y1, x1), (y2, x2)...)
        mean_pt = node_pts.mean(axis=0) # (y, x)
        subroad_pts_lst.append([node_pts, mean_pt[0] * 1000 + mean_pt[1]])
    sort_subroad_pts_lst = sorted(subroad_pts_lst, key=lambda x:x[1])
    sort_subroad_pts_lst = [t[0] for t in sort_subroad_pts_lst]
    # subroad长度
    subroad_len_lst = []
    for subroad_i in range(len(sort_subroad_pts_lst)):
        subroad_pts = sort_subroad_pts_lst[subroad_i]
        subroad_len = len(subroad_pts) + num_ignore
        subroad_len_lst.append(subroad_len)
    # subroad宽度
    bg_pts = np.where(gray == 0)
    bg_pts = np.array(bg_pts).T # ((y1, x1), (y2, x2)...)
    bg_pts = bg_pts[None, ...]
    subroad_width_lst = []
    for subroad_pts in sort_subroad_pts_lst:
        subroad_pts = subroad_pts[:, None, :]
        if bg_pts.shape[1] <= 256 * 256:
            dis_matrix = np.linalg.norm(bg_pts - subroad_pts, ord=2, axis=2)
            min_dis = np.min(dis_matrix, axis=1)
        else:
            min_dis = np.zeros(subroad_pts.shape[0])
            subroad_pts_lst_unit = subroad_pts.shape[0] // 16
            subroad_pts_lst = [subroad_pts[i*subroad_pts_lst_unit:(i+1)*subroad_pts_lst_unit, 0, :] for i in range(16)]            
            for i, subroad_pts_part in enumerate(subroad_pts_lst):
                dis_matrix_part = np.linalg.norm(bg_pts - subroad_pts_part[:, None, :], ord=2, axis=2)
                min_dis_part = np.min(dis_matrix_part, axis=1)
                min_dis[i*subroad_pts_lst_unit:(i+1)*subroad_pts_lst_unit] = min_dis_part
        start, end = 3/10, 7/10
        dis_lst = np.sort(min_dis)
        if len(dis_lst) > 1:
            dis_lst = np.sort(min_dis)[int(start * len(min_dis)):int(end * len(min_dis))]
        subroad_width_lst.append(np.mean(dis_lst) * 2)


    # 根据颜色与宽度判断道路类别
    map_type = 'google' if 'google' in mask_path else 'osm' if 'osm' in mask_path else 'bing'
    map_provide_info = map_color_width_info[map_type]
    subroad_name_lst = []
    if map_type == 'google':
        for subroad_i, subroad_pts in enumerate(sort_subroad_pts_lst):
            cor_y = subroad_pts[:, 0]
            cor_x = subroad_pts[:, 1]
            subimg_bgr = np.mean(img[cor_y, cor_x], axis=0)
            # 获得颜色
            min_color_dis, subimg_color_name = 1e9, 'white'
            for color_name, rgb in map_provide_info['color_name'].items():
                bgr = rgb[::-1]
                color_dis = np.linalg.norm(subimg_bgr - bgr)
                if color_dis < min_color_dis:
                    subimg_color_name = color_name
                    min_color_dis = color_dis
            # 颜色+宽度分类
            min_width_dis, min_width_idx = 1e9, 0
            for type_i, road_typename in enumerate(map_provide_info['name']):
                if subimg_color_name not in road_typename:
                    continue
                width_dis = abs(map_provide_info['width'][type_i] - subroad_width_lst[subroad_i])
                if width_dis < min_width_dis:
                    min_width_dis = width_dis
                    min_width_idx = type_i
            subroad_name = map_provide_info['name'][min_width_idx]
            subroad_name_lst.append(subroad_name)
    elif map_type == 'bing':
        for subroad_i, subroad_pts in enumerate(sort_subroad_pts_lst):
            cor_y = subroad_pts[:, 0]
            cor_x = subroad_pts[:, 1]
            subimg_bgr = np.mean(img[cor_y, cor_x], axis=0)
            # 获得颜色
            min_color_dis, subimg_color_name = 1e9, 'white'
            for color_name, rgb in map_provide_info['color_name'].items():
                bgr = rgb[::-1]
                color_dis = np.linalg.norm(subimg_bgr - bgr)
                if color_dis < min_color_dis:
                    subimg_color_name = color_name
                    min_color_dis = color_dis
            # 颜色+宽度分类
            min_width_dis, min_width_idx = 1e9, 0
            for type_i, road_typename in enumerate(map_provide_info['name']):
                if subimg_color_name not in road_typename:
                    continue
                width_dis = abs(map_provide_info['width'][type_i] - subroad_width_lst[subroad_i])
                if width_dis < min_width_dis:
                    min_width_dis = width_dis
                    min_width_idx = type_i
            subroad_name = map_provide_info['name'][min_width_idx]         
            subroad_name_lst.append(subroad_name)
    elif map_type == 'osm':
        for subroad_i, subroad_pts in enumerate(sort_subroad_pts_lst):
            cor_y = subroad_pts[:, 0]
            cor_x = subroad_pts[:, 1]
            subimg_bgr = np.mean(img[cor_y, cor_x], axis=0)
            # 获得颜色
            min_color_dis, subimg_color_name = 1e9, 'white'
            for color_name, rgb in map_provide_info['color_name'].items():
                bgr = rgb[::-1]
                color_dis = np.linalg.norm(subimg_bgr - bgr)
                if color_dis < min_color_dis:
                    subimg_color_name = color_name
                    min_color_dis = color_dis
            # 颜色+宽度分类
            if subimg_color_name == 'white':
                min_width_dis, min_width_idx = 1e9, 0
                for type_i, road_typename in enumerate(map_provide_info['name']):
                    if subimg_color_name not in road_typename:
                        continue
                    width_dis = abs(map_provide_info['width'][type_i] - subroad_width_lst[subroad_i])
                    if width_dis < min_width_dis:
                        min_width_dis = width_dis
                        min_width_idx = type_i
                subroad_name = map_provide_info['name'][min_width_idx]         
                subroad_name_lst.append(subroad_name)
            else:
                for type_i, road_typename in enumerate(map_provide_info['name']):
                    if subimg_color_name in road_typename:
                        subroad_name = road_typename
                        break      
                subroad_name_lst.append(subroad_name)                

    avail_road_type = np.unique(np.array(subroad_name_lst)).tolist()
    avail_road_length = [0 for _ in range(len(avail_road_type))]
    for road_i in range(len(sort_subroad_pts_lst)):
        road_type = subroad_name_lst[road_i]
        road_type_idx = avail_road_type.index(road_type)
        road_len = subroad_len_lst[road_i]
        avail_road_length[road_type_idx] = avail_road_length[road_type_idx] + road_len
    subroad_info = {'road_type':avail_road_type, 'road_length':avail_road_length, 'road_length_meter':'', 'total_road_length_meter':'', 'total_road_length':[sum(avail_road_length)] + ['' for _ in range(len(avail_road_length) - 1)]}
    if len(subroad_info['road_length']) == 0:
        subroad_info['total_road_length'] = ''
    else:
        subroad_info['total_road_length_meter'] = ['' for _ in range(len(subroad_info['total_road_length']))]
        subroad_info['total_road_length_meter'][0] = subroad_info['total_road_length'][0] * 2.3887
        subroad_info['road_length_meter'] = [t * 2.3887 for t in subroad_info['road_length']]
    if len(subroad_info['road_length']) != 0:
        subroad_info['road_name'] = [map_provide_info['name_map'][t] for t in subroad_info['road_type']]
    else:
        subroad_info['road_name'] = ''
    return subroad_info
    
def get_lat_long(skeleton_node_cor_lst, lat_long):
    if skeleton_node_cor_lst:
        lat_long =  [eval(t) for t in lat_long]
        lat, long = lat_long[0], [1] # lat:经度, long:纬度
        skeleton_node_cor_lst = np.array(skeleton_node_cor_lst) # (y, x)
        skeleton_node_cor_lst[:, 0] = 256 - skeleton_node_cor_lst[:, 0]
        dis = skeleton_node_cor_lst - [127.5, 127.5]
        long_lat_unit = np.array([8.993216192195822e-6, 1.141255544679108e-5])
        long_lat_delta = long_lat_unit * dis
        lat_long_lst = np.array(lat_long) + long_lat_delta[:, ::-1]
        return lat_long_lst.tolist()
    else: 
        return ''

if __name__ == "__main__":
    img_dir = r'map/google'
    img_paths = []
    for root, dirs, files in os.walk(img_dir):
        for file in files:
            if 'bing' not in file:
                if 'vis' in file or '_bi' not in file:
                    continue
            else:
                if 'vis' in file or 'bing_bi' not in file:
                    continue                
            img_paths.append(os.path.join(root, file))
    
    # img_paths = ['17.02527268537679,54.052734375_16_whole_osm_bi.png']
    for mask_path in tqdm.tqdm(img_paths):
        img_path = mask_path.replace('_bi.png', '.png')
        img = cv2.imread(img_path)
        mask = cv2.imread(mask_path)
        gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        skeleton = skeleton_gen(gray)
        skeleton_node, skeleton_node_cor_lst = get_road_intersection(skeleton)
        skeleton_node_lat_long_lst = get_lat_long(skeleton_node_cor_lst, os.path.basename(mask_path).split('_')[0].split(','))
        _data = {'total_junction_num':[len(skeleton_node_cor_lst)] + ['' for _ in range(len(skeleton_node_cor_lst) - 1)], 'junction_coordinate':skeleton_node_cor_lst, 'lat_long':skeleton_node_lat_long_lst}
        if len(skeleton_node_cor_lst) == 0:
            _data['total_junction_num'] = ''
            _data['lat_long'] = ''
        generate_excel(
            header=['total_junction_num', 'junction_coordinate', 'lat_long'], 
            data=_data,
            xlsx_path=mask_path.replace('_bi.png', '_junction.xlsx')
        )
        subroad_info = get_subroad_info(skeleton, skeleton_node_cor_lst, img, gray, mask_path)

        generate_excel(
            header=['road_type', 'road_name', 'road_length', 'road_length_meter', 'total_road_length',  'total_road_length_meter'], 
            data=subroad_info,
            xlsx_path=mask_path.replace('_bi.png', '_road_info.xlsx')
        )        
        cv2.imwrite(mask_path.replace('bi.png', 'bi_vis.png'), skeleton_node)




        

    