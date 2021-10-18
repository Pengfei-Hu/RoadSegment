define(['jquery', 'knockout', 'ojs/ojmodel', 'text!../settings.json'],
    function ($, ko, sett) {
        class MapRecogResults {
            constructor() {
                //this.MapRecogResultsEndpoint = JSON.parse(settings).apiserver;
                //Testing Server(localhost)
                this.MapRecogResultsEndpoint = "http://localhost:85/MapRecogResults";
                //Tacoma Server(Development)
                //this.MapRecogResultsEndpoint = "http://uwtset1.tacoma.uw.edu:85/MapRecogResults";
            }
            initializeModelCollection(endpoint) {
                this.MapRecogResultsModelDef = oj.Model.extend({
                    url: endpoint,
                    idAttribute: "result_id"
                });
                this.MapRecogResultsCollDef = oj.Collection.extend({
                    url: endpoint,
                    comparator: "result_id",
                    model: new this.MapRecogResultsModelDef
                });
                this.MapRecogResults = new this.MapRecogResultsCollDef;

            }
            applyAllGroupOfEffectsToAllImgs(notify) {
                let api_url = this.MapRecogResultsEndpoint +"/SaveAllLocationsPicturesResults";
                this.initializeModelCollection(api_url);
                let MapRecogResultsRow = new this.MapRecogResultsModelDef({}, this.MapRecogResults);
                MapRecogResultsRow.save(null, {
                    type: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    success: (coll, data) => {
                        console.log(data);
                        notify(true, data);
                    },
                    error: (model, xhr, options) => {
                        notify(false, 'Error:' + xhr.textStatus);
                        console.log("Error");
                        console.log(options);
                    },
                });//end fetch
            }

        }//end of class
        return new MapRecogResults();
    });