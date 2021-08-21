/**
 * @ignore
 */
/*
 * Your customer ViewModel code goes here
 */
define(['accUtils', 'jquery', 'knockout', , "ojs/ojbutton", , "ojs/ojinputtext"],
 function(accUtils, $ , ko) {
    function CapturingViewModel() {
        let self = this;

        self.lat = ko.observable(80.6469622);
        self.lon = ko.observable(7.8612675);
        self.startzoomLevel = ko.observable(15);
        self.endzoomLevel = ko.observable(2);





        self.download = () => {
            
            /*var lat = document.getElementById("lat");
            var lon = $('lon').val();
*/
            var data = "lon=" + self.lon() + "&lat=" + self.lat() + "&startz=" + self.startzoomLevel() + "&endz=" + s               $.ajax({

                    url: 'http://127.0.0.1:5000/multi/all',
                    datatype: 'json',
                    type: 'get',
                   crossDomain: true,
                   data: data,
                    success: function () {

                        alert("Map captured successfully！");
                    },
                   error: function (err) {
                       console.log(err);
                        alert("Map captured FAILED");
                    }
                });elf.endzoomLevel();
            

        }




      this.connected = () => {
        accUtils.announce('Capturing page loaded.', 'assertive');
        document.title = "capturing";
        // Implement further logic if needed
      };

      /**
       * Optional ViewModel method invoked after the View is disconnected from the DOM.
       */
      this.disconnected = () => {
        // Implement if needed
      };

      /**
       * Optional ViewModel method invoked after transition to the new View is complete.
       * That includes any possible animation between the old and the new View.
       */
      this.transitionCompleted = () => {
        // Implement if needed
      };
    }

     return CapturingViewModel;
  }
);
