var stage, // GLOBAL
    mainCircle, // GLOBAL
    station, // GLOBAL
    text,
    rectsize = 50 // GLOBAL
;


function init() {
    // Set stage
    nodes = []; // Reset GLOBAL nodes
    stage = new createjs.Stage("GameCanvas");

    // Set text
    text = new createjs.Text("Fill the station!", "20px Arial", "black");
    text.x = 100;
    text.y = 100;
    stage.addChild(text);
    
    // Set mainCircle
    mainCircle = new createjs.Shape();
    mainCircle.graphics.beginFill("DeepSkyBlue")
        .drawCircle(0, 0, 5);
    mainCircle.x = 100;
    mainCircle.y = Math.floor(stage.canvas.width / 3);

    // Set station
    station = new createjs.Shape();
    station.graphics.beginFill("Grey")
        .drawRect(0,0,rectsize, rectsize);
    station.x = Math.floor(stage.canvas.width / 2);
    station.y = mainCircle.y - 25;

    // Event ticker
    createjs.Ticker.addEventListener("tick", update);

    // Set ticker
    createjs.Ticker.setFPS(30);
    
    // Add objects to stage
    stage.addChild(mainCircle);
    stage.addChild(station);
}