using MapsUnderstanding.Models;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MapsUnderstanding.Middleware
{

    public class TileCoordinates
    {
        public Point fromLatLngToPoint(LatLng latLng)
        {
            var siny = Math.Min(Math.Max(Math.Sin(latLng.lat * (Math.PI / 180)),-.9999),.9999);
            return new Point(128 + latLng.lng * (256 / 360),
                    128 + 0.5 * Math.Log((1 + siny) / (1 - siny)) * -(256 / (2 * Math.PI)));
        }

        public LatLng fromPointToLatLng(Point point)
        {
            return new LatLng(
                (2 * Math.Atan(Math.Exp((point.y - 128) / -(256 / (2 * Math.PI)))) - Math.PI / 2) / (Math.PI / 180),
                (point.x - 128) / (256 / 360));
        }

        public Tile getTileAtLatLng(LatLng latLng,int zoom)
        {
            var t = Math.Pow(2, zoom);
            var s = 256 / t;
            var p = fromLatLngToPoint(latLng);
            return new Tile(  Math.Floor(p.x / s), Math.Floor(p.y / s), zoom);
        }
        public Tile normalizeTile(Tile tile)
        {
            var t = Math.Pow(2, tile.z);
            tile.x = ((tile.x % t) + t) % t;
            tile.y = ((tile.y % t) + t) % t;
            return tile;
        }
        public TileBounds getTileBounds(Tile tile)
        {
            tile = this.normalizeTile(tile);
            var t = Math.Pow(2, tile.z);
            var s = 256 / t;
            var sw = new Point( x:tile.x* s, y:(tile.y * s) + s);
            var ne = new Point(x: tile.x * s + s, y: (tile.y * s));
            return new TileBounds( fromPointToLatLng(sw), fromPointToLatLng(ne));
        }
    }
}
