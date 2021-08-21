from os import error
from flask import Flask, jsonify, request
import requests
from bing import TileSystem
import sqlite_util as db
import PIL.Image as Image
from flask_cors import CORS
import uuid
import googlemaps
import pandas as pd
import numpy as np
import json

app = Flask(__name__)
#app = Flask(__name__, static_folder="map")
CORS(app, supports_credentials=True)
t = TileSystem()

HOST = 'uwtset1.tacoma.uw.edu'
USER = 'mapsuser'
PWD = 'mapsuser'
BASE = 'mapsvisions'
location_photos = db.MSSQL(HOST,USER,PWD,BASE)

def get_uuid():
    idd = str(uuid.uuid1())
    return idd.replace('-','')


def download_tile(lat, lon, tileZoom, source):
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    qkStr = t.TileXYToQuadKey(tx, ty, tileZoom)
    if source == 'bing':
        url = 'http://ecn.t0.tiles.virtualearth.net/tiles/r' + qkStr + '.png?g=604'
    elif source == 'google':
        url = 'http://mt0.google.com/vt/lyrs=m@174000000&src=app&x={}&s=&y={}&z={}'.format(tx,ty,tileZoom)
    else:
        url = 'https://a.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom,tx,ty)
    response = requests.get(url, stream=True)
    assert response.status_code == 200, "connect error"
    print('DOWNLOAD {} SUCCESS'.format(source))
#   capture_id = get_uuid()
    pic_name = 'map/{}/{}_{}_{}_{}.png'.format(source, lat, lon, tileZoom, "whole")
    
    with open(pic_name, 'wb') as out_file:
        out_file.write(response.content)
        print(response.content)
    return pic_name

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
                new_qkStr = t.TileXYToQuadKey(tx, ty, tileZoom + multi)
                url = 'http://ecn.t0.tiles.virtualearth.net/tiles/r{}.png?g=604'.format(new_qkStr)
            elif source == 'osm':
                url = 'https://a.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom + multi,tx,ty)
            else:
                return "error"
            response = requests.get(url, stream=True)
            assert response.status_code == 200, "connect error"
            print('DOWNLOAD {} SUCCESS'.format(loc))
            pic_name = 'map/{}/{}_{}_{}_{}.png'.format(source, lat, lon, tileZoom + multi, loc)
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
            from_image = Image.open('map/{}/{}_{}_{}_{}.png'.format(source, lat, lon, tileZoom + multi, i))
            to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
            i += 1
    pic_url = 'map/{}/test/{}_{}_{}_{}.png'.format(source, lat, lon, tileZoom + multi, "whole")
    to_image.save(pic_url) # 保存新图
    return pic_url, transfer_loc_part
#    return transfer_loc_part

def multi_pic_part(lat, lon, tileZoom, multi, source, part_list):
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    qkStr = t.TileXYToQuadKey(tx, ty, tileZoom)
    new_qkr = qkStr + part_list
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
    pic_name = 'map/{}/{}.png'.format(source, part_list)
    # Save Images
    with open(pic_name, 'wb') as out_file:
        out_file.write(response.content)
    part_list = list(map(int,part_list))
    return pic_name
 
@app.route('/pic')
def download_pic():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom =int(request.args["tileZoom"])
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    #bing
    _, bing_pic = download_tile(tx, ty, tileZoom, 'bing')
    location_photos.inser_map(lat, lon, 'B', bing_pic)
    #google
    _, google_pic = download_tile(tx, ty, tileZoom, 'google')
    location_photos.inser_map(lat, lon, 'G', google_pic)
    #osm
    _, osm_pic = download_tile(tx, ty, tileZoom, 'osm')
    location_photos.inser_map(lat, lon, 'O', osm_pic)
    result = {'bing': bing_pic, 'google': google_pic, 'osm': osm_pic}
    return jsonify(result)


@app.route('/multi/part')
def multi_part():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom = int(request.args["tileZoom"])
    endZoomLevel = int(request.args["endzoomLevel"])
    part_list = request.args['partlist']
    #BING
    bing_urls = multi_pic_part(lat, lon, tileZoom, endZoomLevel, 'bing', part_list)
    location_photos.inser_map_part(lat, lon, 'B', tileZoom, bing_urls, part_list, endZoomLevel)
    #GOOGLE
    google_urls = multi_pic_part(lat, lon, tileZoom, endZoomLevel, 'google', part_list)
    location_photos.inser_map_part(lat, lon, 'G', tileZoom, google_urls, part_list, endZoomLevel)
    #OSM
    osm_urls = multi_pic_part(lat, lon, tileZoom, endZoomLevel, 'osm', part_list)
    location_photos.inser_map_part(lat, lon, 'O', tileZoom, osm_urls, part_list, endZoomLevel)
    result = {'bing':bing_urls,'google':google_urls,'osm':osm_urls}
    return jsonify(result)

@app.route('/multi/all')
def multi_all():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom = int(request.args["startz"])
    endZoomLevel = int(request.args["endz"])
    multi = endZoomLevel
    
    for endZoomLevel in range(1, multi + 1):
        bing_result, dic = multi_pic_whole(lat, lon, tileZoom, endZoomLevel, 'bing')
        bing_url = 'map/{}/{}_{}_{}_'.format('bing', lat, lon, tileZoom + endZoomLevel)
        location_photos.inser_map_all(lat, lon, 'B', tileZoom, bing_url,endZoomLevel,dic)
        bing_whole = download_tile(lat, lon, tileZoom,'bing')
        bing_name = 'map/{}/{}_{}_{}_{}.png'.format('bing', lat, lon, tileZoom + endZoomLevel, "whole")
        location_photos.inser_map_whole(lat, lon, 'B', tileZoom, bing_name, endZoomLevel)
        bing_original = 'map/{}/{}_{}_{}_{}.png'.format('bing', lat, lon, tileZoom, "whole")
        location_photos.inser_map_original(lat, lon, 'B', tileZoom, bing_original)

    
        google_result, dic = multi_pic_whole(lat, lon, tileZoom, endZoomLevel, 'google')
        google_url = 'map/{}/{}_{}_{}_'.format('google', lat, lon, tileZoom + endZoomLevel)
        location_photos.inser_map_all(lat, lon, 'G', tileZoom, google_url,endZoomLevel, dic)
        google_whole = download_tile(lat, lon, tileZoom,'google')
        google_name = 'map/{}/{}_{}_{}_{}.png'.format('google', lat, lon, tileZoom + endZoomLevel, "whole")
        location_photos.inser_map_whole(lat, lon, 'G', tileZoom, google_name, endZoomLevel)
        google_original = 'map/{}/{}_{}_{}_{}.png'.format('google', lat, lon, tileZoom, "whole")
        location_photos.inser_map_original(lat, lon, 'G', tileZoom, google_original)

   
        osm_result, dic = multi_pic_whole(lat, lon, tileZoom, endZoomLevel, 'osm')
        osm_url = 'map/{}/{}_{}_{}_'.format('osm', lat, lon, tileZoom + endZoomLevel)
        location_photos.inser_map_all(lat, lon, 'O', tileZoom, osm_url,endZoomLevel,dic)
        osm_whole = download_tile(lat, lon, tileZoom,'osm')
        osm_name = 'map/{}/{}_{}_{}_{}.png'.format('osm', lat, lon, tileZoom + endZoomLevel, "whole")
        location_photos.inser_map_whole(lat, lon, 'O', tileZoom, osm_name, endZoomLevel)
        osm_original = 'map/{}/{}_{}_{}_{}.png'.format('osm', lat, lon, tileZoom, "whole")
        location_photos.inser_map_original(lat, lon, 'O', tileZoom, osm_original)

    result = {'bing':bing_result,'google':google_result,'osm':osm_result}
    results = {'bing':bing_whole,'google':google_whole,'osm':osm_whole}
    return jsonify(result, results)
    

@app.route('/multi/select')
def multi_select():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom = request.args["startz"]
    endZoomLevel = request.args["endz"]
    part_list = request.args['partlist']
    result = location_photos.select_map_part(lat,lon, tileZoom, endZoomLevel, part_list)
    return jsonify(result)

@app.route('/multi/go')
def multi_go():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom = int(request.args["startz"])
    endZoomLevel = int(request.args["endz"])
    part_list = 'whole'
    result = location_photos.select_map_part(lat,lon, tileZoom, endZoomLevel, part_list)
    print("result")
    print(result)
    return jsonify(result)

@app.route('/geocoding')
def geocoding():
    lat = request.args["lat"]
    lon = request.args["lon"]
    gmaps=googlemaps.Client(key='AIzaSyAhRnxOf_ELnG-vuGw3l0Sc_8uyBtvRZS4')
    
    reverse_geocode_result = gmaps.reverse_geocode((lat, lon))
    result = reverse_geocode_result[4]["formatted_address"]
    
    return json.dumps(result)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()





