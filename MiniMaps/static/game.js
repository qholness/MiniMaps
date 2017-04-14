var nodes = []; // GLOBAL -- Used in initGame.js
var circleSpeed = 15;
var capacity = 10; // Capacity of box(es)
var paused = false; // Paused state
var emptying = false; // Emptying box(es) state
var counter = 0;
var node; // Temp pointer for nodes
var trafficNode; // Traffic generator node
var newtext; // Update box(es) text



// Fill the station
function fillStation() {
    if (within(mainCircle.x, station.x)) {
        if (within(mainCircle.y, station.y, 30)) {
            // insert_nodes();
            nodes.push(createTraffic());
            mainCircle.x = 0;
            mainCircle.y = Math.floor(stage.canvas.width / 3);
        }
    }
}

function createTraffic() {
    // Add a new node to the station.
    trafficNode = new createjs.Shape();
    trafficNode.graphics.beginFill("Red")
        .drawCircle(0, 0, 5);
    return trafficNode;
}

function move_child() {
    // Move child node off screen
    if (!node) {
        node = nodes.shift();
        node.x = station.x + rectsize + 10;
        node.y = Math.floor(stage.canvas.width / 3);
        stage.addChild(node);
    }
    else {
        node.x = node.x + 5;
        node.y = node.y + Math.sin(node.y) * 6;
        if (node.x > stage.canvas.width) {
            stage.removeChild(node);
            node = null;
        }
    }
}

function insert_nodes() {
    // Fill the station
    
}

function move_main_circle(speed=circleSpeed) {
    mainCircle.x = mainCircle.x + speed;
    if (mainCircle.x > stage.canvas.width + 10) {
        mainCircle.x = 0;
    }
}

// Move main node with arrow keys
// document.onkeydown = checkKey;
// function checkKey(e) {
//     e = e || window.event;

//     if (e.keyCode == '38') {
//         mainCircle.y = mainCircle.y - circleSpeed;
//     }
//     else if (e.keyCode == '40') {
//         mainCircle.y = mainCircle.y + circleSpeed;
//     }
//     else if (e.keyCode == '37') {
//         mainCircle.x = mainCircle.x - circleSpeed;
//     }
//     else if (e.keyCode == '39') {
//         mainCircle.x = mainCircle.x + circleSpeed;
//     }
// }
var inputText;
function updateCounter() {
    counter = nodes.length;
    inputText = emptying ? 
        "Emptying: " + counter + "|" + capacity 
        : counter + "|" + capacity
    ;
    if (newtext) {
        stage.removeChild(newtext);
        newtext = new createjs.Text(inputText, "16px Arial", "black");
        newtext.x = station.x;
        newtext.y = station.y - 16;
        stage.addChild(newtext);
    }
    else {
        newtext = new createjs.Text(inputText, "16px Arial", "black");
        newtext.x = station.x;
        newtext.y = station.y - 16;
        stage.addChild(newtext);
    }
}

function emptyQueue(maxfill) {
    if (!emptying) {
        move_main_circle();
    }
    if (counter > maxfill) {
        emptying = true;
    }
    if (emptying) {
        if (counter < maxfill ) {
            emptying = false;
        }
        move_main_circle(Math.floor(tempSpeed/2));
    }
    return emptying;
}

var tempSpeed, 
    tempCapacity, 
    tempEmpty;

function update(event) {
    tempCapacity = parseInt(document.getElementById("capacity").value);;
    tempSpeed - parseInt(document.getElementById("speed").value);

    if (parseInt(document.getElementById("speed").value)) {
        tempSpeed = parseInt(document.getElementById("speed").value);
        if (tempSpeed > 0 && tempSpeed < 50) {
            circleSpeed = tempSpeed;
        }
    }
    if (parseInt(document.getElementById("capacity").value)) {
        if (tempCapacity > 0 && tempCapacity < 1000) {
            capacity = parseInt(document.getElementById("capacity").value);
        }
    }

    //Control emptying. Needs some more thought
    // if (parseInt(document.getElementById("empty").value)) {
    //     emptying = true;
    // }
    // else {
    //     if (!emptyQueue) {
    //         emptying = false;
    //     }
    // }

    if (!paused) {
        stage.update(event); // important
        // Move blue circle and fill station if there's less than 10 nodes
        emptyQueue(capacity);
        updateCounter();
        fillStation();
        move_child();
    }
}