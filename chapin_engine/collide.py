from PIL import Image
import numpy as np
from math import sqrt

class Grid:
    def __init__(self, background_image, scale, debug=True, image_out=False):
        self.grid_size = 20
        self.numpy_img = np.array(Image.open(background_image))
        self.x_points = [self.grid_size*x+1 for x in range(1,self.numpy_img.shape[1]) if 0 <= self.grid_size*x+1 <= self.numpy_img.shape[0]]
        self.y_points = [self.grid_size*y+1 for y in range(1,self.numpy_img.shape[0]) if 0 <= self.grid_size*y+1 <= self.numpy_img.shape[0]]

        self.points = []
        self.collision_points = []
        self.path_points = []

        for xP in self.x_points:
            for yP in self.y_points:
                self.points.append((xP,yP))

        if debug:
            for point in self.points:
                if self.numpy_img[point][3] == 255:
                    self.numpy_img[point][:3] = 0
                    self.collision_points.append((point[0]*scale, point[1]*scale))
                else:
                    self.numpy_img[point][:4] = 255
                    self.path_points.append((point[0]*scale, point[1]*scale))
        if image_out:
            pil_img = Image.fromarray(self.numpy_img)
            pil_img.save(str(background_image)[:-4]+'_collision_grid.png')
        return None


def collision_points(grid, mouse_location):
    collision_points_x = [px-mouse_location[0] for px in grid.x_points if px < (mouse_location[0]+grid.grid_size)]
    collision_points_y = [py-mouse_location[1] for py in grid.y_points if py < (mouse_location[1]+grid.grid_size)]
    collision_points = []
    for xP in collision_points_x:
        for yP in collision_points_y:
            collision_points.append((xP,yP))
    return collision_points


def collide(sprite1, mouse_position):
    xi, yi = sprite1[0], sprite1[1]
    xf, yf = mouse_position[0], mouse_position[1]
    dist = sqrt(((yf-yi)**2)+((xi-xf)**2))
    if dist < 100:
        check = True
    else:
        check = False
    return check



if __name__ == "__main__":
    grid = Grid('assets/art/fondo.png', debug=False)
    collision = Collision_points(grid, (300,300))
    print(grid.points.__len__())
