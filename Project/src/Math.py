import pygame
import math
import random

class Vector2:
    def __init__(self, x:float, y:float):
        self.x=x
        self.y=y
    def Dot(self, v):
        return self.x*v.x+self.y*v.y
    def DisToSq(self, b):
        return (self.x-b.x)**2+(self.y-b.y)**2
    def Normalize(self):
        try:
            return Vector2(self.x/self.Length(),self.y/self.Length());
        except:
            return Vector2(0,0)
    def Length(self):
        return math.sqrt(self.LengthSq())
    def LengthSq(self):
        return self.x*self.x+self.y*self.y;
    def AddNum(self, num):
        self.x+=num
        self.y+=num
    def AddVec(self, vec):
        self.x+=vec.x
        self.y+=vec.y
        return self
    def Multiply(self, num):
        self.x*=num
        self.y*=num
        return self
    def MinusVec(self, vec):
        self.x-=vec.x
        self.y-=vec.y
        return self
    def Copy(self):
        return Vector2(self.x, self.y)
    def Truncate(self, maxForce):
        if self.Length()>maxForce:
            r=self.Normalize()
            self.x=r.x*maxForce
            self.y=r.y*maxForce
        return self
    def Rotate(self, angle):
        rad = math.radians(angle)
        cos_theta = math.cos(rad)
        sin_theta = math.sin(rad)
        new_x = self.x * cos_theta - self.y * sin_theta
        new_y = self.x * sin_theta + self.y * cos_theta
        return Vector2(new_x, new_y)
    def Perpendicular(self):
        return Vector2(self.y, -self.x)

def VaV(a,b):
    return Vector2(a.x+b.x, a.y+b.y)
def VaN(a, b):
    return Vector2(a.x+b, a.y+b)
def VmiV(a, b):
    return Vector2(a.x-b.x, a.y-b.y)
def VmiN(a, b):
    return Vector2(a.x-b, a.y-b)
def VmV(a,b):
    return Vector2(a.x*b.x, a.y*b.y)
def VmN(a, b):
    return Vector2(a.x*b, a.y*b)
def VdN(a, b):
    return Vector2(a.x/b, a.y/b)
def dot(x1,x2,y1,y2):
    return x1*x2+y1*y2
def RandomClamped():
    return random.uniform(-1.0, 1.0)
    
class CircleCollider:
    def __init__(self, pos: Vector2, length: float):
        self.mPosition = pos
        self.mLength = length

    def IntersectCircleCollider(self, b):
        return self.mPosition.DisToSq(b.mPosition) < (self.mLength + b.mLength) * (self.mLength + b.mLength)

    def Draw(self, surf):
        #pygame.draw.circle(surf, (255, 0, 0), (self.mPosition.x, self.mPosition.y), self.mLength, 2)
        pass

        

class Collider:
    def __init__(self, position, width=0, length=0, rotation=0):
        self.mPosition = position
        self.mWidth = width
        self.mLength = length
        self.mRotation = math.degrees(rotation)

    def DownRight(self):
        return Vector2(self.mPosition.x + self.mWidth / 2, self.mPosition.y + self.mLength / 2)

    def UpLeft(self):
        return Vector2(self.mPosition.x - self.mWidth / 2, self.mPosition.y - self.mLength / 2)

    def GetRotatedCorners(self):
        half_width = self.mWidth / 2
        half_length = self.mLength / 2

        corners = [
            Vector2(-half_width, -half_length),
            Vector2(half_width, -half_length),
            Vector2(half_width, half_length),
            Vector2(-half_width, half_length)
        ]

        rotated_corners = [corner.Rotate(self.mRotation) for corner in corners]
        
        for i in range(4):
            rotated_corners[i].x += self.mPosition.x
            rotated_corners[i].y += self.mPosition.y

        return rotated_corners

    def Inside(self, vec):
        rotated_corners = self.GetRotatedCorners()
        
        min_x = min(corner.x for corner in rotated_corners)
        max_x = max(corner.x for corner in rotated_corners)
        min_y = min(corner.y for corner in rotated_corners)
        max_y = max(corner.y for corner in rotated_corners)

        return min_x < vec.x < max_x and min_y < vec.y < max_y
    
    def IntersectCollider(self, b):
        corners_a = self.GetRotatedCorners()
        corners_b = b.GetRotatedCorners()

        for i in range(4):
            edge_a = VmiV(corners_a[i], corners_a[(i + 1) % 4])  
            for j in range(4):
                #edge_b = corners_b[j] - corners_b[(j + 1) % 4]
                axis = edge_a.Perpendicular()

                projection_a = [v.Dot(axis) for v in corners_a]
                projection_b = [v.Dot(axis) for v in corners_b]

                min_a, max_a = min(projection_a), max(projection_a)
                min_b, max_b = min(projection_b), max(projection_b)

                if max_a < min_b or max_b < min_a:
                    return False 

        return True 


    def IntersectCircleCollider(self, circle):
        rotated_corners = self.GetRotatedCorners()
        
        nearest_x = max(rotated_corners[0].x, min(circle.mPosition.x, rotated_corners[1].x))
        nearest_y = max(rotated_corners[0].y, min(circle.mPosition.y, rotated_corners[3].y))

        delta_x = circle.mPosition.x - nearest_x
        delta_y = circle.mPosition.y - nearest_y

        distance_sq = delta_x ** 2 + delta_y ** 2
        radius_sq = circle.mLength ** 2

        return distance_sq < radius_sq

    def Draw(self, surf):
        rotated_corners = self.GetRotatedCorners()
        #pygame.draw.polygon(surf, (0, 255, 0), [(corner.x, corner.y) for corner in rotated_corners], 2)