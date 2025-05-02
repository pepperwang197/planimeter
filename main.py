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


def draw_grid(scrn, xmax, ymax, interval=50):
    for i in range(0, xmax, interval):
        pygame.draw.line(scrn, pygame.Color("#bfbfbf"), (i, 0), (i, ymax))

    for i in range(0, ymax, interval):
        pygame.draw.line(scrn, pygame.Color("#bfbfbf"), (0, i), (xmax, i))


def calculate_slope(start: tuple[int, int], end: tuple[int, int]) -> float:
    return math.atan2((end[1] - start[1]), (end[0] - start[0]))


def main():

    xmax = 600
    ymax = 600

    scrn = pygame.display.set_mode((xmax, ymax))
    pygame.display.set_caption("Planimeter simulation")

    P = 300
    T = 300
    CENTER = (100, 100)

    WHEEL_LEN = 20

    all_coords = []
    all_pivots = []
    wheel_positions = []

    M = 0

    light_blue = pygame.Color("#1d88c2")
    magenta = pygame.Color("#b33484")
    yellow = pygame.Color("#e3c51b")

    scrn.fill("white")
    xy = (400, 200)
    pivot = find_circles_intersection(CENTER[0], CENTER[1], xy[0], xy[1], T, P)
    draw_grid(scrn, xmax, ymax)
    pygame.draw.line(scrn, "blue", CENTER, pivot, width=10)
    pygame.draw.line(scrn, "red", xy, pivot, width=10)
    pygame.draw.circle(scrn, light_blue, pivot, 8)
    pygame.draw.circle(scrn, magenta, xy, 8)
    pygame.draw.circle(scrn, "black", CENTER, 8)
    display_text(scrn, "(a,b)", light_blue, pivot)
    display_text(scrn, "(x,y)", magenta, xy)
    display_text(scrn, "(0,0)", "black", CENTER, x_offset=-20, y_offset=-25)
    pygame.display.flip()

    while True:
        scrn.fill("white")
        draw_grid(scrn, xmax, ymax)

        # get user input for current position
        pygame.event.get()
        if pygame.mouse.get_pressed()[0]:
            xy = pygame.mouse.get_pos()
            # calculate pivot point
            pivot = find_circles_intersection(CENTER[0], CENTER[1], xy[0], xy[1], T, P)
            if pivot is not None:
                all_coords.append(xy)
                all_pivots.append(pivot)

        if pivot is not None:
            if len(all_coords) >= 2:
                pygame.draw.lines(scrn, "black", False, all_coords, width=2)

                try:
                    theta1 = calculate_slope(xy, pivot)
                    theta3 = calculate_slope(all_coords[-2], all_pivots[-2])
                    theta = theta3 - theta1

                    delta_s = math.sqrt(
                        (pivot[0] - all_pivots[-2][0]) ** 2
                        + (pivot[1] - all_pivots[-2][1]) ** 2
                    )
                    M += T * theta + delta_s

                    # display_text(
                    #     scrn,
                    #     str(int(theta * 180 / math.pi)),
                    #     yellow,
                    #     (0, 0),
                    #     x_offset=50,
                    #     y_offset=25,
                    # )
                    # display_text(
                    #     scrn,
                    #     str(int(delta_s)),
                    #     yellow,
                    #     (0, 20),
                    #     x_offset=50,
                    #     y_offset=25,
                    # )
                except ZeroDivisionError:
                    pass

                display_text(
                    scrn, str(int(M)), "black", (0, 0), x_offset=50, y_offset=25
                )

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
            display_text(scrn, "W", yellow, wheel, y_offset=-35)

            pygame.display.flip()
        sleep(0.002)


if __name__ == "__main__":
    main()
