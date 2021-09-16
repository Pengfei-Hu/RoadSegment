using MapsUnderstanding.Handlers;
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
