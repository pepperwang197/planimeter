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

    print("circle 1", y_vals_circle1_int)
    print("circle 2", y_vals_circle2_int)

    return (int(x_pivot), list(y_vals_circle1_int & y_vals_circle2_int)[0])


def main():

    scrn = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("image")

    P = 250
    T = 250
    CENTER = (300, 300)

    xy = (0, 0)
    pivot = (0, 0)

    all_coords = []

    while True:
        scrn.fill("black")

        # get user input for current position
        pygame.event.get()
        if pygame.mouse.get_pressed()[0]:
            xy = pygame.mouse.get_pos()
            all_coords.append(xy)
            # calculate pivot point
            pivot = find_intersection(CENTER[0], CENTER[1], xy[0], xy[1], T, P)
            print(pivot)

        if len(all_coords) >= 2:
            pygame.draw.lines(scrn, "white", False, all_coords)

        if pivot[0] != 0 and pivot[1] != 0:
            pygame.draw.line(scrn, "blue", CENTER, pivot, width=10)
            pygame.draw.line(scrn, "red", xy, pivot, width=10)

        pygame.display.flip()
        sleep(0.002)


if __name__ == "__main__":
    main()
