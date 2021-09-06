using MapsUnderstanding.Middleware;
using MapsUnderstanding.Models;
using MapsVisionsAPI.Data;
using MapsVisionsAPI.Models;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Net;
using System.Threading.Tasks;

namespace MapsVisionsAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class LocationPhotosController : Controller
    {
        private string pythonServer = "http://localhost:84/";
        private IGenericRepository<Location_Photos> repository = null;
        private readonly MapsVisionsDbContext _DbContext;

        public LocationPhotosController(MapsVisionsDbContext mapsVisionsDbContext)
        {
            _DbContext = mapsVisionsDbContext;
            this.repository = new GRepository<Location_Photos>(_DbContext);
        }

        [HttpGet("AllLocationPhotos")]
        public IActionResult AllLocationPhotos()
        {
            try
            {
                var model = repository.GetAll();
                return Ok(new { data = model });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }
        static void SaveImage(LatLng latLng)
        {
            string url = "https://mts1.google.com/vt/lyrs=m@186112443&hl=x-local&src=app&x=1325&y=3143&z=13&scale=3";
            WebClient client = new WebClient();
            client.Headers.Add("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; " +
                                  "Windows NT 5.2; .NET CLR 1.0.3705;)");
            Stream stream = client.OpenRead(url);
            Bitmap bitmap = new Bitmap(stream);

            if (bitmap != null)
            {
                bitmap.Save("D:\\MapImg1.png",  ImageFormat.Png);
            }

            stream.Flush();
            stream.Close();
            client.Dispose();
        }
        [HttpGet("DownloadGooglePic")]
        public IActionResult DownloadGooglePic()
        {
            try
            {
                Request.Headers.TryGetValue("latitude", out var latitude);
                Request.Headers.TryGetValue("longitude", out var longitude);
                LatLng latLng = new LatLng(Double.Parse( latitude.ToString()), 
                            Double.Parse(longitude.ToString()));
                var url = "https://mts1.google.com/vt/lyrs=m@186112443&hl=x-local&src=app&x=1325&y=3143&z=13&scale=3";
                SaveImage(latLng);
                return Ok(new { downloaded =true });
            }
            catch (Exception ex)
            {
                Console.Write(ex);
                return BadRequest(new { error = ex.Message, downloaded = false });
            }
        }

        [HttpGet("AllLocationWholePhotos")]
        public IActionResult AllLocationWholePhotos()
        {
            try
            {
                var alldata = repository.GetAll();
                var model = from s in alldata
                                      where s.quarter.Trim()=="whole"
                                      select new { s.lat, s.lng, s.zoom_level ,
                                          Google=(  from g in alldata
                                                    where g.lat == s.lat &&
                                                    g.lng == s.lng &&
                                                    
                                                    g.quarter.Trim()== s.quarter.Trim() &&
                                                    g.zoom_level== s.zoom_level &&
                                                    g.map_provider.Trim() == "G"
                                                    select new { ImgPath = pythonServer + g.capture_url }).FirstOrDefault(),
                                          Bing = (from g in alldata
                                                    where g.lat == s.lat &&
                                                    g.lng == s.lng &&
                                                   
                                                    g.quarter.Trim() == s.quarter.Trim() &&
                                                    g.zoom_level == s.zoom_level &&
                                                    g.map_provider.Trim() == "B"
                                                    select new { ImgPath = pythonServer + g.capture_url }).FirstOrDefault(),
                                          OSM = (from g in alldata
                                                    where g.lat == s.lat &&
                                                    g.lng == s.lng &&
                                                   
                                                    g.quarter.Trim() == s.quarter.Trim() &&
                                                    g.zoom_level == s.zoom_level &&
                                                    g.map_provider.Trim() == "O"
                                                    select new { ImgPath = pythonServer + g.capture_url }).FirstOrDefault()
                                      };
                           
                return Ok(new { data = model.Distinct() });
            }
            catch (Exception ex)
            {
                Debug.Write(ex);
                return BadRequest(new { error = ex.Message });
            }
        }
    }
}
