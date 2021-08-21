import requests
from bing import TileSystem
import sqlite_util as db
import PIL.Image as Image
import uuid

t = TileSystem()
# 

#ZOOM，从1到18
tileZoom = 10
#纬度
lat = 47.6205487650771
#经度
lon = -122.3492975182217


def get_uuid():
    idd = str(uuid.uuid1())
    return idd.replace('-','')

def download_tile(xtile, ytile, tileZoom, source):
    qkStr = t.TileXYToQuadKey(xtile, ytile, tileZoom)
    if source == 'bing':
        url = 'http://ecn.t0.tiles.virtualearth.net/tiles/r' + qkStr + '.png?g=604'
    elif source == 'google':
        url = 'http://mt0.google.com/vt/lyrs=m@174000000&src=app&x={}&s=&y={}&z={}'.format(xtile,ytile,tileZoom)
    else:
        url = 'https://a.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom,xtile,ytile)
    response = requests.get(url, stream=True)
    assert response.status_code == 200, "connect error"
    print('DOWNLOAD {} SUCCESS'.format(source))
    capture_id = get_uuid()
    pic_name = 'map/{}/{}.png'.format(source, capture_id)
    with open(pic_name, 'wb') as out_file:
        out_file.write(response.content)
    return capture_id, pic_name

def multi_pic_whole(lat, lon, tileZoom, multi, source):
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    qkStr = t.TileXYToQuadKey(tx, ty, tileZoom)
    start = qkStr + '0' * multi
    end = qkStr + '3' * multi
    start_tx, start_ty = t.QuadKeyToTileXY(start)
    end_tx, end_ty = t.QuadKeyToTileXY(end)
    loc = 0
    transfer_loc_part = {}
    for ty in range(start_ty, end_ty + 1):
        for tx in range(start_tx, end_tx + 1):
            new_qkStr = t.TileXYToQuadKey(tx, ty, tileZoom + multi)
            part_list = new_qkStr[-multi:]
            transfer_loc_part[loc] = part_list
            if source == 'google':
                url = 'http://mt0.google.com/vt/lyrs=m@174000000&src=app&x={}&s=&y={}&z={}'.format(tx,ty,tileZoom + multi)
            elif source == 'bing':
                url = 'http://ecn.t0.tiles.virtualearth.net/tiles/r{}.png?g=604'.format(new_qkStr)
            elif source == 'osm':
                url = 'https://a.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom + multi,tx,ty)
            else:
                return "error"
            response = requests.get(url, stream=True)
            assert response.status_code == 200, "connect error"
            print('DOWNLOAD {} SUCCESS'.format(loc))
            pic_name = 'map/{}/combine/single/{}.png'.format(source, loc)
            # Save Images
            with open(pic_name, 'wb') as out_file:
                out_file.write(response.content)
            loc += 1
    # Merge
    IMAGE_SIZE = 256  #   Image size is 256*256
    IMAGE_ROW = 2 ** multi  # The row of image
    IMAGE_COLUMN = 2 ** multi # The column of image
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE)) #创建一个新图
    i = 0
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open('map/{}/combine/single/{}.png'.format(source,i))
            to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
            i += 1
    pic_url = 'map/{}/combine/{}.png'.format(source, get_uuid())
    to_image.save(pic_url) # 保存新图
    return pic_url, transfer_loc_part

def multi_pic_part(lat, lon, tileZoom, multi, source, part):
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    qkStr = t.TileXYToQuadKey(tx, ty, tileZoom)
    start = qkStr + '0' * multi
    end = qkStr + '3' * multi
    start_tx, start_ty = t.QuadKeyToTileXY(start)
    end_tx, end_ty = t.QuadKeyToTileXY(end)
    loc = 0
    for ty in range(start_ty, end_ty + 1):
        for tx in range(start_tx, end_tx + 1):
            if source == 'google':
                url = 'http://mt0.google.com/vt/lyrs=m@174000000&src=app&x={}&s=&y={}&z={}'.format(tx,ty,tileZoom + multi)
            elif source == 'bing':
                new_qkStr = t.TileXYToQuadKey(tx, ty, tileZoom + multi)
                url = 'http://ecn.t0.tiles.virtualearth.net/tiles/r{}.png?g=604'.format(new_qkStr)
            elif source == 'osm':
                url = 'https://a.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom + multi,tx,ty)
            else:
                return "error"
            response = requests.get(url, stream=True)
            assert response.status_code == 200, "connect error"
            print('DOWNLOAD {} SUCCESS'.format(loc))
            pic_name = 'map/{}/combine/single/{}.png'.format(source, loc)
            # Save Images
            with open(pic_name, 'wb') as out_file:
                out_file.write(response.content)
            loc += 1
    # Merge
    IMAGE_SIZE = 256  #   Image size is 256*256
    IMAGE_ROW = 2 ** multi  # The row of image
    IMAGE_COLUMN = 2 ** multi # The column of image
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE)) #创建一个新图
    i = 0
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open('map/{}/combine/single/{}.png'.format(source,i))
            to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
            i += 1
    pic_url = 'map/{}/combine/{}_{}_{} {}.png'.format(source, lat, lon, tileZoom, multi)
    to_image.save(pic_url) # 保存新图
    # 切割成四份
    four_name = ['left-top', 'right-top', 'left-bottom', 'right-bottom']
    img = Image.open(pic_url)
    size_img = img.size
    weight = int(size_img[0] // 2)
    height = int(size_img[1] // 2)
    i = 0
    capture_id = get_uuid()
    for j in range(2):
        for k in range(2):
            box = (weight * k, height * j, weight * (k + 1), height * (j + 1))
            region = img.crop(box)
            # 输出路径
            tmp_url = 'map/{}/combine/{}_{}.png'.format(source, capture_id, four_name[i])
            region.save(tmp_url)
            i += 1
    dic ={'UL':'left-top', 'UR':'right-top', 'LL':'left-bottom', 'LR':'right-bottom'}
    result = 'map/{}/combine/{}_{}.png'.format(source, capture_id, dic[part])   
    return result

def multi_pic_single(lat, lon, tileZoom, multi, source, part_list):
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    qkStr = t.TileXYToQuadKey(tx, ty, tileZoom)
    new_qkr = qkStr + part_list
    print(new_qkr)
    new_tx, new_ty = t.QuadKeyToTileXY(new_qkr)
    if source == 'google':
        url = 'http://mt0.google.com/vt/lyrs=m@174000000&src=app&x={}&s=&y={}&z={}'.format(new_tx,new_ty,tileZoom + multi)
    elif source == 'bing':
        url = 'http://ecn.t0.tiles.virtualearth.net/tiles/r{}.png?g=604'.format(new_qkr)
    elif source == 'osm':
        url = 'https://a.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom + multi,new_tx,new_ty)
    else:
        return "error"
    response = requests.get(url, stream=True)
    assert response.status_code == 200, "connect error"
    print('DOWNLOAD {} SUCCESS'.format(part_list))
    pic_name = 'map/{}/combine/single/{}.png'.format(source, part_list)
    # Save Images
    with open(pic_name, 'wb') as out_file:
        out_file.write(response.content)
    part_list = list(map(int,part_list))
    return pic_name


HOST = 'uwtset1.tacoma.uw.edu'
USER = 'mapsuser'
PWD = 'mapsuser'
BASE = 'mapsvisions'
MSSQL = db.MSSQL(HOST,USER,PWD,BASE)
lat = 1.0
lon = 1.0
map_provider = "B"
capture_url = "12313"


print(MSSQL.select_map_part(47,-122, 16,2,'00'))


