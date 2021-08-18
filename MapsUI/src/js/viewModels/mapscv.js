/**
 * @ignore
 */
/*
 * Your incidents ViewModel code goes here
 */
define(['knockout', 'jquery', 'accUtils', 'models/mapimgs.model', "ojs/ojradioset", "ojs/ojlabel",
    "ojs/ojfilepicker", 'ojs/ojinputtext', "ojs/ojformlayout",'ojs/ojavatar'],
 function(ko,$, accUtils, MapImgModel) {
    function MapsCVViewModel() {
        self.fileContent = ko.observable("");
        self.fileNames = ko.observable();
        self.imagePath = ko.observable("https://localhost:44370/Resources/Images/Map1.jpg")



        
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
            });//end upload MapImg
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
