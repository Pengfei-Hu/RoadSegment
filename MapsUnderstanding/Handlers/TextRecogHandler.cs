using MapsUnderstanding.Middleware;
using MapsUnderstanding.Models;
using MapsVisionsAPI.Middleware;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace MapsUnderstanding.Handlers
{
    public class TextRecogHandler
    {
        TesseractReading Tess = new TesseractReading();

        public void readTextDetails(string imagePath,out float confidence, out string text, out string detailedText,out List<TessTextDef> wordsList, out string textList)
        {
            Tess.TesseractReader(imagePath, out confidence, out text, out detailedText);
            wordsList = TextProcessing.CastCSVToDataTable(new StringReader(detailedText), out textList);
        }

        public MapImageRecogResults getTextRecogDetails(string groundTruth, string imagePath, 
            int capture_id,string effects, int resolution,out List<TessTextDef> detectedWordsTable, bool isPathFinal = false)
        {           
            string[] correctWords =TextProcessing.getGoodList( groundTruth);

            double matchingDegree = 0;
            double sumMatchingDegree = 0;
            int countMatchingDegreeRows = 0;
            int wrongWords = 0;
            string bagOfWrongWords = "";
            int undetectedWords = 0;
            int detectedWords = 0;
            double totalMatchingDegree = 0;

            tableOfDetectedWords(imagePath, out var confidence, out var tableOfWordsResult, out var detetectedWords, isPathFinal);
            List<TessTextDef> tableOfWordsResultWithMatchingDegree =
                TextProcessing.getTableWithMatchingDegree(tableOfWordsResult,
                                                correctWords, out wrongWords, out bagOfWrongWords,
                                                out countMatchingDegreeRows, out sumMatchingDegree);

            List<string> undetectedTable =
                 TextProcessing.getTableOfUndetectedWords(correctWords, tableOfWordsResultWithMatchingDegree);

            undetectedWords = undetectedTable.Count;
            detectedWords = tableOfWordsResultWithMatchingDegree.Count;
            if (countMatchingDegreeRows != 0)
                matchingDegree = sumMatchingDegree / countMatchingDegreeRows;
            else
                matchingDegree = 0.0;
            if ((countMatchingDegreeRows + wrongWords + undetectedWords) != 0)
                totalMatchingDegree = sumMatchingDegree / (countMatchingDegreeRows + wrongWords + undetectedWords);
            else
                totalMatchingDegree = 0.0;
            if(detectedWords==0 && correctWords.Length == 0)
            {
                matchingDegree = 1.0;
                totalMatchingDegree = 1.0;
            }
            detectedWordsTable = tableOfWordsResultWithMatchingDegree;
            //precision 	= detected correctly / all detection
            //fraction of relevant instances among the retrieved instances
            double precision = 1.0;
            if(detectedWords + wrongWords!=0)
                precision= (double) detectedWords / (detectedWords + wrongWords);
            //fraction of relevant instances that were retrieved
            //recall  	= detected correctly / ground truth
            double recall = 1.0;
            if(correctWords.Length!=0)
                recall = (double) detectedWords / correctWords.Length;
            //F1 = 2 * (precision * recall)/(precision+recall)
            //This measure is approximately the average of the two when they are close, and is more generally the harmonic mean.
            double f1 = 0.0;
            if(precision + recall!=0)
                f1 = (double) (2 *(precision * recall) / (precision + recall));

            var res = new MapImageRecogResults
            {
                capture_id = capture_id,
                picture_url = imagePath,
                effects = effects,
                resolution = resolution,
                correct_words = string.Join(",", correctWords),
                no_correct_words = correctWords.Length,
                precision = precision,
                recall = recall,
                f1 = f1,
                //detected_words_details = tableOfWordsResultWithMatchingDegree,
                detected_words = detetectedWords,
                no_detected_words = detectedWords,
                undetected_words = string.Join(",", undetectedTable),
                no_undetected_words = undetectedWords,
                wrong_words = bagOfWrongWords,
                no_wrong_words = wrongWords,

                confidence = Math.Round(confidence, 3),
                matching_degree = Math.Round((matchingDegree.ToString() == "NaN") ? 0.0 : double.Parse(matchingDegree.ToString("0.##")), 3),
                total_matching_degree = Double.Parse(totalMatchingDegree.ToString("0.##"))
            };
            return res;
        }


        public void tableOfDetectedWords(string imagePath, out float confidence, out List<TessTextDef> table, out string detectedWords, bool isPathFinal=false)
        {
            string allText = "";
            if (!File.Exists(imagePath))
            {
                Console.WriteLine("-=-=-=-:No Image Exists:-=-=-=-");
                Console.WriteLine( imagePath);
            }
            if (!isPathFinal )
            {
                imagePath = imagePath.ToString().Replace("/", "\\");
                imagePath = ImageFilters.getfilteredImgPath(imagePath);
                imagePath = Path.Combine(Util.mapsPath(), imagePath);
            }
            Console.WriteLine("imagePath::::::" + imagePath);
            string detectedText = "";
            Tess.TesseractReader(imagePath, out confidence, out detectedText, out allText);

            detectedText = string.Join("," ,  TextProcessing.castLinedTextToStringArray(detectedText));

            var tableOfWordsResult = TextProcessing.CastCSVToDataTable(new StringReader(allText), out detectedWords);
            Console.WriteLine("detectedWords::::::::::::::::" + detectedWords);
            Console.WriteLine("detectedText::::::::::::::::" + detectedText);
            table = tableOfWordsResult;
        }

    }
}
