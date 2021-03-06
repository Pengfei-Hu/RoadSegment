/**
 * @ignore
 */
/*
 * Your about ViewModel code goes here
 */
define(['ojs/ojcore', 'knockout', 'jquery', 'accUtils','models/utils.model','models/mapRecogResults.model',
    "ojs/ojprogress-bar", "ojs/ojformlayout",
    "ojs/ojbutton", "ojs/ojinputtext", "ojs/ojlabel"],
    function (oj, ko, $, accUtils,utilsModel, MapRecogResults) {
    function UtilsViewModel() {
        let self = this;
        //functions
        self.loadGroundTruth = () => {
            utilsModel.UpdateLocationsWithoutGroundTruth((success, data) => {
                alert("All New Ground Truths Updates Successfully");
                alert("number of ground-truth loaded:" + data.noOfLocationUpdated)
                console.log(data);
            })
        }//end loadGroundTruth

        self.ApplyAllFiltersToAllImgs = () => {
            alert("This task takes a lot of time, be patient and let the system do the task ");
            MapRecogResults.applyAllGroupOfEffectsToAllImgs((success, data) => {
                alert("All filters applied to all existing images");
                console.log(data);
            })

        }//end loadGroundTruth

        self.UpdateLocationsAddress = () => {
            utilsModel.UpdateLocationsAddress((success, data) => {
                alert("All Locations Now with address");
                console.log(data);
            })

        }//end loadGroundTruth

      this.connected = () => {
        accUtils.announce('Utils page loaded.', 'assertive');
        document.title = "Utility";
      };

      this.disconnected = () => {
      };


      this.transitionCompleted = () => {

      };
    }

     return UtilsViewModel;
  }
);
