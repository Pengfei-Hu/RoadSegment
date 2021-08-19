using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace MapsVisionsAPI.Models
{
    public class Location_Photos
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int capture_id { set; get; }
        public double lng { get; set; }
        public double lat { get; set; }
        public string map_provider { get; set; }
        public int zoom_level { get; set; }
        public string capture_url { get; set; }
        public string quarter { get; set; }
        public int? main_capture_id { get; set; }
        public string city_code { get; set; }
    }
}
