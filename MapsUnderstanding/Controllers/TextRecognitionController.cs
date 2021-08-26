﻿using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Tesseract;
using System.Drawing;
using System.Data;
using MapsVisionsAPI.Middleware;
using System.Diagnostics;
using MapsVisionsAPI.Data.Entities;
using MapsVisionsAPI.Data;
using Microsoft.Extensions.Configuration;
using System.Net;
using MapsUnderstanding.Models;

namespace MapsVisionsAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class TextRecognitionController : Controller
    {
       // protected readonly string mapsFolder = "C:\\Users\\Adel\\source\\repos\\WebDataScience\\MapsVisionGit\\MapsCapturing\\";
        TesseractReading Tess = new TesseractReading();
        public string mapsPath()
        {
            string ApiDir = Directory.GetCurrentDirectory();
            string mapsDir = ApiDir.Substring(0,ApiDir.LastIndexOf("\\") );
            return mapsDir + "\\MapsCapturing";
        }
        [HttpGet("TextList")]
        public IActionResult GetTextList()
        {
            try
            {
                Request.Headers.TryGetValue("imagePath", out var imageName);
                imageName = imageName.ToString().Replace("/", "\\");
                var imagePath = Path.Combine(mapsPath(), imageName);
                float confidence = 0.0f;
                string allText = "";
                string[] wordsList;

                Tess.TesseractReader(imagePath, out confidence, out allText, out _);
                wordsList = TextProcessing.castLinedTextToStringArray(allText);
                //  bool gray = ImageFilters.applyBestEffects1(imagePath);
                return Ok(new {Success=true, Confidence = confidence, wordsList = wordsList, imagePath= imagePath });
            }catch(ArgumentNullException ex)
            {
                return BadRequest(new { Success = false, message ="you must add imagePath in headers of your request", error = ex.Message });
            }
            catch (Exception ex)
            {
                return BadRequest(new { Success = false, error = ex.Message });
            }
        }

        [HttpGet("readDetailsText")]
        public IActionResult readDetailsText()
        {
            try
            {
                Request.Headers.TryGetValue("imagePath", out var imageName);
                imageName = imageName.ToString().Replace("/", "\\");
                var imagePath = Path.Combine(mapsPath(), imageName);
                float confidence = 0.0f;
                string detailedText = "";
                List<TessTextDef> wordsList=new List<TessTextDef>();
                Tess.TesseractReader(imagePath, out confidence, out _, out detailedText);
                wordsList = TextProcessing.CastCSVToDataTable(new StringReader(detailedText));
                return Ok(new { Success = true, Confidence = confidence, wordsList = wordsList, imagePath= imagePath, detailedText= detailedText });
            }
            catch (ArgumentNullException ex)
            {
                return BadRequest(new { Success = false, message = "you must add imagePath in headers of your request", error = ex.Message });
            }
            catch (Exception ex)
            {
                Console.Write(ex);
                return BadRequest(new { Success = false, error = ex.Message });
            }
        }


        [HttpPost("applyFilters1")]
        public IActionResult applyFilters1()
        {
            try
            {
                Request.Headers.TryGetValue("imagePath", out var imageName);
                imageName = imageName.ToString().Replace("/", "\\");
                var imagePath = Path.Combine(mapsPath(), imageName);
                ImageFilters.applyBestEffects1(imagePath);
                return Ok(new { message = "filters applied over the images successfully", imagePath=imagePath });
            }catch(Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }
        [HttpPost("applyFilters2")]
        public IActionResult applyFilters2()
        {
            try
            {
                Request.Headers.TryGetValue("imagePath", out var imageName);
                imageName = imageName.ToString().Replace("/", "\\");
                var imagePath = Path.Combine(mapsPath(), imageName);
                ImageFilters.removeBKEffects(imagePath);
                return Ok(new { message = "filters group(2) applied over the images successfully", imagePath = imagePath });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        private IGenericRepository<MapImageRecogResults> repository = null;

        private readonly MapsVisionsDbContext _DbContext;
        public TextRecognitionController(MapsVisionsDbContext mapsVisionsDbContext)
        {
            _DbContext = mapsVisionsDbContext;
            this.repository = new GRepository<MapImageRecogResults>(_DbContext);
        }

        [HttpGet("MapImageRecogResults")]
        public IActionResult MapImageRecogResults()
        {
            try
            {

                var model = repository.GetAll();
                return Ok(new {data= model }); 
            }
            catch (Exception ex)
            {
                Debug.WriteLine(ex);
                return BadRequest(new { error = ex.Message });
            }
        }

        [HttpGet("DetailsWithFAccuracy")]
        public ActionResult<string> GetDetailsWithFAccuracy()
        {
            try
            {
                   // var imagePath = Path.Combine(Directory.GetCurrentDirectory(), "Resources\\Images\\Thresh", "MANAPAYA-Normal.jpg");
                    Request.Headers.TryGetValue("correctWords", out var allWords);
                    Request.Headers.TryGetValue("imagePath", out var imageName);
                    imageName = imageName.ToString().Replace("/", "\\");
                    var imagePath = Path.Combine(mapsPath(), imageName);

                if (allWords.Count == 0)
                        return BadRequest(new { error = "you must send the correctWords in headers. That contains all correct words in the image" });
                    else
                    {
                        string[] correctWords = allWords[0].Split(",");

                        double matchingDegree = 0;
                        double sumMatchingDegree = 0;
                        int countMatchingDegreeRows = 0;
                        int wrongWords = 0;
                        int undetectedWords = 0;
                        int detectedWords = 0;
                        double totalMatchingDegree = 0;

                        tableOfDetectedWords(imagePath, out var confidence, out var tableOfWordsResult);
                        List<TessTextDef> tableOfWordsResultWithMatchingDegree =
                            TextProcessing.getTableWithMatchingDegree(tableOfWordsResult,
                                                            correctWords, out wrongWords,
                                                            out countMatchingDegreeRows, out sumMatchingDegree);

                        Dictionary<string, string> undetectedTable =
                             TextProcessing.getTableOfUndetectedWords(correctWords, tableOfWordsResultWithMatchingDegree);

                        undetectedWords = undetectedTable.Count;
                        detectedWords = tableOfWordsResultWithMatchingDegree.Count;
                        matchingDegree = sumMatchingDegree / countMatchingDegreeRows;
                        totalMatchingDegree = sumMatchingDegree / (countMatchingDegreeRows + wrongWords + undetectedWords);

                        return Ok(new
                        {
                            DetectedWordsTable = tableOfWordsResultWithMatchingDegree,
                            noDetectedWords = detectedWords,
                            UndetectedWordsTable = undetectedTable,
                            undetectedWords = undetectedWords.ToString(),
                            noWrongWords = wrongWords.ToString(),
                            confidence = confidence,
                            matchingDegree = matchingDegree.ToString(),
                            totalMatchingDegree = totalMatchingDegree.ToString()
                        });
                    }
                
            }
            catch (ArgumentNullException ex)
            {
                return BadRequest(new { Success = false, message = "You must add imagePath and correctWords in headers of your request", error = ex.Message });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        [HttpPost("PostFResultAfterEffects")]
        public ActionResult<string> PostFResultAfterEffects()
        {
            string[] imgs = { "dilate-Google-Map2.jpg", "erosion-Google-Map2.jpg", "gray-Google-Map2.jpg", "normal-Google-Map2.jpg", "opening-Google-Map2.jpg", "result-Google-Map2.jpg", "ThreshMeanCBinary-Google-Map2.jpg" };
            foreach (var img in imgs)
            {
                try
                {
                    var imagePath = Path.Combine(Directory.GetCurrentDirectory(), "Resources\\Images", img);
                    Debug.WriteLine(imagePath);
                    Request.Headers.TryGetValue("correctWords", out var allWords);
                    if (allWords.Count == 0)
                        return BadRequest(new { error = "you must send the correctWords in headers. That contains all correct words in the image" });
                    else
                    {
                        string[] correctWords = allWords[0].Split(",");

                        double matchingDegree = 0;
                        double sumMatchingDegree = 0;
                        int countMatchingDegreeRows = 0;
                        int wrongWords = 0;
                        int undetectedWords = 0;
                        int detectedWords = 0;
                        double totalMatchingDegree = 0;

                        tableOfDetectedWords(imagePath, out var confidence, out var tableOfWordsResult);
                        List<TessTextDef> tableOfWordsResultWithMatchingDegree =
                            TextProcessing.getTableWithMatchingDegree(tableOfWordsResult,
                                                            correctWords, out wrongWords,
                                                            out countMatchingDegreeRows, out sumMatchingDegree);

                        Dictionary<string, string> undetectedTable =
                             TextProcessing.getTableOfUndetectedWords(correctWords, tableOfWordsResultWithMatchingDegree);

                        undetectedWords = undetectedTable.Count;
                        detectedWords = tableOfWordsResultWithMatchingDegree.Count;
                        matchingDegree = sumMatchingDegree / countMatchingDegreeRows;
                        totalMatchingDegree = sumMatchingDegree / (countMatchingDegreeRows + wrongWords + undetectedWords);

                        Debug.WriteLine(
                        new
                        {
                            DetectedWordsTable = tableOfWordsResultWithMatchingDegree,
                            noDetectedWords = detectedWords,
                            UndetectedWordsTable = undetectedTable,
                            undetectedWords = undetectedWords.ToString(),
                            noWrongWords = wrongWords.ToString(),
                            confidence = confidence,
                            matchingDegree = matchingDegree.ToString(),
                            totalMatchingDegree = totalMatchingDegree.ToString()
                        });


                        MapImageRecogResults model = new MapImageRecogResults();
                        model.capture_url ="Resources\\Images\\"+ img;
                        model.lat = 7.7545892f;
                        model.lng = 80.1853365f;
                        model.zoom_level = 10;
                        if (img.IndexOf("Google") != -1) model.map_provider = "Google"; else if (img.IndexOf("Bing") != -1) model.map_provider = "Bing"; else model.map_provider = "OSM";
                        model.quarter = "whole";
                        model.effects = img.Substring(0, img.IndexOf("-"));
                        model.no_detected_words = detectedWords;
                        model.no_undetected_words = undetectedWords;
                        model.no_wrong_words = wrongWords;
                        model.confidence =confidence;
                        if (matchingDegree != matchingDegree) model.matching_degree = 0; else model.matching_degree = Convert.ToSingle(matchingDegree);
                        model.total_matching_degree =Convert.ToSingle( totalMatchingDegree);

                        repository.Insert(model);
                        repository.Save();

                        
                    }

                }
                catch (Exception ex)
                {
                    return BadRequest(new { error = ex.Message });
                }
            }
            return Ok(new { message = "All captured maps stored into the database" });
        }
        private void tableOfDetectedWords(string imagePath, out float confidence, out List<TessTextDef> table)
        {
                string allText ="";
                Tess.TesseractReader(imagePath, out confidence,out _, out allText);
                var tableOfWordsResult =TextProcessing.CastCSVToDataTable(new StringReader(allText));
                table = tableOfWordsResult;
        }
    }
}
