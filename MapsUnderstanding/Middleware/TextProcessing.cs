using MapsUnderstanding.Models;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace MapsVisionsAPI.Middleware
{
    public class TextProcessing
    {
        public static TessTextDef getTessTextDef(string[] rowData)
        {
            TessTextDef tessText = new TessTextDef();
            tessText.level = Int32.Parse(rowData[0]);
            tessText.page_num = Int32.Parse(rowData[1]);
            tessText.block_num = Int32.Parse(rowData[2]);
            tessText.par_num = Int32.Parse(rowData[3]);
            tessText.line_num = Int32.Parse(rowData[4]);
            tessText.word_num = Int32.Parse(rowData[5]);
            tessText.left = Int32.Parse(rowData[6]);
            tessText.top = Int32.Parse(rowData[7]);
            tessText.width = Int32.Parse(rowData[8]);
            tessText.height = Int32.Parse(rowData[9]);
            tessText.confidence = Int32.Parse(rowData[10]);
           
            var text = getGoodList(rowData[11].ToString());
            //Console.Write(JsonConvert.SerializeObject(results, Formatting.Indented));
            if (text.Length > 0)
                if (text[0].Trim().Length > 0)
                {
                    tessText.text = text[0].Trim();
                    return tessText;
                }
                else
                    return null;
            else
                return null;
        }
        public static string[] getGoodList(string fullText)
        {
            try
            {
                string pattern = @"\w\d{1,4}";
                Regex rg = new Regex(pattern);
                string[] bagOfWords = fullText.Split(",");
                Console.WriteLine("Correct Words Before:" + bagOfWords.Length);
                List<string> filteredWords = new List<string>();
                foreach (var word in bagOfWords)
                    if (!rg.Match(word).Success && word.Trim().Length > 1)
                    {
                        var wordWithoutSpecialChars = Regex.Replace(word.Trim(), "[^a-zA-Z0-9\\s]+", "");
                        if (wordWithoutSpecialChars.Length > 2)
                            filteredWords.Add(wordWithoutSpecialChars);
                        else
                            if (isWhiteList(wordWithoutSpecialChars))
                            filteredWords.Add(wordWithoutSpecialChars);
                    }
                Console.WriteLine("Correct Words After:" + filteredWords.Count);
                return filteredWords.ToArray();
            }catch(Exception ex)
            {
                return new string[] {};
            }
        }
        public static bool isWhiteList(string wordWithoutSpecialChars)
        {
            return "Rd,St".ToLower().IndexOf(wordWithoutSpecialChars.ToLower()) != -1;
        }
        public static List<TessTextDef> CastCSVToDataTable(StringReader reader, out string detectedWords)
        {
            string line = "";
            List<TessTextDef> datatable = new List<TessTextDef>();
            detectedWords = "";
            while ((line = reader.ReadLine()) != null)
            {
                string[] rowData = line.Split('\t');
               
                if (rowData[rowData.Length - 1].Trim().Length > 0)
                {
                    var tessText = getTessTextDef(rowData);
                    if (tessText != null)
                    {
                        datatable.Add(tessText);
                        detectedWords += tessText.text+",";
                    }
                }
            }
            if (detectedWords.Length > 0)
                detectedWords = detectedWords.Substring(0, detectedWords.Length - 1);
            return datatable;
        }
        public static string[] castLinedTextToStringArray(string allText)
        {
           string [] arrText = allText.Split("\n").Where(ele => ele.Trim() != "").ToArray();
            return getGoodList(string.Join(",", arrText));
        }
        public static List<string> getTableOfUndetectedWords(string[] CorrectWords, List<TessTextDef> tableOfWordsResult)
        {
            List<string> undetectedTable = new List<string>();
            for (int x = 0; x < CorrectWords.Length; x++)
            {
                bool exists = false;
                for (int row = 0; row < tableOfWordsResult.Count; row++)
                {
                    TessTextDef line = tableOfWordsResult[row];

                    string CWordTable = line.CorrectWord.ToString();
                    if (CWordTable.Trim().Length > 0)
                        if (CorrectWords[x].Trim().Contains(CWordTable))
                        {
                            exists = true;
                            continue;
                        }
                }
                if (!exists)
                {
                    undetectedTable.Add(CorrectWords[x]);
                }

            }
            return undetectedTable;
        }
        public static List<TessTextDef> getTableWithMatchingDegree(List<TessTextDef> tableOfWordsResult, string[] correctWords, 
                                out int wrongWords, out string bagOfWrongWords, out int countMatchingDegreeRows, 
                                out double sumMatchingDegree)
        {
            List<TessTextDef> tableOfWordsResultWithMatchingDegree = new List<TessTextDef>();
            wrongWords = 0;
            bagOfWrongWords = "";
            countMatchingDegreeRows = 0;
            sumMatchingDegree = 0;
            int lineno = 0;

            foreach (var line in tableOfWordsResult)
            {
                TessTextDef rowData = line;

                //System.Array.Resize<string>(ref rowData, 14);

                if (rowData.text.Trim().Length > 0)
                {
                    var res = FuzzyText.FindMatchingDegree(rowData.text.ToString(), correctWords, 0.4);

                    rowData.CorrectWord = res[0, 0]; //Correct Word
                    rowData.MatchingDegree =Double.Parse( res[0, 1]); //Matching Degree

                    if (rowData.MatchingDegree.ToString() == "0")
                    {
                        wrongWords += 1;
                        bagOfWrongWords += rowData.text.Trim() + ",";
                    }
                    else
                    {
                        countMatchingDegreeRows += 1;

                        sumMatchingDegree += rowData.MatchingDegree;
                        tableOfWordsResultWithMatchingDegree.Add(rowData);
                    }
                    lineno += 1;

                }
            }
            if (wrongWords > 0)
                bagOfWrongWords = bagOfWrongWords.Substring(0, bagOfWrongWords.Length - 1);

            return tableOfWordsResultWithMatchingDegree;
        }
    }
}
