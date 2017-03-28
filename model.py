class WindowPos:
    def __init__(self,x,y,width,height):
        self.x = x;
        self.y = y;
        self.width = width;
        self.height = height;

    def getX2(self):
        return self.x + self.width;

    def getY2(self):
        return self.y + self.height;

    def getCoordsProportionally(self, otherWindowPos, otherCoords):
        return;

class Coords:
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
