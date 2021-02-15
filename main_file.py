import pygame
import threading
from pygame import mixer
from input import input_box
from main_module import main as main_module

number_of_grey = "7"
WIDTH, HEIGHT = 800, 900
GAMEDISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
MENU_IMG = pygame.transform.smoothscale(pygame.image.load(r"project_files/menu.png").convert(),
                                        (WIDTH, HEIGHT))
GAMEDISPLAY.fill((0, 0, 0))
white = (255, 255, 255)

mixer.init()
pygame.init()

def hover_sound():
    mixer.music.load('project_files/hover.wav')
    mixer.music.play()
    pygame.mixer.music.set_volume(0.1)

def click_sound():
    mixer.music.load('project_files/click.wav')
    mixer.music.play()
    pygame.mixer.music.set_volume(1)

def main():
    global number_of_grey
    clock = pygame.time.Clock()
    selected_option = 1

    def redraw_windows():
        GAMEDISPLAY.blit(MENU_IMG, (0, 0))
        draw_rectangle()
        pygame.display.update()

    def draw_rectangle():
        if selected_option == 0:
            pygame.draw.line(GAMEDISPLAY, (0, 0, 0), (236, 267), (584, 267), 3)
            pygame.draw.line(GAMEDISPLAY, (0, 0, 0), (236, 335), (584, 335), 3)
        elif selected_option == 1:
            pygame.draw.line(GAMEDISPLAY, (0, 0, 0), (188, 439), (638, 439), 3)
            pygame.draw.line(GAMEDISPLAY, (0, 0, 0), (316, 589), (512, 589), 3)
        elif selected_option == 2:
            pygame.draw.line(GAMEDISPLAY, (0, 0, 0), (342, 665), (486, 665), 3)
            pygame.draw.line(GAMEDISPLAY, (0, 0, 0), (342, 733), (486, 733), 3)
    while True:
        clock.tick(60)
        redraw_windows()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                if event.pos[0] in range(236, 586) and event.pos[1] in range(272, 327):
                    if selected_option != 0:
                        threading.Thread(target=hover_sound).start()
                    selected_option = 0

                elif event.pos[0] in range(185, 524) and event.pos[1] in range(447, 583):
                    if selected_option != 1:
                        threading.Thread(target=hover_sound).start()
                    selected_option = 1
                elif event.pos[0] in range(347, 465) and event.pos[1] in range(676, 728):
                    if selected_option != 2:
                        threading.Thread(target=hover_sound).start()
                    selected_option = 2
                else:
                    selected_option = 1000
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(236, 586) and event.pos[1] in range(272, 327):
                    threading.Thread(target=click_sound).start()
                    main_module(number_of_grey)
                elif event.pos[0] in range(185, 524) and event.pos[1] in range(447, 583):
                    threading.Thread(target=click_sound).start()
                    number_of_grey = input_box().strip()
                    number_of_grey = int(number_of_grey)

                elif event.pos[0] in range(347, 465) and event.pos[1] in range(676, 728):
                    pygame.quit()
                    quit()
                else:
                    pass


if __name__ == "__main__":
    main()
