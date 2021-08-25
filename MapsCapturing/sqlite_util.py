# -*- coding: utf-8 -*-
# __author__ = 'Yao Jia Wei'

from PIL.Image import NONE
from numpy.lib.function_base import append
import pymssql
import datetime
class MSSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
 
    def GetConnect(self):
        if not self.db:
            raise(NameError,'No data')
        self.conn = pymssql.connect(server=self.host,user=self.user,password=self.pwd,database=self.db,charset='utf8')
        cur = self.conn.cursor()
        print("Connection Success!")
        if not cur:
            raise(NameError,'Connect Failure')
        else:
            return cur

    def inser_map(self, lat, lon, map_provider, capture_url):
        val = (lat, lon, map_provider, capture_url,'whole')
        c = self.GetConnect()
        idd = c.execute("INSERT INTO location_photos(lat,lng,map_provider,capture_url,quarter) VALUES (%s,%s,%s,%s,%s)",val)
        self.conn.commit()
        self.conn.close()
        print("Records created successfully")
        return idd

    def inser_map_part(self, lat, lon, map_provider, zoom_level, capture_url, part_list, multi):
        
        c = self.GetConnect()
        time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        val = (lat, lon, map_provider, zoom_level+multi, capture_url,part_list,zoom_level,time_str)
        idd = c.execute("INSERT INTO location_photos(lat,lng,map_provider,zoom_level,capture_url,quarter,main_capture_id,timestamp) VALUES (%s,%s,%s,%d,%s,%s,%d,%s)",val)
        self.conn.commit()
        self.conn.close()
        print("Records created successfully")
        return idd
    
    def inser_map_whole(self, lat, lon, map_provider, zoom_level, capture_url, multi):
        time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        val = (lat, lon, map_provider, zoom_level+multi, capture_url,'whole',zoom_level,time_str)
        c = self.GetConnect()
        idd = c.execute("INSERT INTO location_photos(lat,lng,map_provider,zoom_level,capture_url,quarter,main_capture_id,timestamp) VALUES (%s,%s,%s,%d,%s,%s,%d,%s)",val)
        self.conn.commit()
        self.conn.close()
        print("Records created successfully")
        return idd

    def inser_map_original(self, lat, lon, map_provider, zoom_level, capture_url):
        time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        val = (lat, lon, map_provider, zoom_level, capture_url,'whole',time_str)
        c = self.GetConnect()
        idd = c.execute("INSERT INTO location_photos(lat,lng,map_provider,zoom_level,capture_url,quarter,timestamp) VALUES (%s,%s,%s,%d,%s,%s,%s)",val)
        self.conn.commit()
        self.conn.close()
        print("Records created successfully")
        return idd

    def inser_map_all(self, lat, lon, map_provider, zoom_level, capture_url, multi, dic,main_capture_id):
        time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        c = self.GetConnect()
        # for i in range(2**(multi * 2)):
            #pic_url = capture_url + '{}.png'.format(i)
        print((lat, lon, map_provider, zoom_level+multi, capture_url,dic,main_capture_id))
        val = (lat, lon, map_provider, zoom_level+multi, capture_url,dic,main_capture_id,time_str)
        idd = c.execute("INSERT INTO location_photos(lat,lng,map_provider,zoom_level,capture_url,quarter,main_capture_id,timestamp) VALUES (%s,%s,%s,%d,%s,%s,%d,%s)",val)
        self.conn.commit()
        self.conn.close()
        print("Records created successfully")
        return idd

    def select_map_part(self, lat, lon, zoom_level, multi, quarter):
        c = self.GetConnect()
        query = "SELECT * FROM location_photos WHERE lat = %d AND lng = %d AND zoom_level = %d AND quarter = %s "
        val =  (lat, lon, zoom_level+ multi, quarter)
        print(query)
        print(val)
        c.execute(query, val)
        data_list = c.fetchall()
        res = {}
        for data in data_list:
            source =data[3].strip()
            if source == 'B':
                res['bing'] = data[5]
            elif source == 'G':
                res['google'] = data[5]
            else:
                res['osm'] = data[5]
        self.conn.close()
        print("Records SELECT successfully")
        return res

    def select_map_whole(self, lat, lon, zoom_level, multi, quarter):
        c = self.GetConnect()
        val =  (lat, lon, zoom_level+ multi, quarter)
        c.execute("SELECT * FROM location_photos WHERE lat = %s AND lng = %s AND zoom_level = %d AND quarter = %s ", val)
        data_list = c.fetchall()
        res = {}
        for data in data_list:
            source =data[3].strip()
            if source == 'B':
                res['bing'] = data[5]
            elif source == 'G':
                res['google'] = data[5]
            else:
                res['osm'] = data[5]
        self.conn.close()
        print("Records SELECT successfully")
        return res

    def get_main_capture_id(self, lat, lon, zoom_level, map_provider):
        c = self.GetConnect()
        val =  (lat, lon, zoom_level, map_provider)
        c.execute("SELECT * FROM location_photos WHERE lat = %s AND lng = %s AND zoom_level = %d AND map_provider = %s AND quarter = 'whole'", val)
        main_capture_id = 0
        try:
            data_list = c.fetchall()
            main_capture_id = data_list[0][0]
        except:
            print("data not exists")
        self.conn.close()
        print("Records SELECT successfully")
        return main_capture_id

    def get_capture_id(self, lat, lon, zoom_level,multi, map_provider):
        c = self.GetConnect()
        val =  (lat, lon, zoom_level + multi, map_provider)
        c.execute("SELECT * FROM location_photos WHERE lat = %s AND lng = %s AND zoom_level = %d AND map_provider = %s ", val)
        capture_id = 0
        try:
            data_list = c.fetchall()
            capture_id = data_list[0][0]
        except:
            print("data not exists")
        self.conn.close()
        print("Records SELECT successfully")
        return capture_id
    def get_Next_id(self):
        c = self.GetConnect()
        
        c.execute("SELECT IDENT_CURRENT('location_photos') + IDENT_INCR('location_photos')")
        Next_id = 0
        try:
            data_list = c.fetchall()
            Next_id = data_list[0][0]
        except:
            print("data not exists")
        self.conn.close()
        print("Records SELECT successfully")
        return Next_id
        
