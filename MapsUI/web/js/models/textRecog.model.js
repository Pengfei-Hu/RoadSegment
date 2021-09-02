define(['jquery', 'knockout', 'ojs/ojmodel', 'text!../settings.json'],
    function ($, ko, sett) {
        class MapsImgs {
            constructor() {
                //this.mapsImgsEndpoint = JSON.parse(settings).apiserver;
                //Testing Server(localhost)
                this.mapsImgsEndpoint = "http://localhost:85/TextRecognition/";
                //Tacoma Server(Development)
                //this.mapsImgsEndpoint = "http://uwtset1.tacoma.uw.edu:85/TextRecognition/";
                
            }
            initializeModelCollection(endpoint) {
                this.MapsImgsModelDef = oj.Model.extend({
                    url: endpoint,
                    idAttribute: "filename"
                });
                this.MapsImgsCollDef = oj.Collection.extend({
                    url: endpoint,
                    comparator: "filename",
                    model: new this.MapsImgsModelDef
                });
                this.mapsImgs = new this.MapsImgsCollDef;

            }
            getImageDetails(api_url, imagePath, notify) {
                this.initializeModelCollection(api_url);
                let mapsImgsRow = new this.MapsImgsModelDef({}, this.mapsImgs);
                mapsImgsRow.fetch({
                    headers: {
                        // 'Authorization': 'Basic cmVhZGVyX3VzZXI6RkBrZSEyMw==',
                        'imagePath': imagePath,
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
                });//end fetch
            }
            readTextList(imagePath, notify) {
                let api_url = this.mapsImgsEndpoint + "TextList";
                this.getImageDetails(api_url, imagePath, notify);
            }
            readDetailsText(imagePath, notify) {
                let api_url = this.mapsImgsEndpoint + "readDetailsText";
                this.getImageDetails(api_url, imagePath, notify);
            }

            //get FAccuracy
            getFAccuracy(correctWords, imagePath, notify) {
                let api_url = this.mapsImgsEndpoint + "DetailsWithFAccuracy";
                this.initializeModelCollection(api_url);
                let mapsImgsRow = new this.MapsImgsModelDef({}, this.mapsImgs);

                mapsImgsRow.fetch({
                    headers: {
                        // 'Authorization': 'Basic cmVhZGVyX3VzZXI6RkBrZSEyMw==',
                        'Content-Type': 'application/json',
                        'correctWords': correctWords,
                        'imagePath': imagePath
                    },
                    success: function (coll, data) {
                        console.log("------------------------------")
                        console.log("correctWords:" + correctWords);
                        console.log("imagePath:" + imagePath);
                        console.log("--------------RESULT----------")
                        console.log(data);
                        notify(true, data);
                    },
                    error: function (model, xhr, options) {
                        notify(false, `Error Code: ${xhr.status}, msg:${options.textStatus} `);
                    }
                });
            }

        }//end of class
        return new MapsImgs();
    });