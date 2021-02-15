import pygame
import time
import random
from pygame import mixer


def click_sound():
    mixer.music.load('project_files/click.wav')
    mixer.music.play()
    pygame.mixer.music.set_volume(1)


def destroy_sound():
    mixer.music.load('project_files/destroy.wav')
    mixer.music.play()
    pygame.mixer.music.set_volume(0.5)
    time.sleep(0.2)


def start_sound():
    mixer.music.load('project_files/start.ogg')
    mixer.music.play()
    pygame.mixer.music.set_volume(0.5)
    time.sleep(0.2)


pygame.mixer.init()
pygame.init()
WIDTH, HEIGHT = 800, 900
PYGAMEDISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

font_1 = pygame.font.SysFont('comicsans', 40)
font_2 = pygame.font.SysFont('comicsans', 30)
white, black = (255, 255, 255), (0, 0, 0)

BG = pygame.transform.smoothscale(pygame.image.load(r"project_files/wood_bg.png").convert(),
                                  (WIDTH, HEIGHT))
GREY = pygame.transform.smoothscale(pygame.image.load(r"project_files/grey_block.png").convert(), (89, 89))
RED_TANK = pygame.transform.smoothscale(pygame.image.load(r"project_files/red_player.png").convert(), (89, 89))
BLUE_TANK = pygame.transform.smoothscale(pygame.image.load(r"project_files/blue_player.png").convert(), (89, 89))
LASER = pygame.transform.smoothscale(pygame.image.load(r"project_files/laser.png").convert(), (89, 89))

LASER_GUN = pygame.transform.smoothscale(pygame.image.load(r"project_files/laser_gun.png").convert(), (89, 89))

position_valid = {}
for j in range(7):
    y = 150 + (j * 90)
    for i in range(0, 7):
        x = 85 + (i * 90)
        position_valid[len(position_valid)] = (x, y)

lasers_pos = []
blue_score = 0
red_score = 0
deactivated_robots_list = []
BASIC_BODY = pygame.transform.smoothscale(pygame.image.load(r"project_files/basic-armor.png").convert(), (89, 89))
LIGHT_BODY = pygame.transform.smoothscale(pygame.image.load(r"project_files/light_armor.png").convert(), (89, 89))
BATTLE_BODY = pygame.transform.smoothscale(pygame.image.load(r"project_files/battle_body.png").convert(), (89, 89))


def auto_move(player, enemy_player):
    old_x, old_y = player.x, player.y
    if (abs(player.y - enemy_player.y) / 90) > 1:
        player.move_forward()
    elif (abs(player.x - enemy_player.x) / 90) > 0:
        if abs(player.x - 90 - enemy_player.x - 90) / 90 > abs(player.x - enemy_player.x) / 90:
            player.move_right()
        else:
            player.move_left()
    for grey in deactivated_robots_list:
        while grey.x == player.x and grey.y == player.y and grey.player_img == GREY or grey.x == old_x and grey.y == old_y and grey.player_img == GREY or player.x == enemy_player.x and player.y == enemy_player.y or (
        player.x, player.y) not in position_valid.values():
            player.x, player.y = old_x, old_y
            random_move = random.choice([player.move_right, player.move_left, player.move_forward, player.move_back])
            random_move()
            if (player.x, player.y) not in position_valid.values():
                player.x, player.y = old_x, old_y
                continue
    for grey in deactivated_robots_list:
        if player.x == grey.x and player.y == grey.y and grey.player_img != GREY:
            grey.x = -999999
            grey.y = -999999
            if grey.player_img == EXPLOSION:
                player.gun = "explosion"
                player.gun_img = EXPLOSION
                player.gun_damage = 1
            elif grey.player_img == SWORD:
                player.gun = "sword"
                player.gun_img = SWORD
                player.gun_damage = 2
            elif grey.player_img == BASIC:
                player.gun = "basic"
                player.gun_img = BASIC
            elif grey.player_img == LASER_GUN:
                player.gun = "laser"
                player.gun_img = LASER_GUN
                player.gun_damage = 1
            elif grey.player_img == TWIN_LASER:
                player.gun = "twin_laser"
                player.gun_img = TWIN_LASER
                player.gun_damage = 1
            elif grey.player_img == BASIC_BODY:
                player.body = "simple_body"
                player.body_img = BASIC_BODY
                player.hp = 2
            elif grey.player_img == LIGHT_BODY:
                player.body = "light_body"
                player.body_img = LIGHT_BODY
                player.hp = 3
            elif grey.player_img == BATTLE_BODY:
                player.body = "battle_body"
                player.body_img = BATTLE_BODY
                player.hp = 5
    player.movement -= 1

    if player.movement >= 2:
        auto_move(player, enemy_player)
        player.movement += 1

    player.fire_shell()
    for (x, y) in lasers_pos:
        if enemy_player.x == x and enemy_player.y == y:
            if enemy_player.body == "simple_body":
                enemy_player.initial_hp = 2
            elif enemy_player.body == "light_body":
                enemy_player.initial_hp = 3
            elif enemy_player.body == "battle_body":
                enemy_player.initial_hp = 5
            enemy_player.hp -= player.gun_damage
            enemy_player.health = (enemy_player.hp / enemy_player.initial_hp) * 100
            if enemy_player.health < 0:
                enemy_player.health = 0


EXPLOSION = pygame.transform.smoothscale(pygame.image.load(r"project_files/exploison.png").convert(), (89, 89))
BASIC = pygame.transform.smoothscale(pygame.image.load(r"project_files/basic.png").convert(), (89, 89))
TWIN_LASER = pygame.transform.smoothscale(pygame.image.load(r"project_files/twin_laser.png").convert(), (89, 89))
SWORD = pygame.transform.smoothscale(pygame.image.load(r"project_files/sword.png").convert(), (89, 89))


class DeactivatedRobot(pygame.sprite.Sprite):
    global turn, pos_grey

    def __init__(self, pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.active = False
        self.y = pos[1]
        self.player_img = image
        self.x = pos[0]

    def draw_tank(self):
        PYGAMEDISPLAY.blit(self.player_img, (self.x, self.y))


class Tanks(pygame.sprite.Sprite):
    global turn, pos_grey

    def __init__(self, pos, image, color):
        pygame.sprite.Sprite.__init__(self)
        self.gun = "basic"
        self.gun_damage = 1
        self.color = color
        self.movement = 1
        self.y = pos[1]
        self.hp = 2
        self.body = "simple_body"
        self.player_img = image
        self.gun_img = BASIC
        self.body_img = BASIC_BODY
        self.x = pos[0]
        self.health = 100
        self.initial_hp = 2

    def draw_tank(self):
        PYGAMEDISPLAY.blit(self.player_img, (self.x, self.y))

    def move_forward(self):
        if self.color == "blue":
            self.y += 90
        else:
            self.y -= 90

    def move_right(self):
        self.x += 90

    def move_left(self):
        self.x += -90

    def move_back(self):
        if self.color == "blue":
            self.y -= 90
        else:
            self.y += 90

    def fire_shell(self):
        if self.gun == 'basic':
            if self.color == "blue":
                lasers_pos.append((self.x, self.y + 90))
            else:
                lasers_pos.append((self.x, self.y - 90))
        elif self.gun == "laser":
            if self.color == "blue":
                for i in range(1, 7):
                    lasers_pos.append((self.x, self.y + 90 * i))
            else:
                for i in range(1, 7):
                    lasers_pos.append((self.x, self.y - 90 * i))
        elif self.gun == "twin_laser":
            if self.color == "blue":
                for i in range(1, 7):
                    lasers_pos.append((self.x + 90 * i, self.y))
                    lasers_pos.append((self.x - 90 * i, self.y))
            else:
                for i in range(1, 7):
                    lasers_pos.append((self.x + 90 * i, self.y))
                    lasers_pos.append((self.x - 90 * i, self.y))
        elif self.gun == "sword":
            if self.color == "blue":
                lasers_pos.append((self.x, self.y + 90))
                lasers_pos.append((self.x + 90, self.y + 90))
                lasers_pos.append((self.x - 90, self.y + 90))
            else:
                lasers_pos.append((self.x, self.y - 90))
                lasers_pos.append((self.x + 90, self.y - 90))
                lasers_pos.append((self.x - 90, self.y - 90))
        elif self.gun == "explosion":
            if self.color == "blue":
                lasers_pos.append((self.x, self.y + 90))
                lasers_pos.append((self.x + 90, self.y + 90))
                lasers_pos.append((self.x - 90, self.y + 90))
                lasers_pos.append((self.x - 90, self.y))
                lasers_pos.append((self.x + 90, self.y))
                lasers_pos.append((self.x + 90, self.y - 90))
                lasers_pos.append((self.x - 90, self.y - 90))
                lasers_pos.append((self.x, self.y - 90))
            else:
                lasers_pos.append((self.x, self.y - 90))
                lasers_pos.append((self.x + 90, self.y - 90))
                lasers_pos.append((self.x - 90, self.y - 90))
                lasers_pos.append((self.x - 90, self.y))
                lasers_pos.append((self.x + 90, self.y))
                lasers_pos.append((self.x + 90, self.y + 90))
                lasers_pos.append((self.x - 90, self.y + 90))
                lasers_pos.append((self.x, self.y + 90))
        temp_lasers_list = []
        for x, y in lasers_pos:
            for grey in deactivated_robots_list:
                if x == grey.x and y == grey.y:
                    if grey.player_img == GREY:
                        grey.player_img = random.choice(
                            [BASIC_BODY, LIGHT_BODY, BATTLE_BODY, BASIC, LASER_GUN, TWIN_LASER, EXPLOSION, SWORD])
            if (x, y) in position_valid.values():
                temp_lasers_list.append((x, y))
        lasers_pos.clear()
        lasers_pos.extend(temp_lasers_list)


def main(number_of_deactivated_robots):
    global blue_score, red_score
    clock = pygame.time.Clock()
    stop = False
    red_score = 0
    blue_score = 0
    red_1 = Tanks(position_valid[random.randint(42, 48)], RED_TANK, "red")
    blue_1 = Tanks(position_valid[random.randint(0, 6)], BLUE_TANK, "blue")
    robot_turn = "red"

    def reset_the_game():
        (red_1.x, red_1.y) = position_valid[random.randint(42, 48)]
        (blue_1.x, blue_1.y) = position_valid[random.randint(0, 6)]
        for player in [red_1, blue_1]:
            if player.body == "simple_body":
                player.hp = 2
                player.health = 100
                player.movement = 1
            elif player.body == "light_body":
                player.hp = 3
                player.health = 100
                player.movement = 2
            else:
                player.hp = 5
                player.health = 100
                player.movement = 1
        lasers_pos.clear()
        deactivated_robots_list.clear()
        draw_deactivated_robots()
        paint_pygame_windows()

    def draw_health():
        font = pygame.font.Font(None, 30)
        pygame.draw.line(PYGAMEDISPLAY, black, (400, 0), (400, 150), 6)
        red_player_text = font.render(f"RED PLAYER SCORE:-- {red_score}", True, (255, 0, 0))
        blue_player_text = font.render(f"BLUE PLAYER SCORE:-- {blue_score}", True, (0, 0, 255))
        pygame.draw.rect(PYGAMEDISPLAY, (255, 0, 0), (85, 30, 300 * red_1.health / 100, 30), border_radius=8)
        pygame.draw.rect(PYGAMEDISPLAY, black, (85, 30, 300, 30), 6, border_radius=8)
        # blue player
        pygame.draw.rect(PYGAMEDISPLAY, (0, 0, 255), (430, 30, 300 * blue_1.health / 100, 30), border_radius=8)
        pygame.draw.rect(PYGAMEDISPLAY, black, (430, 30, 300, 30), 6, border_radius=8)

        PYGAMEDISPLAY.blit(red_player_text, (130, 5))
        PYGAMEDISPLAY.blit(blue_player_text, (470, 5))

        for player in [red_1, blue_1]:
            if player == red_1:
                IMAGE_SMALL_BODY = pygame.transform.scale(player.body_img, (50, 50))
                IMAGE_SMALL_GUN = pygame.transform.scale(player.gun_img, (50, 50))
                PYGAMEDISPLAY.blit(IMAGE_SMALL_BODY, (180, 70))
                PYGAMEDISPLAY.blit(IMAGE_SMALL_GUN, (230, 70))
                pygame.draw.rect(PYGAMEDISPLAY, black, (180, 70, 100, 50), 2, border_radius=8)
            else:
                IMAGE_SMALL_BODY = pygame.transform.scale(player.body_img, (50, 50))
                IMAGE_SMALL_GUN = pygame.transform.scale(player.gun_img, (50, 50))
                PYGAMEDISPLAY.blit(IMAGE_SMALL_BODY, (530, 70))
                PYGAMEDISPLAY.blit(IMAGE_SMALL_GUN, (580, 70))
                pygame.draw.rect(PYGAMEDISPLAY, black, (530, 70, 100, 50), 2, border_radius=8)

    def paint_pygame_windows():
        global blue_score, red_score
        PYGAMEDISPLAY.blit(BG, (0, 0))
        pygame.draw.rect(PYGAMEDISPLAY, (50, 50, 50), (85, 150, 630, 630))
        pygame.draw.rect(PYGAMEDISPLAY, (173, 228, 255), (85, 150, 630, 90))
        pygame.draw.rect(PYGAMEDISPLAY, (186, 97, 104), (85, 690, 630, 90))
        draw_health()

        red_1.draw_tank()
        blue_1.draw_tank()

        if len(lasers_pos) != 0:
            for x in deactivated_robots_list:
                x.draw_tank()
            for i in range(8):
                pygame.draw.line(PYGAMEDISPLAY, white, (85 + (i * 90), 150), (85 + (i * 90), 780), 3)
                for i in range(8):
                    pygame.draw.line(PYGAMEDISPLAY, white, (85, 150 + (i * 90)), (715, 150 + (i * 90)), 3)
            for x in lasers_pos:
                PYGAMEDISPLAY.blit(LASER, x)

            lasers_pos.clear()
            pygame.display.update()
            time.sleep(0.5)
            pygame.event.clear()
            paint_pygame_windows()
        for x in deactivated_robots_list:
            x.draw_tank()
        for i in range(8):
            pygame.draw.line(PYGAMEDISPLAY, white, (85 + (i * 90), 150), (85 + (i * 90), 780), 3)
            for i in range(8):
                pygame.draw.line(PYGAMEDISPLAY, white, (85, 150 + (i * 90)), (715, 150 + (i * 90)), 3)
        if red_1.hp <= 0:
            blue_score += 1
            red_1.hp = 2
            blue_1.hp = 2
            blue_1.health = 100
            red_1.health = 100
            destroy_sound()
            reset_the_game()
            pygame.event.clear()
        elif blue_1.hp <= 0:
            red_score += 1
            red_1.hp = 2
            red_1.health = 100
            blue_1.hp = 2
            blue_1.health = 100
            destroy_sound()
            reset_the_game()
            pygame.event.clear()
        pygame.display.update()

    def draw_deactivated_robots():
        temp_list = [x for x in range(7, 42)]
        random.shuffle(temp_list)
        for i in temp_list[:int(number_of_deactivated_robots)]:
            deactivated_robots_list.append(DeactivatedRobot(position_valid[i], GREY))

    draw_deactivated_robots()
    start_sound()
    while not stop:
        clock.tick(60)
        paint_pygame_windows()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound()
                if robot_turn == "red":
                    red_1.movement = 2
                    if red_1.body == "light_body":
                        red_1.movement = 3
                    auto_move(red_1, blue_1)
                    robot_turn = "blue"
                else:
                    blue_1.movement = 2
                    if blue_1.body == "light_body":
                        blue_1.movement = 3
                    auto_move(blue_1, red_1)
                    pygame.event.clear()
                    robot_turn = "red"
                pass


if __name__ == "__main__":
    main(7)
