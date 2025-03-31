let handData = [];
let zoom = 1;
let offsetX = 0;
let offsetY = 0;

function preload() {
  // Load the JSON file containing the hand pose data
  handData = loadJSON('hand_pose_data.json');
}

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);
  noFill();
}

function draw() {
  background(200);

  // Handle zoom (mouse scroll)
  scale(zoom);
  translate(offsetX, offsetY);

  // Draw the hand landmarks
  stroke(0);
  strokeWeight(5);
  
  for (let i = 0; i < handData.length; i++) {
    const hand = handData[i];
    
    beginShape();
    for (let j = 0; j < hand.length; j++) {
      const landmark = hand[j];
      const x = landmark.x * width - width / 2;
      const y = landmark.y * height - height / 2;
      const z = landmark.z * 500;  // Scale the z-axis for visibility
      vertex(x, y, z);
    }
    endShape(CLOSE);
  }
}

function mouseWheel(event) {
  // Zoom in/out with mouse scroll
  zoom += event.delta * 0.001;
  zoom = constrain(zoom, 0.5, 3);
}

function keyPressed() {
  if (keyCode === ENTER) {
    // Load new hand pose data by clicking or triggering with 'Enter'
    handData = loadJSON('hand_pose_data.json');
  }
}
