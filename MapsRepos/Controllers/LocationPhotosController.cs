using MapsRepos.Data;
using MapsRepos.Models;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;

namespace MapsRepos.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class LocationPhotosController : Controller
    {
        private string mainSolutionFolder = "C:\\Users\\Adel\\source\\repos\\WebDataScience\\MapsVisionGit";
        private string pythonServer = "http://localhost:5000/";
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
        [HttpGet("AllLocationWholePhotos")]
        public IActionResult AllLocationWholePhotos()
        {
            try
            {
                var alldata = repository.GetAll();
                var model = from s in alldata
                                      where s.quarter.Trim()=="whole"
                                      select new { s.lat, s.lng, s.zoom_level, 
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
