import pygame
import random
import sys
import math

pygame.init()

# --- Настройки экрана ---
WIDTH, HEIGHT = 1100, 2100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уклонение от врагов")
clock = pygame.time.Clock()

# --- Цвета ---
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (225,0,0)
GREEN = (0,255,0)
GOLD = (255,215,0)
BLUE = (0,0,255)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
CYAN = (0,255,255)
RAINBOW = [RED, ORANGE, GOLD, GREEN, CYAN, BLUE, PURPLE]

# --- Фоны ---
MENU_BG = (10, 10, 30)
SHOP_BG = (20, 10, 40)
GAME_BG = (0, 0, 0)

# --- Магазин ---
color_categories = {
    "Простые": {
        "Зеленый": [GREEN, 50],
        "Серый": [(128,128,128), 50],
        "Фиолетовый": [PURPLE, 50],
    },
    "Яркие": {
        "Оранжевый": [ORANGE, 100],
        "Голубой": [CYAN, 100],
        "Золотой": [GOLD, 100],
    },
    "Необыкновенные": {
        "Радужный": [RAINBOW, 150],
    },
}

selected_color = BLUE
coins = 999

# --- Шрифты ---
font = pygame.font.SysFont("monospace", 35)
game_over_font = pygame.font.SysFont("comicsansms", 60)
start_font = pygame.font.SysFont("comicsansms", 50)
tobish_font = pygame.font.SysFont("comicsansms", 100)

# --- Звёзды для игры ---
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(120)]

def draw_star_background(color=WHITE):
    for star in stars:
        star[1] += 2
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0
        pygame.draw.circle(screen, color, star, 2)

# --- Центрированный текст ---
def draw_text_center(text, font, color, center_x, center_y):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(center_x, center_y))
    screen.blit(rendered, rect)

# --- Спиральная анимация ---
def spiral_animation():
    b = 0
    x, y = WIDTH//2, HEIGHT//2
    angle = 0
    pos_list = [(x,y)]
    while b < 200:
        screen.fill(BLACK)  # без фона
        angle += math.radians(b)
        x_new = WIDTH//2 + int(b*3*math.cos(angle))
        y_new = HEIGHT//2 + int(b*3*math.sin(angle))
        pos_list.append((x_new, y_new))
        for i in range(1, len(pos_list)):
            color = RAINBOW[i % len(RAINBOW)]
            pygame.draw.line(screen, color, pos_list[i-1], pos_list[i], 2)
        b +=1
        pygame.display.flip()
        clock.tick(120)

    # Текст "Тобиш" через градацию серого
    for alpha in list(range(255,0,-5)):
        screen.fill(BLACK)
        gray_color = (alpha, alpha, alpha)
        text_surface = tobish_font.render("Тобиш", True, gray_color)
        rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text_surface, rect)
        pygame.display.flip()
        pygame.time.delay(20)

# --- Магазин ---
def shop():
    global selected_color, coins
    category_selected = None
    while True:
        screen.fill(SHOP_BG)
        draw_text_center("Магазин", game_over_font, WHITE, WIDTH//2, 80)
        draw_text_center(f"Монеты: {coins}", font, WHITE, WIDTH//2, 140)
        y_offset = 200
        buttons = []
        if category_selected is None:
            for category in color_categories:
                button = pygame.Rect(WIDTH//2-150, y_offset, 300, 50)
                buttons.append((button, category))
                pygame.draw.rect(screen, GREEN, button)
                draw_text_center(category, font, BLACK, WIDTH//2, y_offset+25)
                y_offset += 70
        else:
            for name, (color, price) in color_categories[category_selected].items():
                button = pygame.Rect(WIDTH//2-100, y_offset, 200, 50)
                buttons.append((button, name, color, price))
                pygame.draw.rect(screen, color if isinstance(color, tuple) else WHITE, button)
                draw_text_center(f"{name} ({price})", font, BLACK, WIDTH//2, y_offset+25)
                y_offset += 80
        back_button = pygame.Rect(WIDTH//2-100, y_offset, 200,50)
        pygame.draw.rect(screen, RED, back_button)
        draw_text_center("Назад", font, BLACK, WIDTH//2, y_offset+25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if category_selected is None:
                    for button, category in buttons:
                        if button.collidepoint(event.pos):
                            category_selected = category
                else:
                    for button, name, color, price in buttons:
                        if button.collidepoint(event.pos):
                            if coins >= price:
                                coins -= price
                                selected_color = color
                if back_button.collidepoint(event.pos):
                    if category_selected is None:
                        return
                    else:
                        category_selected = None
        pygame.display.flip()
        clock.tick(30)

# --- Экран старта ---
def start_screen():
    while True:
        screen.fill(MENU_BG)
        button_rect = pygame.Rect(WIDTH//2-150, HEIGHT//2-50, 300,100)
        shop_button = pygame.Rect(WIDTH//2-100, HEIGHT//2+100, 200,50)
        pygame.draw.rect(screen, GREEN, button_rect)
        pygame.draw.rect(screen, GOLD, shop_button)
        draw_text_center("Start Game", start_font, BLACK, WIDTH//2, HEIGHT//2)
        draw_text_center("Магазин", font, BLACK, WIDTH//2, HEIGHT//2+125)
        draw_text_center(f"Монеты: {coins}", font, WHITE, WIDTH//2, 50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos): return
                if shop_button.collidepoint(event.pos): shop()
        pygame.display.flip()
        clock.tick(30)

# --- Game Over ---
def game_over_screen(final_score):
    while True:
        screen.fill(GAME_BG)
        draw_star_background()
        draw_text_center("GAME OVER", game_over_font, RED, WIDTH//2, HEIGHT//2-100)
        draw_text_center(f"Очки: {final_score}", font, WHITE, WIDTH//2, HEIGHT//2)
        restart_button = pygame.Rect(WIDTH//2-100, HEIGHT//2+100, 200,50)
        pygame.draw.rect(screen, GREEN, restart_button)
        draw_text_center("Restart", font, BLACK, WIDTH//2, HEIGHT//2+125)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos): return

        pygame.display.flip()
        clock.tick(30)

# --- Игровой цикл ---
def game_loop():
    global coins, selected_color
    player_pos = [WIDTH//2, HEIGHT//2]
    enemies = []
    score = 0
    color_index = 0
    enemy_size = 40

    while True:
        screen.fill(GAME_BG)
        draw_star_background()
        if isinstance(selected_color, list):
            color_index = (pygame.time.get_ticks()//200)%len(RAINBOW)
            player_color = RAINBOW[color_index]
        else:
            player_color = selected_color

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEMOTION:
                player_pos[0] = event.pos[0]-25
                player_pos[1] = event.pos[1]-25

        pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], 50,50))

        # --- Враги ---
        if random.randint(1,20)==1:
            side = random.choice(["top","bottom","left","right"])
            if side=="top":
                x = random.randint(0, WIDTH-enemy_size)
                y = -enemy_size
                dx, dy = 0, 4
            elif side=="bottom":
                x = random.randint(0, WIDTH-enemy_size)
                y = HEIGHT
                dx, dy = 0, -4
            elif side=="left":
                x = -enemy_size
                y = random.randint(0, HEIGHT-enemy_size)
                dx, dy = 4, 0
            else:  # right
                x = WIDTH
                y = random.randint(0, HEIGHT-enemy_size)
                dx, dy = -4, 0
            angle = random.uniform(0, 2*math.pi)
            enemies.append({'x': x, 'y': y, 'dx': dx, 'dy': dy, 'angle': angle})

        # --- Обновление врагов ---
        for enemy in enemies[:]:
            enemy['x'] += enemy['dx']
            enemy['y'] += enemy['dy']
            enemy['angle'] += 0.05
            # Синусоидальные колебания для "невесомости"
            enemy['x'] += math.sin(enemy['angle'])*3
            enemy['y'] += math.cos(enemy['angle'])*3
            pygame.draw.rect(screen, RED, (enemy['x'], enemy['y'], enemy_size, enemy_size))

            # --- Столкновение с игроком ---
            if (player_pos[0] < enemy['x'] + enemy_size and player_pos[0] + 50 > enemy['x'] and
                player_pos[1] < enemy['y'] + enemy_size and player_pos[1] + 50 > enemy['y']):
                game_over_screen(score)
                return

            # --- Проверка выхода за экран ---
            if (enemy['x'] < -enemy_size or enemy['x'] > WIDTH or
                enemy['y'] < -enemy_size or enemy['y'] > HEIGHT):
                enemies.remove(enemy)
                score += 1
                if score % 15 == 0:
                    coins += 1

        draw_text_center(f"Счёт: {score}", font, WHITE, WIDTH//2, 30)
        draw_text_center(f"Монеты: {coins}", font, WHITE, WIDTH//2, 70)

        # Победа при 200 очках
        if score >= 200:
            coins += 30
            screen.fill(GAME_BG)
            draw_star_background()
            draw_text_center("YOU WIN!", game_over_font, GREEN, WIDTH//2, HEIGHT//2-50)
            draw_text_center(f"Очки: {score}", font, WHITE, WIDTH//2, HEIGHT//2+30)
            pygame.display.flip()
            pygame.time.delay(3000)
            return

        pygame.display.flip()
        clock.tick(30)

# --- Главный цикл ---
animation_done = False
while True:
    if not animation_done:
        spiral_animation()
        animation_done = True
    start_screen()
    game_loop()