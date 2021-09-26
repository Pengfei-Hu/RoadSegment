using MapsUnderstanding.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace MapsUnderstanding.Models
{
    //[Keyless]
    public class MapImageRecogResults
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int result_id { set; get; }
        public int capture_id { set; get; }
        public string picture_url { get; set; }
        public int resolution { get; set; }
        public string detected_words { get; set; }
        //public List<TessTextDef> detected_words_details { get; set; }
        public int no_detected_words { get; set; }
        public string undetected_words { get; set; }
        public int no_undetected_words { get; set; }
        public string correct_words { get; set; }
        public int no_correct_words { get; set; }
        public string wrong_words{ get; set; }
        public int no_wrong_words { get; set; }
        public string effects { get; set; }
        public Double confidence { get; set; }
        public Double matching_degree { get; set; }
        public Double total_matching_degree { get; set; }
        public Double recall { get; set; }
        public Double precision { get; set; }
        public Double f1 { get; set; }

    }
}
