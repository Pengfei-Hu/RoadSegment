import os
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
from generateBi import BiSystem
import sys
from generateSki import *
import cv2

#app = Flask(__name__)
app = Flask(__name__, static_folder="map")
CORS(app, supports_credentials=True)
t = TileSystem()
bi = BiSystem()

HOST = 'uwtset1.tacoma.uw.edu'
USER = 'mapsuser'
PWD = 'mapsuser'
BASE = 'mapsvisions'
location_photos = db.MSSQL(HOST,USER,PWD,BASE)
BINGMAP_URLWITHKEY = url = 'https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/latitude,longitude/zoomLevel?mapLayer=Basemap&format=png&mapMetadata=0&key=AofpOSpDDFfDdakQfgd1kEx7-uaOH1yokGbBf_pgLyFCfAJ5Lkkx7UdpzPngObmC'

def get_uuid():
    idd = str(uuid.uuid1())
    return idd.replace('-','')


def get_Insert_id():
    id = location_photos.get_Next_id()
    return id



def updateLocationAddress(lat, lng):
    address =location_photos.get_geocoding(lat, lng)
    no= location_photos.updateAddressOfLatLng(lat, lng, address)
    return json.dumps(no)


def download_google_tiles(url, lat,lon,tileZoom, quarter ,main_capture_id ):
    #url = 'https://mts1.google.com/vt/lyrs=m@186112443&hl=en&src=app&x=1485&s=&y=985&z=11'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    tiles_urls = "["
    #capture_id = get_Insert_id()
    for x in range(1,5):
        current_url = url
        current_url = current_url+"&scale="+str(x)
        print(current_url)
        pic_name = 'map/google/{}-{}-{}-{}-{}-{}-g.png'.format(lat, lon, tileZoom,quarter ,main_capture_id,str( x*256) )
        response = requests.get(current_url, stream=True, headers=headers)
        with open(pic_name, 'wb') as out_file:
            out_file.write(response.content)
        data= {"url":pic_name,"resolution":x*256}
        tiles_urls= tiles_urls +json.dumps(data)+","
    #Downloading capture without label
    download_google_nolbl_tile(lat,lon,tileZoom, quarter ,main_capture_id)
    tiles_urls = tiles_urls[0:len(tiles_urls)-1]
    tiles_urls = tiles_urls +"]"
    return tiles_urls

#the code of OSM & Bing now the same with google. becuase we don't have any resolutions yet from osm, bing.
# but when we have another resolution from bing and osm we may change all this code to another

def download_osm_tiles(url, lat,lon,tileZoom, quarter ,main_capture_id ):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    tiles_urls = "["
    #capture_id = get_Insert_id()
    for x in range(1,2):            # One Iteration Until now becuase we don't have more resolutions
        current_url = url
        current_url = current_url   # We will add something here to get more resolutions
        pic_name = 'map/osm/{}-{}-{}-{}-{}-{}-o.png'.format(lat, lon, tileZoom,quarter ,main_capture_id,str( x*256) )
        response = requests.get(current_url, stream=True, headers=headers)
        with open(pic_name, 'wb') as out_file:
            out_file.write(response.content)
        data= {"url":pic_name,"resolution":x*256}
        tiles_urls= tiles_urls +json.dumps(data)+","
    #Downloading capture without label
    download_osm_nolbl_tile(lat,lon,tileZoom, quarter ,main_capture_id)
    tiles_urls = tiles_urls[0:len(tiles_urls)-1]
    tiles_urls = tiles_urls +"]"
    return tiles_urls

def download_bing_tiles(url, lat,lon,tileZoom, quarter ,main_capture_id, quadKey):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    tiles_urls = "["
    #capture_id = get_Insert_id()
    for x in range(1,3):            # Two Iterations for (256,512) resolutions only
        current_url = url.replace('latitude',lat).replace('longitude',lon)
        if x==1:
            current_url = current_url.replace('zoomLevel',str(tileZoom)) + "&mapSize=256,256"
        elif x==2:
            current_url = current_url.replace('zoomLevel',str(tileZoom+1) ) + "&mapSize=512,512"
        print(current_url)
        pic_name = 'map/bing/{}-{}-{}-{}-{}-{}-{}-b.png'.format(lat, lon, tileZoom,quarter ,main_capture_id,str( x*256), quadKey)
        response = requests.get(current_url, stream=True, headers=headers)
        with open(pic_name, 'wb') as out_file:
            out_file.write(response.content)
        data= {"url":pic_name,"resolution":x*256}
        tiles_urls= tiles_urls +json.dumps(data)+","
    
    tiles_urls = tiles_urls[0:len(tiles_urls)-1]
    tiles_urls = tiles_urls +"]"
    return tiles_urls

def download_tile(lat, lon, tileZoom, source):
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    qkStr = t.TileXYToQuadKey(tx, ty, tileZoom)
    capture_id = get_Insert_id()
    if source == 'bing':
        #Downloading capture without label
        download_bing_nolbl_tile(lat,lon,tileZoom, capture_id,"whole",qkStr)
        return download_bing_tiles(BINGMAP_URLWITHKEY, lat,lon,tileZoom, capture_id,"whole",qkStr)
    elif source == 'google':
        #Downloading capture without label
        download_google_nolbl_tile(lat,lon,tileZoom, capture_id,"whole")
        url = 'https://mts1.google.com/vt/lyrs=m@186112443&hl=en&src=app&x={}&s=&y={}&z={}'.format(tx,ty,tileZoom)
        return download_google_tiles(url, lat,lon,tileZoom, capture_id,"whole")
    else:
        #Downloading capture without label
        download_osm_nolbl_tile(lat,lon,tileZoom, capture_id,"whole")
        url = 'https://c.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom,tx,ty)
        return download_osm_tiles(url, lat,lon,tileZoom,capture_id, "whole")

    #response = requests.get(url, stream=True)
    #assert response.status_code == 200, "connect error"
    #print('DOWNLOAD {} SUCCESS'.format(source))
#   #capture_id = get_uuid()
    #capture_id = get_Insert_id()
    #pic_name = 'map/{}/{}.png'.format(source,capture_id )
    
    #with open(pic_name, 'wb') as out_file:
    #    out_file.write(response.content)
    #    print(response.content)
    #return pic_name

def multi_pic_whole(lat, lon, tileZoom, multi, source, APIName, main_capture_Id,quadKey):
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
                #Downloading capture without label
                download_google_nolbl_tile(lat,lon,tileZoom + multi, part_list,main_capture_Id)
                url = 'https://mts1.google.com/vt/lyrs=m@186112443&hl=en&src=app&x={}&s=&y={}&z={}'.format(tx,ty,tileZoom + multi)
                pic_name = download_google_tiles(url, lat,lon,tileZoom + multi, part_list,main_capture_Id )
            elif source == 'bing':
                new_qkStr = t.TileXYToQuadKey(tx, ty, tileZoom + multi)
                #Downloading capture without label
                download_bing_nolbl_tile(lat,lon,tileZoom + multi, part_list,main_capture_Id,new_qkStr)
                #url = 'http://ecn.t0.tiles.virtualearth.net/tiles/r{}.png?g=604&imageWidth=512'.format(new_qkStr) the old url
                pic_name = download_bing_tiles(BINGMAP_URLWITHKEY, lat,lon,tileZoom + multi, part_list,main_capture_Id,new_qkStr)
            elif source == 'osm':
                #Downloading capture without label
                download_osm_nolbl_tile(lat,lon,tileZoom + multi, part_list,main_capture_Id)
                url = 'https://c.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom + multi,tx,ty)
                pic_name = download_osm_tiles(url, lat,lon,tileZoom + multi, part_list,main_capture_Id )
            else:
                return "error"
            #response = requests.get(url, stream=True)
            #assert response.status_code == 200, "connect error"
            #print('DOWNLOAD {} SUCCESS'.format(loc))
            #capture_id = get_Insert_id()
            #pic_name = 'map/{}/{}.png'.format(source, capture_id)
            #print('pic_name: {} \n'.format(pic_name))
            # Save Images
            #with open(pic_name, 'wb') as out_file:
            #    out_file.write(response.content)
            
            loc += 1

            location_photos.inser_map_all(lat, lon, APIName, tileZoom, pic_name, multi, part_list, main_capture_Id,quadKey)
    # Merge
#    IMAGE_SIZE = 256  #   Image size is 256*256
 #   IMAGE_ROW = 2 ** multi  # The row of image
#    IMAGE_COLUMN = 2 ** multi # The column of image
 #   to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE)) #创建一个新图
 #   i = 0
 #   for y in range(1, IMAGE_ROW + 1):
 #      for x in range(1, IMAGE_COLUMN + 1):
 #           from_image = Image.open('map/{}/{}_{}_{}_{}.png'.format(source, lat, lon, tileZoom + multi, i))
 #           to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
 #           i += 1
 #   pic_url = 'map/{}/{}_{}_{}_{}.png'.format(source, lat, lon, tileZoom + multi, "whole")
 #   to_image.save(pic_url) # 保存新图
 #   return pic_url, transfer_loc_part
#    return transfer_loc_part
    return pic_name, transfer_loc_part

def multi_pic_part(lat, lon, tileZoom, multi, source, part_list):
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    qkStr = t.TileXYToQuadKey(tx, ty, tileZoom)
    new_qkr = qkStr + part_list
    new_tx, new_ty = t.QuadKeyToTileXY(new_qkr)
    if source == 'google':
        url = 'https://mts1.google.com/vt/lyrs=m@186112443&hl=en&src=app&x={}&s=&y={}&z={}&scale=4'.format(new_tx,new_ty,tileZoom + multi)
    elif source == 'bing':
        url = 'http://ecn.t0.tiles.virtualearth.net/tiles/r{}.png?g=604&imageWidth=1024'.format(new_qkr)
    elif source == 'osm':
        url = 'https://a.tile.openstreetmap.org/{}/{}/{}.png'.format(tileZoom + multi,new_tx,new_ty)
    else:
        return "error"
    response = requests.get(url, stream=True)
    assert response.status_code == 200, "connect error"
    print('DOWNLOAD {} SUCCESS'.format(part_list))
    capture_id = get_Insert_id()
    pic_name = 'map/{}/{}.png'.format(source, capture_id)
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
    quadKey = int(request.args["quadkey"])
    i = endZoomLevel - tileZoom
    multi = 1
    
    #Generate initial iamges
    bing_whole = download_tile(lat, lon, tileZoom,'bing')
    #    bing_name = 'map/{}/{}_{}_{}_{}.png'.format('bing', lat, lon, tileZoom + endZoomLevel, "whole")
    #    location_photos.inser_map_whole(lat, lon, 'B', tileZoom, bing_name, endZoomLevel)
#    bing_original = 'map/{}/{}.png'.format('bing', bing_whole)
    location_photos.inser_map_original(lat, lon, 'B', tileZoom, bing_whole,quadKey)

    google_whole = download_tile(lat, lon, tileZoom,'google')
    #    google_name = 'map/{}/{}_{}_{}_{}.png'.format('google', lat, lon, tileZoom + endZoomLevel, "whole")
    #    location_photos.inser_map_whole(lat, lon, 'G', tileZoom, google_name, endZoomLevel)
#    google_original = 'map/{}/{}.png'.format('google', google_whole)
    location_photos.inser_map_original(lat, lon, 'G', tileZoom, google_whole,quadKey)

    osm_whole = download_tile(lat, lon, tileZoom,'osm')
    #    osm_name = 'map/{}/{}_{}_{}_{}.png'.format('osm', lat, lon, tileZoom + endZoomLevel, "whole")
    #    location_photos.inser_map_whole(lat, lon, 'O', tileZoom, osm_name, endZoomLevel)
 #   osm_original = 'map/{}/{}.png'.format('osm', osm_whole)
    location_photos.inser_map_original(lat, lon, 'O', tileZoom, osm_whole,quadKey)
    
    
    
    main_capture_id_bing = location_photos.get_main_capture_id(lat, lon, tileZoom, 'B')
    main_capture_id_google = location_photos.get_main_capture_id(lat, lon, tileZoom, 'G')
    main_capture_id_osm = location_photos.get_main_capture_id(lat, lon, tileZoom, 'O')
    print(main_capture_id_bing)
    result = {}
    results = {}
    #Generate partial images
    for multi in range(1, i + 1):
        bing_result, dic = multi_pic_whole(lat, lon, tileZoom, multi, 'bing', "B",  main_capture_id_bing,quadKey)
        # bing_url = 'map/{}/{}_'.format('bing', bing_result)
        # location_photos.inser_map_all(lat, lon, 'B', tileZoom, bing_url,multi,dic, main_capture_id_bing)
    
        google_result, dic = multi_pic_whole(lat, lon, tileZoom, multi, 'google',"G",  main_capture_id_google,quadKey)
        # google_url = 'map/{}/{}_'.format('google', google_result)
        # location_photos.inser_map_all(lat, lon, 'G', tileZoom, google_url,multi, dic, main_capture_id_google)
        
        osm_result, dic = multi_pic_whole(lat, lon, tileZoom, multi, 'osm', "O",  main_capture_id_osm,quadKey)
        # osm_url = 'map/{}/{}_'.format('osm', osm_result)
        # location_photos.inser_map_all(lat, lon, 'O', tileZoom, osm_url,multi,dic, main_capture_id_osm)
        # srt3 = 'osm_{}'.format(osm_result)
        # result[str3] = osm_result

    #update the address of this lat/lng for all provider
    updateLocationAddress(lat, lon)

    # result = {'bing':bing_result,'google':google_result,'osm':osm_result}
    results = {'bing':bing_whole,'google':google_whole,'osm':osm_whole}
    return jsonify(result, results)
    

@app.route('/multi/select')
def multi_select():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom =float( request.args["startz"])
    endZoomLevel =float( request.args["endz"])
    part_list = request.args['partlist']
    type(tileZoom)
    type(endZoomLevel)
    multi = endZoomLevel - tileZoom
    result = location_photos.select_map_part(lat,lon, tileZoom, multi, part_list)
    return jsonify(result)

@app.route('/multi/go')
def multi_go():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom = int(request.args["startz"])
    endZoomLevel = int(request.args["endz"])
    part_list = 'whole'
    multi = endZoomLevel - tileZoom
    result = location_photos.select_map_part(lat,lon, tileZoom, multi, part_list)
    print("result")
    print(result)
    return jsonify(result)


@app.route('/geocoding')
def geocoding():
    lat = request.args["lat"]
    lon = request.args["lon"]
#    gmaps=googlemaps.Client(key='AIzaSyAhRnxOf_ELnG-vuGw3l0Sc_8uyBtvRZS4')
    
#    reverse_geocode_result = gmaps.reverse_geocode((lat, lon))
#    result = reverse_geocode_result[4]["formatted_address"]
    result = location_photos.get_geocoding(lat, lon)
    print(result)
    return result


@app.route('/providerWordsStats')
def providerWordsStats():
    country = ""
    if len(request.args)!=0 or request.args["country"]=="null" :
        country = request.args["country"]
        print(type(country))
    return json.dumps(location_photos.get_places_number_words(country))

@app.route('/UpdateLocationsAddress')
def updateLocationsAddress():
    return json.dumps(location_photos.addAddressToAllLocationsWithoutAddress())

@app.route('/quadKeyToLatLong')
def quadKeyToLatLong():
    quadKey = request.args["quadKey"]
    tileZoom = len(quadKey)
    tileX, tileY = t.QuadKeyToTileXY(quadKey)
    pixelX, pixelY = t.TileXYToPixelXY(tileX, tileY)
    latitude, longitude = t.PixelXYToLatLong(pixelX, pixelY, tileZoom)
    result = {'latitude':latitude,'longitude':longitude}
    return json.dumps(result)

def download_bing_nolbl_tile(lat,lon,tileZoom, quarter ,main_capture_id, quadKey):
    url = '''http://ak.dynamic.t2.tiles.virtualearth.net/comp/ch/{}?mkt=en-us&it=G&rs=1&shading=hill&n=z&cb=1'''.format(quadKey)
    response = requests.get(url, stream=True)
    assert response.status_code == 200, "connect error"
    pic_name = 'map/bing/{}-{}-{}-{}-{}-{}-{}-b-lbl0.png'.format(lat, lon, tileZoom,quarter ,main_capture_id,str(512), quadKey)
    print(pic_name)
    with open(pic_name, 'wb') as out_file:
        out_file.write(response.content)
    return True

def download_google_nolbl_tile(lat,lon,tileZoom, quarter ,main_capture_id):
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    scale = 2
    url = '''https://mts0.google.com/vt/lyrs=m@289000001&hl=en&src=app&x={}&y={}&z={}&scale={}&s=Gal&apistyle=s.t:0|s.e:l|p.v:off'''.format(tx,ty,tileZoom,scale)
    response = requests.get(url, stream=True)
    assert response.status_code == 200, "connect error"
    pic_name = 'map/google/{}-{}-{}-{}-{}-{}-g-lbl0.png'.format(lat, lon, tileZoom,quarter ,main_capture_id,str(512) )
    print(pic_name)
    with open(pic_name, 'wb') as out_file:
        out_file.write(response.content)
    return True

def download_osm_nolbl_tile(lat,lon,tileZoom, quarter ,main_capture_id):
    px, py = t.LatLongToPixelXY(float(lat), float(lon), tileZoom)
    tx, ty = t.PixelXYToTileXY(px, py)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    url = "https://a.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{}/{}/{}@2x.png".format(tileZoom,tx,ty)
    response = requests.get(url, stream=True, headers=headers)
    assert response.status_code == 200, "connect error"
    pic_name = 'map/osm/{}-{}-{}-{}-{}-{}-o-lbl0.png'.format(lat, lon, tileZoom,quarter ,main_capture_id,str( 512) )
    print(pic_name)
    with open(pic_name, 'wb') as out_file:
        out_file.write(response.content)
    return True


@app.route('/nolabel/pic')
def download_no_label_pic():
    lat = request.args["lat"]
    lon = request.args["lon"]
    tileZoom =int(request.args["tileZoom"])
    osm_name, google_name, bing_name = download_tile_Nolbl(lat, lon, tileZoom)
    #Result
    result = {'osm': osm_name, 'google': google_name,'bing': bing_name}
    return jsonify(result)



@app.route('/pic2Bi')
def pic2Bi():
    #lat = request.args["lat"]
    #lon = request.args["lon"]
    #tileZoom =int(request.args["tileZoom"])


    #osm
    osm_name = request.args["osm"] #'MapsCapturing/map/osm/{},{}_{}_whole_osm.png'.format(lat,lon,tileZoom) 
    bi.genetare_osm_bi(osm_name)
    bi_osm_img_path = osm_name.replace('.png', '_bi.png')
    
    #google
    google_name = request.args["google"] # 'MapsCapturing/map/google/{},{}_{}_whole_google.png'.format(lat,lon,tileZoom) 
    print("***************:"+google_name)
    bi.genetare_google_bi(google_name)
    bi_google_img_path = google_name.replace('.png', '_bi.png')
    #bing
    bing_name = request.args["bing"] # 'v
    bi.genetare_osm_bi(bing_name)
    bi_bing_img_path = bing_name.replace('.png', '_bi.png')
    
 #  location_photos.inser_bi_all(get_uuid, lat, lon, map_provider, zoom_level, bi_img_path)
    result = {'google': bi_google_img_path,'osm':bi_osm_img_path,'bing':bi_bing_img_path}
    return jsonify(result)


# http://127.0.0.1:84/bi2Skeleton?bing_bi=map/bing/25.35891851754525-51.4324951171875-16-15934-whole-256-1230230212032013-b-lbl0_bi.png&google_bi=map/google/25.35891851754525-51.4324951171875-16-15935-whole-256-g-lbl0_bi.png&osm_bi=map/osm/25.35891851754525-51.4324951171875-16-15936-whole-256-o-lbl0_bi.png
@app.route('/bi2Skeleton')
def bi2Skeleton():
    osm_name = request.args["osm_bi"]
    bing_name = request.args["bing_bi"]
    google_name = request.args["google_bi"]
    print(osm_name) # MapsCapturing\map\osm\25.35891851754525-51.4324951171875-16-15936-whole-256-o-lbl0_bi.png
    print(bing_name)
    print(google_name)
    #OSM
    mask_path = osm_name
    img_path = mask_path.replace('_bi.png', '.png')
    img = cv2.imread(img_path)
    mask = cv2.imread(mask_path)
    print(os.getcwd())
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    skeleton = skeleton_gen(gray)
    skeleton_node, skeleton_node_cor_lst = get_road_intersection(skeleton)
    intersection_path = mask_path.replace('bi.png', 'bi_vis.png')
    cv2.imwrite(intersection_path, skeleton_node)  
    osm_result = {'junction_img_path':intersection_path}
    
    #BING
    #BING
    mask_path = bing_name
    img_path = mask_path.replace('_bi.png', '.png')
    img = cv2.imread(img_path)
    mask = cv2.imread(mask_path)
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    skeleton = skeleton_gen(gray)
    skeleton_node, skeleton_node_cor_lst = get_road_intersection(skeleton)
    intersection_path = mask_path.replace('bi.png', 'bi_vis.png')
    cv2.imwrite(intersection_path, skeleton_node)  
    bing_result = {'junction_img_path':intersection_path}
    
    #Google
    mask_path = google_name
    img_path = mask_path.replace('_bi.png', '.png')
    img = cv2.imread(img_path)
    mask = cv2.imread(mask_path)
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    skeleton = skeleton_gen(gray)
    skeleton_node, skeleton_node_cor_lst = get_road_intersection(skeleton)
    intersection_path = mask_path.replace('bi.png', 'bi_vis.png')
    cv2.imwrite(intersection_path, skeleton_node)  
    google_result = {'junction_img_path':intersection_path}

    result = {'osm':osm_result,'bing':bing_result,'google':google_result}
    return jsonify(result)

# http://127.0.0.1:84/bi2info?bing_bi=map/bing/25.35891851754525-51.4324951171875-16-15934-whole-256-1230230212032013-b-lbl0_bi.png&google_bi=map/google/25.35891851754525-51.4324951171875-16-15935-whole-256-g-lbl0_bi.png&osm_bi=map/osm/25.35891851754525-51.4324951171875-16-15936-whole-256-o-lbl0_bi.png
@app.route('/bi2info')
def bi2info():
    osm_name = request.args["osm_bi"]
    bing_name = request.args["bing_bi"]
    google_name = request.args["google_bi"]

    #OSM
    mask_path = osm_name
    img_path = mask_path.replace('_bi.png', '.png')
    img = cv2.imread(img_path)
    mask = cv2.imread(mask_path)
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    skeleton = skeleton_gen(gray)
    skeleton_node, skeleton_node_cor_lst = get_road_intersection(skeleton)
    # TODO
    skeleton_node_lat_long_lst = get_lat_long(skeleton_node_cor_lst, os.path.basename(mask_path).split('-')[:2])
    _data = {'total_junction_num':[len(skeleton_node_cor_lst)] + ['' for _ in range(len(skeleton_node_cor_lst) - 1)], 'junction_coordinate':skeleton_node_cor_lst, 'lat_long':skeleton_node_lat_long_lst}
    if len(skeleton_node_cor_lst) == 0:
        _data['total_junction_num'] = ''
        _data['lat_long'] = ''
    excel_junction_path, excel_road_info_path = mask_path.replace('_bi.png', '_junction.xlsx'), mask_path.replace('_bi.png', '_road_info.xlsx')
    generate_excel(
        header=['total_junction_num', 'junction_coordinate', 'lat_long'], 
        data=_data,
        xlsx_path=excel_junction_path
    )
    subroad_info = get_subroad_info(skeleton, skeleton_node_cor_lst, img, gray, mask_path)
    generate_excel(
        header=['road_type', 'road_name', 'road_length', 'road_length_meter', 'total_road_length',  'total_road_length_meter'], 
        data=subroad_info,
        xlsx_path=excel_road_info_path
    )
    intersection_path = mask_path.replace('bi.png', 'bi_vis.png')
    cv2.imwrite(intersection_path, skeleton_node)  
    osm_result = {'excel_junction_path':excel_junction_path, 'excel_road_info_path':excel_road_info_path}
    
    #BING
    mask_path = bing_name
    img_path = mask_path.replace('_bi.png', '.png')
    img = cv2.imread(img_path)
    mask = cv2.imread(mask_path)
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    skeleton = skeleton_gen(gray)
    skeleton_node, skeleton_node_cor_lst = get_road_intersection(skeleton)
    skeleton_node_lat_long_lst = get_lat_long(skeleton_node_cor_lst, os.path.basename(mask_path).split('-')[:2])
    _data = {'total_junction_num':[len(skeleton_node_cor_lst)] + ['' for _ in range(len(skeleton_node_cor_lst) - 1)], 'junction_coordinate':skeleton_node_cor_lst, 'lat_long':skeleton_node_lat_long_lst}
    if len(skeleton_node_cor_lst) == 0:
        _data['total_junction_num'] = ''
        _data['lat_long'] = ''
    excel_junction_path, excel_road_info_path = mask_path.replace('_bi.png', '_junction.xlsx'), mask_path.replace('_bi.png', '_road_info.xlsx')
    generate_excel(
        header=['total_junction_num', 'junction_coordinate', 'lat_long'], 
        data=_data,
        xlsx_path=excel_junction_path
    )
    subroad_info = get_subroad_info(skeleton, skeleton_node_cor_lst, img, gray, mask_path)
    generate_excel(
        header=['road_type', 'road_name', 'road_length', 'road_length_meter', 'total_road_length',  'total_road_length_meter'], 
        data=subroad_info,
        xlsx_path=excel_road_info_path
    )
    intersection_path = mask_path.replace('bi.png', 'bi_vis.png')
    cv2.imwrite(intersection_path, skeleton_node)  
    bing_result = {'excel_junction_path':excel_junction_path, 'excel_road_info_path':excel_road_info_path}
    
    #Google
    mask_path = google_name
    img_path = mask_path.replace('_bi.png', '.png')
    img = cv2.imread(img_path)
    mask = cv2.imread(mask_path)
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    skeleton = skeleton_gen(gray)
    skeleton_node, skeleton_node_cor_lst = get_road_intersection(skeleton)
    skeleton_node_lat_long_lst = get_lat_long(skeleton_node_cor_lst, os.path.basename(mask_path).split('-')[:2])
    _data = {'total_junction_num':[len(skeleton_node_cor_lst)] + ['' for _ in range(len(skeleton_node_cor_lst) - 1)], 'junction_coordinate':skeleton_node_cor_lst, 'lat_long':skeleton_node_lat_long_lst}
    if len(skeleton_node_cor_lst) == 0:
        _data['total_junction_num'] = ''
        _data['lat_long'] = ''
    excel_junction_path, excel_road_info_path = mask_path.replace('_bi.png', '_junction.xlsx'), mask_path.replace('_bi.png', '_road_info.xlsx')
    generate_excel(
        header=['total_junction_num', 'junction_coordinate', 'lat_long'], 
        data=_data,
        xlsx_path=excel_junction_path
    )
    subroad_info = get_subroad_info(skeleton, skeleton_node_cor_lst, img, gray, mask_path)
    generate_excel(
        header=['road_type', 'road_name', 'road_length', 'road_length_meter', 'total_road_length',  'total_road_length_meter'], 
        data=subroad_info,
        xlsx_path=excel_road_info_path
    )
    intersection_path = mask_path.replace('bi.png', 'bi_vis.png')
    cv2.imwrite(intersection_path, skeleton_node)  
    google_result = {'excel_junction_path':excel_junction_path, 'excel_road_info_path':excel_road_info_path}

    result = {'osm':osm_result,'bing':bing_result,'google':google_result}
    return jsonify(result)

if __name__ == '__main__':
    app.run( port=84)

