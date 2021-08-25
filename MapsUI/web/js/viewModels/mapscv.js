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
    "ojs/ojfilepicker",  "ojs/ojformlayout", 'ojs/ojavatar','ojs/ojinputtext', 'ojs/ojdialog',
    'ojs/ojtable', "ojs/ojknockout", "ojs/ojoption", "ojs/ojmenu", "ojs/ojbutton"],
    function (oj, ko, $, accUtils, MapImgModel, TextRecogModel, ArrayDataProvider, FlattenedTreeDataProviderView, ArrayTreeDataProvider, KnockoutTemplateUtils) {
    function MapsCVViewModel() {
        
        self.showTable = ko.observable(true);
        self.msgTitle = ko.observable();
        self.msgBody = ko.observable();
        self.allLocationWholePhotos = ko.observableArray([]);
        self.partlist = ko.observable("");
        self.lastCorrectPartlist = ko.observable("");
        self.data_multi = ko.observable(0);
        self.bingImagePath = ko.observable("https://blogs.bing.com/BingBlogs/files/dc/dce88d2a-2bf9-4c65-9cca-1c425d571e75.png");
        self.googleImagePath = ko.observable("https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Google_Maps_Logo_2020.svg/1137px-Google_Maps_Logo_2020.svg.png");
        self.osmImagePath = ko.observable("https://upload.wikimedia.org/wikipedia/commons/b/b0/Openstreetmap_logo.svg");
        self.lat = ko.observable(80.6469622);
        self.lng = ko.observable(7.8612675);
        self.startzoomLevel = ko.observable(15);
        self.endzoomLevel = ko.observable(17);
        self.address = ko.observable("");


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
                    self.launchedFrom(+ context.rowIndex + ", " + context.columnIndex );
                }
                self.lng(self.allLocationWholePhotos()[context.rowIndex].lng);
                self.lat(self.allLocationWholePhotos()[context.rowIndex].lat);
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

        self.backToMain = () => {
            self.showTable(true);
        }
        //Dialogs
        self.closeDialog = () => {
            document.getElementById("msgDialog").close();
        }

        self.actionMenuListener = (event, context) => {
            var selectMenuItem = event.detail.selectedValue;
            var rowData = context.item.data
            console.log(rowData);
            if (selectMenuItem == "ExtractAllText") {

            } else if (selectMenuItem == "Visualize") {
                self.startzoomLevel(rowData["zoom_level"]);
                self.lat(rowData["lat"]);
                self.lng(rowData["lng"]);

                self.display();
                self.showTable(false);
            }

           /* const rowIndex = this.empArray.indexOf(context.item.data);
            if (event.detail.selectedValue === "delete") {
                this.empArray.splice(rowIndex, 1);
            }
            else if (event.detail.selectedValue === "approve") {
                const rowData = context.item.data;
                rowData.Status = "Approved";
                this.empArray.splice(rowIndex, 1, rowData);
            }*/
        };


  
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
                alert("It is the first level we have");
            }
            
            if (self.partlist() != "") {
                send_info()
            } else {
                send_mu()
            }
            
        }
        self.server = ko.observable("http://localhost:5000/");
        function send_info() {
            var data = "lon=" + self.lng() + "&lat=" + self.lat() + "&startz=" + self.startzoomLevel() + "&endz=" + self.data_multi().toString() + "&partlist=" + self.partlist().toString();
            console.log('http://127.0.0.1:5000/multi/select get:')
            console.log(data);
            $.ajax({
                url: 'http://127.0.0.1:5000/multi/select',
                datatype: 'json',
                type: 'get',
                crossDomain: true,
                data: data,
                success: function (data) {
                    console.log(data);
                    console.log("success send_info");
                    if (data.bing != undefined) {
                        self.bingImagePath(self.server() + data.bing);
                        self.googleImagePath(self.server() + data.google);
                        self.osmImagePath(self.server() + data.osm);
                        self.lastCorrectPartlist(self.partlist());
                    } else {
                        if (self.data_multi() > self.startzoomLevel())
                            self.data_multi(self.data_multi() - 1);
                        else
                            self.data_multi(self.data_multi() + 1);
                        console.log("DataMulti=" + self.data_multi());
                        self.partlist(self.lastCorrectPartlist().substring(0, self.lastCorrectPartlist().length ));
                        console.log("partlist=" + self.partlist());
                        console.log("lastCorrectPartlist=" + self.lastCorrectPartlist());
                        alert("We don't have another level yet.")
                    }

                },
                error: function (err) {
                    alert("This is the depth level we have (send_info)")
                    console.log(err);
                }
            })
        }
        function send_mu(data) {
            var data = "lon=" + self.lng() + "&lat=" + self.lat() + "&startz=" + self.startzoomLevel() + "&endz=" + self.data_multi().toString();
            //           "lon=" + data.field.lon + "&lat= " + data.field.lat + "&tileZoom= " + data.field.tileZoom + "&endzoomLevel=" + data_multi,
            //lon=7.8612675&lat=80.6469622&startz=12&endz=0
            console.log(data);
            $.ajax({
                url: 'http://127.0.0.1:5000/multi/go',
                datatype: 'json',
                type: 'get',
                crossDomain: true,
                data: data,
                success: function (data) {
                    console.log(data);
                    console.log("success send_mu");
                    console.log("http://127.0.0.1:5000/multi/go get:")
                    console.log(data);
                    self.bingImagePath(self.server() + data.bing);
                    self.googleImagePath(self.server() + data.google);
                    self.osmImagePath(self.server() + data.osm);
                },
                error: function (err) {
                    alert("This is the depth level we have (go)")
                    console.log(err);
                }
            })
        }


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
