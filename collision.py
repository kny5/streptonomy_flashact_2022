from PIL import Image, ImageDraw
import numpy as np

im = np.array(Image.open('assets/art/fondo.png'))

grid_size = 30
x_points = [grid_size*x+1 for x in range(1,im.shape[0]) if 0 <= grid_size*x+1 <= im.shape[0]]
y_points = [grid_size*y+1 for y in range(1,im.shape[1]) if 0 <= grid_size*y+1 <= im.shape[1]]

points = []

for xP in x_points:
    for yP in y_points:
        points.append((xP,yP))

print(x_points)
print(y_points)

for point in points:
    if im[point][3] == 255:
        im[point][:3] = 0
        im[point][3] = 255
    else:
        im[point][:3] = 255
        im[point][3] = 255

#for point in points:
#    print(im[point])

border = []
for pX, pY in points:
    #check points values

    print(im[pX][pY])
    matrix = [(-1,1),(0,1),(1,1),(-1,0),(1,0),(-1,-1),(0,-1),(1,-1)]
    for _x,_y in matrix:
        try:
            cell = im[grid_size*_x+pX][grid_size*_y+pY]
            if cell[0] == 0 and cell[3] == 255:
                im[grid_size*_x+pX][grid_size*_y+pY][:3] == 255
            #border.append(pX
            #border.append(pY)
            #border.append((pX,pY))
        except:
            pass

#print(points[0][0])

pil_img = Image.fromarray(im)
print(pil_img.mode)
# RGB

pil_img.save('assets/art/fondo_collision_grid.png')

line = Image.open('assets/art/fondo_collision_grid.png')
line_draw = ImageDraw.Draw(line)
line_draw.line(border, fill=None, width=2)
line.show()
