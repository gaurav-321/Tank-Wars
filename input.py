import pygame as pg

pg.init()


def input_box():
    screen = pg.display.set_mode((800, 900))
    MENU_IMG = pg.transform.smoothscale(pg.image.load(r"project_files/bg_empty.png").convert(),
                                        (800, 900))

    font = pg.font.Font(None, 50)
    clock = pg.time.Clock()
    input_box = pg.Rect(400, 350, 140, 35)
    info_text = font.render(f"ENTER NUMBER OF ROBOTS", True, (0, 0, 0))
    font = pg.font.Font(None, 35)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = '7'
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                return int(text)
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        done = True
                        return text

                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        screen.blit(MENU_IMG, (0, 0))
        # Render the current text.
        txt_surface = font.render(text, True, (255, 255, 255))
        # Resize the box if the text is too long.
        width = max(25, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)
        screen.blit(info_text, (180, 280))
        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    TEXT = input_box()


