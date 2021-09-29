using MapsUnderstanding.Middleware;
using MapsUnderstanding.Models;
using MapsVisionsAPI.Middleware;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace MapsUnderstanding.Handlers
{
    public class CVHandler
    {
        public List<ColorsCounts> colorsCounter(string imageName)
        {
            try
            {
                imageName = imageName.ToString().Replace("/", "\\");
                var imagePath = Path.Combine(Util.mapsPath(), imageName);
                Console.WriteLine("colorsCounter for image: " + imagePath);
                return ImageFilters.getKMeansColors(imagePath);
            }catch(Exception ex)
            {
                Console.WriteLine(ex.Message);
                Console.Write(ex.StackTrace);
                return null;
            }
        }

        public string applyEffectsToImgs(string imagesName, string filters)
        {
            string[] imgs = imagesName.ToString().Split(",");
            Console.WriteLine(filters.ToString());
            string[] filtersName = filters.ToString().Split(",");

            string log = "";
            foreach (var img in imgs)
            {
                var imageName = img.ToString().Replace("/", "\\");
                var imagePath = Path.Combine(Util.mapsPath(), imageName);
                ImageFilters.removeEffectedImg(imagePath);
                log += "Image Name:" + imageName + " ; \n";
                try
                {
                    foreach (var filterName in filtersName)
                    {
                        if (filterName.Trim().ToLower() == "resize")
                        {
                            ImageFilters.applyResizeFilter(imagePath);
                            log += "Resize filter applied; \n";
                        }else
                        if (filterName.Trim().ToLower() == "bgbitwise")
                        {
                            ImageFilters.applyBGBitwise(imagePath);
                            log += "BKBitwise filter applied; \n";
                        }
                        else if (filterName.Trim().ToLower() == "bgtransparent")
                        {
                            if (ImageFilters.applyBGTransparent(imagePath))
                                log += "BKTransparent filter applied; \n";
                            else
                                log += "BKTransparent not applied; \n";
                        }
                        else if (filterName.Trim().ToLower() == "bgtrans2white")
                        {
                            if (ImageFilters.applyBGTrans2White(imagePath))
                                log += "BGTrans2White filter applied; \n";
                            else
                                log += "BKTransparent not applied; \n";
                        }
                        else if (filterName.Trim().ToLower() == "enhancedetail")
                        {
                            ImageFilters.applyEnhanceDetailFilter(imagePath);
                            log += "enhanceDetail filter applied; \n";
                        }
                        else if (filterName.Trim().ToLower() == "gray")
                        {
                            ImageFilters.applyGrayFilter(imagePath);
                            log += "gray filter applied; \n";

                        }
                        else if (filterName.Trim().ToLower() == "dilate")
                        {
                            ImageFilters.applyDilateFilter(imagePath);
                            log += "dilate filter applied;\n ";
                        }
                        else if (filterName.Trim().ToLower() == "erosion")
                        {
                            ImageFilters.applyErosionFilter(imagePath);
                            log += "Erosion filter applied; \n";
                        }
                        else if (filterName.Trim().ToLower() == "thresh")
                        {
                            if (ImageFilters.applyThresholdFilter(imagePath))
                                log += "Thresh filter applied; \n";
                            else
                                log += "Thresh filter not applied; \n";
                        }
                        else if (filterName.Trim().ToLower() == "contours")
                        {
                            if (ImageFilters.applyContoursFilter(imagePath))
                                log += "Text Contours filter applied; \n";
                            else
                                log += "Text Contours not applied; \n";
                        }
                        else if (filterName.Trim().ToLower() == "bitwisetext")
                        {
                            if (ImageFilters.applyBitwiseText(imagePath))
                                log += "bitwiseText filter applied; \n";
                            else
                                log += "bitwiseText not applied; \n";
                        }
                        else if (filterName.Trim().ToLower() == "kmeans")
                        {
                            if (ImageFilters.applyKMeansFilter(imagePath))
                                log += "KMeans filter applied; \n";
                            else
                                log += "KMeans not applied; \n";
                        }
                    }
                }
                catch (Exception ex)
                {
                    log += "Exception:" + ex.Message + " ; \n";
                }
            }
            return log;
        }

    }
}
