from time import sleep
import math
import pygame
import sympy


def find_circles_intersection(x1, y1, x2, y2, r1, r2):
    x = sympy.Symbol("x")

    y = (
        (r1**2 - r2**2) - (x1**2 - x2**2) - (y1**2 - y2**2) + 2 * x * (x1 - x2)
    ) / (-2 * (y1 - y2))

    f = sympy.Poly((x - x2) ** 2 + (y - y2) ** 2 - r2**2)
    x_vals = sympy.nroots(f)

    try:
        x_pivot = float(x_vals[0])

        y = sympy.Symbol("y")
        y_vals_circle1 = sympy.nroots(
            sympy.Poly((y - y2) ** 2 + (x_pivot - x2) ** 2 - r2**2)
        )
        y_vals_circle2 = sympy.nroots(
            sympy.Poly((y - y1) ** 2 + (x_pivot - x1) ** 2 - r1**2)
        )

        y_vals_circle1_int = {int(num) for num in y_vals_circle1}
        y_vals_circle2_int = {int(num) for num in y_vals_circle2}

        return (int(x_pivot), list(y_vals_circle1_int & y_vals_circle2_int)[0])

    except (TypeError, IndexError):
        return None


def find_circle_line_intersect(x0, y0, r, m):
    x = sympy.Symbol("x")

    f = sympy.Poly((x - x0) ** 2 * (m**2 + 1) - r**2)
    x_vals = sympy.nroots(f)

    y_vals = []
    for i, x_val in enumerate(x_vals):
        x_vals[i] = int(x_val)
        y_vals.append(int(m * (x_val - x0) + y0))

    return ((x_vals[0], y_vals[0]), (x_vals[1], y_vals[1]))


def display_text(scrn, text, color, coords, x_offset=10, y_offset=25):
    pygame.font.init()
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = (coords[0] + x_offset, coords[1] + y_offset)
    scrn.blit(text, text_rect)


def draw_grid(scrn, xmax, ymax, center, interval=50):
    for i in range(0, xmax, interval):
        pygame.draw.line(scrn, pygame.Color("#bfbfbf"), (i, 0), (i, ymax))

    for i in range(0, ymax, interval):
        pygame.draw.line(scrn, pygame.Color("#bfbfbf"), (0, i), (xmax, i))

    # pygame.draw.line(
    #     scrn, pygame.Color("#737373"), (center[0], 0), (center[0], ymax), width=2
    # )
    # pygame.draw.line(
    #     scrn, pygame.Color("#737373"), (0, center[1]), (xmax, center[1]), width=2
    # )


def draw_button(scrn):
    pygame.draw.rect(scrn, pygame.Color("#bfbfbf"), pygame.Rect(500, 0, 100, 100))
    display_text(scrn, "RESET", "black", (550, 50), x_offset=0, y_offset=0)


def calculate_slope(start: tuple[int, int], end: tuple[int, int]) -> float:
    return math.atan2((end[1] - start[1]), (end[0] - start[0]))


def sim(scrn, xmax, ymax):

    pygame.display.set_caption("Planimeter simulation")

    P = 800
    T = 400
    CENTER = (200, 200)

    WHEEL_LEN = 20

    all_coords = []
    all_pivots = []
    wheel_positions = []

    light_blue = pygame.Color("#1d88c2")
    magenta = pygame.Color("#b33484")
    yellow = pygame.Color("#e3c51b")

    scrn.fill("white")
    xy = (800, 400)
    pivot = find_circles_intersection(CENTER[0], CENTER[1], xy[0], xy[1], P, T)
    draw_grid(scrn, xmax, ymax, CENTER)
    pygame.draw.line(scrn, "blue", CENTER, pivot, width=10)
    pygame.draw.line(scrn, "red", xy, pivot, width=10)
    pygame.draw.circle(scrn, light_blue, pivot, 8)
    pygame.draw.circle(scrn, magenta, xy, 8)
    pygame.draw.circle(scrn, "black", CENTER, 8)
    display_text(scrn, "(a,b)", light_blue, pivot)
    display_text(scrn, "(x,y)", magenta, xy)
    display_text(scrn, "(0,0)", "black", CENTER, x_offset=-20, y_offset=-25)

    draw_button(scrn)

    pygame.display.flip()

    while True:
        scrn.fill("white")
        draw_grid(scrn, xmax, ymax, CENTER)

        # get user input for current position
        pygame.event.get()
        if pygame.mouse.get_pressed()[0]:
            xy = pygame.mouse.get_pos()
            if xy[0] > 500 and xy[1] < 100:
                return
            # calculate pivot point
            pivot = find_circles_intersection(CENTER[0], CENTER[1], xy[0], xy[1], P, T)
            if pivot is not None:
                all_coords.append(xy)
                all_pivots.append(pivot)

        if pivot is not None:
            if len(all_coords) >= 2:
                pygame.draw.lines(scrn, "black", False, all_coords, width=2)

            wheel = (
                pivot[0] + (pivot[0] - xy[0]) / 4,
                pivot[1] + (pivot[1] - xy[1]) / 4,
            )
            wheel_positions.append(wheel)
            try:
                wheel_endpoints = find_circle_line_intersect(
                    wheel[0],
                    wheel[1],
                    WHEEL_LEN,
                    (-(xy[0] - pivot[0]) / (xy[1] - pivot[1])),
                )
                pygame.draw.line(
                    scrn, yellow, wheel_endpoints[0], wheel_endpoints[1], width=10
                )
                pygame.draw.circle(scrn, yellow, wheel_endpoints[0], 5)
                pygame.draw.circle(scrn, yellow, wheel_endpoints[1], 5)
            except ZeroDivisionError:
                pass

            pygame.draw.line(scrn, "blue", CENTER, pivot, width=10)
            pygame.draw.line(scrn, "red", xy, wheel, width=10)
            pygame.draw.circle(scrn, light_blue, pivot, 8)
            pygame.draw.circle(scrn, magenta, xy, 8)
            pygame.draw.circle(scrn, "black", CENTER, 8)
            pygame.draw.circle(scrn, yellow, wheel, 8)
            display_text(scrn, "(a,b)", light_blue, pivot)
            display_text(scrn, "(x,y)", magenta, xy)
            display_text(scrn, "(0,0)", "black", CENTER, x_offset=-20, y_offset=-25)
            display_text(scrn, "W", yellow, wheel, x_offset=-30, y_offset=0)

            draw_button(scrn)

            pygame.display.flip()
        sleep(0.002)


def main():

    xmax = 1500
    ymax = 1000
    scrn = pygame.display.set_mode((xmax, ymax))

    while True:
        sim(scrn, xmax, ymax)


if __name__ == "__main__":
    main()
