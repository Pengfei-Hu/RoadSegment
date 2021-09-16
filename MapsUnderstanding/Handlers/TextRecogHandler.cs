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
    public class TextRecogHandler
    {
        TesseractReading Tess = new TesseractReading();
        public MapImageRecogResults getTextRecogDetails(string groundTruth, string imagePath, 
            int capture_id,string effects, int resolution)
        {
            string[] correctWords = groundTruth.Split(",");

            if (correctWords[0] == "")
                correctWords = correctWords.Where((source, index) => index != 0).ToArray();
            Console.WriteLine("allWords=" + groundTruth);
            Console.WriteLine("correctWords.length=" + correctWords.Length);
            Console.WriteLine("correctWords=" + correctWords);

            double matchingDegree = 0;
            double sumMatchingDegree = 0;
            int countMatchingDegreeRows = 0;
            int wrongWords = 0;
            string bagOfWrongWords = "";
            int undetectedWords = 0;
            int detectedWords = 0;
            double totalMatchingDegree = 0;

            tableOfDetectedWords(imagePath, out var confidence, out var tableOfWordsResult, out var detetectedWords);
            List<TessTextDef> tableOfWordsResultWithMatchingDegree =
                TextProcessing.getTableWithMatchingDegree(tableOfWordsResult,
                                                correctWords, out wrongWords, out bagOfWrongWords,
                                                out countMatchingDegreeRows, out sumMatchingDegree);

            List<string> undetectedTable =
                 TextProcessing.getTableOfUndetectedWords(correctWords, tableOfWordsResultWithMatchingDegree);

            undetectedWords = undetectedTable.Count;
            detectedWords = tableOfWordsResultWithMatchingDegree.Count;
            matchingDegree = sumMatchingDegree / countMatchingDegreeRows;
            totalMatchingDegree = sumMatchingDegree / (countMatchingDegreeRows + wrongWords + undetectedWords);

            return new MapImageRecogResults
            {
                
                capture_id = capture_id,
                picture_url = imagePath,
                effects = effects,
                resolution = resolution,
                //detected_words_details = tableOfWordsResultWithMatchingDegree,
                detected_words = detetectedWords,
                no_detected_words = detectedWords,
                undetected_words = string.Join(",", undetectedTable) ,
                no_undetected_words = undetectedWords,
                wrong_words = bagOfWrongWords,
                no_wrong_words = wrongWords,

                confidence = Math.Round(confidence,3),
                matching_degree= Math.Round((matchingDegree.ToString() == "NaN") ? 0f :float.Parse( matchingDegree.ToString("0.##")),3),
                total_matching_degree = Math.Round(float.Parse( totalMatchingDegree.ToString("0.##")),3)
            };
        }

        public void tableOfDetectedWords(string imagePath, out float confidence, out List<TessTextDef> table, out string detectedWords)
        {
            string allText = "";
            imagePath = imagePath.ToString().Replace("/", "\\");
            imagePath = ImageFilters.getfilteredImgPath(imagePath);
            imagePath = Path.Combine(Util.mapsPath(), imagePath);
            Tess.TesseractReader(imagePath, out confidence, out detectedWords, out allText);

            detectedWords = string.Join("," ,  TextProcessing.castLinedTextToStringArray(detectedWords));
            Console.WriteLine("ImagePath:" +  imagePath);
            Console.WriteLine("detectedWords:" + detectedWords);

            var tableOfWordsResult = TextProcessing.CastCSVToDataTable(new StringReader(allText));
            table = tableOfWordsResult;
        }

    }
}
