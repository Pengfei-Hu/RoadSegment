using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MapsUnderstanding.Models
{
    public class LatLng
    {
        public double lat { set; get; }
        public double lng { set; get; }
        public LatLng(double lat, double lng)
        {
            this.lat = lat;
            this.lng = lng;
        }
    }
    public class Point
    {
        public double x { set; get; }
        public double y { set; get; }
        public Point(double x, double y)
        {
            this.x = x;
            this.y = y;
        }

    }
    public class Tile
    {
        public double x { set; get; }
        public double y { set; get; }
        public int z { set; get; }
        public Tile(double x, double y, int z)
        {
            this.x = x;
            this.y = y;
            this.z = z;
        }
    }
    public class TileBounds
    {
        public TileBounds(LatLng sw, LatLng ne)
        {
            this.sw = sw;
            this.ne = ne;
        }
        public LatLng sw { set; get; }
        public LatLng ne { set; get; }
    }
}
