#2D Console Rendering API v2 for Python 3+ and JavaScript by Jordan Greydanus (Kyranok)
print("Powered by 2DCR _Kyranok")
print("2D Console Rendering API for Python 3+ and JavaScript v2")
print(" ")
#<--Beginning of 2DCR's code, don't change anything until later-->
WORLDX = 0
WORLDY = 0
EMPTYICON = "_"
activePoints = [] #Don't change this variable
import math
class point: #Create a class for a point
  def __init__(self, x, y, icon):
    self.x = x
    self.y = y
    self.icon = icon
    self.visible = True
    self.parent = False
    activePoints.append(self)
  def move(self, x, y): #Moves a point by the X and Y
    self.x = self.x+x
    self.y = self.y+y
  def position(self, x, y): #Point's position will become the X and Y
    self.x = x
    self.y = y
  def hide(self): #Hides the point
    global activePoints
    self.visible = False
    if self in activePoints: #Hide point if it's visible
      activePoints.remove(self)
  def show(self): #Shows the point
    global activePoints
    self.visible = True
    if self not in activePoints: #Show point if it's hidden
      activePoints.append(self)
  def checkCollide(self, check):
    hit = False
    try: #If it's a list, check if one of its points collides
      for i in range(len(check.list)):
        if check.list[i].x == self.x and check.list[i].y == self.y and check.list[i].visible:
          hit = check.list[i]
    except: #Not a list
      try: #Check if the point collides
        if check.x == self.x and check.y == self.y and check.visible:
          hit = check
      except: #Invalid input
        hit = False
    return hit
  def clone(self):
    return point(self.x, self.y, self.icon)
  def distance(self, check):
    return math.sqrt((check.x - self.x)*(check.x - self.x) + (check.y - self.y)*(check.y - self.y))
class points: #Create a class for a group of points
  def __init__(self, list):
    self.list = list
    for i in range(len(list)):
      self.list[i].parent = self
  def show(self): #Shows the points
    for i in range(len(self.list)):
      self.list[i].show()
  def hide(self): #Hides the points
    for i in range(len(self.list)):
      self.list[i].hide()
  def add(self, a): #The specified point will be added
    self.list.append(a)
    a.parent = self
    return a #Return the point if adjustment is necessary
  def remove(self, r): #The specified point will be removed
    self.list.remove(r)
    r.parent = False
    r.hide()
    return r #The point is returned so it can be used again if desired
  def clear(self): #Clears the list of points
    self.hide()
    self.list = []  
  def pointFromIcon(self, icon): #Returns the point in the list from its icon
    found = False
    for i in range(len(self.list)):
      if self.list[i].icon == icon:
        found = self.list[i]
    return found
  def pointFromCoords(self, x, y): #Returns a point from its coords
    found = False
    for i in range(len(self.list)):
      if self.list[i].x == x and self.list[i].y == y:
        found = self.list[i]
    return found
  def checkCollide(self, check):
    found = False
    for i in range(len(self.list)):
      if self.list[i].checkCollide(check) and self.list[i].visible:
        found = self.list[i]
    return found
  def move(self, x, y):
    for i in range(len(self.list)):
      self.list[i].move(x, y)
  def clone(self):
    newPoints = points([])
    for i in range(len(self.list)):
      newPoints.add(self.list[i].clone())
    return newPoints
  def fill(self, minX, minY, maxX, maxY, icon):
    for y in range(minY, maxY+1):
      for x in range(minX, maxX+1):
        self.add(point(x,y,icon))
def renderRegion(minX, minY, maxX, maxY):
  for y in range(minY, maxY+1):
    row = ""
    for x in range(minX, maxX+1):
      newPoint = EMPTYICON
      if len(activePoints) > 0:
        for i in range(len(activePoints)):
          if isinstance(activePoints[i], list):
            for ii in range(len(activePoints[i])):
              if activePoints[i][ii].x == x and activePoints[i][ii].y == y:
                newPoint = activePoints[i][ii].icon
          else:
            if activePoints[i].x == x and activePoints[i].y == y:
              newPoint = activePoints[i].icon
      row = row + newPoint
    print(row)
def render():
  renderRegion(0,0,(WORLDX-1),(WORLDY-1))
def collisionFree(x,y, exception):
  check = True
  for i in range(len(activePoints)):
    if activePoints[i].x == x and activePoints[i].y == y:
      if activePoints[i] != exception:
        check = False
  return check
def checkCollide(x,y, exception):
  check = False
  for i in range(len(activePoints)):
    if activePoints[i].x == x and activePoints[i].y == y:
      if activePoints[i] != exception:
        check = activePoints[i]
  return check
def checkInRegion(check, minX, minY, maxX, maxY):
    found = False
    try: #If it's a list, check if it's in the cam
      for i in range(len(check.list)):
        item = check.list[i]
        if item.x <= maxX and item.y <= maxY and item.x >= minX and item.y >= minY:
          found = check.list[i]
    except: #Not a list
      try: #Check if the point is in the cam
        if check.x <= maxX and check.y <= maxY and check.x >= minX and check.y >= minY: found = check
      except: #Invalid input
        found = False
    return found  
#<--End of 2DCR's code-->
def demo():
  print("2D Console Rendering begins with a square.")
  WORLDX = int(input("Type the width of the world in 'numerals' and press Enter: for ex'10': "))  #Width of the world. Coords will be 0-(WORLDX-1)
  WORLDY = int(input("Type the height of the world in 'numerals' and press Enter: for ex'10': "))  #Height of the world. Coords will be 0-(WORLDY-1)
  EMPTYICON = input("Enter the 'unit tile character set' you wish to represent each empty space on the board: for ex'01':")  #The character used to display emptiness
  render()
  print("Now we can begin world editing.")
  PICON = input("Enter your UTCS you wish to be displayed as: for ex' A':")
  player = point(round(WORLDX/2),round(WORLDY/2),PICON)
  print("You're in the center ("+str(player.x)+","+str(player.y)+") of our screen.")
  render()
  next = input("Enter 'move' or 'edit' or 'r' to reset or press any key to idle: ")
  if (next == "r"):
    demo()
demo()