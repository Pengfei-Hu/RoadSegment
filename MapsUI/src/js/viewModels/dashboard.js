/**
 * @ignore
 */
/*
 * Your dashboard ViewModel code goes here
 */
define(['ojs/ojcore', 'knockout', 'jquery', "ojs/ojarraydataprovider", 'models/stats.model',
    'accUtils', 'models/mapimgs.model', "ojs/ojoffcanvas", "ojs/ojknockout", "ojs/ojchart", "ojs/ojtoolbar",
    "ojs/ojmenu", "ojs/ojbutton", "ojs/ojoption", "ojs/ojselectsingle"],
    function (oj, ko, $, ArrayDataProvider, statsModel, accUtils, MapImgModel) {
        function DashboardViewModel() {
            let self = this;
            self.jsonData = ko.observable("");
            self.countrySelectVal = ko.observable();
            self.countries = ko.observableArray([]);
            self.countriesDP = new ArrayDataProvider(self.countries, {
                keyAttributes: "value",
            });
            self.countrySelectVal.subscribe(function (selectedCountry) {
                self.loadStats(selectedCountry);
            });
            self.loadCountries = () => {
                MapImgModel.getCountriesWeHave((success, result) => {
                    if (result.data != undefined) {
                        result.data = result.data.filter(val => { console.log(val); val = val.toString().replace('\"', ''); return true; });
                        self.countries(result.data);
                        self.countries.valueHasMutated();
                    } else {
                        console.log(result);
                    }
                });
            }
            self.loadCountries();


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

            self.loadStats = (country) => {
                statsModel.getProvidersPlacesWords(country, (success, result) => {

                    console.log("result");
                    console.log(result);

                    self.jsonData(result.wordsMapProviderResult);
                    self.dataPerPlaces(result.wordsMapProviderPerPlacesResult);

                    self.dataAll(result.wordsMapProviderResult);
                    console.log("result.wordsMapProviderResult");
                    console.log(result.wordsMapProviderResult);
                    self.dataFiltersMapProvider(result.filtersMapProviderResult);
                    self.datafiltersDWU(result.filtersDetectedWrongUndetectedResult);
                    self.dataResolutionAccuracy(result.resolutionEffectsAccuracyResult);
                    self.dataImpactOfResolutionOnAccuracy(result.impactOfResolutionOnAccuracyResult);
                    self.datafiltersMDRecallPreF1For256(result.filtersMDRecallPreF1For256);
                    self.datafiltersMDRecallPreF1ForGoogle(result.filtersMDRecallPreF1ForGoogle);
                });
            }
            self.loadStats("");


            self.parseJSONToCSVStr = (jsonData) => {
                if (jsonData.length == 0) {
                    return '';
                }

                let keys = Object.keys(jsonData[0]);
                console.log("keys:" + keys)
                let columnDelimiter = ',';
                let lineDelimiter = '\n';

                let csvColumnHeader = keys.join(columnDelimiter);
                let csvStr = csvColumnHeader + lineDelimiter;

              //  jsonData.forEach(data => {
                    jsonData.forEach(item => {
                        keys.forEach((key, index) => {
                            console.log(item[key]);
                            csvStr += (item[key] == null) ? "" : item[key].toString().replace(/,/g, '-');
                            if (index < keys.length - 1) {
                                csvStr += columnDelimiter;
                            }
                            //    csvStr += item[key];
                        });
                        csvStr += lineDelimiter;
                    });
              //  });//whole
                return encodeURIComponent(csvStr);;
            }

            self.exportToCsvFile = () => {
                let csvStr = self.parseJSONToCSVStr(self.jsonData());
                let dataUri = 'data:text/csv;charset=utf-8,' + csvStr;

                let exportFileDefaultName = 'data.csv';

                let linkElement = document.createElement('a');
                linkElement.setAttribute('href', dataUri);
                linkElement.setAttribute('download', exportFileDefaultName);
                linkElement.click();
            }


      this.connected = () => {
        accUtils.announce('Dashboard page loaded.', 'assertive');
        document.title = "Dashboard";
        // Implement further logic if needed
      };

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
