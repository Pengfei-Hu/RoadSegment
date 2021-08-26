define(['jquery', 'knockout', 'ojs/ojmodel', 'text!../settings.json'],
    function ($, ko, sett) {
        class MapsImgs {
            constructor() {
                //this.mapsImgsEndpoint = JSON.parse(settings).apiserver;
                this.mapsImgsEndpoint = "https://localhost:44370/";
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
                        console.log(api_url);
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
            readTextList(imagePath, notify) {
                let api_url = this.mapsImgsEndpoint + "TextRecognition/TextList";
                this.getImageDetails(api_url, imagePath, notify);
            }
            readDetailsText(imagePath, notify) {
                let api_url = this.mapsImgsEndpoint + "TextRecognition/readDetailsText";
                this.getImageDetails(api_url, imagePath, notify);
            }

        }//end of class
        return new MapsImgs();
    });