using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using MapsUnderstanding.Models;
using OpenCvSharp;
using OpenCvSharp.Extensions;

namespace MapsVisionsAPI.Middleware
{
    public class ImageFilters
    {
        public static bool applyGrayscale(string imagePath)
        {            
            Mat Grayscale = Cv2.ImRead(imagePath, ImreadModes.Grayscale);
            return saveMatImage(Grayscale, "Grayscale1", imagePath);
        }

        public static string getfilteredImgPath(string sourcePath)
        {
            if (sourcePath.IndexOf("filtered-") == -1)
                return Path.Combine(sourcePath.Substring(0, sourcePath.LastIndexOf("\\") + 1),
                          "filtered-" + sourcePath.Substring(sourcePath.LastIndexOf("\\") + 1));
            else
                return sourcePath;
        }

        
        internal static List<ColorsCounts> getColorsCounts(string imagePath)
        {
            Dictionary<string, int> colorsCounter = new Dictionary<string, int>();
            List<ColorsCounts> colorsCounts=new List<ColorsCounts>();

            Mat img = readFilteredImg(imagePath);
            var matIndex = new Mat<Vec3b>(img); // cv::Mat_<cv::Vec3b>
            var indexer = matIndex.GetIndexer();

            for (int y = 0; y < img.Height; y++)
            {
                for (int x = 0; x < img.Width; x++)
                {
                    Vec3b color = indexer[y, x];
                    if (!(color.Item0 == 0 && color.Item0 == 0 && color.Item0 == 0))
                    {
                        //indexer[y, x] = color;
                        int currentCounter = 0;
                        string key = "rgb("+color.Item0.ToString() + "," + color.Item1.ToString()
                                + "," + color.Item2.ToString()+")";
                        if (colorsCounts.Exists(ele => ele.color == key))
                        {
                            var colorCount = colorsCounts.Find(ele => ele.color == key);
                            colorsCounts.Remove(colorCount);
                            colorCount.count = colorCount.count + 1;
                            colorsCounts.Add(colorCount);
                        }
                        else
                            colorsCounts.Add(new ColorsCounts { color = key, count = 1 });

                        if (colorsCounter.TryGetValue(key, out currentCounter))
                            colorsCounter[key] = ++currentCounter;
                        else
                            colorsCounter.Add(key, 1);
                    }
                }
            }
            
            return colorsCounts;
        }
        public static List<ColorsCounts> getKMeansColors(string imagePath)
        {
            List<ColorsCounts> colorsCounts = new List<ColorsCounts>();
            Mat image = readFilteredImg(imagePath);
            Mat kmeansImg = new Mat();
            var colorsCounter = Kmeans(image, ref kmeansImg, 6);
            foreach(var colorCount in colorsCounter)
                if(colorCount.Key!="255,255,255")
                    colorsCounts.Add(new ColorsCounts { color = colorCount.Key, count = colorCount.Value });
            saveMatImage(kmeansImg, "kmeans", imagePath);
            return colorsCounts;
        }
        protected static bool IsFileLocked(FileInfo file)
        {
            try
            {
                using (FileStream stream = file.Open(FileMode.Open, FileAccess.Read, FileShare.None))
                {
                    stream.Close();
                }
            }
            catch (IOException)
            {
                //the file is unavailable because it is:
                //still being written to
                //or being processed by another thread
                //or does not exist (has already been processed)
                return true;
            }

            //file is not locked
            return false;
        }
        private static bool saveMatImage(Mat img, string name, string sourcePath)
        {
            var imagePath = Path.Combine(sourcePath.Substring(0,sourcePath.LastIndexOf("\\")+1),
                   name +"-"+ sourcePath.Substring(sourcePath.LastIndexOf("\\")+1));
            //if (! IsFileLocked(new FileInfo(imagePath))){
            img.SaveImage(imagePath);
            img.Dispose();
                /*using (Bitmap bitmap = BitmapConverter.ToBitmap(img))
                {
                    bitmap.Save(imagePath);
                }*/
                    
            //}
            return true;
        }
        public static bool removeEffectedImg(string imagePath)
        {
            if (File.Exists(getfilteredImgPath(imagePath)))
            {
                File.Delete(getfilteredImgPath(imagePath));

            }
            return saveMatImage(readFilteredImg(imagePath), "filtered", imagePath);
        }
        public static bool applyGrayFilter(string imagePath)
        {
            Mat image = readFilteredImg(imagePath);
            Mat grayImg = new Mat();
            Cv2.CvtColor(image, grayImg, ColorConversionCodes.BGR2GRAY);
            return saveMatImage(grayImg, "filtered", imagePath);
        }
        private static Mat readFilteredImg(string imagePath)
        {
            Mat image;
            if (!File.Exists(getfilteredImgPath(imagePath)))
                image = Cv2.ImRead(imagePath, ImreadModes.Unchanged);
            else
                image = Cv2.ImRead(getfilteredImgPath(imagePath), ImreadModes.Unchanged);
            return image;
        }
        public static bool applyDilateFilter(string imagePath)
        {
            Mat image= readFilteredImg(imagePath);
            Mat dilateImg = new Mat();
            Cv2.Dilate(image, dilateImg, null, null, 1);
            return saveMatImage(dilateImg, "filtered", imagePath);
        }
        public static Dictionary<string, int> Kmeans(Mat input, ref Mat output, int k)
        {
            Dictionary<string, int> colorsCounter = new Dictionary<string, int>();
            using (Mat points = new Mat())
            {
                using (Mat labels = new Mat())
                {
                    using (Mat centers = new Mat())
                    {
                        int width = input.Cols;
                        int height = input.Rows;

                        points.Create(width * height, 1, MatType.CV_32FC3);
                        centers.Create(k, 1, points.Type());
                        output.Create(height, width, input.Type());

                        // Input Image Data
                        int i = 0;
                        for (int y = 0; y < height; y++)
                        {
                            for (int x = 0; x < width; x++, i++)
                            {
                                Vec3f vec3f = new Vec3f
                                {
                                    Item0 = input.At<Vec3b>(y, x).Item0,
                                    Item1 = input.At<Vec3b>(y, x).Item1,
                                    Item2 = input.At<Vec3b>(y, x).Item2
                                };
                                points.Set<Vec3f>(i, vec3f);
                            }
                        }

                        // Criteria:
                        // – Stop the algorithm iteration if specified accuracy, epsilon, is reached.
                        // – Stop the algorithm after the specified number of iterations, MaxIter.
                        var criteria = new TermCriteria(type: CriteriaTypes.Eps | CriteriaTypes.MaxIter, maxCount: 10, epsilon: 1.0);

                        // Finds centers of clusters and groups input samples around the clusters.
                        Cv2.Kmeans(data: points, k: k, bestLabels: labels, criteria: criteria, attempts: 3, flags: KMeansFlags.PpCenters, centers: centers);

                        // Output Image Data
                        i = 0;
                        for (int y = 0; y < height; y++)
                        {
                            for (int x = 0; x < width; x++, i++)
                            {
                                int index = labels.Get<int>(i);

                                Vec3b vec3b = new Vec3b();

                                int firstComponent = Convert.ToInt32(Math.Round(centers.At<Vec3f>(index).Item0));
                                firstComponent = firstComponent > 255 ? 255 : firstComponent < 0 ? 0 : firstComponent;
                                vec3b.Item0 = Convert.ToByte(firstComponent);

                                int secondComponent = Convert.ToInt32(Math.Round(centers.At<Vec3f>(index).Item1));
                                secondComponent = secondComponent > 255 ? 255 : secondComponent < 0 ? 0 : secondComponent;
                                vec3b.Item1 = Convert.ToByte(secondComponent);

                                int thirdComponent = Convert.ToInt32(Math.Round(centers.At<Vec3f>(index).Item2));
                                thirdComponent = thirdComponent > 255 ? 255 : thirdComponent < 0 ? 0 : thirdComponent;
                                vec3b.Item2 = Convert.ToByte(thirdComponent);

                                output.Set<Vec3b>(y, x, vec3b);
                                int currentCounter = 0;
                                string key = vec3b.Item0.ToString() + "," + vec3b.Item1.ToString()
                                        + "," + vec3b.Item2.ToString();
                                if (colorsCounter.TryGetValue(key, out currentCounter))
                                    colorsCounter[key] = ++currentCounter;
                                else
                                    colorsCounter.Add(key, 1);
                            }
                        }

                    }
                }
            }
            return colorsCounter;
        }
        public static bool applyKMeansFilter(string imagePath)
        {
            Mat image = readFilteredImg(imagePath);
            Mat kmeansImg = new Mat();
            var colorsCounter = Kmeans(image, ref kmeansImg, 3);
            return saveMatImage(kmeansImg, "filtered", imagePath);
        }
        public static bool applyResizeFilter(string imagePath)
        {
            Mat image = readFilteredImg(imagePath);
            Mat rescaledImage = new Mat();
            var scale_percent = 400; // percent of original size
            var width = (int) image.Width * scale_percent / 100;
            var height = (int)image.Height * scale_percent / 100;
            Cv2.Resize(image, rescaledImage, new OpenCvSharp.Size(width, height), 2, 2, InterpolationFlags.Area);
            return saveMatImage(rescaledImage, "filtered", imagePath);
        }
        public static bool applyEnhanceDetailFilter(string imagePath)
        {
            Mat image = readFilteredImg(imagePath);
            Mat enhanceImage = new Mat();
            Cv2.DetailEnhance(image, enhanceImage, 10, 0.15f);
            return saveMatImage(enhanceImage, "filtered", imagePath);
        }
        public static bool applyBitwiseText(string imagePath)
        {
            Mat imageImg = readFilteredImg(imagePath);
            Mat grayImg = new Mat();
            Mat threshImg = new Mat();
            Cv2.CvtColor(imageImg, grayImg, ColorConversionCodes.BGR2GRAY);
            Mat kernel = Cv2.GetStructuringElement(MorphShapes.Rect, new OpenCvSharp.Size(1, 1));
            Cv2.Dilate(grayImg, grayImg, kernel);                         //dilate to remove text and tables
            Cv2.Threshold(grayImg, threshImg, 118, 255, ThresholdTypes.Binary);     //change white background to black

            Cv2.Threshold(grayImg, grayImg, 100, 255, ThresholdTypes.BinaryInv);   //invert binary image for easier processing
            Mat final = grayImg;
            Cv2.BitwiseNot(grayImg, threshImg, final);
            return saveMatImage(threshImg, "filtered", imagePath);
        }
        public static bool applyContoursFilter(string imagePath)
        {
            try
            {
                TesseractReading tess = new TesseractReading();
                Mat image = readFilteredImg(imagePath);

                Mat img_gray = new Mat();
                Mat thresh = new Mat();
                OpenCvSharp.Point[][] contours;
                // OpenCvSharp.Point[][] acceptedContours;
                float confidence;
                string allText;
                string csvText;
                Cv2.CvtColor(image, img_gray, ColorConversionCodes.BGR2GRAY);
                Cv2.Threshold(img_gray, thresh, 200, 255, ThresholdTypes.BinaryInv);
                var lastImagePath = "";
                if (!File.Exists(getfilteredImgPath(imagePath)))
                    lastImagePath = imagePath;
                else
                    lastImagePath = getfilteredImgPath(imagePath);

                tess.TesseractReader(lastImagePath, out confidence, out allText, out csvText);


                //Mat[] contours;
                HierarchyIndex[] hierarchy;
                Cv2.FindContours(thresh, out contours, out hierarchy, RetrievalModes.Tree, ContourApproximationModes.ApproxSimple);
                Mat image_txt = image.EmptyClone(); // New White Image
                image_txt = image_txt.SetTo(Scalar.White);

                List<OpenCvSharp.Rect> rects = getRectangles(ref image_txt, new StringReader(csvText), "");

                for (int i = 1; i < contours.Length; i++)
                {
                    if (Cv2.ContourArea(contours[i]) > 4 && Cv2.ContourArea(contours[i]) < 100)
                    {
                       // Console.WriteLine("ContourArea=" + Cv2.ContourArea(contours[i]));
                        Cv2.DrawContours(image_txt, contours, i, Scalar.Black);
                    }
                }
                saveMatImage(image_txt, "filtered", imagePath);
                return true;
            }catch(Exception ex)
            {
                Console.Write(ex);
                return false;
            }
        }

        public static bool applyErosionFilter(string imagePath)
        {
            Mat image = readFilteredImg(imagePath);
            Mat erodeImg = new Mat();
            Cv2.Erode(image, erodeImg, null, null, 1);
            return saveMatImage(erodeImg, "filtered", imagePath);
        }
        public static bool applyThresholdFilter(string imagePath)
        {
            try
            {
                Mat image = readFilteredImg(imagePath);
                Mat threshImg = new Mat();
                Mat grayImg = new Mat();
                Cv2.CvtColor(image, grayImg, ColorConversionCodes.BGR2GRAY);
                Cv2.AdaptiveThreshold(grayImg, threshImg, 255, AdaptiveThresholdTypes.MeanC, ThresholdTypes.Binary, 17, 13);
                return saveMatImage(threshImg, "filtered", imagePath);
            }catch(Exception ex)
            {
                Console.Write(ex);
                return false;
            }
        }

        public static bool applyBestEffects1(string imagePath)
        {
            Mat image = Cv2.ImRead(imagePath, ImreadModes.Unchanged);
            Mat grayImg=new Mat();
            Mat erosion = new Mat();
            Mat thresh = new Mat();
            Mat opening = new Mat();
            Mat dilate = new Mat();
            
            Cv2.CvtColor(image, grayImg, ColorConversionCodes.BGR2GRAY);

            //gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            Mat kernel = Cv2.GetStructuringElement(MorphShapes.Rect, new OpenCvSharp.Size(3, 3));

            Cv2.AdaptiveThreshold(grayImg, thresh, 255, AdaptiveThresholdTypes.MeanC, ThresholdTypes.Binary, 17,13);
            Cv2.Erode(grayImg, erosion, null, null, 1);
            Cv2.Dilate(grayImg, dilate, null,null,  1);
            // thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)

            // Morph open
            // kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

            Cv2.MorphologyEx(thresh, opening, MorphTypes.Erode, kernel,null, 1);
            //opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 1)

            //Remove noise by filtering using contour area
            Mat[] contours;//= new Mat[]();
            Mat hierarchy = new Mat();
            Mat cnts = new Mat();
            Cv2.FindContours(opening, out contours, hierarchy, RetrievalModes.External, 
                ContourApproximationModes.ApproxSimple);
            //cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if (contours.Length == 2)
                cnts = contours[0];
            else
                cnts = contours[1];
            int x = 0;
            foreach(var c in contours)
            {
  /*              
               Mat img_contours =Cv2.
# draw the contours on the empty image
cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3)
*/
                saveMatImage(c, "contours"+x.ToString(), imagePath);
                x++;
                double area=  Cv2.ContourArea(c);
                if (area < 10)
                    Cv2.DrawContours(opening, new[] { c }, -1, Scalar.Black, -1);
            }
            /*
            for c in cnts:
                area = cv2.contourArea(c)
                if area < 10:
                    cv2.drawContours(opening, [c], -1, (0, 0, 0), -1)
                */
            // Invert image for result
            Mat result = 255 - opening;
            saveMatImage(image, "normal", imagePath);
            saveMatImage(grayImg, "gray", imagePath);
            saveMatImage(dilate, "dilate", imagePath);
            saveMatImage(erosion, "erosion", imagePath);
            saveMatImage(thresh, "ThreshMeanCBinary", imagePath);
            saveMatImage(opening, "opening", imagePath);
            saveMatImage(result, "result", imagePath);
            return true;
        }
        public static bool applyBGTransparent(string imagePath)
        {
            try
            {
                Mat src = readFilteredImg(imagePath);
                Mat dst = new Mat(), tmp = new Mat(), alpha = new Mat();

                Cv2.CvtColor(src, tmp, ColorConversionCodes.BGR2GRAY);
                Cv2.Threshold(tmp, alpha, 50, 255, ThresholdTypes.Binary);
                Mat[] rgb;
                Cv2.Split(src, out rgb);

                Mat[] rgba = { rgb[0], rgb[1], rgb[2], alpha };
                Cv2.Merge(rgba, dst);
                return saveMatImage(dst, "filtered", imagePath);
            }
            catch (Exception ex)
            {
                Console.Write(ex);
                return false;
            }
        }
        public static bool applyBGTrans2White(string imagePath)
        {
            try
            {
                Mat src = readFilteredImg(imagePath);
                Mat dst = convertTransparentToWhite(src);
                return saveMatImage(dst, "filtered", imagePath);
            }
            catch (Exception ex)
            {
                Console.Write(ex);
                return false;
            }
        }

        public static Mat convertTransparentToWhite(Mat mat)
        {
            Mat dst = mat.EmptyClone();
            dst = dst.SetTo(Scalar.White);
            var mat3 = new Mat<Vec3b>(mat); // cv::Mat_<cv::Vec3b>
            var indexer = mat3.GetIndexer();

            for (int y = 0; y < mat.Height; y++)
            {
                for (int x = 0; x < mat.Width; x++)
                {
                    Vec3b color = indexer[y, x];
                    //  if ( !(color.Item0 == 0 && color.Item0 == 0 && color.Item0 == 0))
                    //     dst.Set<Vec3b>(x, y, color);

                    // dst.Set(x, y, color);
                    if (!(color.Item0 == 0 && color.Item0 == 0 && color.Item0 == 0))
                    {
                        //byte temp = color.Item0;
                        //color.Item0 = color.Item2; // B <- R
                        //color.Item2 = temp;        // R <- B
                        indexer[y, x] = color;
                    }
                    else
                    {
                        color.Item0 = 255;
                        color.Item1 = 255;
                        color.Item2 = 255;
                        indexer[y, x] = color;

                    }
                    /* Console.Write("color.Item0=" + color.Item0+"\t");
                     Console.Write("color.Item1=" + color.Item1 + "\t");
                     Console.Write("color.Item2=" + color.Item2);
                     Console.WriteLine("");*/

                }
            }
            return mat;
        }
        public static bool applyBGBitwise(string imagePath)
        {
            try
            {
                Mat imageL1 = readFilteredImg(imagePath);
                Mat imageL1C = readFilteredImg(imagePath);
                Cv2.CvtColor(imageL1C, imageL1C, ColorConversionCodes.BGR2BGRA);
                Cv2.CvtColor(imageL1, imageL1, ColorConversionCodes.BGR2GRAY);
                Cv2.CvtColor(imageL1, imageL1, ColorConversionCodes.BGR2BGRA);
                Mat kernel = Cv2.GetStructuringElement(MorphShapes.Rect, new OpenCvSharp.Size(1, 1));
                Mat morphed = new Mat();
                Cv2.MorphologyEx(imageL1, morphed, MorphTypes.Close, kernel);
                Cv2.Dilate(imageL1, imageL1, kernel, null, 1, BorderTypes.Default, Scalar.Black);                         //dilate to remove text and tables
                Cv2.Threshold(imageL1, imageL1, 120, 255, ThresholdTypes.Binary);     //change white background to black

                Cv2.Threshold(imageL1, imageL1, 118, 255, ThresholdTypes.BinaryInv);   //invert binary image for easier processing
                Cv2.Dilate(imageL1, imageL1, null, null, 4);
                Cv2.Erode(imageL1, imageL1, null, null, 1);
                Mat final = imageL1C.EmptyClone(); // New White Image
                final = final.SetTo(Scalar.White);

                Cv2.BitwiseAnd(imageL1C, imageL1, final);
                //Cv2.DetailEnhance(dst, dst, 10, 0.15f);
                return saveMatImage(final, "filtered", imagePath);
            }
            catch (Exception ex)
            {
                Console.Write(ex);
                return false;
            }
        }
            
        public static string removeBKEffects(string imagePath)
        {
            Mat image;
            Mat img_gray = new Mat();
            Mat thresh = new Mat();
            OpenCvSharp.Point[][] contours;
            // OpenCvSharp.Point[][] acceptedContours;
            float confidence;
            string allText;
            string csvText;
            string path = imagePath.Substring(0, imagePath.LastIndexOf("\\"));
            string grayImgPath = Path.Combine(path, "gray.png");
            string filePath = Path.Combine(path, "gray.txt");

            TesseractReading tess = new TesseractReading();
            image = Cv2.ImRead(imagePath); // BitmapConverter.ToMat(original)
                                           // convert the image to grayscale format
            Cv2.CvtColor(image, img_gray, ColorConversionCodes.BGR2GRAY);

            Cv2.Threshold(img_gray, thresh, 200, 255, ThresholdTypes.BinaryInv);
            Cv2.ImWrite(grayImgPath, thresh);
            tess.TesseractReader(grayImgPath, out confidence, out allText, out csvText);


            //Mat[] contours;
            HierarchyIndex[] hierarchy;
            Cv2.FindContours(thresh, out contours, out hierarchy, RetrievalModes.Tree, ContourApproximationModes.ApproxSimple);
            Mat image_txt = image.EmptyClone(); // New White Image
            image_txt = image_txt.SetTo(Scalar.White);

            List<OpenCvSharp.Rect> rects = getRectangles(ref image_txt, new StringReader(csvText), filePath);

            //Cv2.InRange()
            for (int i = 1; i < contours.Length; i++)
            {
                if (Cv2.ContourArea(contours[i]) > 4 && Cv2.ContourArea(contours[i]) < 85)
                {

                    //Console.WriteLine("ContourArea=" + Cv2.ContourArea(contours[i]));
                    // if (ContourIntoRect(contours[i], rects))
                    Cv2.DrawContours(image_txt, contours, i, Scalar.Black);
                    // else
                    //   Cv2.DrawContours(image_txt, contours, i, Scalar.Red);

                    /* Cv2.ImShow("Image Text", image_txt);
                     Cv2.WaitKey(0);
                     Cv2.DestroyAllWindows();*/
                }
            }
            Bitmap bitmap = BitmapConverter.ToBitmap(image_txt);
            string newImgPath = imagePath.Substring(0, imagePath.LastIndexOf("."))+ "_text.png";
            bitmap.Save(newImgPath);
            return newImgPath;
        }
        private static List<OpenCvSharp.Rect> getRectangles(ref Mat img_txt, StringReader csvText, string filePath)
        {
            string line = "";
            List<OpenCvSharp.Rect> rects = new List<OpenCvSharp.Rect>();
            while ((line = csvText.ReadLine()) != null)
            {
                var cells = line.Split("\t");
                string word = cells[11].Trim();
                if ((cells[10].Trim() != "-1") && (word != ""))
                {
                    /*if (word.Length > 2)
                    {*/
                    OpenCvSharp.Rect rect = new OpenCvSharp.Rect(
                            Int32.Parse(cells[6].Trim()),
                            Int32.Parse(cells[7].Trim()),
                            Int32.Parse(cells[8].Trim()),
                            Int32.Parse(cells[9].Trim()));
                    rects.Add(rect);
                    //   Cv2.Rectangle(img_txt, rect, Scalar.Purple);
                    if(filePath!="")
                        File.AppendAllText(filePath, line + "\n");
                    /*Cv2.ImShow("Image Text", img_gray);
                    Cv2.WaitKey(0);
                    Cv2.DestroyAllWindows();*/
                    /*}*/
                }
            }
            return rects;
            //Cv2.ImShow("Gray mage", img_gray);
            //Cv2.WaitKey(0);
            //Cv2.DestroyAllWindows();

        }

    }
}
