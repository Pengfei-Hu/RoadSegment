using MapsUnderstanding.Models;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
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
            tessText.height = Int32.Parse(rowData[8]);
            tessText.width = Int32.Parse(rowData[9]);
            tessText.confidence = Int32.Parse(rowData[10]);
            tessText.text = rowData[11].ToString();
             return tessText;
        }
        public static List<TessTextDef> CastCSVToDataTable(StringReader reader)
        {
            string line = "";
            List<TessTextDef> datatable = new List<TessTextDef>();
            while ((line = reader.ReadLine()) != null)
            {
                string[] rowData = line.Split('\t');
               
                if (rowData[rowData.Length - 1].Trim().Length > 0)
                {
                    datatable.Add(getTessTextDef(rowData));
                }
            }
            return datatable;
        }
        public static string[] castLinedTextToStringArray(string allText)
        {
            return allText.Split("\n").Where(ele => ele.Trim() != "").ToArray();
        }
        public static Dictionary<string, string> getTableOfUndetectedWords(string[] CorrectWords, List<TessTextDef> tableOfWordsResult)
        {
            Dictionary<string, string> undetectedTable = new Dictionary<string, string>();
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
                    undetectedTable.Add(CorrectWords[x], "0");
                }

            }
            return undetectedTable;
        }
        public static List<TessTextDef> getTableWithMatchingDegree(List<TessTextDef> tableOfWordsResult, string[] correctWords, 
                                out int wrongWords, out int countMatchingDegreeRows, out double sumMatchingDegree)
        {
            List<TessTextDef> tableOfWordsResultWithMatchingDegree = new List<TessTextDef>();
            wrongWords = 0;
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
                        wrongWords += 1;
                    else
                    {
                        countMatchingDegreeRows += 1;

                        sumMatchingDegree += rowData.MatchingDegree;
                        tableOfWordsResultWithMatchingDegree.Add(rowData);
                    }
                    lineno += 1;

                }

            }
            return tableOfWordsResultWithMatchingDegree;
        }
    }
}
