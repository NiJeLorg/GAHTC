// global variables
var canvasF;
const layerId = localStorage.getItem('layerId');
const zoom = localStorage.getItem('zoom');
const mapBound = JSON.parse(localStorage.getItem('bounds'));
const southWest = [
        mapBound._southWest.lat, mapBound._southWest.lng
    ],
    northEast = [
        mapBound._northEast.lat, mapBound._northEast.lng
    ],
    mapBounds = [southWest, northEast];
var imageQuality = 'medium';
// initialize the map
var map, isDown;

function initializeFabric() {
    canvasF = new fabric.Canvas("c");
    canvasF.setHeight($("#map-canvas").height());
    canvasF.setWidth($("#map-canvas").width());
    canvasF.selection = false;

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
    var public_map = document.getElementById('public-check').checked ?  "True": 'False';
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
        },
        error: function (e) {
            console.log(e, "ERROR");
        }
    });
}



function changeObjectSelection(value) {
    canvasF.forEachObject(function (obj) {
        obj.selectable = value;
    });
    canvasF.renderAll();
}

function removeEvents() {
    canvasF.isDrawingMode = false;
    canvasF.selection = true;
    canvasF.off('mouse:down');
    canvasF.off('mouse:up');
    canvasF.off('mouse:move');
}

function mapbuilderShapeEventHandlers() {
    // mapbuilder toolbar event handlers
    $("#freedraw")
        .click(function () {
            removeEvents();
            changeObjectSelection(false);
            canvasF.isDrawingMode = true;
            canvasF.freeDrawingBrush.width = 6;
            canvasF.on("mouse:up", function () {
                canvasF.isDrawingMode = false;
            });
        });

    $("#rect").click(function () {

        removeEvents();
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
                strokeWidth: 3,
                selectable: true,
                fill: "rgba(233,116,81,0.5)",
                stroke: 'black',
                transparentCorners: false
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
            removeEvents();
        });
    });

    $("#circle").click(function () {
        var circle, isDown, origX, origY;
        removeEvents();
        changeObjectSelection(true);
        canvasF.on('mouse:down', function (o) {
            isDown = true;
            var pointer = canvasF.getPointer(o.e);
            origX = pointer.x;
            origY = pointer.y;
            circle = new fabric.Circle({
                left: pointer.x,
                top: pointer.y,
                radius: 1,
                strokeWidth: 3,
                fill: "rgba(233,116,81,0.5)",
                stroke: 'black',
                selectable: true,
                originX: 'center',
                originY: 'center'
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
            removeEvents();
        });


    });

    $("#text").click(function () {
        var text = new fabric.IText("Insert Text", {
            left: 150,
            top: 50,
            fontWeight: "normal",
            fontFamily: "Source Sans Pro",
            fontSize: 20
        });
        canvasF
            .add(text)
            .setActiveObject(text);
    });

    $("#line").click(function () {
        removeEvents();
        changeObjectSelection(false);
        canvasF.on('mouse:down', function (o) {
            isDown = true;
            var pointer = canvasF.getPointer(o.e);
            var points = [pointer.x, pointer.y, pointer.x, pointer.y];
            line = new fabric.Line(points, {
                strokeWidth: 8,
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
            removeEvents();
        });
    });

    $("#poly").click(function () {
        removeEvents();
        changeObjectSelection(false);
        var startPoint = new fabric.Point(0, 0);
        var polygonPoints = [];
        var lines = [];
        var isDrawing = false;

        document
            .getElementById("poly")
            .onclick = function () {
            if (isDrawing) {
                finalize();
            } else {
                isDrawing = true;
            }
        };
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
        canvasF.on("mouse:down", function (evt) {
            if (isDrawing) {
                var _mouse = this.getPointer(evt.e);
                var _x = _mouse.x;
                var _y = _mouse.y;
                var line = new fabric.Line([
                    _x, _y, _x, _y
                ], {
                    strokeWidth: 5,
                    stroke: "black",
                    selectable: false,
                    stroke: "red"
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

        function finalize() {
            isDrawing = false;

            lines.forEach(function (line) {
                line.remove();
            });

            canvasF
                .add(makePolygon())
                .renderAll();
            canvasF.selection = true;
            lines.length = 0;
            polygonPoints.length = 0;
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

            polygonPoints.push(new fabric.Point(polygonPoints[0].x, polygonPoints[0].y));

            return new fabric.Polygon(polygonPoints.slice(), {
                left: left,
                top: top,
                fill: "rgba(233,116,81,0.5)",
                stroke: "black",
                strokeWidth: 3
            });
        }
    });

    $("#pin").click(function () {
        removeEvents();
        changeObjectSelection(false);
        fabric
            .Image
            .fromURL("../../static/mapbuilder/css/images/marker-icon.png", function (oImg) {
                oImg
                    .scale(0.2)
                    .set("flipX", true);
                canvasF.add(oImg);
            });
    });

    $("#image").click(function () {
        removeEvents();
        changeObjectSelection(false);
        $("#file-image").trigger("click");
    });

    $("#file-image").change(function (e) {

        var file = e.target.files[0];
        var reader = new FileReader();
        reader.onload = function (f) {
            var data = f.target.result;
            fabric
                .Image
                .fromURL(data, function (img) {
                    var oImg = img.set({width: 125, height: 170});
                    canvasF
                        .add(oImg)
                        .renderAll();
                    var a = canvasF.setActiveObject(oImg);
                });
        };
        reader.readAsDataURL(file);
    });

    $("#select").click(function () {
        removeEvents();
        changeObjectSelection(true);
        canvasF.selection = true;
    });

    $("#arrow").click(function () {
        removeEvents();
        changeObjectSelection(false);
        event.preventDefault();
        var triangle = new fabric.Triangle({
            width: 10,
            height: 15,
            fill: "red",
            left: 235,
            top: 65,
            angle: 90
        });

        var line = new fabric.Line([
            50, 100, 200, 100
        ], {
            left: 75,
            top: 70,
            stroke: "red"
        });

        var objs = [line, triangle];

        var alltogetherObj = new fabric.Group(objs);
        canvasF.add(alltogetherObj);
    });
}

function mapbuilderFontFormattingEventHandlers() {
    // font formating
    $("#f-bold")
        .click(function (e) {
            canvasF
                .getActiveObject()
                .set("fontWeight", "bold");
            canvasF.renderAll();
        });
    $("#f-italic").click(function (e) {
        canvasF
            .getActiveObject()
            .set("fontWeight", "italic");
        canvasF.renderAll();
    });

    $("#underline").click(function (e) {
        canvasF
            .getActiveObject()
            .setTextDecoration("underline");
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
        canvasF
            .getActiveObject()
            .set("fontSize", fontSize);
        canvasF.renderAll();
    });

    $(".delete-shape-icon").on("click", function () {
        canvasF.remove(canvasF.getActiveObject());
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
                    strokeWidth: strokeWidth || 3,
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
        'background-size': '100% 100%'
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
        createImage(canvasF);
    });
    $('#close-icon').click(function (e) {
        $('.publish-modal').css("display", "none");
    });
    $('#download').click(function (e) {
        if (imageQuality === 'small') {
            width = 854;
            height = 480;
        } else if (imageQuality === 'medium') {
            width = 1280;
            height = 720;
        } else if (imageQuality === 'large') {
            width = 1920;
            height = 1080;
        }
        if (document.getElementById('pdf').checked) {
            downloadPdf(canvasF, width, height);
        } else {
            downloadImage(width, height);
        }
        if (document.getElementById('public-check').checked) {
            saveMapDetails();

        }
    });
    $('#save').click(function () {
        saveMapDetails();
    });
    $('#public-check').change(function(){
        saveMapDetails()
    });

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
    link.click()
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
    if (currentMapImage) {
        var img = new Image;
        img.src = currentMapImage;
        img.onload = function () {
            $('#lmap').remove();
            $('.canvas-container').css('display', 'block');
            const imageBackgroundUrl = "" + currentMapImage + "";
            console.log("Loaded");


            if (currentMapObjects) {
                console.log(JSON.parse(currentMapObjects.replace(/&quot;/g, '"')), "objects");
                canvasF.loadFromJSON(JSON.parse(currentMapObjects.replace(/&quot;/g, '"')), function () {
                     canvasF.setBackgroundImage(imageBackgroundUrl, canvasF.renderAll.bind(canvasF), {
                        scaleX: canvasF.width / img.width,
                        scaleY: canvasF.height / img.height
                    });
                            // canvasF.renderAll();
                }, function (o, object) {

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
    if (mapId === "") {
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
        .keyup(function (e) {
            if (e.keyCode == 8) {
                canvasF.remove(canvasF.getActiveObject());
            }
        })
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



