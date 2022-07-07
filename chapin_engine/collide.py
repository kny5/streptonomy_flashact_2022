from PIL import Image
import numpy as np
from math import sqrt

class Grid:
    def __init__(self, background_image, scale, debug=False, image_out=False):
        self.size = 20
        self.numpy_img = np.array(Image.open(background_image))
        shape = self.numpy_img.shape
        self.numpy_img = self.numpy_img.reshape((shape[1], shape[0], shape[2]))
        print("check "*90)
        print(self.numpy_img.shape)
        self.shape = (self.numpy_img.shape[0]*scale, self.numpy_img.shape[1]*scale)
        self.x_points = [self.size*x*scale for x in range(1,self.numpy_img.shape[0]) if 0 <= self.size*x*scale <= self.numpy_img.shape[0]-1]
        self.y_points = [self.size*y*scale for y in range(1,self.numpy_img.shape[1]) if 0 <= self.size*y*scale <= self.numpy_img.shape[1]-1]

        self.points = []
        self.collision_points = []
        self.path_points = []

        for xP in self.x_points:
            for yP in self.y_points:
                self.points.append((xP,yP))
                if self.numpy_img[(xP, yP)][3] == 255:
                    self.collision_points.append((xP,yP))
                else:
                    self.numpy_img[(xP, yP)][:4] = 255
                    self.path_points.append((xP, yP))

        if image_out:
            pil_img = Image.fromarray(self.numpy_img)
            pil_img.save(str(background_image)[:-4]+'_collision_grid.png')
        return None


def collide(sprite1, mouse_position):
    xi, yi = sprite1[0], sprite1[1]
    xf, yf = mouse_position[0], mouse_position[1]
    dist = sqrt(((yf-yi)**2)+((xi-xf)**2))
    if dist < 100:
        check = True
    else:
        check = False
    return check


def line_segment(mouse, nitro_point):
    bx = mouse.x
    by = mouse.y
    ax = nitro_point[0]
    ay = nitro_point[1]
    bax = bx - ax
    bay = by - ay
    balen = sqrt( bax**2 + bay**2 )
    delta = -100
    bcx = bax * delta / balen
    bcy = bay * delta / balen

    cx = bx + bcx
    cy = by + bcy
    return (cx, cy)


def path(mouse, grid_obj):
    collission_x = np.asarray(grid_obj.x_points)
    collission_y = np.asarray(grid_obj.y_points)
    x_co = False
    y_co = False
    for x in np.nditer(collission_x):
        if mouse[0] -grid_obj.size < x < mouse[0] + grid_obj.size:
        #if mouse[0] == x:
            x_co = True
    for y in np.nditer(collission_y):
        if mouse[1] -grid_obj.size < y < mouse[1] + grid_obj.size:
        #if mouse[1] == y:
            y_co = True
    print(x_co + y_co)
    return x_co + y_co


if __name__ == "__main__":
    grid = Grid('assets/art/fondo.png', debug=False)
    collision = Collision_points(grid, (300,300))
    print(grid.points.__len__())
