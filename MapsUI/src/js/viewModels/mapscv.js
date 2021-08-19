/**
 * @ignore
 */
/*
 * Your incidents ViewModel code goes here
 */
define(['ojs/ojcore', 'knockout', 'jquery', 'accUtils', 'models/mapimgs.model', 'models/textRecog.model',
    'ojs/ojarraydataprovider',
    "ojs/ojflattenedtreedataproviderview", "ojs/ojarraytreedataprovider", "ojs/ojknockouttemplateutils",
    "ojs/ojradioset", "ojs/ojlabel", "ojs/ojrowexpander",
    "ojs/ojfilepicker", 'ojs/ojinputtext', "ojs/ojformlayout", 'ojs/ojavatar','ojs/ojinputtext', 'ojs/ojdialog',
    'ojs/ojtable', "ojs/ojknockout", "ojs/ojoption", "ojs/ojmenu", "ojs/ojbutton"],
    function (oj, ko, $, accUtils, MapImgModel, TextRecogModel, ArrayDataProvider, FlattenedTreeDataProviderView, ArrayTreeDataProvider, KnockoutTemplateUtils) {
    function MapsCVViewModel() {
        
        self.showTable = ko.observable(true);
        self.msgTitle = ko.observable();
        self.msgBody = ko.observable();
        self.allLocationWholePhotos = ko.observableArray([]);


        //Get All Data from the array to the table interface
        /*self.dataProvider = new ArrayDataProvider(self.allLocationWholePhotos, {
            keyAttributes: "capture_id",
            implicitSort: [{ attribute: "capture_id", direction: "ascending" }],
        });*/
        this.KnockoutTemplateUtils = KnockoutTemplateUtils;
        this.arrayTreeDataProvider = new ArrayTreeDataProvider(self.allLocationWholePhotos, { keyAttributes: "lat" });
        this.dataProvider = ko.observable(new FlattenedTreeDataProviderView(this.arrayTreeDataProvider));

        self.refreshAllData = (filterValue) => {
            MapImgModel.getAllLocationWholePhotos((success, serverResult) => {
                if (filterValue == undefined) {
                    
                    self.allLocationWholePhotos(serverResult);
                    console.log(serverResult);
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


        self.selectedMenuItem = ko.observable("None selected yet");
        self.launchedFrom = ko.observable("None launched yet");

        self.myActionFunction = (event) => {
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
                    self.launchedFrom(+ context.rowIndex + ", " + context.columnIndex );
                }
            }
        };

        self.ExtractText = (row, map_provider) => {
            console.log("row" + row);
            if (map_provider == "all") {
                
            }else  if (self.allLocationWholePhotos()[row][map_provider] == null) {
                alert("No Image To Extract the text");
            } else {
                var imgPath = self.allLocationWholePhotos()[row][map_provider]["imgPath"];
                TextRecogModel.readTextList(imgPath, (success, data) => {
                    self.msgTitle("Extracted Successfully");
                    var result = "confidence:" + data.confidence + "\t wordsList:" + data.wordsList;
                    self.msgBody(result);
                    document.getElementById("msgDialog").open();
                    console.log(data);
                });
            }
            
        }


        //Dialogs
        self.closeDialog = () => {
            document.getElementById("msgDialog").close();
        }


        /*
         * The old work. that dr-ali stopped
        self.fileContent = ko.observable("");
        self.fileNames = ko.observable();
        self.imagePath = ko.observable("https://localhost:44370/Resources/Images/Map1.jpg");
        self.selectFiles = (event) => {
            self.fileNames(Array.prototype.map.call(event.detail.files, (file) => {
                return file.name;
            }));
            var files = event.detail.files;

            for (var i = 0; i < files.length; i++) {
                var file = files[i];
                console.log("files.length:" + files.length);
                self.fileContent(file);

                var reader = new FileReader();
                reader.addEventListener("loadend", function () {
                    self.fileContent(reader.result);
                });
                // reader.readAsText(file);
            }
            if (files.length < 1)
                self.fileContent("");
          //console.log(self.fileContent());
        }

        self.uploadMapImage = () => {
            MapImgModel.addMapImg(self.fileContent(), (success, msg) => {
                alert(msg);
                location.reload();
            });//end upload MapImg
        }
        */




      this.connected = () => {
        accUtils.announce('MapsCV page loaded.', 'assertive');
          document.title = "MapsCV";
      };
      this.disconnected = () => {
      };

      this.transitionCompleted = () => {
      };
    }

    return MapsCVViewModel;
  }
);
