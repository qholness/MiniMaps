var stage, circle, rect, stations, laststation, stationgraphics;
var lat, lon, station;
var rectsize = 10;
stations = [];
// 




function init() {
    stage = new createjs.Stage("demoCanvas");


    // Set circle
    circle = new createjs.Shape();
    circle.graphics.beginFill("DeepSkyBlue")
        .drawCircle(0, 0, 5);
    circle.x = 100;
    circle.y = 100;


    // Set stations
    {% for index, row in data.iterrows() %}
        lat = {{ row['POINT_X'] }};
        lon = {{ row['POINT_Y'] }};
        station = new createjs.Shape();
        stationgraphics = station.graphics;
        stationgraphics.beginFill("Red")
            .drawRect(0, 0, rectsize, rectsize);
        stationgraphics.moveTo(lat, lon);
        station.x = lat;
        station.y = lon;
        if (laststation) {
            stationgraphics.setStrokeStyle(3);
            stationgraphics.beginStroke('black');
            stationgraphics.lineTo(laststation.x, laststation.y);
            stationgraphics.endStroke();
        }
        stage.addChild(station);
        stations.push(station);
        laststation = station;
    {% endfor %}



    stage.addChild(circle);


    // Event ticker
    createjs.Ticker.addEventListener("tick", tick);


    // Set ticker
    createjs.Ticker.setFPS(60);


    // Keyboard inputs
    document.addEventListener('keydown', function(event) {
        if(event.keyCode == 37) {
            // Left
            circle.x = circle.x - 5;
        }
        if(event.keyCode == 39) {
            // Left
            circle.x = circle.x + 5;
        }
        if(event.keyCode == 38) {
            // Up
            circle.y = circle.y - 5;
        }
        if(event.keyCode == 40) {
            // Down
            circle.y = circle.y + 5;
        }
    });
}

// Pause
function pause(){
    createjs.Ticker.setPaused(true);
}

// 
function within(x, y, distance=5) {
    if (Math.abs(x - y) < distance ) {
        return true
    }
    return false;
}

// s
function findslope(x1,x2,y1,y2){
    return (x2-x1)/(y2-y1);
}


function tick(event) {

    stage.update(event); // important!!
    
    // Remove nodes
    /*for (var i=0; i < stations.length; i++) {
        station = stations[i];
        if (within(xpos, station.x) && within(ypos, station.y)) {
            stations.splice(i, 1, station);
            stage.removeChild(stations[i]);
            console.log("Ding");
        }
    }*/
}