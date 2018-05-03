
$('#rect').click(function(){
    var rect = new fabric.Rect({
    left: 100,
    top: 100,
    fill: 'blue',
    width: 100,
    height: 100,
    opacity: 0.5
    });
canvasF.add(rect).setActiveObject(rect);
})


$('#freedraw').click(function(){
    canvasF.isDrawingMode = true;
    canvasF.freeDrawingBrush.width = 6;
    canvasF.on('mouse:up', function () {
        canvasF.isDrawingMode = false;
    });
})
$('#line').click(function(){
    var line = new fabric.Line([50, 100, 200, 200], {
    left: 170,
    top: 150,
    stroke: 'blue',
    strokeWidth: 5,
    originX: 'center',
    originY: 'center',
    hasControls: true,
    hasBorders: false,
    });
    canvasF.add(line).setActiveObject(line)
})

$('#poly').click(function(){
    var startPoint = new fabric.Point(0, 0);
    var polygonPoints = [];
    var lines = [];
    var isDrawing = false;

    document.getElementById("poly").onclick = function () {
        if (isDrawing) {
            finalize();    
        }
        else {
          isDrawing = true;
        }
      };
    fabric.util.addListener(window, "dblclick", function () { 
    if (isDrawing) {
        finalize();    
    }
    });
    fabric.util.addListener(window, "keyup", function (evt) { 
        if (evt.which === 13 && isDrawing) {
            finalize();    
        }
      });
    canvasF.on('mouse:down', function (evt) {
        if (isDrawing) {
            var _mouse = this.getPointer(evt.e);    
            var _x = _mouse.x;
            var _y = _mouse.y;
            var line = new fabric.Line([_x, _y, _x, _y], {
            strokeWidth: 1,
            selectable: false,
            stroke: 'red'
            });
            polygonPoints.push(new fabric.Point(_x, _y));
            lines.push(line);
            
            this.add(line);
            this.selection = false;
        }
      });
      canvasF.on('mouse:move', function (evt) {
        if (lines.length && isDrawing) {  
            var _mouse = this.getPointer(evt.e);    
            lines[lines.length-1].set({
            x2: _mouse.x,
            y2: _mouse.y
          }).setCoords();
          this.renderAll();
        }
        }); 
        function finalize () {
            isDrawing = false;
    
        lines.forEach(function (line) {
            line.remove();
        });
    
      canvasF.add(makePolygon()).renderAll();
      canvasF.selection = true;
      lines.length = 0;
      polygonPoints.length = 0;
    }
    function makePolygon () {

        var left = fabric.util.array.min(polygonPoints, "x");
        var top = fabric.util.array.min(polygonPoints, "y");
      
        polygonPoints.push(new fabric.Point(polygonPoints[0].x, polygonPoints[0].y));
      
        return new fabric.Polygon(polygonPoints.slice(), {
          left: left,
          top: top,
          fill: 'rgba(255,0,0,.5)',
          stroke: 'black'
        });
      }
});

$('#circle').click(function(){
    var circle = new fabric.Circle({ 
        radius: 50, 
        fill: 'blue',
        top: 100, 
        left: 100,
        opacity:0.5
    });
    canvasF.add(circle).setActiveObject(circle);
})

$('#pin').click(function(){
    fabric.Image.fromURL('../../static/mapbuilder/css/images/marker-icon.png', function(oImg) {
        oImg.scale(0.2).set('flipX', true);
        canvasF.add(oImg);
    });
})

$('#text').click(function(){
    var text = new fabric.IText('Insert Text', {
        left: 150,
        top: 50,
        fontWeight: 'normal',
        fontFamily: 'Arial',
        fontSize: 20
    });
    canvasF.add(text).setActiveObject(text);
    
})

$('#image').click(function(){
    $('#file-image').trigger('click')
});

$('#file-image').change(function(e){

    var fileType = e.target.files[0].type;
    var url = URL.createObjectURL(e.target.files[0]);

    if (fileType === 'image/png') { //check if png
        fabric.Image.fromURL(url, function(img) {
            img.set({
                width: 180,
                height: 180
            });
            canvasF.add(img);
        });
    } else if (fileType === 'image/svg+xml') { //check if svg
        fabric.loadSVGFromURL(url, function(objects, options) {
            var svg = fabric.util.groupSVGElements(objects, options);
            svg.scaleToWidth(180);
            svg.scaleToHeight(180);
            canvasF.add(svg);
        });
    }
});

$('select').click(function(){
    canvasF.selection = true;
    console.log('hey you', canvasF.selection)
})


$('#f-bold').click(function(e){
    canvasF.getActiveObject().set('fontWeight', 'bold');
    canvasF.renderAll();
})
$('#f-italic').click(function(e){
    canvasF.getActiveObject().set('fontWeight', 'italic');
    canvasF.renderAll();
})

$('#underline').click(function(e){
    canvasF.getActiveObject().setTextDecoration('underline');
    canvasF.renderAll();
})


$('#align-left').click(function(e){
    canvasF.getActiveObject().set('textAlign', 'left');
    canvasF.renderAll();
})
$('#align-right').click(function(e){
    canvasF.getActiveObject().set('textAlign', 'right');
    canvasF.renderAll();
})
$('#align-center').click(function(e){
    canvasF.getActiveObject().set('textAlign', 'center');
    canvasF.renderAll();
})
$('#justify').click(function(e){
    canvasF.getActiveObject().set('textAlign', 'justify');
    canvasF.renderAll();
})
