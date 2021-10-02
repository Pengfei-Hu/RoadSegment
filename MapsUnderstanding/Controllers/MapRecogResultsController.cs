using MapsUnderstanding.Data;
using MapsUnderstanding.Handlers;
using MapsUnderstanding.Middleware;
using MapsUnderstanding.Models;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MapsUnderstanding.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class MapRecogResultsController : Controller
    {
        private IGenericRepository<MapImageRecogResults> repository = null;
        private readonly MapsVisionsDbContext _DbContext;
        private IEnumerable<MapImageRecogResults> allMapImageRecogResults=null;
        public MapRecogResultsController(MapsVisionsDbContext mapsVisionsDbContext)
        {
            _DbContext = mapsVisionsDbContext;
            this.repository = new GRepository<MapImageRecogResults>(_DbContext);
        }
        public IEnumerable<MapImageRecogResults> getAllMapImageRecogResults()
        {
            return repository.GetAll();
        }
        [HttpGet("testController")]
        public IActionResult testController()
        {
            return Ok(new { controller= "run successfully" });
        }
        [HttpPost("SaveAllLocationsPicturesResults")]
        public IActionResult SaveAllLocationsPicturesResults()
        {
            Console.WriteLine("SaveAllLocationsPicturesResults function");
            try
            {
                CVHandler cv = new CVHandler();
                LocationPhotosController locPhotos = new LocationPhotosController(_DbContext);
                allMapImageRecogResults = getAllMapImageRecogResults();
                Console.WriteLine("Count"+ allMapImageRecogResults.Count());
                /*string[] filtersGroups = {  "WithoutEffects", "resize", "gray", "resize,gray", "resize,gray,EnhanceDetail", 
                                            "resize,gray,BitwiseText", "resize,gray,BitwiseText,EnhanceDetail", "KMeans", 
                                            "BitwiseText", "EnhanceDetail", "enhanceDetail,resize", "enhanceDetail,contours", 
                                            "enhanceDetail,bitwiseText", "bitwiseText,enhanceDetail", 
                                            "resize,bitwiseText,enhanceDetail", "enhanceDetail,resize,bitwiseText", 
                                            "enhanceDetail,resize,KMeans", "resize,Kmeans", "resize,bitwiseText",
                                            "resize,enhanceDetail,bitwiseText", "bitwiseText,resize,enhanceDetail" };*/

                string[] filtersGroups = {  "bgbitwise,bgtransparent,bgtrans2white,enhanceDetail,resize,bitwiseText",
                                            "enhanceDetail,resize,bitwiseText,bgbitwise,bgtransparent,bgtrans2white"};

                var locPhotosData = locPhotos.getAllLocationPhotosData();
                Console.WriteLine("locPhotosData Count" + locPhotosData.Count());
                List<CaptureUrl> allCaptures = new List<CaptureUrl>();
                TextRecogHandler textRecog = new TextRecogHandler();
                List<MapImageRecogResults> allResults = new List<MapImageRecogResults>();
                int correctCounter = 0;
                int incorrectCounter = 0;

                foreach (var location in locPhotosData)
                {

                List<CaptureUrl> captures = JsonConvert.DeserializeObject<List<CaptureUrl>>(location.capture_url);
                //allCaptures.AddRange(captures);

                foreach (var capture in captures)
                {
                    if (!IsCaptureProcessedBefore(allMapImageRecogResults, capture))
                    {
                        allCaptures.Add(capture);
                        foreach (string filtersGroup in filtersGroups)
                        {
                            cv.applyEffectsToImgs(capture.url, filtersGroup);
                            var results = textRecog.getTextRecogDetails(location.ground_truth, capture.url, location.capture_id, filtersGroup, capture.resolution, out _);
                            allResults.Add(results);
                            repository.Insert(results);
                                try
                                {
                                    //Console.Write(JsonConvert.SerializeObject(results, Formatting.Indented));
                                    repository.Save();
                                    Console.WriteLine("Saved: "+(++correctCounter));
                                 }
                                catch (Exception ex)
                                {
                                    Console.Write(ex);
                                    Console.WriteLine("******Error******:" + ex.Message);
                                    Console.WriteLine("Rejected: " + (++incorrectCounter));
                                    System.IO.File.AppendAllText(Util.mapsPath() + @"\map\log\errorsLog.txt", ex.Message + Environment.NewLine);
                                }
                            }
                    }

                }
            }
                
                return Ok(new { results = allResults });
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
                Console.WriteLine(ex.StackTrace);
                return BadRequest(new { error = ex.Message });
            }
        }

        private bool IsCaptureProcessedBefore(IEnumerable<MapImageRecogResults> allMapImageRecogResults, CaptureUrl capture)
        {
            /*
             * we need to add the same filter in this condition
            if (allMapImageRecogResults.Count()>0)
                foreach(var recogRes in allMapImageRecogResults)
                    if(recogRes.picture_url==capture.url && recogRes.resolution == capture.resolution)
                        return true;
            */
            return false;
        }
    }
}
