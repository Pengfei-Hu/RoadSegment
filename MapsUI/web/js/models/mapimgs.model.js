define(['jquery', 'knockout', 'ojs/ojmodel', 'text!../settings.json'],
    function ($, ko, sett) {
        class MapsImgs {
            constructor() {
                //this.mapsImgsEndpoint = JSON.parse(settings).apiserver;
                this.mapsImgsEndpoint = "https://localhost:44370/";
                this.pythonEndpoint = "http://localhost:5000/";
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
            getMapsImgsList(notify) {
                let api_url = this.mapsImgsEndpoint;
                this.initializeModelCollection(api_url);
                let mapsImgsRow = new this.MapsImgsModelDef({}, this.mapsImgs);
                mapsImgsRow.fetch({
                    headers: {
                       // 'Authorization': 'Basic cmVhZGVyX3VzZXI6RkBrZSEyMw==',
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

            addMapImg(imageData, notify) {
                let api_url = this.mapsImgsEndpoint +"upload/UploadMapImage"; 
                
                this.initializeModelCollection(api_url);
                let mapsImgsRow = new this.MapsImgsModelDef({
                    // "id": id.toString(),
                }, this.mapsImgs);
                //AJAX (Take Time)
                
                        if (imageData != "") {
                            let imgForm = new FormData();

                            imgForm.append("imageFile", imageData);
                            $.ajax({
                                type: 'POST',
                                processData: false,
                                contentType: false,
                                enctype: 'multipart/form-data',
                                url: api_url,
                                data: imgForm,
                                success: function (data) {
                                    console.log(data);
                                    notify(true, `Image Uploaded Successfully `);
                                },
                                error: function (model, xhr, options) {
                                    console.log("Error");
                                    console.log(options);
                                    console.log(xhr);
                                    console.log(model);
                                    notify(false, `Error Code: ${xhr.status}, msg:${options.textStatus} `);
                                }
                            });
                        } else {
                            notify(false, 'No Image to upload');
                        }
                        
                    
            };//end addMapsImg

            updateClass(id, title, description, isUpdate, notify) {

            }
            deleteArticle(id, notify) {
                let api_url = this.mapsImgsEndpoint + "/" + id
                this.initializeModelCollection(api_url);
                let mapsImgsRow = new this.MapsImgsModelDef({
                    "id": id
                }, this.mapsImgs);
            mapsImgsRow.save(null, {
                type: "DELETE",
                success: function (model, response, options) {

                    notify(true, "التصنيف الذى كان يحمل الرقم:" + id + " قد تم حذفه نهائيا");
                },
                error: function (model, xhr, options) {
                    notify(false, `Error Code: ${xhr.status}, msg:${options.textStatus} `);
                }
            });
            }
            getAllLocationWholePhotos(notify) {
                let api_url = this.mapsImgsEndpoint + "LocationPhotos/AllLocationWholePhotos";
                this.initializeModelCollection(api_url);
                let mapsImgsRow = new this.MapsImgsModelDef({}, this.mapsImgs);

                mapsImgsRow.fetch({
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

            getAddressOfLatLng(lat, lng, notify) {
                let api_url = this.pythonEndpoint + "geocoding?" + "lon=" + lng + "&lat=" + lat;
                this.initializeModelCollection(api_url);
                let mapsImgsRow = new this.MapsImgsModelDef({}, this.mapsImgs);

                mapsImgsRow.fetch({
                    headers: {
                        // 'Authorization': 'Basic cmVhZGVyX3VzZXI6RkBrZSEyMw==',
                        
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
        return new MapsImgs();
    });