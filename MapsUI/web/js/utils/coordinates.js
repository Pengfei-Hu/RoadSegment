define(['jquery', 'knockout', 'ojs/ojmodel', 'text!../settings.json'],
    function ($, ko, sett) {
        class Coordinates {

            constructor() {
                this.EarthRadius = 6378137;
                this.MinLatitude = -85.05112878;
                this.MaxLatitude = 85.05112878;
                this.MinLongitude = -180;
                this.MaxLongitude = 180;
            }


            /// <summary>  
            /// Clips a number to the specified minimum and maximum values.  
            /// </summary>  
            /// <param name="n">The number to clip.</param>  
            /// <param name="minValue">Minimum allowable value.</param>  
            /// <param name="maxValue">Maximum allowable value.</param>  
            /// <returns>The clipped value.</returns>  

            Clip(n, minValue, maxValue) {
                return Math.min(Math.max(n, minValue), maxValue);
            }

            /// <summary>  
            /// Determines the map width and height (in pixels) at a specified level  
            /// of detail.  
            /// </summary>  
            /// <param name="levelOfDetail">Level of detail, from 1 (lowest detail)  
            /// to 23 (highest detail).</param>  
            /// <returns>The map width and height in pixels.</returns>  
            MapSize(levelOfDetail) {
                return 256 << levelOfDetail;
            }

            /// <summary>  
            /// Determines the ground resolution (in meters per pixel) at a specified  
            /// latitude and level of detail.  
            /// </summary>  
            /// <param name="latitude">Latitude (in degrees) at which to measure the  
            /// ground resolution.</param>  
            /// <param name="levelOfDetail">Level of detail, from 1 (lowest detail)  
            /// to 23 (highest detail).</param>  
            /// <returns>The ground resolution, in meters per pixel.</returns>  
            GroundResolution(latitude, levelOfDetail) {
                latitude = Clip(latitude, this.MinLatitude, this.MaxLatitude);
                return Math.Cos(latitude * Math.PI / 180) * 2 * Math.PI * this.EarthRadius / this.MapSize(levelOfDetail);
            }

            /// <summary>  
            /// Determines the map scale at a specified latitude, level of detail,  
            /// and screen resolution.  
            /// </summary>  
            /// <param name="latitude">Latitude (in degrees) at which to measure the  
            /// map scale.</param>  
            /// <param name="levelOfDetail">Level of detail, from 1 (lowest detail)  
            /// to 23 (highest detail).</param>  
            /// <param name="screenDpi">Resolution of the screen, in dots per inch.</param>  
            /// <returns>The map scale, expressed as the denominator N of the ratio 1 : N.</returns>  
            MapScale(latitude, levelOfDetail, screenDpi) {
                return GroundResolution(latitude, levelOfDetail) * screenDpi / 0.0254;
            }

            /// <summary>  
            /// Converts a point from latitude/longitude WGS-84 coordinates (in degrees)  
            /// into pixel XY coordinates at a specified level of detail.  
            /// </summary>  
            /// <param name="latitude">Latitude of the point, in degrees.</param>  
            /// <param name="longitude">Longitude of the point, in degrees.</param>  
            /// <param name="levelOfDetail">Level of detail, from 1 (lowest detail)  
            /// to 23 (highest detail).</param>  
            /// <param name="pixelX">Output parameter receiving the X coordinate in pixels.</param>  
            /// <param name="pixelY">Output parameter receiving the Y coordinate in pixels.</param>  
            LatLongToPixelXY(latitude, longitude, levelOfDetail, pixelX, pixelY) {
                latitude = Clip(latitude, this.MinLatitude, this.MaxLatitude);
                longitude = Clip(longitude, this.MinLongitude, this.MaxLongitude);

                var x = (longitude + 180) / 360;
                var sinLatitude = Math.Sin(latitude * Math.PI / 180);
                var y = 0.5 - Math.Log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * Math.PI);

                var mapSize = MapSize(levelOfDetail);
                pixelX = parseInt(Clip(x * mapSize + 0.5, 0, mapSize - 1));
                pixelY = parseInt(Clip(y * mapSize + 0.5, 0, mapSize - 1));
            }

            /// <summary>  
            /// Converts a pixel from pixel XY coordinates at a specified level of detail  
            /// into latitude/longitude WGS-84 coordinates (in degrees).  
            /// </summary>  
            /// <param name="pixelX">X coordinate of the point, in pixels.</param>  
            /// <param name="pixelY">Y coordinates of the point, in pixels.</param>  
            /// <param name="levelOfDetail">Level of detail, from 1 (lowest detail)  
            /// to 23 (highest detail).</param>  
            /// <param name="latitude">Output parameter receiving the latitude in degrees.</param>  
            /// <param name="longitude">Output parameter receiving the longitude in degrees.</param>  
            PixelXYToLatLong(pixelX, pixelY, levelOfDetail, notify) {
                var mapSize = this.MapSize(levelOfDetail);
                var x = (this.Clip(pixelX, 0, mapSize - 1) / mapSize) - 0.5;
                var y = 0.5 - (this.Clip(pixelY, 0, mapSize - 1) / mapSize);

                var latitude = 90 - 360 * Math.atan(Math.exp(-y * 2 * Math.PI)) / Math.PI;
                var longitude = 360 * x;
                notify(latitude, longitude);
            }

            /// <summary>  
            /// Converts pixel XY coordinates into tile XY coordinates of the tile containing  
            /// the specified pixel.  
            /// </summary>  
            /// <param name="pixelX">Pixel X coordinate.</param>  
            /// <param name="pixelY">Pixel Y coordinate.</param>  
            /// <param name="tileX">Output parameter receiving the tile X coordinate.</param>  
            /// <param name="tileY">Output parameter receiving the tile Y coordinate.</param>  
            PixelXYToTileXY(pixelX, pixelY, tileX, tileY) {
                tileX = pixelX / 256;
                tileY = pixelY / 256;
            }

            /// <summary>  
            /// Converts tile XY coordinates into pixel XY coordinates of the upper-left pixel  
            /// of the specified tile.  
            /// </summary>  
            /// <param name="tileX">Tile X coordinate.</param>  
            /// <param name="tileY">Tile Y coordinate.</param>  
            /// <param name="pixelX">Output parameter receiving the pixel X coordinate.</param>  
            /// <param name="pixelY">Output parameter receiving the pixel Y coordinate.</param>  
            TileXYToPixelXY(tileX, tileY,notify) {
                var pixelX = tileX * 256;
                var pixelY = tileY * 256;
                notify(pixelX, pixelY);
            }

            /// <summary>  
            /// Converts tile XY coordinates into a QuadKey at a specified level of detail.  
            /// </summary>  
            /// <param name="tileX">Tile X coordinate.</param>  
            /// <param name="tileY">Tile Y coordinate.</param>  
            /// <param name="levelOfDetail">Level of detail, from 1 (lowest detail)  
            /// to 23 (highest detail).</param>  
            /// <returns>A string containing the QuadKey.</returns>  
            TileXYToQuadKey(tileX, tileY, levelOfDetail) {
                var quadKey;
                for (var i = levelOfDetail; i > 0; i--) {
                    var digit = '0';
                    var mask = 1 << (i - 1);
                    if ((tileX & mask) != 0) {
                        digit++;
                    }
                    if ((tileY & mask) != 0) {
                        digit++;
                        digit++;
                    }
                    quadKey.Append(digit);
                }
                return quadKey.ToString();
            }

            /// <summary>  
            /// Converts a QuadKey into tile XY coordinates.  
            /// </summary>  
            /// <param name="quadKey">QuadKey of the tile.</param>  
            /// <param name="tileX">Output parameter receiving the tile X coordinate.</param>  
            /// <param name="tileY">Output parameter receiving the tile Y coordinate.</param>  
            /// <param name="levelOfDetail">Output parameter receiving the level of detail.</param>
            //convert the lat/lng to PixelXY after that convert PixelXY to TileXY and after that from TileXY to QuadKey and vice versa
            QuadKeyToTileXY(quadKey, notify) { //tileX, tileY, levelOfDetail) {
                console.log(quadKey);
                let tileObj = {
                    tileX: 0,
                    tileY: 0,
                    levelOfDetail: quadKey.length
                };
                for (var i = tileObj.levelOfDetail; i > 0; i--) {
                    var mask = 1 << (i - 1);
                    switch (quadKey[tileObj.levelOfDetail - i]) {
                        case '0':
                            break;

                        case '1':
                            tileObj.tileX |= mask;
                            break;

                        case '2':
                            tileObj.tileY |= mask;
                            break;

                        case '3':
                            tileObj.tileX |= mask;
                            tileObj.tileY |= mask;
                            break;

                        default:
                            throw new ArgumentException("Invalid QuadKey digit sequence.");
                    }
                }
                notify(tileObj);
            }
        }
        return new Coordinates();
    });