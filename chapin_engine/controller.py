from math import atan, degrees, sqrt, pi, tan


count_x = 0
count_y = 0
factor = 50
speed_calibration = 0.7


def rotate_streptonomy(sprite):
    rotated = map(lambda x: pygame.transform.rotate(x, streptonomy_angle), sprites)
    return list(rotated)


def scale_streptonomy(sprites):
    scaled = map(lambda x: pygame.transform.scale(x, streptonomy_size), sprites)
    return list(scaled)


def controller_angle(mouse_position, display_size):
    xi, yi = 0, 0
    xf, yf = mouse_position[0]-display_size[0]/2, mouse_position[1]-display_size[1]/2
    try:
        m = (yf-yi)/(xf-xi)
        dx = xi-xf
        dy = yi-yf
    except:
        m = 0
    if m >= 0:
        angle = atan(m)
    else:
        angle = pi + atan(m)
    return 90 - degrees(angle)


def controller_lenght(mouse_position):
    xi, yi = display_size[0]/2, display_size[1]/2
    xf, yf = mouse_position[0], mouse_position[1]
    return sqrt(((yf-yi)**2)+((xi-xf)**2))


def controller_scroll(mouse_position, display_size, game_display_size):
    global count_x, count_y, factor

    xi, yi = display_size[0]/2, display_size[1]/2
    xf, yf = mouse_position[0], mouse_position[1]
    speed = sqrt(((yf-yi)**2)+((xi-xf)**2)) / factor

    if speed > speed_calibration:
        if xf > xi:
            x_sense = 1*speed
        else:
            x_sense = -1*speed
        if yf > yi:
            y_sense = 1*speed
        else:
            y_sense = -1*speed

        count_x -= x_sense
        count_y -= y_sense

        if 0 <= count_x:
            count_x += x_sense
        if 0 <= count_y:
            count_y += y_sense
        if not count_x > (display_size[0] - game_display_size[0]):
            count_x -= -x_sense
        if not count_y > (display_size[1]- game_display_size[1]):
            count_y -= -y_sense

    #print(count_x, count_y)
    return (count_x, count_y)


def controller_zoom():
    pass
