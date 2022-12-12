var pontos1 = [];
var pontos2 = [];
const planetarray = [];
const size = 35;
var average = [0,0];

function setup() {
  createCanvas(windowWidth, windowHeight);
  background(40,42,53);
  textSize(width / 10);
  textAlign(CENTER, CENTER);
  noLoop();
}


class Planet{
  constructor(x,y,vx,vy){
    this.x = x;
    this.y = y;
    this.vx = vx;
    this.vy = vy;
  }
  new(){
    this.x = this.x + this.vx;
    this.y = this.y + this.vy;
  }
}




function draw() {
  background(40,42,53);
  if(frameCount === 1){
    fill("white")
    text("Carrega em qualquer\n sítio do ecrã", width/2, height/2);
    return;
  }
  noFill();
  strokeWeight(10);
  stroke(0,200,200);
  beginShape();
  
  for(let i = 0; i< pontos2.length; i++){
    pontos2[i][0] += 2
    curveVertex(pontos2[i][0], pontos2[i][1])}

  curveVertex(average[0],average[1]);

  for(let i = pontos1.length - 1; i >= 0; i--){
    pontos1[i][0] -= 2;
    curveVertex(pontos1[i][0], pontos1[i][1])}
  endShape();
 
  for(let i = 0; i<planetarray.length; i++){
    planetarray[i].vx += (windowWidth/2 - planetarray[i].x)/1000;
    planetarray[i].vy += (windowHeight/2 - planetarray[i].y)/1000}
  
    
  strokeWeight(4);
  stroke(255);
  fill(122,122,122);
  for(let i = 0; i< planetarray.length; i++){
    planetarray[i].new();
    circle(planetarray[i].x,planetarray[i].y, 40)}
    /*Calculations for the average point*/
  average = [windowWidth/2, windowHeight/2];
  for(let i = 0; i <planetarray.length; i++){
    average[0] += planetarray[i].x - windowWidth/2;
    average[1] += planetarray[i].y - windowHeight/2;
  }
  fill(0,100,100);
  circle(average[0], average[1], 40);
  
  if(pontos1.length < size){
    pontos1.push([average[0], average[1]]);
    pontos2.push([average[0], average[1]]);
  }
  else{
    if(frameCount%10 == 0){
    pontos1.shift(); pontos2.shift();
    pontos1.push([average[0], average[1]]); pontos2.push([average[0], average[1]])}
  }
}



function mousePressed() {
  pontos1 = [];
  pontos2 = [];
  planetarray.push(new Planet(mouseX,mouseY,0,0));
  loop();
  return false;
}
