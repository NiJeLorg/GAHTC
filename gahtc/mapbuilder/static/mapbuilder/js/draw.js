// global variables
let canvasF;

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

function mapbuilderShapeEventHandlers() {
  // mapbuilder toolbar event handlers
  $("#freedraw")
    .click(function () {
      canvasF.isDrawingMode = true;
      canvasF.freeDrawingBrush.width = 6;
      canvasF.on("mouse:up", function () {
        canvasF.isDrawingMode = false;
      });
    });

  $("#rect").click(function () {
    var rect = new fabric.Rect({
      left: 100,
      top: 100,
      fill: "rgba(233,116,81,0.5)",
      width: 100,
      height: 100,
      hasBorder: true,
      strokeWidth: 3,
      stroke: "#000"
    });
    canvasF
      .add(rect)
      .setActiveObject(rect);
  });

  $("#circle").click(function () {
    var circle = new fabric.Circle({
      radius: 50,
      fill: "rgba(233,116,81,0.5)",
      top: 100,
      left: 100,
      strokeWidth: 3,
      stroke: "black"
    });
    canvasF
      .add(circle)
      .setActiveObject(circle);
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
    var line = new fabric.Line([
      50, 100, 200, 200
    ], {
      left: 170,
      top: 150,
      stroke: "black",
      strokeWidth: 8,
      originX: "center",
      originY: "center",
      hasControls: true,
      hasBorders: false
    });
    canvasF
      .add(line)
      .setActiveObject(line);
  });

  $("#poly").click(function () {
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

  $("select").click(function () {
    canvasF.selection = true;
  });

  $("#arrow").click(function () {
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
    console.log("object");
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
  let fillColor,
    strokeColor,
    strokeWidth,
    fontColor,
    fontSize,
    fontFamily;

  $("#fillColor").on("click", () => {
    $("#fillColorPicker").spectrum("toggle");
    return false;
  });

  $("#strokeColor").on("click", () => {
    $("#strokeColorPicker").spectrum("toggle");
    return false;
  });

  $("#fontColor").on("click", () => {
    $("#fontColorPicker").spectrum("toggle");
    return false;
  });

  $("#fillColorPicker").spectrum({
    color: "#f00",
    change: color => {
      fillColor = color.toHexString();
      canvasF
        .getActiveObject()
        .set("fill", fillColor);
      canvasF.renderAll();
    }
  });

  $("#strokeColorPicker").spectrum({
    color: "#f00",
    change: color => {
      strokeColor = color.toHexString();
      canvasF
        .getActiveObject()
        .set({
          strokeWidth: strokeWidth || 1,
          stroke: strokeColor
        });
      canvasF.renderAll();
    }
  });

  $("#fontColorPicker").spectrum({
    color: "#f00",
    change: color => {
      fontColor = color.toHexString();
      canvasF
        .getActiveObject()
        .set({fill: fontColor});
      canvasF.renderAll();
    }
  });
}

initializeFabric();
mapbuilderShapeEventHandlers();
mapbuilderShapeFormattingEventHandlers();
mapbuilderFontFormattingEventHandlers();
initializeSpectrum();

$(document).ready(function () {
  $(document)
    .keyup(function (e) {
      if (e.keyCode == 8) {
        canvasF.remove(canvasF.getActiveObject());
      }
    })
})