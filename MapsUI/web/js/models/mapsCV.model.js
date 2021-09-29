define(['jquery', 'knockout', 'ojs/ojmodel', 'text!../settings.json'],
    function ($, ko, sett) {
        class mapsCV {
            constructor() {
                //this.mapsCVEndpoint = JSON.parse(settings).apiserver;
                //Testing Server(localhost)
                this.mapsCVEndpoint = "http://localhost:85/cv/";
                //Tacoma Server(Development)
                //this.mapsCVEndpoint = "http://uwtset1.tacoma.uw.edu:85/cv/";
                
            }
            initializeModelCollection(endpoint) {
                this.mapsCVModelDef = oj.Model.extend({
                    url: endpoint,
                    idAttribute: "filename"
                });
                this.mapsCVCollDef = oj.Collection.extend({
                    url: endpoint,
                    comparator: "filename",
                    model: new this.mapsCVModelDef
                });
                this.mapsCV = new this.mapsCVCollDef;

            }
            setImageEffects(api_url, imagePath, effects, notify) {
                this.initializeModelCollection(api_url);
                let mapsCVRow = new this.mapsCVModelDef({}, this.mapsCV);
                mapsCVRow.save(null, {
                    type:'POST',
                    headers: {
                        'imagePath': imagePath,
                        'effects': effects,
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
            setGrayEffect(imagePath, notify) {
                let api_url = this.mapsCVEndpoint + "applyGrayFilter";
                this.setImageEffects(api_url, imagePath,"gray", notify);
            }
            setGrayEffectAllImgs(imagePath,effects, notify) {
                let api_url = this.mapsCVEndpoint + "applyEffectsToAllImgs";
                this.setImageEffects(api_url, imagePath, effects, notify);
            }

            readDetailsText(imagePath, notify) {
                let api_url = this.mapsCVEndpoint + "readDetailsText";
                this.getImageDetails(api_url, imagePath, notify);
            }

            //get FAccuracy
            getFAccuracy(correctWords, imagePath, notify) {
                console.log("correctWords:" + correctWords);
                console.log("imagePath:" + imagePath);

                let api_url = this.mapsCVEndpoint + "DetailsWithFAccuracy";
                this.initializeModelCollection(api_url);
                let mapsCVRow = new this.mapsCVModelDef({}, this.mapsCV);

                mapsCVRow.fetch({
                    headers: {
                        // 'Authorization': 'Basic cmVhZGVyX3VzZXI6RkBrZSEyMw==',
                        'Content-Type': 'application/json',
                        'correctWords': correctWords,
                        'imagePath': imagePath
                    },
                    success: function (coll, data) {
                        console.log("all data");
                        console.log(data);
                        notify(true, data);
                    },
                    error: function (model, xhr, options) {
                        notify(false, `Error Code: ${xhr.status}, msg:${options.textStatus} `);
                    }
                });
            }

            //get Colors Counts
            getColorsCounts(bingImg, googleImg, osmImg, notify) {
                let api_url = this.mapsCVEndpoint + "getColorsCountsForAllImgs";
                this.initializeModelCollection(api_url);
                let mapsCVRow = new this.mapsCVModelDef({
                    "imagesPaths": bingImg + "," + googleImg + "," + osmImg
                }, this.mapsCV);

                mapsCVRow.fetch({
                    headers: {
                        // 'Authorization': 'Basic cmVhZGVyX3VzZXI6RkBrZSEyMw==',
                        'Content-Type': 'application/json',
                        "imagesPaths": bingImg + "," + googleImg + "," + osmImg
                    },
                    success: function (coll, data) {
                        console.log("all data");
                        console.log(data);
                        notify(true, data);
                    },
                    error: function (model, xhr, options) {
                        notify(false, `Error Code: ${xhr.status}, msg:${options.textStatus} `);
                    }
                });
            }
        }//end of class
        return new mapsCV();
    });