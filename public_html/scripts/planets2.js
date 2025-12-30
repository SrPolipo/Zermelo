function preload() {
  planetData = loadJSON('./data/planet_positions.json');
}

function setup() {
  let cnv = createCanvas(windowWidth*0.8, windowHeight*0.8);
  cnv.parent("planetas")
  angleMode(DEGREES);
  noLoop();
}

function draw() {
  background(10);
  translate(width / 2, height / 2);

  let min_distance = Math.min(width,height)

  let now = new Date();
  let target = new Date(2026, 2, 18); // March 18
  let diff = target - now; // difference in milliseconds

  let days = Math.floor(diff / (1000 * 60 * 60 * 24));
  let hours = Math.ceil((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));


  // Display countdown
  fill(255);
  textSize(24);
  textAlign(CENTER, TOP);
  text(`Time until March 18th: ${days}d ${hours}h`, 0, -height/2 + 20);


  let radii = {
    Mercury: min_distance*0.1,
    Venus: min_distance*0.225,
    Earth: min_distance*0.25,
    Mars: min_distance*0.3,
    Jupiter: min_distance*0.4,
    Saturn: min_distance*0.45
  };
  
  let colors = {
    Mercury: '#B5B5B5',
    Venus: '#F5DEB3',
    Earth: '#3399FF',
    Mars: '#FF3333',
    Jupiter: '#FFCC99',
    Saturn: '#FFDD77'
  };

  let sizes = {
    Mercury: 8,
    Venus: 10,
    Earth: 12,
    Mars: 14,
    Jupiter: 16,
    Saturn: 18
  };

  let today = new Date();
  let year = today.getFullYear();        
  let month = today.getMonth() + 1;        
  let day = today.getDate();

  month = month < 10 ? '0' + month : month;
  day = day < 10 ? '0' + day : day;

  const formattedDate = `${year}-${month}-${day}`;
  const today_data = planetData[formattedDate];

  // Sun
  fill(255, 200, 0);
  noStroke();
  circle(0, 0, 30);


  // Planets
  for (let p in today_data) {
    let x = cos(today_data[p]) * radii[p];
    let y = sin(today_data[p]) * radii[p];

    fill(colors[p]);
    circle(x, y, sizes[p]);
  }
}
