from flask import Flask, jsonify, request
import requests
from bing import TileSystem
import sqlite_util as db
import PIL.Image as Image
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app, supports_credentials=True)
t = TileSystem()
# 
HOST = 'uwtset1.tacoma.uw.edu'
USER = 'mapsuser'
PWD = 'mapsuser'
BASE = 'mapsvisions'
MSSQL = db.MSSQL(HOST,USER,PWD,BASE)
MSSQL.GetConnect()

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

def multi_pic(lat, lon, tileZoom, multi, source):
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
    to_image.save('map/{}/combine/{}_{}_{} {}.png'.format(source, lat, lon, tileZoom, multi)) # 保存新图
    capture_id = get_uuid()
    result = []
    pic_url = 'map/{}/combine/{}.png'.format(source, capture_id)
    result.append(pic_url)
    # 切割成四份
    four_name = ['left-top', 'right-top', 'left-bottom', 'right-bottom']
    img = Image.open(pic_url)
    size_img = img.size
    weight = int(size_img[0] // 2)
    height = int(size_img[1] // 2)
    i = 0
    for j in range(2):
        for k in range(2):
            box = (weight * k, height * j, weight * (k + 1), height * (j + 1))
            region = img.crop(box)
            # 输出路径
            tmp_url = 'map/{}/combine/{}_{}'.format(source, capture_id, four_name[i])
            region.save(tmp_url)
            result.append(tmp_url)
            i += 1
    return result
 
@app.route('/pic')
def download_pic():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom =int(request.args["tileZoom"])
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    #bing
    bing_id, bing_pic = download_tile(tx, ty, tileZoom, 'bing')
    location_photos.inser_map(bing_id, lat, lon, 'B', bing_pic)
    #google
    google_id, google_pic = download_tile(tx, ty, tileZoom, 'google')
    location_photos.inser_map(google_id, lat, lon, 'G', google_pic)
    #osm
    osm_id, osm_pic = download_tile(tx, ty, tileZoom, 'osm')
    location_photos.inser_map(osm_id, lat, lon, 'O', osm_pic)
    result = {'bing': bing_pic, 'google': google_pic, 'osm': osm_pic}

    return jsonify(result)

@app.route('/multi')
def multi():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom = int(request.args["tileZoom"])
    multi = int(request.args["multi"])
    bing_urls = multi_pic(lat, lon, tileZoom, multi, 'bing')
    google_urls = multi_pic(lat, lon, tileZoom, multi, 'google')
    osm_urls = multi_pic(lat, lon, tileZoom, multi, 'osm')
    result = {'bing':bing_urls,'google':google_urls,'osm':osm_urls}

    return jsonify(result)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()





