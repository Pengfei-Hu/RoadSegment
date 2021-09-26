/**
 * @ignore
 */
/*
 * Your dashboard ViewModel code goes here
 */
define(['ojs/ojcore', 'knockout', 'jquery', "ojs/ojarraydataprovider", 'models/stats.model',
    'accUtils', "ojs/ojoffcanvas", "ojs/ojknockout", "ojs/ojchart", "ojs/ojtoolbar",
    "ojs/ojmenu", "ojs/ojbutton", "ojs/ojoption"],
    function (oj, ko, $, ArrayDataProvider, statsModel, accUtils) {
        function DashboardViewModel() {
            let self = this;
            self.googlSelectedMenuItem = ko.observable("(None selected yet)");
            self.googleMenuItemAction = (event) => {
                self.googlSelectedMenuItem(event.detail.selectedValue);
            };

            self.stackValue = ko.observable("off");
            self.orientationValue = ko.observable("vertical");


            self.dataPerPlaces = ko.observableArray([]);
            self.dataProviderPerPlace = new ArrayDataProvider(self.dataPerPlaces, {});

            self.dataAll = ko.observableArray([]);
            self.dataProviderAll = new ArrayDataProvider(self.dataAll, {});

            self.dataFiltersMapProvider= ko.observableArray([]);
            self.filtersMapProviderData = new ArrayDataProvider(self.dataFiltersMapProvider, {});

            self.datafiltersDWU = ko.observableArray([]);
            self.filtersDetectedWrongUndetectedDataProvider = new ArrayDataProvider(self.datafiltersDWU, {});

            self.dataResolutionAccuracy = ko.observableArray([]);
            self.resolutionAccuracyDataProvider = new ArrayDataProvider(self.dataResolutionAccuracy, {});

            self.dataImpactOfResolutionOnAccuracy = ko.observableArray([]);
            self.dataImpactOfResolutionOnAccuracyDataProvider = new ArrayDataProvider(self.dataImpactOfResolutionOnAccuracy, {});

            self.datafiltersMDRecallPreF1For256 = ko.observableArray([]);
            self.datafiltersMDRecallPreF1For256DataProvider = new ArrayDataProvider(self.datafiltersMDRecallPreF1For256, {});

            self.datafiltersMDRecallPreF1ForGoogle = ko.observableArray([]);
            self.datafiltersMDRecallPreF1ForGoogleDataProvider = new ArrayDataProvider(self.datafiltersMDRecallPreF1ForGoogle, {});


            statsModel.getProvidersPlacesWords((success, result) => {
                self.dataPerPlaces(result.wordsMapProviderPerPlacesResult);
                self.dataAll(result.wordsMapProviderResult);
                self.dataFiltersMapProvider(result.filtersMapProviderResult);
                self.datafiltersDWU(result.filtersDetectedWrongUndetectedResult);
                self.dataResolutionAccuracy(result.resolutionEffectsAccuracyResult);
                self.dataImpactOfResolutionOnAccuracy(result.impactOfResolutionOnAccuracyResult);
                self.datafiltersMDRecallPreF1For256(result.filtersMDRecallPreF1For256);
                self.datafiltersMDRecallPreF1ForGoogle(result.filtersMDRecallPreF1ForGoogle);
            });


      this.connected = () => {
        accUtils.announce('Dashboard page loaded.', 'assertive');
        document.title = "Dashboard";
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


    return DashboardViewModel;
  }
);
