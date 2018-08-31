// global variables
var canvasF;
const layerId = localStorage.getItem('layerId');
const zoom = localStorage.getItem('zoom');
const mapBound = JSON.parse(localStorage.getItem('bounds'));
var mapBounds;
if(mapBound) {
    const southWest = [
        mapBound._southWest.lat, mapBound._southWest.lng
    ],
    northEast = [
        mapBound._northEast.lat, mapBound._northEast.lng
    ];
    mapBounds = [southWest, northEast];
}

var imageQuality = 'medium';
// initialize the map
var map, isDown, lastDrawnID;

function initializeFabric() {
    canvasF = new fabric.Canvas("c");
    canvasF.setHeight($("#map-canvas").height());
    canvasF.setWidth($("#map-canvas").width());
    // canvasF.selection = false;

    fabric
        .Object
        .prototype
        .set({transparentCorners: false, borderColor: "#3D95F6", cornerColor: "#3D95F6"});
}


function intializeMap() {
    $.LoadingOverlay("show", {
        image: "",
        fontawesome: "fa fa-cog fa-spin",
        text: "Generating your map canvas"
    });
    map = L.map('lmap', {
        center: [
            localStorage.getItem('lat'),
            localStorage.getItem('long')
        ],
        minZoom: zoom,
        maxZoom: zoom,
        zoomControl: false,
        downloadable: true,
        printable: true,
        maxBounds: mapBounds,
        preferCanvas: true
    }).on('load', function () {
        const tileLayer = L
            .tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributor' +
                's, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imager' +
                'y © <a href="http://mapbox.com">Mapbox</a>',
                id: layerId,
                accessToken: window.MAPBOX_ACCESS_TOKEN
            })
            .addTo(map);
        tileLayer.on('load', function () {

            leafletImage(map, function (err, canvas) {
                var url = canvas.toDataURL('image/png');
                const img = new Image;
                var dimensions = map.getSize();
                img.width = dimensions.x;
                img.height = dimensions.y;
                img.src = url;
                img.onload = function () {
                    $('#lmap').remove();
                    $('.canvas-container').css('display', 'block');
                    const imageBackgroundUrl = "" + url + "";
                    canvasF.setBackgroundImage(imageBackgroundUrl, canvasF.renderAll.bind(canvasF));
                };
                $.LoadingOverlay("hide");
            })

        })
    });

    map.fitBounds(mapBounds);

}

function saveMapDetails() {
    var map_id = mapId || $("#projectid").text();
    var map_name = $("#projectname").text();
    var csrftoken = Cookies.get('csrftoken');
    var map_image = canvasF.toDataURL('image/png').replace("data:image/png;base64,", "");
    var base_map_image = canvasF.backgroundImage.toDataURL('image/png').replace("data:image/png;base64,", "");
    //var map_image = canvasF.toDataURL('image/png');
    //var base_map_image = canvasF.backgroundImage.toDataURL('image/png');
    var public_map = document.getElementById('public-check').checked && $('#publish').data('clicked')?  "True": 'False';
    var canvasCopy = _.cloneDeep(canvasF);
    canvasCopy.backgroundImage = null;
    var map_data = JSON.stringify(canvasCopy);

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        type: "POST",
        url: "/mapbuilder/map-export/",
        data: {
            map_id: map_id,
            map_name: map_name,
            public_map: public_map,
            map_image: map_image,
            map_data: map_data,
            base_map_image: base_map_image
        },
        success: function (data) {
            $("#projectid").text(data.map_id);
            $('.publish-modal').css("display", "none");
            $.LoadingOverlay("hide");
            $('.download-save-modal').css("display", "block");
        },
        error: function (e) {
            console.log(e, "ERROR");
        }
    });
}

function changeCursor(cursorType) {
    canvasF.defaultCursor = cursorType;
}

function changeObjectSelection(value) {
    canvasF.forEachObject(function (obj) {
        obj.selectable = value;
        if (value) {
            obj.hoverCursor = 'move';
        } else {
            obj.hoverCursor = 'crosshair';
            $('#select').removeClass('active');
        }
    });
    canvasF.renderAll();
}

function removeEvents() {
    canvasF.deactivateAll().renderAll();
    $('.toolbar-icon').removeClass('active');
    canvasF.isDrawingMode = false;
    canvasF.selection = true;
    canvasF.off('mouse:down');
    canvasF.off('mouse:up');
    canvasF.off('mouse:move');
    changeCursor('auto');
}


function mapbuilderShapeEventHandlers() {
    // mapbuilder toolbar event handlers
    $("#freedraw")
        .click(function () {
            // check to see if button is active, and if so, deactivate and remove events
            if ($(this).hasClass('active')) {
                removeEvents();
                changeObjectSelection(true);
            } else {
                removeEvents();
                $(this).addClass('active');
                changeCursor('crosshair');
                changeObjectSelection(false);
                canvasF.isDrawingMode = true;
                canvasF.freeDrawingBrush.width = 4;
                canvasF.on("mouse:up", function () {
                    // lastDrawnID = this._objects.length - 1;
                    // canvasF.setActiveObject(canvasF.item(lastDrawnID));
                });
            }
            
        });

    $("#rect").click(function () {
        if ($(this).hasClass('active')) {
            removeEvents();
            changeObjectSelection(true);
        } else {
            removeEvents();
            $(this).addClass('active');
            changeCursor('crosshair');
            changeObjectSelection(false);         

            canvasF.on('mouse:down', function (o) {
                isDown = true;
                var pointer = canvasF.getPointer(o.e);
                origX = pointer.x;
                origY = pointer.y;
                var pointer = canvasF.getPointer(o.e);
                rect = new fabric.Rect({
                    left: origX,
                    top: origY,
                    originX: 'left',
                    originY: 'top',
                    width: pointer.x - origX,
                    height: pointer.y - origY,
                    angle: 0,
                    strokeWidth: 4,
                    selectable: true,
                    fill: "rgba(233,116,81,1)",
                    stroke: 'black',
                    transparentCorners: false,
                    opacity: 1
                });
                canvasF.add(rect);
            });

            canvasF.on('mouse:move', function (o) {
                if (!isDown) return;
                var pointer = canvasF.getPointer(o.e);

                if (origX > pointer.x) {
                    rect.set({
                        left: Math.abs(pointer.x)
                    });
                }
                if (origY > pointer.y) {
                    rect.set({
                        top: Math.abs(pointer.y)
                    });
                }

                rect.set({
                    width: Math.abs(origX - pointer.x)
                });
                rect.set({
                    height: Math.abs(origY - pointer.y)
                });
                
                canvasF.renderAll();
            });

            canvasF.on('mouse:up', function (o) {
                isDown = false;
                rect.setCoords();
                changeObjectSelection(false);
                canvasF.deactivateAll().renderAll();
            });

        }

    });

    $("#circle").click(function () {
        var circle, isDown, origX, origY;

        if ($(this).hasClass('active')) {
            removeEvents();
            changeObjectSelection(true);
        } else {
            removeEvents();
            $(this).addClass('active');
            changeCursor('crosshair');
            changeObjectSelection(false);

            canvasF.on('mouse:down', function (o) {
                isDown = true;
                var pointer = canvasF.getPointer(o.e);
                origX = pointer.x;
                origY = pointer.y;
                circle = new fabric.Circle({
                    left: pointer.x,
                    top: pointer.y,
                    radius: 1,
                    strokeWidth: 4,
                    fill: "rgba(233,116,81,1)",
                    stroke: 'black',
                    selectable: true,
                    originX: 'center',
                    originY: 'center',
                    opacity: 1
                });
                canvasF.add(circle);
            });
    
            canvasF.on('mouse:move', function (o) {
                if (!isDown) return;
                var pointer = canvasF.getPointer(o.e);
                circle.set({
                    radius: Math.abs(origX - pointer.x)
                });
                canvasF.renderAll();
            });
    
            canvasF.on('mouse:up', function (o) {
                isDown = false;
                circle.setCoords();
                changeObjectSelection(false);
                canvasF.deactivateAll().renderAll();
            });

        }

    });

    $("#text").click(function () {
        if ($(this).hasClass('active')) {
            removeEvents();
            changeObjectSelection(true);
        } else {
            removeEvents();
            $(this).addClass('active');
            changeCursor('text');
            changeObjectSelection(false);

            canvasF.on('mouse:down', function (o) {
                var pointer = canvasF.getPointer(o.e);
                var text = new fabric.IText("Insert Text", {
                    left: pointer.x,
                    top: pointer.y,
                    fontWeight: "normal",
                    fontFamily: "Source Sans Pro",
                    fontSize: 16
                });
                removeEvents();
                changeObjectSelection(true);
                canvasF
                    .add(text)
                    .setActiveObject(text);

            });



        }

    });

    $("#line").click(function () {

        if ($(this).hasClass('active')) {
            removeEvents();
            changeObjectSelection(true);
        } else {
            removeEvents();
            $(this).addClass('active');
            changeCursor('crosshair');

            changeObjectSelection(false);

            canvasF.on('mouse:down', function (o) {
                isDown = true;
                var pointer = canvasF.getPointer(o.e);
                var points = [pointer.x, pointer.y, pointer.x, pointer.y];
                line = new fabric.Line(points, {
                    strokeWidth: 4,
                    stroke: 'black',
                    originX: 'center',
                    originY: 'center',
                    selectable: true
                });
                canvasF.add(line);
            });
            canvasF.on('mouse:move', function (o) {
                if (!isDown) return;
                var pointer = canvasF.getPointer(o.e);
                line.set({
                    x2: pointer.x,
                    y2: pointer.y
                });
                canvasF.renderAll();
            });
    
            canvasF.on('mouse:up', function (o) {
                isDown = false;
                line.setCoords();
                changeObjectSelection(false);
                canvasF.deactivateAll().renderAll();    
            });
        
        }

    });

    $("#poly").click(function () {
        if ($(this).hasClass('active')) {
            removeEvents();
            changeObjectSelection(true);
        } else {
            changeObjectSelection(false);
            var polygonPoints = [];
            var lines = [];
            var isDrawing = false;

            fabric
                .util
                .addListener(window, "dblclick", function () {
                    if (isDrawing) {
                        finalize();
                    }
                });
            fabric
                .util
                .addListener(window, "keyup", function (evt) {
                    if (evt.which === 13 && isDrawing) {
                        finalize();
                    }
                });

            function setUpPolyDraw() {
                removeEvents();
                $("#poly").addClass('active');
                changeCursor('crosshair');
                changeObjectSelection(false);
                polygonPoints = [];
                lines = [];
                isDrawing = false;

                if (isDrawing) {
                    finalize();
                } else {
                    isDrawing = true;
                }
    

                canvasF.on("mouse:down", function (evt) {
                    if (isDrawing) {
                        var _mouse = this.getPointer(evt.e);
                        var _x = _mouse.x;
                        var _y = _mouse.y;
                        var line = new fabric.Line([
                            _x, _y, _x, _y
                        ], {
                            strokeWidth: 4,
                            stroke: "black",
                            selectable: false,
                        });
                        polygonPoints.push(new fabric.Point(_x, _y));
                        lines.push(line);
    
                        this.add(line);
                        this.selection = false;
                    }
                });
                canvasF.on("mouse:move", function (evt) {
                    if (lines.length && isDrawing) {
                        var _mouse = this.getPointer(evt.e);
                        lines[lines.length - 1]
                            .set({x2: _mouse.x, y2: _mouse.y})
                            .setCoords();
                        this.renderAll();
                    }
                });
            }

            function finalize() {
                isDrawing = false;

                lines.forEach(function (line) {
                    line.remove();
                });

                canvasF
                    .add(makePolygon())
                    .renderAll();
                canvasF.selection = true;
                setUpPolyDraw();
            }

            function makePolygon() {
                var left = fabric
                    .util
                    .array
                    .min(polygonPoints, "x");
                var top = fabric
                    .util
                    .array
                    .min(polygonPoints, "y");

                console.log(polygonPoints);
                polygonPoints.push(new fabric.Point(polygonPoints[0].x, polygonPoints[0].y));

                return new fabric.Polygon(polygonPoints.slice(), {
                    left: left,
                    top: top,
                    fill: "rgba(233,116,81,1)",
                    stroke: "black",
                    strokeWidth: 4,
                    opacity: 1
                });
            }

            setUpPolyDraw();

        }

    });

    $("#pin").click(function () {

        if ($(this).hasClass('active')) {
            removeEvents();
            changeObjectSelection(true);
        } else {
            removeEvents();
            $(this).addClass('active');
            changeCursor('crosshair');

            canvasF.on('mouse:down', function (o) {
                var pointer = canvasF.getPointer(o.e);
                var x = pointer.x - 17;
                var y = pointer.y - 40;
                fabric
                    .Image
                    .fromURL("../../static/mapbuilder/css/images/marker-icon.png", function (oImg) {
                        oImg
                            .scale(0.1)
                            .set("flipX", true)
                            .set({ left: x, top: y });
                            canvasF
                                .add(oImg);
                    });

            });

            canvasF.on('mouse:up', function (o) {
                changeObjectSelection(false);
                canvasF.deactivateAll().renderAll();
            });

        }

    });

    $("#image").click(function () {
        if ($(this).hasClass('active')) {
            removeEvents();
            changeObjectSelection(true);
        } else {
            removeEvents();
            $(this).addClass('active');

            changeObjectSelection(true);
            $("#file-image").trigger("click");
        }
    });

    $("#file-image").change(function (e) {

        var file = e.target.files[0];
        var reader = new FileReader();
        reader.onload = function (f) {
            var data = f.target.result;
            fabric
                .Image
                .fromURL(data, function (img) {
                    canvasF
                        .add(img)
                        .renderAll();
                    canvasF.setActiveObject(img);
                    removeEvents();
                });
        };
        reader.readAsDataURL(file);
    });

    $("#select").click(function () {
        if ($(this).hasClass('active')) {
            removeEvents();
            changeObjectSelection(true);
        } else {
            removeEvents();
            $(this).addClass('active');
            changeObjectSelection(true);
            canvasF.selection = true;
        }

    });

    $("#arrow").click(function () {
        if ($(this).hasClass('active')) {
            removeEvents();
            changeObjectSelection(true);
        } else {
            removeEvents();
            $(this).addClass('active');
            changeCursor('crosshair');
            changeObjectSelection(false);

            // event.preventDefault();
            // var triangle = new fabric.Triangle({
            //     width: 10,
            //     height: 15,
            //     fill: "rgba(233,116,81,1)",
            //     left: 235,
            //     top: 65,
            //     angle: 90
            // });
    
            // var line = new fabric.Line([
            //     50, 100, 200, 100
            // ], {
            //     left: 75,
            //     top: 70,
            //     stroke: "red"
            // });
    
            // var objs = [line, triangle];
    
            // var alltogetherObj = new fabric.Group(objs);
            // canvasF.add(alltogetherObj);

            function createArrowHead(line) {
                var headLength = 15,
              
                    x1 = line.x1,
                    y1 = line.y1,
                    x2 = line.x2,
                    y2 = line.y2,
              
                    dx = x2 - x1,
                    dy = y2 - y1,
              
                    angle = Math.atan2(dy, dx);
              
                angle *= 180 / Math.PI;
                angle += 90;
              
                var triangle = new fabric.Triangle({
                  angle: angle,
                  fill: 'black',
                  top: y2,
                  left: x2,
                  height: headLength,
                  width: headLength,
                  originX: 'center',
                  originY: 'center',
                  selectable: false
                });
              
                return triangle;
            }

            canvasF.on('mouse:down', function (o) {
                isDown = true;
                var pointer = canvasF.getPointer(o.e);
                var points = [pointer.x, pointer.y, pointer.x, pointer.y];
                line = new fabric.Line(points, {
                    strokeWidth: 4,
                    stroke: 'black',
                    originX: 'center',
                    originY: 'center',
                    selectable: true
                });

                //canvasF.add(line);

            });
            canvasF.on('mouse:move', function (o) {
                if (!isDown) return;
                var pointer = canvasF.getPointer(o.e);
                line.set({
                    x2: pointer.x,
                    y2: pointer.y
                });
                canvasF.renderAll();
            });
    
            canvasF.on('mouse:up', function (o) {
                isDown = false;
                line.setCoords();

                var triangle = createArrowHead(line);

                var objs = [line, triangle];
        
                var alltogetherObj = new fabric.Group(objs);
                canvasF.add(alltogetherObj);
                //canvasF.remove(line);

                
                changeObjectSelection(false);
                // lastDrawnID = this._objects.length - 1;
                // canvasF.setActiveObject(canvasF.item(lastDrawnID));
    
            });

        }

    });

    canvasF.on('selection:cleared', function (){
        disableToolbars();
    }); 

    canvasF.on('object:selected', function () {
        if (canvasF.getActiveObject().get('type')==="i-text"){
            $('.format-icons').css({'pointer-events': 'auto', 'background': '#fff'});
        } else {
            $('.edit-icons').css({'pointer-events': 'auto', 'background': '#fff'});
            $('#select').addClass('active');
        }
     });
     
}



function mapbuilderFontFormattingEventHandlers() {
    // font formating
    $("#f-bold")
        .click(function (e) {
            if (canvasF.getActiveObject().get("fontWeight") != 'bold') {
                canvasF
                    .getActiveObject()
                    .set("fontWeight", "bold");
            } else {
                canvasF
                    .getActiveObject()
                    .set("fontWeight", "normal");
            }
            canvasF.renderAll();
        });
    $("#f-italic").click(function (e) {
        if (canvasF.getActiveObject().get("fontStyle") != 'italic') {
            canvasF
                .getActiveObject()
                .set("fontStyle", "italic");
        } else {
            canvasF
                .getActiveObject()
                .set("fontStyle", "normal");
        }
        canvasF.renderAll();
    });

    $("#underline").click(function (e) {
        console.log(canvasF.getActiveObject());
        if (canvasF.getActiveObject().get("textDecoration") != 'underline') {
            canvasF
                .getActiveObject()
                .set("textDecoration", "underline");
        } else {
            canvasF
                .getActiveObject()
                .set("textDecoration", "none");
        }
        canvasF.renderAll();
    });
    $("#align-left").click(function (e) {
        canvasF
            .getActiveObject()
            .set("textAlign", "left");
        canvasF.renderAll();
    });
    $("#align-right").click(function (e) {
        canvasF
            .getActiveObject()
            .set("textAlign", "right");
        canvasF.renderAll();
    });
    $("#align-center").click(function (e) {
        canvasF
            .getActiveObject()
            .set("textAlign", "center");
        canvasF.renderAll();
    });
    $("#justify").click(function (e) {
        canvasF
            .getActiveObject()
            .set("textAlign", "justify");
        canvasF.renderAll();
    });
    $(".font-family-option").on("click", function () {
        fontFamily = $(this).text();
        canvasF
            .getActiveObject()
            .set("fontFamily", fontFamily);
        canvasF.renderAll();
    });
}

function mapbuilderShapeFormattingEventHandlers() {
    // mapbuilder dropdown menu event handlers
    $(".stroke-weight-option")
        .on("click", function () {
            strokeWidth = parseInt(/\d+/g.exec($(this).text())[0]);
            canvasF
                .getActiveObject()
                .set("strokeWidth", strokeWidth);
            canvasF.renderAll();
            strokeWidth = 1;
        });

    $(".font-size-option").on("click", function () {
        fontSize = parseInt(/\d+/g.exec($(this).text())[0]);
        console.log(fontSize);
        canvasF
            .getActiveObject()
            .set("fontSize", fontSize);
        canvasF.renderAll();
    });

    $(".delete-shape-icon").on("click", function () {
        canvasF.remove(canvasF.getActiveObject());
        disableToolbars();
    });

    $(".stroke-style-option").on("click", function () {
        var dashedStyle = $(this).attr("id");
        if (dashedStyle == "solid") {
            canvasF
                .getActiveObject()
                .set("strokeDashArray", [0, 0]);
        } else if (dashedStyle == "dashed") {
            canvasF
                .getActiveObject()
                .set("strokeDashArray", [10, 5]);
        } else if (dashedStyle == "dotted") {
            canvasF
                .getActiveObject()
                .set("strokeDashArray", [1, 10]);
            canvasF
                .getActiveObject()
                .set("strokeLineCap", "round");
        }
        canvasF.renderAll();
    });

    $('#opacity').click(function (e){
        $('.slider-container').css('display','block')
        var objectOpacity = canvasF.getActiveObject().opacity
        var input = document.getElementById('opacitySlider')
        input.value = objectOpacity * 100
        $(document).mouseup(function(e) {
            var container = $(".slider-container");
            if (!container.is(e.target) && container.has(e.target).length === 0) 
           {
               container.hide();
           }
        });
    })
    
    $('.opacity-slider').change(function (){
        var opacity = $(".opacity-slider").val();
        opacity = opacity / 100;
        canvasF.getActiveObject().setOpacity(opacity)
        canvasF.renderAll();
    });
}

function initializeSpectrum() {
    // event handlers spectrum
    var fillColor,
        strokeColor,
        strokeWidth,
        fontColor,
        fontSize,
        fontFamily;

    $("#fillColor").on("click", function () {
        $("#fillColorPicker").spectrum("toggle");
        return false;
    });

    $("#strokeColor").on("click", function () {
        $("#strokeColorPicker").spectrum("toggle");
        return false;
    })
    ;

    $("#fontColor").on("click", function () {
        $("#fontColorPicker"
        ).spectrum("toggle");
        return false;
    })
    ;

    $("#fillColorPicker").spectrum({
        color: "#f00",
        change: function (color) {
            fillColor = color.toHexString();
            canvasF
                .getActiveObject()
                .set("fill", fillColor);
            canvasF.renderAll();
        }
    })
    ;

    $("#strokeColorPicker").spectrum({
        color: "#f00",
        change: function (color) {
            strokeColor = color.toHexString();
            canvasF
                .getActiveObject()
                .set({
                    strokeWidth: strokeWidth || 4,
                    stroke: strokeColor
                });
            canvasF.renderAll();
        }
    })
    ;

    $("#fontColorPicker").spectrum({
        color: "#f00",
        change: function (color) {
            fontColor = color.toHexString();
            canvasF
                .getActiveObject()
                .set({fill: fontColor});
            canvasF.renderAll();
        }
    })
}

const createImage = function (canvasF) {
    const url = canvasF.toDataURL('image/png');
    const imageBackgroundUrl = "url(" + url + ")";
    const img = new Image;
    $('#images').css({
        'background': imageBackgroundUrl,
        'background-repeat': 'no-repeat',
        'background-size': '100% auto'
    })
    img.src = url;
    img.onload = function () {
        $('#loader').hide();
    }
}

function mapActionHandlers() {
    $('#close-button').click(function (e) {
        $('.modal').css("display", "none");
    });
    $('#modal-close-button').click(function (e) {
        $('.download-save-modal').css("display", "none");
    });
    $('#exit-modal').click(function (e) {
        $('.download-save-modal').css("display", "none");
    });
    $('.ok-button').click(function (e) {
        $('.modal').css("display", "none");
        var val = $("#project-title").val()
        $("#projectname").html(val);
    });
    $('#editIcon').click(function (e) {
        $('.modal').css("display", "block");
    });

    $('#publish').click(function (e) {
        $('.publish-modal').css("display", "flex");
        $(this).data('clicked', true);
        createImage(canvasF);
    });
    $('#close-icon').click(function (e) {
        $('.publish-modal').css("display", "none");
    });
    $('#download').click(function (e) {
        console.log("hello");
        // get the dimensions of #map-canvas and calculate the appropriate sizes for image quality
        var canvasWidth = $('#map-canvas').width();
        var canvasHeight = $('#map-canvas').height();
        if (imageQuality === 'small') {
            height = 480;
            width = (height / canvasHeight) * canvasWidth;
        } else if (imageQuality === 'medium') {
            height = 720;
            width = (height / canvasHeight) * canvasWidth;
        } else if (imageQuality === 'large') {
            height = 1080;
            width = (height / canvasHeight) * canvasWidth;
        }
        if (document.getElementById('pdf').checked) {
            downloadPdf(canvasF, width, height);
        } else {
            downloadImage(width, height);
        }
        if (document.getElementById('public-check').checked) {
            saveMapDetails();
        }
        $('.download-save-modal-content h3').html('Great! Your map has been downloaded.');
    })
    $('#save').click(function () {
        $.LoadingOverlay("show", {
            image: "",
            fontawesome: "fa fa-cog fa-spin",
            text: "Saving Map Details"
        });
        saveMapDetails();
        $('.download-save-modal-content h3').html('Great! Your map has been saved.');
    });

}

function disableToolbars(){
    //console.log(canvasF.getObjects().length);
    if (canvasF.getObjects().length === 0) {
        $('.edit-icons').css({'pointer-events': 'none', 'background': '#d2d2d2'});
        $('.toolbar-icon').removeClass('active');
    }
    if (canvasF.getObjects("i-text").length === 0) {
        $('.format-icons').css({'pointer-events': 'none', 'background': '#d2d2d2'});
    }
}

function dataURLtoBlob(dataurl) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], {type: mime});
}

function resizeImage(img, width, height) {
    var result = new Image();
    var canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    canvas.getContext('2d').drawImage(img, 0, 0, width, height);
    result.src = canvas.toDataURL();
    return result;
}

function downloadImage(width, height) {
    var link = document.createElement('a');
    var fabricImage = new Image();
    if (document.getElementById('png').checked) {
        fabricImage.src = canvasF.toDataURL('image/png');
        var resizedImage = resizeImage(fabricImage, width, height);
        var blob = dataURLtoBlob(resizedImage.src);
        var objectUrl = URL.createObjectURL(blob)
        link.href = objectUrl
        link.download = "mymap.png";
    } else {
        fabricImage.src = canvasF.toDataURL('image/jpeg');
        var resizedImage = resizeImage(fabricImage, width, height);
        var blob = dataURLtoBlob(resizedImage.src);
        var objectUrl = URL.createObjectURL(blob);
        link.href = objectUrl
        link.download = "mymap.jpg";
    }
    console.log(link);
    link.click();
}

function downloadPdf(canvasF, width, height) {
    // const url = canvasF.toDataURL("image/svg+xml", 1.0);
    var fabricImage = new Image();
    fabricImage.src = canvasF.toDataURL("image/svg+xml", 1.0);
    var pdf = new jsPDF();
    var resizedImage = resizeImage(fabricImage, width, height);
    // var blob = dataURLtoBlob(resizedImage.src);
    // var objectUrl = URL.createObjectURL(blob);
    pdf.addImage(resizedImage.src, 'PNG', 15, 30, 180, 160);
    pdf.save("mymap.pdf");

}

function updateCanvasWithExistingMap() {
    console.log(currentMapImage);
    if (currentMapImage == '/media/') {
        currentMapImage = preloadedMapImage; 
    }

    if (currentMapImage) {
        document.getElementById("project-title").value = currentMapName;
        $("#projectname").html(currentMapName);
        var img = new Image;
        img.src = currentMapImage;
        img.onload = function () {
            $('#lmap').remove();
            $('.canvas-container').css('display', 'block');
            const imageBackgroundUrl = "" + currentMapImage + "";


            if (currentMapObjects !== 'None') {
                console.log(JSON.parse(currentMapObjects.replace(/&quot;/g, '"')), "objects");
                canvasF.loadFromJSON(JSON.parse(currentMapObjects.replace(/&quot;/g, '"')), function () {
                     canvasF.setBackgroundImage(imageBackgroundUrl, canvasF.renderAll.bind(canvasF), {
                        originX: 'left',
                        originY: 'top'
                      });
                }, function (o, object) {
                        object.on('mousedown', function(e){
                           $('.edit-icons').css({'pointer-events': 'auto', 'background': '#fff'});
                        });
                });

            }else{
                canvasF.setBackgroundImage(imageBackgroundUrl, canvasF.renderAll.bind(canvasF), {
                    originX: 'left',
                    originY: 'top'
                });
            }
        }
        ;
        console.log("Set Exisitng Image as map");
    }
}

$(document).ready(function () {
    initializeFabric();
    
    // console.log(currentMapJson, currentMapImage);
    if (mapId === "" || mapId === "False"  || mapId === false) {
        intializeMap();

    } else {
        updateCanvasWithExistingMap();
    }

    mapbuilderShapeEventHandlers();
    mapbuilderShapeFormattingEventHandlers();
    mapbuilderFontFormattingEventHandlers();
    mapActionHandlers();
    initializeSpectrum();
    $(document)
        .keydown(function (e) {
            if ((e.keyCode == 8 || e.keyCode == 46) && canvasF.getActiveObject().get('type')!=="i-text") {
                e.preventDefault();
                canvasF.remove(canvasF.getActiveObject());
                disableToolbars();
            }
            if (e.keyCode == 13 && $(".modal").css('display').toLowerCase() == 'block') {
                $('.modal').css("display", "none");
                var val = $("#project-title").val()
                $("#projectname").html(val);
            }
        });
    
    // disable event handling
    $('.edit-icons,.format-icons ').css('pointer-events', 'none');

    $('#text').on('click', function () {
        $('.format-icons').css({'pointer-events': 'auto', 'background': '#fff'});
    });
    $('.draw-icons a')
        .not('#text')
        .on('click', function () {
            $('.edit-icons').css({'pointer-events': 'auto', 'background': '#fff'});
        });
    $('.button-switcher button').click(function () {
        $(this).siblings().removeClass('size-btn-active');
        $(this).addClass('size-btn-active');
        if (this.id === 'small') {
            imageQuality = 'small'
        } else if (this.id === 'medium') {
            imageQuality = 'medium'
        } else {
            imageQuality = 'large'
        }
    })
});



