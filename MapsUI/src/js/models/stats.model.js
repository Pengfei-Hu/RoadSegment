define(['jquery', 'knockout', 'ojs/ojmodel', 'text!../settings.json'],
    function ($, ko, sett) {
        class Stats {
            constructor() {
                //this.StatsEndpoint = JSON.parse(settings).apiserver;
                //Testing Server(localhost)
                this.StatsEndpoint = "http://localhost:84/";
                this.pythonEndpoint = "http://localhost:84/";
                //Tacoma Server(Development)
                
                //this.StatsEndpoint = "http://uwtset1.tacoma.uw.edu:84/";
                //this.pythonEndpoint = "http://uwtset1.tacoma.uw.edu:84/";
                
            }
            initializeModelCollection(endpoint) {
                this.StatsModelDef = oj.Model.extend({
                    url: endpoint,
                    idAttribute: "filename"
                });
                this.StatsCollDef = oj.Collection.extend({
                    url: endpoint,
                    comparator: "filename",
                    model: new this.StatsModelDef
                });
                this.Stats = new this.StatsCollDef;

            }
            getProvidersPlacesWords(country, notify) {
                let api_url = this.StatsEndpoint +"providerWordsStats?country="+country;
                this.initializeModelCollection(api_url);
                let StatsRow = new this.StatsModelDef({}, this.Stats);
                StatsRow.fetch({
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

            getAllLocationWholePhotos(notify) {
                let api_url = this.StatsEndpoint + "LocationPhotos/AllLocationWholePhotos";
                this.initializeModelCollection(api_url);
                let StatsRow = new this.StatsModelDef({}, this.Stats);

                StatsRow.fetch({
                    headers: {
                       // 'Authorization': 'Basic cmVhZGVyX3VzZXI6RkBrZSEyMw==',
                        'Content-Type': 'application/json'
                    },
                    success: function (coll, data) {
                        //format result from server to be as table array provider

                        var arrObjs = Object.entries(data).map((val) => {
                            return val[1]
                        });
                        //remove any null elements in array
                        arrObjs = arrObjs.filter(img => img != null)
                        console.log(arrObjs);
                        notify(true, arrObjs[0]);
                    },
                    error: function (model, xhr, options) {
                        notify(false, `Error Code: ${xhr.status}, msg:${options.textStatus} `);
                    }
                });
            }
            //get the name of the location
            getAddressOfLatLng(lat, lng, notify) {
                let api_url = this.pythonEndpoint + "geocoding?" + "lon=" + lng + "&lat=" + lat;
                this.initializeModelCollection(api_url);
                let StatsRow = new this.StatsModelDef({}, this.Stats);

                StatsRow.fetch({
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    success: function (coll, data) {
                        notify(true, data);
                    },
                    error: function (model, xhr, options) {
                       
                        notify(false, `Error Code: ${xhr.status}, msg:${options.textStatus} `);
                    }
                });
            }


        }//end of class
        return new Stats();
    });