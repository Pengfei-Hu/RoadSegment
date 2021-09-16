define(['jquery', 'knockout', 'ojs/ojmodel', 'text!../settings.json'],
    function ($, ko, sett) {
        class Utils {
            constructor() {
                //this.UtilsEndpoint = JSON.parse(settings).apiserver;
                //Testing Server(localhost)
                this.UtilsEndpoint = "http://localhost:85/LocationPhotos/";
                //Tacoma Server(Development)
                //this.UtilsEndpoint = "http://uwtset1.tacoma.uw.edu:85/LocationPhotos/";
                
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

        }//end of class
        return new Utils();
    });