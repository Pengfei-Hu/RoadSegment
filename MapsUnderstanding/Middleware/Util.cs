using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace MapsUnderstanding.Middleware
{
    public class Util
    {
        public static string mapsPath()
        {
            string ApiDir = Directory.GetCurrentDirectory();
            string mapsDir = ApiDir.Substring(0, ApiDir.LastIndexOf("\\"));
            return mapsDir + "\\MapsCapturing";
        }
        public static string mapsPathProvider(string firstLetterOfProvider)
        {
            string ApiDir = Directory.GetCurrentDirectory();
            string mapsDir = ApiDir.Substring(0, ApiDir.LastIndexOf("\\"));
            return mapsDir + "\\MapsCapturing\\map\\"+ ((firstLetterOfProvider.ToLower()=="g")?"google":(firstLetterOfProvider.ToLower()=="b")?"bing":(firstLetterOfProvider.ToLower()=="o")?"osm":"")+"\\";
        }
    }
}
