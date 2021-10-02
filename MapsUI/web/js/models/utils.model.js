define(['jquery', 'knockout', 'ojs/ojmodel', 'text!../config/settings.json'],
    function ($, ko,model, sett) {
        class Utils {
            constructor() {
                console.log(sett);
                sett = JSON.parse(sett);
                console.log(sett.apiserver);
                //this.UtilsEndpoint = JSON.parse(settings).apiserver;
                //Testing Server(localhost)
                this.UtilsEndpoint = "http://localhost:85/LocationPhotos/";
                this.pythonEndpoint = "http://localhost:84/";
                //Tacoma Server(Development)
                //this.UtilsEndpoint = "http://uwtset1.tacoma.uw.edu:85/LocationPhotos/";
                //this.pythonEndpoint = "http://uwtset1.tacoma.uw.edu:84/";
            }
            initializeModelCollection(endpoint) {
                this.UtilsModelDef = oj.Model.extend({
                    url: endpoint,
                    idAttribute: "capture_id"
                });
                this.UtilsCollDef = oj.Collection.extend({
                    url: endpoint,
                    comparator: "capture_id",
                    model: new this.UtilsModelDef
                });
                this.Utils = new this.UtilsCollDef;

            }
            UpdateLocationsWithoutGroundTruth(notify) {
                this.initializeModelCollection(this.UtilsEndpoint +"UpdateLocationsWithoutGroundTruth");
                let UtilsRow = new this.UtilsModelDef({}, this.Utils);
                UtilsRow.save(null, {
                    type: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    success: (coll, data) => {
                        notify(true, data);
                    },
                    error: (model, xhr, options) => {
                        notify(false, 'Error:' + xhr.textStatus);
                        console.log("Error");
                        console.log(options);
                    },
                });//end
            }
            UpdateLocationsAddress(notify) {
                this.initializeModelCollection(this.pythonEndpoint +"UpdateLocationsAddress");
                let UtilsRow = new this.UtilsModelDef({}, this.Utils);
                UtilsRow.fetch({
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    success: (coll, data) => {
                        notify(true, data);
                    },
                    error: (model, xhr, options) => {
                        notify(false, 'Error:' + xhr.textStatus);
                        console.log("Error");
                        console.log(options);
                    },
                });//end
            }

        }//end of class
        return new Utils();
    });