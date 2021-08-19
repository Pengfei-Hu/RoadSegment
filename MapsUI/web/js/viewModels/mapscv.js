/**
 * @ignore
 */
/*
 * Your incidents ViewModel code goes here
 */
define(['knockout', 'jquery', 'accUtils', 'models/mapimgs.model','ojs/ojarraydataprovider',
     "ojs/ojradioset", "ojs/ojlabel", 'ojs/ojarraydataprovider',
    "ojs/ojfilepicker", 'ojs/ojinputtext', "ojs/ojformlayout", 'ojs/ojavatar','ojs/ojinputtext', 'ojs/ojdialog',
    'ojs/ojtable'],
    function (ko, $, accUtils, MapImgModel, ArrayDataProvider ) {
    function MapsCVViewModel() {
        
        self.showTable = ko.observable(true);
        self.msgTitle = ko.observable();
        self.msgBody = ko.observable();
        self.allLocationWholePhotos = ko.observableArray([]);


        //Get All Data from the array to the table interface
        self.dataProvider = new ArrayDataProvider(self.allLocationWholePhotos, {
            keyAttributes: "capture_id",
            implicitSort: [{ attribute: "capture_id", direction: "ascending" }],
        }
        );

        self.refreshAllData = (filterValue) => {
            MapImgModel.getAllLocationWholePhotos((success, serverResult) => {
                if (filterValue == undefined) {
                    
                    self.allLocationWholePhotos(serverResult);
                    console.log(self.allLocationWholePhotos());
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

        self.ReadingText = (event, context) => {
            ;
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
