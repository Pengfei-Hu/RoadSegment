using MapsUnderstanding.Handlers;
using MapsUnderstanding.Middleware;
using MapsUnderstanding.Models;
using MapsVisionsAPI.Middleware;
using Microsoft.AspNetCore.Mvc;
using OpenCvSharp;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace MapsUnderstanding.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class CVController : Controller
    {
        CVHandler cv = new CVHandler();

        [HttpPost("applyGrayFilter")]
        public IActionResult applyGrayFilter()
        {
            try
            {
                Request.Headers.TryGetValue("imagePath", out var imageName);
                Request.Headers.TryGetValue("filters", out var filters);
                imageName = imageName.ToString().Replace("/", "\\");
                var imagePath = Path.Combine(Util.mapsPath(), imageName);
                Console.WriteLine(imagePath);
                ImageFilters.applyGrayFilter(imagePath);
                return Ok(new { message = "filters applied over the images successfully", imagePath = imagePath });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        [HttpPut("applyFilterAndRead")]
        public IActionResult applyFilterAndRead()
        {
            try
            {
                Request.Headers.TryGetValue("imagePath", out var imagePath);
                Request.Headers.TryGetValue("effects", out var filters);
                string log = cv.applyEffectsToImgs(imagePath.ToString(), filters.ToString());

                float confidence = 0.0f;
                string detailedText = "";
                List<TessTextDef> wordsList = new List<TessTextDef>();
                string textList = "", text="";
                TextRecogHandler textRecog = new TextRecogHandler();
                imagePath = imagePath.ToString().Replace("/", "\\");
                imagePath = Path.Combine(Util.mapsPath(), imagePath);
                var imageFilteredPath = ImageFilters.getfilteredImgPath(imagePath);
                textRecog.readTextDetails(imageFilteredPath, out confidence, out text, out detailedText, out wordsList, out textList);
                List<ColorsCounts> colorsCounts= ImageFilters.getKMeansColors(imagePath);
                var imageKMeansPath = ImageFilters.getfilteredImgPath(imagePath, "kmeans");
                //Mat img_txt = ImageFilters.readFilteredImg(imageKMeansPath, "kmeans");
                ImageFilters.kmeansTextOnly(imagePath,imageKMeansPath, new StringReader(detailedText));
                //var rects = ImageFilters.getRectangles(ref img_txt, new StringReader(detailedText));

                return Ok(new { Success = true, Confidence = confidence, 
                                wordsList = wordsList, textList = textList,text= text, 
                                imagePath = imagePath, detailedText = detailedText,
                                imageColorsCounts = colorsCounts});
            }
            catch (ArgumentNullException ex)
            {
                return BadRequest(new { Success = false, message = "you must add imagePath in headers of your request", error = ex.Message });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        [HttpPost("applyEffectsToAllImgs")]
        public IActionResult applyEffectsToAllImgs()
        {
            try
            {
                Request.Headers.TryGetValue("imagePath", out var imagesName);
                Request.Headers.TryGetValue("effects", out var filters);
                string log = cv.applyEffectsToImgs(imagesName.ToString(), filters.ToString());
                return Ok(new { message = "filters applied over the images successfully", log = log });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        [HttpGet("getColorsCountsForAllImgs")]
        public IActionResult getColorsCountsForAllImgs()
        {
            Console.WriteLine("getColorsCountsForAllImgs function");
            try
            {
                Request.Headers.TryGetValue("imagesPaths", out var imagesPaths);
                string[] imgs = imagesPaths.ToString().Split(",");
                Console.WriteLine("Images Pathes:::: "+imagesPaths);
                List<ColorsCounts>      bingColorsCounter = new List<ColorsCounts>(), 
                                        googleColorsCounter = new List<ColorsCounts>(), 
                                        osmColorsCounter =new List<ColorsCounts>();
                foreach (var img in imgs)
                {
                    var imageName = img.ToString().Replace("/", "\\");
                    var imagePath = Path.Combine(Util.mapsPath(), imageName);
                    if (imagePath.IndexOf("bing") != -1)
                        bingColorsCounter = cv.colorsCounter(imagePath);
                        
                    else if (imagePath.IndexOf("google") != -1)
                        googleColorsCounter = cv.colorsCounter(imagePath);
                    else if (imagePath.IndexOf("osm") != -1)
                        osmColorsCounter = cv.colorsCounter(imagePath);
                }
                return Ok(new { success=true, 
                                bingColorsCounter= bingColorsCounter,
                                googleColorsCounter= googleColorsCounter , 
                                osmColorsCounter= osmColorsCounter});
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                Console.Write(ex.StackTrace);
                return BadRequest(new {success=false, error = ex.Message });
            }
        }

        [HttpPost("applyFilters2")]
        public IActionResult applyFilters2()
        {
            try
            {
                Request.Headers.TryGetValue("imagePath", out var imageName);
                imageName = imageName.ToString().Replace("/", "\\");
                var imagePath = Path.Combine(Util.mapsPath(), imageName);
                ImageFilters.removeBKEffects(imagePath);
                return Ok(new { message = "filters group(2) applied over the images successfully", imagePath = imagePath });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }
    }
}
