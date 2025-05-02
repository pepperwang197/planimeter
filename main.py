from time import sleep
import pygame
import sympy


def find_intersection(x1, y1, x2, y2, r1, r2):
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


def display_text(scrn, text, color, coords, x_offset=10, y_offset=25):
    pygame.font.init()
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = (coords[0] + x_offset, coords[1] + y_offset)
    scrn.blit(text, text_rect)


def draw_grid(scrn, xmax, ymax, interval=20):
    for i in range(0, xmax, interval):
        pygame.draw.line(scrn, pygame.Color("#bfbfbf"), (i, 0), (i, ymax))

    for i in range(0, ymax, interval):
        pygame.draw.line(scrn, pygame.Color("#bfbfbf"), (0, i), (xmax, i))


def main():

    xmax = 500
    ymax = 500

    scrn = pygame.display.set_mode((xmax, ymax))
    pygame.display.set_caption("Planimeter simulation")

    P = 300
    T = 300
    CENTER = (100, 100)

    all_coords = []
    # wheel_positions = []  ############

    light_blue = pygame.Color("#1d88c2")
    magenta = pygame.Color("#b33484")

    scrn.fill("white")
    xy = (400, 200)
    pivot = find_intersection(CENTER[0], CENTER[1], xy[0], xy[1], T, P)
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
            pivot = find_intersection(CENTER[0], CENTER[1], xy[0], xy[1], T, P)
            if pivot is not None:
                all_coords.append(xy)

        if pivot is not None:
            if len(all_coords) >= 2:
                pygame.draw.lines(scrn, "black", False, all_coords, width=2)

            # wheel = (
            #     xy[0] + (pivot[0] - xy[0]) / 2,
            #     xy[1] + (pivot[1] - xy[1]) / 2,
            # )  ###############
            # wheel_positions.append(wheel)  ###########
            # if len(wheel_positions) >= 2:
            #     pygame.draw.lines(
            #         scrn, "orange", False, wheel_positions, width=2
            #     )  ###############

            pygame.draw.line(scrn, "blue", CENTER, pivot, width=10)
            pygame.draw.line(scrn, "red", xy, pivot, width=10)
            pygame.draw.circle(scrn, light_blue, pivot, 8)
            pygame.draw.circle(scrn, magenta, xy, 8)
            pygame.draw.circle(scrn, "black", CENTER, 8)
            display_text(scrn, "(a,b)", light_blue, pivot)
            display_text(scrn, "(x,y)", magenta, xy)
            display_text(scrn, "(0,0)", "black", CENTER, x_offset=-20, y_offset=-25)
            pygame.display.flip()
        sleep(0.002)


if __name__ == "__main__":
    main()
