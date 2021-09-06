using MapsUnderstanding.Middleware;
using MapsVisionsAPI.Middleware;
using Microsoft.AspNetCore.Mvc;
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
        [HttpPost("applyEffectsToAllImgs")]
        public IActionResult applyEffectsToAllImgs()
        {
            try
            {
                Request.Headers.TryGetValue("imagePath", out var imagesName);
                Request.Headers.TryGetValue("effects", out var filters);
                string[] imgs = imagesName.ToString().Split(",");
                Console.WriteLine(filters.ToString());
                string[] filtersName = filters.ToString().Split(",");
                
                string log = "";
                foreach (var img in imgs) {
                    var imageName = img.ToString().Replace("/", "\\");
                    var imagePath = Path.Combine(Util.mapsPath(), imageName);
                    ImageFilters.removeEffectedImg(imagePath);
                    log += "Image Name:" + imageName + " ; \n";
                    try
                    {
                        foreach (var filterName in filtersName)
                        {
                            if (filterName.Trim() == "gray")
                            {
                                ImageFilters.applyGrayFilter(imagePath);
                                log += "gray filter applied; \n";

                            }
                            else if (filterName.Trim() == "dilate")
                            {
                                ImageFilters.applyDilateFilter(imagePath);
                                log += "dilate filter applied;\n ";
                            }
                            else if (filterName.Trim() == "resize")
                            {
                                ImageFilters.applyResizeFilter(imagePath);
                                log += "Resize filter applied; \n";
                            }
                            else if (filterName.Trim() == "erosion")
                            {
                                ImageFilters.applyErosionFilter(imagePath);
                                log += "Erosion filter applied; \n";
                            }
                            else if (filterName.Trim() == "thresh")
                            {
                                if(ImageFilters.applyThresholdFilter(imagePath))
                                    log += "Thresh filter applied; \n";
                                else
                                    log += "Thresh filter not applied; \n";
                            }
                            else if (filterName.Trim() == "contours")
                            {
                                if (ImageFilters.applyContoursFilter(imagePath))
                                    log += "Text Contours filter applied; \n";
                                else
                                    log += "Text Contours not applied; \n";
                            }
                        }
                    }catch(Exception ex)
                    {
                        log+="Exception:"+ ex.Message+" ; \n";
                    }
                }
                return Ok(new { message = "filters applied over the images successfully", log = log });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
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
