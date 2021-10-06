using MapsUnderstanding.Handlers;
using MapsUnderstanding.Middleware;
using MapsUnderstanding.Models;
using MapsUnderstanding.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Primitives;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Net;
using System.Threading.Tasks;

namespace MapsUnderstanding.Controllers
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
        public IEnumerable<Location_Photos> getAllLocationPhotosData()
        {
            return repository.GetAll();
        }
        [HttpGet("testController")]
        public IActionResult testController()
        {
            return Ok(new { controller = "run successfully" });
        }

        [HttpGet("AllLocationPhotos")]
        public IActionResult AllLocationPhotos()
        {
            try
            {
                var model = getAllLocationPhotosData();
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

        [HttpGet("getCountriesWeHave")]
        public IActionResult getCountriesWeHave()
        {
            try
            {
                var alldata = getAllLocationPhotosData();
                var model = from s in alldata
                            where s.address != null
                            select new { value = s.address.Substring(s.address.LastIndexOf(",") + 1).Trim(),
                                    label = s.address.Substring(s.address.LastIndexOf(",") + 1).Trim()
                            };

                return Ok(new { data = model.Distinct() });
            }
            catch (Exception ex)
            {
                Debug.Write(ex);
                return BadRequest(new { error = ex.Message });
            }
        }

        [HttpGet("AllLocationWholePhotos")]
        public IActionResult AllLocationWholePhotos()
        {
            try
            {
                var alldata = getAllLocationPhotosData();
                var model = from s in alldata
                                      where s.quarter.Trim()=="whole"
                                      select new { s.lat, s.lng,s.zoom_level, s.capture_quadKey, s.address,
                                          Google=(  from g in alldata
                                                    where g.lat == s.lat &&
                                                    g.lng == s.lng &&
                                                    
                                                    g.quarter.Trim()== s.quarter.Trim() &&
                                                    g.zoom_level== s.zoom_level &&
                                                    g.map_provider.Trim() == "G"
                                                    select new { ImgPath =  g.capture_url, ground_truth = g.ground_truth }).FirstOrDefault(),
                                          Bing = (from g in alldata
                                                    where g.lat == s.lat &&
                                                    g.lng == s.lng &&
                                                   
                                                    g.quarter.Trim() == s.quarter.Trim() &&
                                                    g.zoom_level == s.zoom_level &&
                                                    g.map_provider.Trim() == "B"
                                                    select new { ImgPath =  g.capture_url, ground_truth = g.ground_truth }).FirstOrDefault(),
                                          OSM = (from g in alldata
                                                    where g.lat == s.lat &&
                                                    g.lng == s.lng &&
                                                   
                                                    g.quarter.Trim() == s.quarter.Trim() &&
                                                    g.zoom_level == s.zoom_level &&
                                                    g.map_provider.Trim() == "O"
                                                    select new { ImgPath = g.capture_url, ground_truth = g.ground_truth }).FirstOrDefault()
                                      };
                           
                return Ok(new { data = model.Distinct() });
            }
            catch (Exception ex)
            {
                Debug.Write(ex);
                return BadRequest(new { error = ex.Message });
            }
        }
        [HttpPut("UpdateLocationsWithoutGroundTruth")]
        public IActionResult UpdateLocationsWithoutGroundTruth()
        {
            try
            {
                Request.Headers.TryGetValue("all", out var all);
                var alldata = getAllLocationPhotosData();
                var model = alldata;
                if(all != StringValues.Empty)
                    model = from table in alldata
                                where table.ground_truth == null
                                select table;
                int noLocations = 0;
                foreach (var location in model)
                {
                    string filePath = Util.mapsPathProvider(location.map_provider.Trim()) + location.lat + "-" + location.lng + "-" + location.zoom_level + "-" + location.quarter.Trim() + ".txt";
                    
                    if (System.IO.File.Exists(filePath))
                    {
                        location.ground_truth = System.IO.File.ReadAllText(filePath);
                        noLocations += 1;
                        repository.Update(location);
                    }
                }
                repository.Save();
                Console.WriteLine("Database updated: no of files"+ noLocations);
                return Ok(new { data = getAllLocationPhotosData(), noOfLocationUpdated= noLocations });
            }
            catch (Exception ex)
            {
                Console.Write(ex);
                return BadRequest(new { error = ex.Message });
            }
        }

        public class GroundTruths
        {
            public int[] capture_ids { set; get; }
            public string[] ground_truths { get; set; }
        }

        [HttpPut("UpdateLocationsWithNewGroundTruths")]
        public IActionResult UpdateLocationsWithNewGroundTruths([FromBody] GroundTruths groundTruths)
        {
            try
            {
                var alldata = getAllLocationPhotosData();
                var model = alldata;
                    model = from table in alldata
                            where  groundTruths.capture_ids.Contains(table.capture_id)
                            select table;
                int noLocations = 0;
                foreach (var location in model)
                {
                    var index = Array.IndexOf(groundTruths.capture_ids, location.capture_id);
                    location.ground_truth = groundTruths.ground_truths[index];
                    Console.WriteLine("CaptureId=" + location.capture_id + ", new groundTruth=" + groundTruths.ground_truths[index]);
                    noLocations += 1;
                    repository.Update(location);

                }
                repository.Save();
                Console.WriteLine("Database updated: no of files" + noLocations);
                return Ok(new { data = getAllLocationPhotosData(), noOfLocationUpdated = noLocations });
            }
            catch (Exception ex)
            {
                Console.Write(ex);
                return BadRequest(new { error = ex.Message });
            }
        }



    }
}
