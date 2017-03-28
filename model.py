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
        propX = self.width / otherWindowPos.width;
        propY = self.height / otherWindowPos.height;
        
        offX = otherCoords.x * propX;
        offY = otherCoords.y * propY;
        
        return Coords(self.x + offX, self.y + offY);

class Coords:
    def __init__(self,x,y):
        self.x = x;
        self.y = y;

class SimpleShootHistory:
    def __init__(self, stackSize):
        self.stackSize = stackSize;

    def newFrame(self, POIs):
        return;

    def newPOI(self, POI):
        return;

    def 
