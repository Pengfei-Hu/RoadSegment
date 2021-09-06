/**
 * @ignore
 */
/*
 * Your customer ViewModel code goes here
 */
define(['ojs/ojcore', 'knockout', 'jquery', 'accUtils',  "ojs/ojprogress-bar",
    "ojs/ojbutton", "ojs/ojformlayout", "ojs/ojinputtext", "ojs/ojlabel"],

 function(oj, ko, $, accUtils ) {
    function CapturingViewModel() {
        var self = this;
        
        self.lat = ko.observable(6.9184);
        self.lon = ko.observable(79.9909);
        self.startzoomLevel = ko.observable(9);
        self.endzoomLevel = ko.observable(10);

        this.downloadImages = () => {
            var progress = document.getElementById("progressBarWrapper");
            progress.style.visibility = "visible";
            /*var lat = document.getElementById("lat");
            var lon = $('lon').val();
*/
            var data = "lon=" + self.lon() + "&lat=" + self.lat() + "&startz=" + self.startzoomLevel() + "&endz=" + self.endzoomLevel();
            $.ajax({
                    url: 'http://localhost:84/multi/all',
                    datatype: 'json',
                    type: 'get',
                   crossDomain: true,
                   data: data,
                    success: function () {
                        progress.style.visibility = "hidden";
                        alert("Map captured successfully！");
                       
                    },
                error: function (err) {
                    progress.style.visibility = "hidden";
                       console.log(err);
                        alert("Map captured FAILED");
                    }
            });
          
            

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
