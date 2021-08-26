using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MapsUnderstanding.Models
{
    public class TessTextDef
    {
        //public int no { set; get; }
        public int level { set; get; }
        public int page_num { set; get; }
        public int block_num { set; get; }
        public int par_num { set; get; }
        public int line_num { set; get; }
        public int word_num { set; get; }
        public int left { set; get; }
        public int top { set; get; }
        public int height { set; get; }
        public int width { set; get; }
        public double confidence { set; get; }
        public string text { set; get; }
        public string CorrectWord { set; get; }
        public double MatchingDegree { set; get; }

    }
}
