/**
 * @ignore
 */
/*
 * Your incidents ViewModel code goes here
 */
define(['ojs/ojcore', 'knockout', 'jquery', 'accUtils', 'models/mapimgs.model', 'models/textRecog.model',
    'models/mapsCV.model', 'ojs/ojarraydataprovider',
    "ojs/ojflattenedtreedataproviderview", "ojs/ojarraytreedataprovider", "ojs/ojknockouttemplateutils",
    "ojs/ojradioset", "ojs/ojlabel", "ojs/ojrowexpander", "ojs/ojmessages", "ojs/ojcheckboxset", "ojs/ojlabelvalue",
    "ojs/ojfilepicker", "ojs/ojformlayout", 'ojs/ojavatar', 'ojs/ojinputtext', 'ojs/ojdialog',
    'ojs/ojtable', "ojs/ojknockout", "ojs/ojoption", "ojs/ojmenu", "ojs/ojbutton", "ojs/ojcollapsible"],
    function (oj, ko, $, accUtils, MapImgModel, TextRecogModel, mapsCVModel, ArrayDataProvider, FlattenedTreeDataProviderView, ArrayTreeDataProvider, KnockoutTemplateUtils) {
        function MapsCVViewModel() {
            let self = this;
            self.imagesServer = "http://localhost:84/";
            self.showTable = ko.observable(true);
            self.msgTitle = ko.observable();
            self.msgBody = ko.observable();
            self.allLocationWholePhotos = ko.observableArray([]);
            self.partlist = ko.observable("");
            self.lastCorrectPartlist = ko.observable("");
            self.data_multi = ko.observable(0);
            self.bingImagePath = ko.observable("https://blogs.bing.com/BingBlogs/files/dc/dce88d2a-2bf9-4c65-9cca-1c425d571e75.png");
            self.bingCaptureId = ko.observable(0);
            self.googleImagePath = ko.observable("https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Google_Maps_Logo_2020.svg/1137px-Google_Maps_Logo_2020.svg.png");
            self.googleCaptureId = ko.observable(0);
            self.osmImagePath = ko.observable("https://upload.wikimedia.org/wikipedia/commons/b/b0/Openstreetmap_logo.svg");
            self.osmCaptureId = ko.observable(0);
            self.bingEffImagePath = ko.observable();
            self.googleEffImagePath = ko.observable();
            self.osmEffImagePath = ko.observable();


            self.lat = ko.observable(80.6469622);
            self.lng = ko.observable(7.8612675);
            self.startzoomLevel = ko.observable(15);
            self.endzoomLevel = ko.observable(17);
            self.address = ko.observable("");

            self.showImagesPath = ko.observable(false);
            self.showExtractedTextUnderMaps = ko.observable(false);
            self.showExtractedTextDetails = ko.observable(false);
            self.showMeasureAccuracy = ko.observable(false);
            self.showMeasureAccuracyResult = ko.observable(false);
            self.showMeasureAccuracyAfterEffects = ko.observable(false);
            self.showAccuracyResults = ko.observable(false);
            self.showAccuracyFilteredResults = ko.observable(false);

            self.selectedOptions = ko.observableArray([]);

            self.bingOCRResult = ko.observable("");
            self.googleOCRResult = ko.observable("");
            self.osmOCRResult = ko.observable("");



            self.bingDetailsOCRResult = ko.observable("");
            self.googleDetailsOCRResult = ko.observable("");
            self.osmDetailsOCRResult = ko.observable("");

            self.messages = ko.observableArray([]);;
            self.messagesDataprovider = new ArrayDataProvider(self.messages);

            //Get All Data from the array to the table interface
            /*self.dataProvider = new ArrayDataProvider(self.allLocationWholePhotos, {
                keyAttributes: "capture_id",
                implicitSort: [{ attribute: "capture_id", direction: "ascending" }],
            });*/
            this.KnockoutTemplateUtils = KnockoutTemplateUtils;
            this.arrayTreeDataProvider = new ArrayTreeDataProvider(self.allLocationWholePhotos, { keyAttributes: "lat" });
            this.dataProvider = ko.observable(new FlattenedTreeDataProviderView(this.arrayTreeDataProvider));

            self.formatImgPaths = (serverResult) => {
                serverResult.forEach((location, index) => {
                    location.bing.imgPath = JSON.parse(location.bing.imgPath);
                    location.bing.imgPath.forEach((path, i) => {
                        path.url = self.imagesServer + path.url;
                        location.bing.imgPath[i] = path;
                    });
                    location.google.imgPath = JSON.parse(location.google.imgPath);
                    location.google.imgPath.forEach((path, i) => {
                        path.url = self.imagesServer + path.url;
                        location.google.imgPath[i] = path;
                    });
                    location.osm.imgPath = JSON.parse(location.osm.imgPath);
                    location.osm.imgPath.forEach((path, i) => {
                        path.url = self.imagesServer + path.url;
                        location.osm.imgPath[i] = path;
                    });

                    serverResult[index] = location
                });
                console.log("Server Data");
                console.log(serverResult);
                return serverResult;
            }
            self.refreshAllData = (filterValue) => {
                MapImgModel.getAllLocationWholePhotos((success, serverResult) => {
                    if (filterValue == undefined) {

                        self.allLocationWholePhotos(self.formatImgPaths(serverResult));
                    } else {
                        let filteredResult = serverResult.filter(locationPhoto => {

                            /*if (article.summary == undefined) article.summary = "";
                            if (article.content == undefined) article.content = "";
                            if (article.title.toLowerCase().indexOf(filterValue.toLowerCase()) != -1 ||
                                article.summary.toLowerCase().indexOf(filterValue.toLowerCase()) != -1 ||
                                article.content.toLowerCase().indexOf(filterValue.toLowerCase()) != -1)*/
                            return true;
                            //else
                            //    return false;
                        });
                        self.allLocationWholePhotos(filteredResult);
                    }
                    self.allLocationWholePhotos.valueHasMutated(); //Notify to subscribers(Refersh)
                });
            }
            //load all data for first time page load
            self.refreshAllData();

            self.test = () => {
                alert("TestFunction");
            }
            self.selectedMenuItem = ko.observable("None selected yet");
            self.launchedFrom = ko.observable("None launched yet");

            self.myActionFunction = (event, data, idx) => {
                cell = self.launchedFrom().split(',');
                if (event.detail.selectedValue == "ExtractText") {
                    if (cell[1] == 4)
                        ExtractText(cell[0], "google");
                    else if (cell[1] == 3)
                        ExtractText(cell[0], "bing");
                    else if (cell[1] == 5)
                        ExtractText(cell[0], "osm");
                    else
                        ExtractText(cell[0], "all");

                } else if (event.detail.selectedValue == "Visualize") {
                    console.log(event.detail);
                    console.log(data);
                    console.log(idx);
                    if (self.allLocationWholePhotos()[cell[0]] != undefined) {
                        self.lat(self.allLocationWholePhotos()[cell[0]].lat);
                        self.lng(self.allLocationWholePhotos()[cell[0]].lng);
                        self.startzoomLevel(self.allLocationWholePhotos()[cell[0]].zoom_level);
                        console.log("row=" + cell[0]);
                        console.log(self.startzoomLevel());
                    }
                    self.showTable(false);

                }

                self.selectedMenuItem(event.detail.selectedValue);
            };
            self.myBeforeOpenFunction = (event) => {
                const target = event.detail.originalEvent.target;
                const context = document.getElementById("mapImgsTable").getContextByNode(target);
                if (context != null) {
                    if (context.subId === "oj-table-header") {
                        self.launchedFrom("Header: [" + context.index + "]");
                    }
                    else if (context.subId === "oj-table-cell") {

                        console.log(context.rowIndex);
                        self.launchedFrom(+ context.rowIndex + ", " + context.columnIndex);
                    }
                    self.lng(self.allLocationWholePhotos()[context.rowIndex].lng);
                    self.lat(self.allLocationWholePhotos()[context.rowIndex].lat);
                }
            };

            self.ExtractText = (row, map_provider) => {
                console.log("row" + row);
                if (map_provider == "all") {

                } else if (self.allLocationWholePhotos()[row][map_provider] == null) {

                    self.messages().push({ summary: 'No Image To Extract the text', autoTimeout: 1000 });
                    self.messages.valueHasMutated();
                } else {
                    var imgPath = self.allLocationWholePhotos()[row][map_provider]["imgPath"];
                    imgPath = imgPath.substring(imgPath.indexOf("map"));
                    TextRecogModel.readTextList(imgPath, (success, data) => {
                        self.msgTitle("Extracted Successfully");
                        var result = "confidence:" + data.confidence + "\t wordsList:" + data.wordsList;
                        self.msgBody(result);
                        document.getElementById("msgDialog").open();
                        console.log(data);
                    });
                }

            }

            self.backToMain = () => {

                self.showTable(true);
            }
            //Dialogs
            self.closeDialog = () => {
                document.getElementById("msgDialog").close();
            }

            self.hideAllPanels = () => {
                self.showAccuracyResults(false);
                self.showMeasureAccuracyAfterEffects(false);
                self.showMeasureAccuracy(false);
                self.showExtractedTextUnderMaps(true);
                self.showImagesPath(true);
                self.showExtractedTextDetails(false);
                self.showTable(false);
                self.showAccuracyFilteredResults(false);
            }
            self.actionMenuListener = (event, context) => {
                var selectMenuItem = event.detail.selectedValue;
                var rowData = context.item.data
                //console.log(rowData);
                self.startzoomLevel(rowData["zoom_level"]);
                self.lat(rowData["lat"]);
                self.lng(rowData["lng"]);
                self.hideAllPanels();
                if (selectMenuItem == "ExtractAllText") {
                    self.showExtractedTextUnderMaps(true);
                    self.display();
                } else if (selectMenuItem == "Visualize") {
                    self.display();
                } else if (selectMenuItem == "ExtractDetails") {
                    self.showExtractedTextDetails(true);
                    self.display();
                }
                else if (selectMenuItem == "MeasureAccuracy") {
                    self.showMeasureAccuracy(true);
                    self.showMeasureAccuracyResult(true);
                    self.display();
                } else if (selectMenuItem == "MeasureAccuracyAfterEffects") {
                    self.showMeasureAccuracyAfterEffects(true);
                    self.showMeasureAccuracy(true);
                    //may need changes here
                    self.showAccuracyFilteredResults(true);
                    self.display();
                }

            };

            //Fuzzy Measurments

            //Bing Measurments Attributes
            self.bingManualText = ko.observable("");
            self.bingAvgMDegree = ko.observable("");
            self.bingUndetectedWords = ko.observable("");
            self.bingWrongWords = ko.observable("");
            self.bingTotalMDegree = ko.observable("");
            self.bingUndetectedWordsArr = ko.observable("");
            self.bingWrongWordsArr = ko.observable("");
            self.bingNoDetectedWords = ko.observable("");
            self.bingFDetails = ko.observableArray([]);
            //for filtered Images
            self.fbingAvgMDegree = ko.observable("");
            self.fbingUndetectedWords = ko.observable("");
            self.fbingWrongWords = ko.observable("");
            self.fbingTotalMDegree = ko.observable("");
            self.fbingUndetectedWordsArr = ko.observable("");
            self.fbingWrongWordsArr = ko.observable("");
            self.fbingNoDetectedWords = ko.observable("");
            self.fbingFDetails = ko.observableArray([]);

            self.bingFDetailsDataprovider = new ArrayDataProvider(self.bingFDetails, {
                keyAttributes: "text",
                implicitSort: [{ attribute: "matchingDegree", direction: "ascending" }],
            });
            //for filtered images
            self.fbingFDetailsDataprovider = new ArrayDataProvider(self.fbingFDetails, {
                keyAttributes: "text",
                implicitSort: [{ attribute: "matchingDegree", direction: "ascending" }],
            });

            //Google Measurments Attributes
            self.googleManualText = ko.observable("");
            self.googleAvgMDegree = ko.observable("");
            self.googleUndetectedWords = ko.observable("");
            self.googleWrongWords = ko.observable("");
            self.googleTotalMDegree = ko.observable("");
            self.googleUndetectedWordsArr = ko.observable("");
            self.googleWrongWordsArr = ko.observable("");
            self.googleNoDetectedWords = ko.observable("");
            self.googleFDetails = ko.observableArray([]);
            //for filtered images
            self.fgoogleAvgMDegree = ko.observable("");
            self.fgoogleUndetectedWords = ko.observable("");
            self.fgoogleWrongWords = ko.observable("");
            self.fgoogleTotalMDegree = ko.observable("");
            self.fgoogleUndetectedWordsArr = ko.observable("");
            self.fgoogleWrongWordsArr = ko.observable("");
            self.fgoogleNoDetectedWords = ko.observable("");
            self.fgoogleFDetails = ko.observableArray([]);


            self.googleFDetailsDataprovider = new ArrayDataProvider(self.googleFDetails, {
                keyAttributes: "text",
                implicitSort: [{ attribute: "matchingDegree", direction: "ascending" }],
            });
            //for filtered images
            self.fgoogleFDetailsDataprovider = new ArrayDataProvider(self.fgoogleFDetails, {
                keyAttributes: "text",
                implicitSort: [{ attribute: "matchingDegree", direction: "ascending" }],
            });

            //OSM Measurments Attributes
            self.osmManualText = ko.observable("");
            self.osmAvgMDegree = ko.observable("");
            self.osmUndetectedWords = ko.observable("");
            self.osmWrongWords = ko.observable("");
            self.osmTotalMDegree = ko.observable("");
            self.osmUndetectedWordsArr = ko.observable("");
            self.osmWrongWordsArr = ko.observable("");
            self.osmNoDetectedWords = ko.observable("");
            self.osmFDetails = ko.observableArray([]);

            //for filtered images
            self.fosmAvgMDegree = ko.observable("");
            self.fosmUndetectedWords = ko.observable("");
            self.fosmWrongWords = ko.observable("");
            self.fosmTotalMDegree = ko.observable("");
            self.fosmUndetectedWordsArr = ko.observable("");
            self.fosmWrongWordsArr = ko.observable("");
            self.fosmNoDetectedWords = ko.observable("");
            self.fosmFDetails = ko.observableArray([]);


            self.osmFDetailsDataprovider = new ArrayDataProvider(self.osmFDetails, {
                keyAttributes: "text",
                implicitSort: [{ attribute: "matchingDegree", direction: "ascending" }],
            });
            //for filtered images
            self.fosmFDetailsDataprovider = new ArrayDataProvider(self.fosmFDetails, {
                keyAttributes: "text",
                implicitSort: [{ attribute: "matchingDegree", direction: "ascending" }],
            });

            self.getFAccuracyBing = () => {
                TextRecogModel.getFAccuracy(self.bingManualText(), self.bingImagePath().substring(self.bingImagePath().indexOf("map")),
                    (success, data) => {
                        console.log("getFAccuracyBing");
                        console.log(data);
                        self.bingNoDetectedWords(data.results.no_detected_words);
                        self.bingAvgMDegree(data.results.matching_degree);
                        self.bingUndetectedWords(data.results.no_undetected_words);
                        self.bingWrongWords(data.results.no_wrong_words);
                        self.bingTotalMDegree(data.results.total_matching_degree);
                        self.bingUndetectedWordsArr(data.results.undetected_words);
                        self.bingWrongWordsArr(data.results.wrong_words);
                        self.bingFDetails(data.detectedWordsTable);
                        self.bingFDetails.valueHasMutated();
                    });
                TextRecogModel.getFAccuracy(self.bingManualText(), self.bingEffImagePath().substring(self.bingEffImagePath().indexOf("map"), self.bingEffImagePath().indexOf("?")),
                    (success, data) => {
                        self.fbingNoDetectedWords(data.results.no_detected_words);
                        self.fbingAvgMDegree(data.results.matching_degree);
                        self.fbingUndetectedWords(data.results.no_undetected_words);
                        self.fbingWrongWords(data.results.no_wrong_words);
                        self.fbingTotalMDegree(data.results.total_matching_degree);
                        self.fbingUndetectedWordsArr(data.results.undetected_words);
                        self.fbingWrongWordsArr(data.results.wrong_words);
                        self.fbingFDetails(data.detectedWordsTable);
                        self.fbingFDetails.valueHasMutated();
                    });
            }
            self.getFAccuracyGoogle = () => {
                TextRecogModel.getFAccuracy(self.googleManualText(), self.googleImagePath().substring(self.googleImagePath().indexOf("map")),
                    (success, data) => {
                        self.googleNoDetectedWords(data.results.no_detected_words);
                        self.googleAvgMDegree(data.results.matching_degree);
                        self.googleUndetectedWords(data.results.no_undetected_words);
                        self.googleWrongWords(data.results.no_wrong_words);
                        self.googleTotalMDegree(data.results.total_matching_degree);
                        self.googleUndetectedWordsArr(data.results.undetected_words);
                        self.googleWrongWordsArr(data.results.wrong_words);
                        self.googleFDetails(data.detectedWordsTable);
                        self.googleFDetails.valueHasMutated();
                    });
                TextRecogModel.getFAccuracy(self.googleManualText(), self.googleEffImagePath().substring(self.googleEffImagePath().indexOf("map"), self.googleEffImagePath().indexOf("?")),
                    (success, data) => {
                        self.fgoogleNoDetectedWords(data.results.no_detected_words);
                        self.fgoogleAvgMDegree(data.results.matching_degree);
                        self.fgoogleUndetectedWords(data.results.no_undetected_words);
                        self.fgoogleWrongWords(data.results.no_wrong_words);
                        self.fgoogleTotalMDegree(data.results.total_matching_degree);
                        self.fgoogleUndetectedWordsArr(data.results.undetected_words);
                        self.fgoogleWrongWordsArr(data.results.wrong_words);
                        self.fgoogleFDetails(data.detectedWordsTable);
                        self.fgoogleFDetails.valueHasMutated();
                    });
            }
            self.getFAccuracyOSM = () => {
                TextRecogModel.getFAccuracy(self.osmManualText(), self.osmImagePath().substring(self.osmImagePath().indexOf("map")),
                    (success, data) => {
                        self.osmNoDetectedWords(data.results.no_detected_words);
                        self.osmAvgMDegree(data.results.matching_degree);
                        self.osmUndetectedWords(data.results.no_undetected_words);
                        self.osmWrongWords(data.results.no_wrong_words);
                        self.osmTotalMDegree(data.results.total_matching_degree);
                        self.osmUndetectedWordsArr(data.results.undetected_words);
                        self.osmWrongWordsArr(data.results.wrong_words);
                        self.osmFDetails(data.detectedWordsTable);
                        self.osmFDetails.valueHasMutated();
                    });

                TextRecogModel.getFAccuracy(self.osmManualText(), self.osmEffImagePath().substring(self.osmEffImagePath().indexOf("map"), self.osmEffImagePath().indexOf("?")),
                    (success, data) => {
                        self.fosmNoDetectedWords(data.results.no_detected_words);
                        self.fosmAvgMDegree(data.results.matching_degree);
                        self.fosmUndetectedWords(data.results.no_undetected_words);
                        self.fosmWrongWords(data.results.no_wrong_words);
                        self.fosmTotalMDegree(data.results.total_matching_degree);
                        self.fosmUndetectedWordsArr(data.results.undetected_words);
                        self.fosmWrongWordsArr(data.results.wrong_words);
                        self.fosmFDetails(data.detectedWordsTable);
                        self.fosmFDetails.valueHasMutated();
                    });
            }

            self.FAccuracy = () => {
                self.showMeasureAccuracyResult(true);
                self.showAccuracyResults(true);
                self.getFAccuracyBing();
                self.getFAccuracyGoogle();
                self.getFAccuracyOSM();
            }

            self.ApplyEffects = () => {
                var imagesPathes = self.bingImagePath().substring(self.bingImagePath().indexOf("map")) +
                    "," + self.googleImagePath().substring(self.googleImagePath().indexOf("map")) +
                    "," + self.osmImagePath().substring(self.osmImagePath().indexOf("map"));
                console.log(self.selectedOptions())
                mapsCVModel.setGrayEffectAllImgs(imagesPathes, self.selectedOptions(), (success, data) => {
                    self.bingEffImagePath(self.bingEffImagePath() + "?ref=" + new Date().getTime());
                    self.googleEffImagePath(self.googleEffImagePath() + "?ref=" + new Date().getTime());
                    self.osmEffImagePath(self.osmEffImagePath() + "?ref=" + new Date().getTime());
                    console.log(success);
                    console.log(data);
                    self.showMeasureAccuracyResult(true);
                });

            }


            self.bingOCRDetails = ko.observableArray([]);
            bingDetailsOCRResultDataprovider = new ArrayDataProvider(self.bingOCRDetails, {
                keyAttributes: "text",
                implicitSort: [{ attribute: "confidence", direction: "ascending" }],
            });

            self.googleOCRDetails = ko.observableArray([]);
            googleDetailsOCRResultDataprovider = new ArrayDataProvider(self.googleOCRDetails, {
                keyAttributes: "text",
                implicitSort: [{ attribute: "confidence", direction: "ascending" }],
            });
            self.osmOCRDetails = ko.observableArray([]);
            osmDetailsOCRResultDataprovider = new ArrayDataProvider(self.osmOCRDetails, {
                keyAttributes: "text",
                implicitSort: [{ attribute: "confidence", direction: "ascending" }],
            });

            self.readOCRResult = (newPath) => {
                return new Promise((resolve, reject) => {
                    var imagePath = newPath.substring(newPath.indexOf("map"));
                    TextRecogModel.readTextList(imagePath, (success, data) => {
                        if (success)
                            resolve("confidence:" + data.confidence + "\n wordsList:" + data.wordsList);
                        else
                            reject("Sorry, i can't extract the text from this image");
                    });
                });
            };
            self.readOCRResultDetails = (newPath) => {
                return new Promise((resolve, reject) => {
                    var imagePath = newPath.substring(newPath.indexOf("map"));
                    TextRecogModel.readDetailsText(imagePath, (success, data) => {
                        if (success) {
                            resolve(data);
                        }
                        else
                            reject("Sorry, i can't extract the text from this image");
                    });
                });
            };
            self.getFilteredPath = (newPath) => {
                return newPath.substring(0, newPath.lastIndexOf("/") + 1).toString() +
                    "filtered-" + newPath.substring(newPath.lastIndexOf("/") + 1);
            }
            self.bingImagePath.subscribe(function (newPath) {

                self.bingEffImagePath(self.getFilteredPath(newPath));
                self.readOCRResult(newPath)
                    .then(result => {
                        self.bingOCRResult(result);
                    }).catch(err => {
                        self.bingOCRResult(err);
                    });

                self.readOCRResultDetails(newPath)
                    .then(result => {
                        self.bingDetailsOCRResult(result);
                        self.bingOCRDetails(result.wordsList);
                        self.bingOCRDetails.valueHasMutated();
                    }).catch(err => {
                        self.bingDetailsOCRResult(err);
                    });

            });
            self.googleImagePath.subscribe(function (newPath) {
                self.googleEffImagePath(self.getFilteredPath(newPath));
                self.readOCRResult(newPath)
                    .then(result => {
                        self.googleOCRResult(result);
                    }).catch(err => {
                        self.googleOCRResult(err);
                    });

                self.readOCRResultDetails(newPath)
                    .then(result => {
                        self.googleDetailsOCRResult(result);
                        self.googleOCRDetails(result.wordsList);
                        self.googleOCRDetails.valueHasMutated();
                    }).catch(err => {
                        self.googleDetailsOCRResult(err);
                    });
            });
            self.osmImagePath.subscribe(function (newPath) {
                self.osmEffImagePath(self.getFilteredPath(newPath));
                self.readOCRResult(newPath)
                    .then(result => {
                        self.osmOCRResult(result);
                    }).catch(err => {
                        self.osmOCRResult(err);
                    });
                self.readOCRResultDetails(newPath)
                    .then(result => {
                        self.osmDetailsOCRResult(result);
                        self.osmOCRDetails(result.wordsList);
                        self.osmOCRDetails.valueHasMutated();
                    }).catch(err => {
                        self.osmDetailsOCRResult(err);
                    });
            });

            self.upperLeft = () => {
                self.partlist(self.partlist() + "0");
                self.data_multi(self.data_multi() + 1);
                if (self.partlist() != "") {
                    send_info()
                } else {
                    send_mu()
                }

            }

            self.upperRight = () => {
                self.data_multi(self.data_multi() + 1);
                self.partlist(self.partlist() + "1");
                if (self.partlist() != "") {
                    send_info()
                } else {
                    send_mu()
                }
            }

            self.display = () => {
                self.data_multi(self.startzoomLevel());
                self.partlist("");
                if (self.partlist() != "") {
                    send_info()
                } else {
                    send_mu()
                }
                MapImgModel.getAddressOfLatLng(self.lat(), self.lng(), (success, result) => {

                    self.address(result);


                });

            }

            self.bottomLeft = () => {
                self.data_multi(self.data_multi() + 1);
                self.partlist(self.partlist() + "2");
                if (self.partlist() != "") {
                    send_info()
                } else {
                    send_mu()
                }

            }

            self.bottomRight = () => {
                self.data_multi(self.data_multi() + 1);
                self.partlist(self.partlist() + "3");
                if (self.partlist() != "") {
                    send_info()
                } else {
                    send_mu()
                }

            }


            self.preZoomLevel = () => {
                // self.data_multi(self.data_multi() - 1);
                // self.data_multi(self.data_multi() + 1);
                // if (self.partlist() != self.lastCorrectPartlist()) {
                if (self.partlist().length > 1) {
                    self.partlist(self.partlist().substring(0, self.partlist().length - 1));
                    self.data_multi(self.data_multi() - 1);
                } else if (self.partlist().length == 1) {
                    self.partlist("");
                    self.data_multi(self.data_multi() - 1);
                } else if (self.partlist().length == 0) {
                    //alert("It is the first level we have");
                    self.messages().push({ summary: 'It is the first level we have', autoTimeout: 1000 });
                    self.messages.valueHasMutated();
                }

                if (self.partlist() != "") {
                    send_info()
                } else {
                    send_mu()
                }

            }
            self.pythonServer = ko.observable("http://localhost:84/");
            function send_info() {
                var data = "lon=" + self.lng() + "&lat=" + self.lat() + "&startz=" + self.startzoomLevel() + "&endz=" + self.data_multi().toString() + "&partlist=" + self.partlist().toString();
                console.log(data);
                $.ajax({
                    url: self.pythonServer() + "multi/select",
                    datatype: 'json',
                    type: 'get',
                    crossDomain: true,
                    data: data,
                    success: function (data) {
                        console.log(data);
                        console.log("success send_info");
                        if (data.bing != undefined) {
                            self.displayImgAndGroundTruth(data);
                            self.lastCorrectPartlist(self.partlist());
                        } else {
                            if (self.data_multi() > self.startzoomLevel())
                                self.data_multi(self.data_multi() - 1);
                            else
                                self.data_multi(self.data_multi() + 1);
                            console.log("DataMulti=" + self.data_multi());
                            self.partlist(self.lastCorrectPartlist().substring(0, self.lastCorrectPartlist().length));
                            console.log("partlist=" + self.partlist());
                            console.log("lastCorrectPartlist=" + self.lastCorrectPartlist());
                            //alert("We don't have another level yet.")
                            self.messages().push({ summary: "We don't have another level yet", autoTimeout: 1000 });
                            self.messages.valueHasMutated();
                        }

                    },
                    error: function (err) {
                        // alert("This is the depth level we have (send_info)")
                        self.messages().push({ summary: "This is the depth level we have (send_info)", autoTimeout: 1000 });
                        self.messages.valueHasMutated();
                        console.log(err);
                    }
                })
            }
            self.SaveGroundTruth = () => {
                alert("Save ground truth")
            }

            function send_mu(data) {
                var data = "lon=" + self.lng() + "&lat=" + self.lat() + "&startz=" + self.startzoomLevel() + "&endz=" + self.data_multi().toString();
                //           "lon=" + data.field.lon + "&lat= " + data.field.lat + "&tileZoom= " + data.field.tileZoom + "&endzoomLevel=" + data_multi,
                //lon=7.8612675&lat=80.6469622&startz=12&endz=0
                //console.log(data);
                $.ajax({
                    url: self.pythonServer() + "multi/go",
                    datatype: 'json',
                    type: 'get',
                    crossDomain: true,
                    data: data,
                    success: function (data) {
                        console.log("--------------------");
                        console.log(data);
                        self.displayImgAndGroundTruth(data);
                    },
                    error: function (err) {
                        self.messages().push({ summary: "This is the depth level we have (go)", autoTimeout: 1000 });
                        self.messages.valueHasMutated();
                        console.log(err);
                    }
                })
            }

            self.displayImgAndGroundTruth = (data) => {
                bing = JSON.parse(data.bing);
                self.bingManualText(data.bing_groundTruth);
                self.bingCaptureId(data.bing_captureId);
                google = JSON.parse(data.google);
                self.googleManualText(data.google_groundTruth);
                self.googleCaptureId(data.google_captureId);
                osm = JSON.parse(data.osm);
                self.osmManualText(data.osm_groundTruth);
                self.osmCaptureId(data.osm_captureId);
                self.bingImagePath(self.pythonServer() + bing[0].url);
                self.googleImagePath(self.pythonServer() + google[0].url);
                self.osmImagePath(self.pythonServer() + osm[0].url);
            }
            this.connected = () => {
                accUtils.announce('MapsCV page loaded.', 'assertive');
                document.title = "MapsCV";
                document.getElementById("bottomRightArea").addEventListener("click", self.bottomRight, false);
                document.getElementById("bottomLeftArea").addEventListener("click", self.bottomLeft, false);
                document.getElementById("upperRightArea").addEventListener("click", self.upperRight, false);
                document.getElementById("upperLeftArea").addEventListener("click", self.upperLeft, false);
            };
            this.disconnected = () => {
            };

            this.transitionCompleted = () => {
            };
        }

        return MapsCVViewModel;
    }
);
