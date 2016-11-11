ArrayList<PVector> points = new ArrayList<PVector>();
IntList inventory = new IntList();
int num = 7;

float sign(PVector p1, PVector p2, PVector p3)
{
  return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y);
}

boolean PointInTriangle(PVector pt, PVector v1, PVector v2, PVector v3)
{
  boolean b1, b2, b3;

  b1 = sign(pt, v1, v2) < 0.0f;
  b2 = sign(pt, v2, v3) < 0.0f;
  b3 = sign(pt, v3, v1) < 0.0f;

  return ((b1 == b2) && (b2 == b3));
}

void setup()
{
  size(480, 640);
  noLoop();
  smooth(8);
  for(int i = 0; i < num; i++)
  {
    points.add(new PVector(int(random(480)), int(random(640))));
    inventory.append(i);
  }
  points.add(new PVector(int(0), int(0)));
  inventory.append(num);
  points.add(new PVector(int(0), int(640)));
  inventory.append(num + 1);
  points.add(new PVector(int(480), int(0)));
  inventory.append(num + 2);
  points.add(new PVector(int(480), int(640)));
  inventory.append(num + 3);
  println(points);
  println(inventory);
}

void draw()
{
  background(0, 0, 0);
  noStroke();
  //inventory.shuffle();
  //triangle(points.get(inventory.get(0)).x, points.get(inventory.get(0)).y, points.get(inventory.get(1)).x, points.get(inventory.get(1)).y, points.get(inventory.get(2)).x, points.get(inventory.get(2)).y);
  // All combinations
  color from = color(random(0, 100), random(0, 100), random(0, 100));
  color to = color(random(200, 255), random(200, 255), random(200, 255));
  float shift = 0;
  for(int i = 0; i < num + 4; i++)
  {
    for(int j = 0; j < num + 4; j++)
    {   
      for(int k = 0; k < num + 4; k++)
      {
        //println(i); println(j); println(k);   
        if ((i != j) & (i != k) & (j != k))
        {
          println("ok");
          shift = shift + 0.002;
          println(shift);
          color interC = lerpColor(from, to, shift);
          fill(random(0, 255), random(0, 255), random(0, 255), 150);
          //fill(interC, 50);
          boolean dec = false;
          for(int pi = 0; pi < num + 4; pi++)
          {
            boolean answer = PointInTriangle(points.get(inventory.get(pi)), points.get(inventory.get(i)), points.get(inventory.get(j)), points.get(inventory.get(k)));
            println(answer);
            if (answer == true)
            {
              dec = true;
            }
            //triangle(points.get(inventory.get(i)).x, points.get(inventory.get(i)).y, points.get(inventory.get(j)).x, points.get(inventory.get(j)).y, points.get(inventory.get(k)).x, points.get(inventory.get(k)).y);
          }
          float d1 = PVector.dist(points.get(inventory.get(i)), points.get(inventory.get(j)));
          float d2 = PVector.dist(points.get(inventory.get(i)), points.get(inventory.get(k)));
          float d3 = PVector.dist(points.get(inventory.get(j)), points.get(inventory.get(k)));
          println(d1,d2,d3);
          if ((d1 >= 350.0) | (d2 >= 350.0) | (d3 >= 350.0))
          {
            dec = true;
          }
          float sq = abs(sign(points.get(inventory.get(i)), points.get(inventory.get(j)), points.get(inventory.get(k)))) / 2.0;
          println(sq);
          if (sq <= 10000)
          {
            dec = true;
          }
          if (dec == false)
          {
            println("drawn");
            triangle(points.get(inventory.get(i)).x, points.get(inventory.get(i)).y, points.get(inventory.get(j)).x, points.get(inventory.get(j)).y, points.get(inventory.get(k)).x, points.get(inventory.get(k)).y);
          }
        }
        println("---");
      }
    }
  }
  // Find insider
  //for(int i = 3; i < num; i++)
  //{
  //  boolean answer = PointInTriangle(points.get(inventory.get(i)), points.get(inventory.get(0)), points.get(inventory.get(1)), points.get(inventory.get(2)));
  //  println(answer);
  //}
  // Draw all points
  stroke(0, 255, 0);
  strokeWeight(7);
  for (PVector p : points)
  {
    point(p.x, p.y);
  }
  loadPixels();
  for (int i = 0; i < pixels.length; i++)
  {
    color n = color(random(255));
    color c = pixels[i];
    color result = lerpColor(c, n, random(0.11));
    pixels[i] = random(1) <= 1.0? result:c;
  } 
  updatePixels();
}