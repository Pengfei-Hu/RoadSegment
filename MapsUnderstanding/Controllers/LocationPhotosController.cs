using MapsVisionsAPI.Data;
using MapsVisionsAPI.Models;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;

namespace MapsVisionsAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class LocationPhotosController : Controller
    {
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
                                      select s;
                           
                return Ok(new { data = model });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }
    }
}
