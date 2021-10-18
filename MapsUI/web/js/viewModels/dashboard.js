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
                country = (country == null) ? "" : country
                statsModel.getProvidersPlacesWords(country, (success, result) => {

                    console.log("result");
                    console.log(result);

                    self.jsonData(result);
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

                try {
                    let firstRow = "filtersDetectedWrongUndetectedResult, , , , ,filtersMDRecallPreF1For256, , , ,filtersMDRecallPreF1ForGoogle, , , , ,filtersMapProviderResult, , ,impactOfResolutionOnAccuracyResult, , , , , resolutionEffectsAccuracyResult, , ,wordsMapProviderPerPlacesResult, , ,wordsMapProviderResult, , \n";

                    let csvStr = "";
                    let columnDelimiter = ',';
                    let lineDelimiter = '\n';
                    //  jsonData.forEach(data => {
                    for (var objName in jsonData) {
                        if (Object.prototype.hasOwnProperty.call(jsonData, objName)) {
                            csvStr += "\n" + objName + "\n"
                            console.log("jsonData[objName]"); console.log(jsonData[objName]);
                            let keys = Object.keys(jsonData[objName][0]);
                            let csvColumnHeader = keys.join(columnDelimiter);
                            csvStr += csvColumnHeader + lineDelimiter;
                            jsonData[objName].forEach(item => {
                                keys.forEach((key, index) => {
                                    csvStr += (item[key] == null) ? "" : item[key].toString().replace(/,/g, '-');
                                    if (index < keys.length - 1) {
                                        csvStr += columnDelimiter;
                                    }
                                    //    csvStr += item[key];
                                });
                                csvStr += lineDelimiter;
                            });
                            //  });//whole
                        }
                    }
                    return encodeURIComponent(csvStr);
                } catch (ex) {
                    alert("Please select country that has stats data!, to download")
                }
            }

            self.exportToCsvFile = () => {
                let csvStr = self.parseJSONToCSVStr(self.jsonData());
                let dataUri = 'data:text/csv;charset=utf-8,' + csvStr;

                let exportFileDefaultName = (self.countrySelectVal() == null) ? 'All-data.csv' : self.countrySelectVal()+ '-data.csv';

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
