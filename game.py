from modules.window import Window, Background, CoordinateManager
from modules.enemy import Enemy, WaveController
from modules.tower import Tower, Projectile
from modules.player import Player
from modules.button import Button
import pygame, sys, os

pygame.init()

# Set up the drawing window
win = Window(1286, 768)
screen = win._screen

# create main background
main_background = Background("./assets/backgrounds/map.png", [0, 0])

# create menu background
menu_background = Background("./assets/backgrounds/menu-bg.png", [0, 0])

# create player
player = Player()

# create coordinate manager
coordinate_manager = CoordinateManager()

wave_controller = WaveController()

# Create a custom event for adding a new enemy every second
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)
# Create a custom event for adding waves
ADDWAVE = pygame.USEREVENT + 2

# handle framerate
clock = pygame.time.Clock()

font = pygame.font.Font("assets/font.ttf", 36)
current_score = 0

def add_score(base_score, multiplier=1):
    global current_score
    current_score += base_score * multiplier

def end_game():
    final_score = current_score + (player.money * 10)
    game_over(final_score)

def input_name():
    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        screen.fill((255, 255, 255))
        txt_surface = font.render(name, True, (0, 0, 0))
        width = max(200, txt_surface.get_width()+10)
        pygame.draw.rect(screen, (0, 0, 0), (100, 100, width, 32), 2)
        screen.blit(txt_surface, (100, 100))
        pygame.display.flip()
    return name

def game_over(score):
    name = input_name()
    with open("scoreboard.txt", "a") as file:
        file.write(f"{name}: {score}\n")

def show_scoreboard():
    scores = []
    with open("scoreboard.txt", "r") as file:
        for line in file:
            name, score = line.strip().split(": ")
            scores.append((name, int(score)))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    while True:
        screen.fill((200, 200, 200))
        y = 50
        for i, (name, score) in enumerate(sorted_scores):
            text = font.render(f"{i+1}. {name}: {score}", True, (0, 0, 0))
            screen.blit(text, (100, y))
            y += 30
        pygame.display.flip()    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

def play():
    global current_score
    current_score = 0
    # set display caption
    pygame.display.set_caption("Canyon Defenders")
    # main game loop
    while True:
        # get events
        for event in pygame.event.get():
            # handle quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # handle enemy spawn
            elif event.type == ADDENEMY:
                wave_index = wave_controller._wave_index
                if wave_controller._spawn_count < wave_controller._enemy_numbers[wave_index]:
                    wave_controller._spawn_count += 1
                    # create new enemy 
                    new_enemy = Enemy(wave_controller._enemy_healths[wave_index] , wave_controller._enemy_speeds[wave_index], wave_controller._enemy_rewards[wave_index], coordinate_manager._waypoints)
                    win.all_sprites.add(new_enemy)
                    win.enemies.add(new_enemy)
                # We need 5 seconds delay here 
                else:
                    # If wave is finished
                    if len(win.enemies) == 0:
                        # handle game win
                        if wave_index >= len(wave_controller._enemy_numbers):
                            pygame.quit()
                            sys.exit()
                        # Stop the ADDENEMY event
                        pygame.time.set_timer(ADDENEMY, 0)
                        # Set the DELAYWAVE event to trigger after 5 seconds
                        pygame.time.set_timer(ADDWAVE, 5000)
                        wave_controller._spawn_count = 0
                        wave_controller._wave_index += 1
            elif event.type == ADDWAVE:
                # Stop the ADDWAVE event
                pygame.time.set_timer(ADDWAVE, 0)
                # Start the next wave by setting the ADDENEMY event to trigger again
                pygame.time.set_timer(ADDENEMY, wave_controller._enemy_rate[wave_controller._wave_index])


            # handle tower buy 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # get mouse position
                pos = pygame.mouse.get_pos()

                for i in range(len(coordinate_manager.buy_tower_coords)):
                    x = win._SCREEN_WIDTH//2 - coordinate_manager.buy_tower_coords[i]["tower"].get_width()//2 + (i-1.5)*1.5*coordinate_manager.buy_tower_coords[i]["tower"].get_width()
                    y = 15
                    # check if user clicked a tower buy image
                    if x < pos[0] < x + coordinate_manager.buy_tower_coords[i]["tower"].get_width() and y < pos[1] < y + coordinate_manager.buy_tower_coords[i]["tower"].get_height():
                        win.mouse_pressed = True
                        win.purchased_tower = coordinate_manager.determine_tower(coordinate_manager.buy_tower_coords[i]['tower_price'], coordinate_manager.buy_tower_coords[i]["tower"])
                # Check if the user clicked on a tower to upgrade
                for tower in win.towers:
                    if tower.rect.collidepoint(pos):
                        upgrade_button = Button(image=pygame.image.load("assets/Upgrade Button2.png"), 
                                                pos=(tower.rect.centerx - 20, tower.rect.bottom + 10),
                                                #pos=(tower.rect.right + 10, tower.rect.top),
                                                text_input="UPGRADE", font=get_font(20), 
                                                base_color=(215, 252, 212), hovering_color=(255, 255, 255))
                        screen.blit(upgrade_button.image, upgrade_button.rect)
                        # Check for mouse click on the upgrade button
                        if upgrade_button.check_for_input(pos):
                        # Check if the player has enough money for the upgrade
                            if tower.level < 3 and player.money >= tower.upgrade_cost:
                            # Deduct the upgrade cost from player's money
                                player.money -= tower.upgrade_cost
                                # Upgrade the tower
                                tower.upgrade()
                            else:
                                print("Tower is already at maximum level")
                        else:
                            # Player does not have enough money for the upgrade
                            print("Not enough money for the upgrade")
            # handle drop 
            elif event.type == pygame.MOUSEBUTTONUP:
                win.mouse_pressed = False
                # get mouse position
                pos = pygame.mouse.get_pos()
                # If user purchased a tower
                if win.purchased_tower:
                    # check if mouse coordinate is valid
                    valid_coordinate = coordinate_manager.is_coordinate_valid_placement_point(pos[0], pos[1], coordinate_manager._placement_blocks, win, player)
                    
                    if valid_coordinate[0] and valid_coordinate[1]:
                        # coordinate is valid, create new tower 
                        player.money -= win.purchased_tower["price"]
                        # get towers x,y position
                        x = valid_coordinate[0]["x"] + (valid_coordinate[0]["width"] / 2)
                        y = valid_coordinate[0]["y"] + (valid_coordinate[0]["height"] / 2)
                        # create new tower with purchased tower 
                        new_tower = Tower(valid_coordinate[1],win.purchased_tower["range"], win.purchased_tower["damage"], win.purchased_tower["img"], win.purchased_tower["shooting_speed"], win.purchased_tower["shooting_rate"], valid_coordinate[0]["width"], valid_coordinate[0]["height"], x, y)
                        # add tower to the sprite groups
                        win.all_sprites.add(new_tower)
                        win.towers.add(new_tower)
                        # set the purchased tower to none
                        win.purchased_tower = None

        # handle dragging purchased tower 
        if win.mouse_pressed:
            # get mouse position
            pos = pygame.mouse.get_pos()
            # calculate the position of the top-left corner of the tower image
            x = pos[0] - win.purchased_tower["surface"].get_width() // 2
            y = pos[1] - win.purchased_tower["surface"].get_height() // 2
            # blit the tower image to the screen at the new position
            screen.blit(win.purchased_tower["surface"], (x, y))
            # Set purchased tower to default (None)
            pygame.display.update()

        # handle when player out of health
        if player.health <= 0:
            # this will change
            end_game()
            pygame.quit()
            sys.exit()
    
        # add background
        screen.blit(main_background._image, main_background._rect)

        # draw all sprites
        for entity in win.all_sprites:
            screen.blit(entity._surf, entity.rect)

        # make enemies move and draw their health
        for enemy in win.enemies:
            enemy.draw_health(screen, win)
            enemy.update(player)   
            
        # add projectiles to enemies in range
        for tower in win.towers:
            tower.draw_level(screen)
            tower.draw_range_box(screen)
            # find the enemies in towers range
            range_enemies = [enemy for enemy in win.enemies if tower.range_box.colliderect(enemy.rect)]
            # set towers shooting rate delay
            if tower.shoot_timer >= tower._shooting_rate:
                tower.shoot_timer = 0
                if range_enemies:
                    # shoot projectile to first locked out enemy
                    new_projectile = Projectile(tower, range_enemies[0])
                    win.all_sprites.add(new_projectile)
                    win.projectiles.add(new_projectile)
            else:
                tower.shoot_timer += 1
        
        # shoot all projectiles
        for projectile in win.projectiles:
            if projectile._enemy.rect.x > 0:
                # projectile folllows the enemy
                projectile.update(win)
                if projectile.rect.colliderect(projectile._enemy.rect):
                    # when projectile hits the enemy, reflect the damage to enemy and kill the projectile
                    projectile._enemy.health -= projectile._tower._damage
                    if projectile._enemy.health <= 0:
                        add_score(50)  # 적을 죽일 때마다 50점 추가
                    projectile.kill()

        # 루프 내에 업그레이드 버튼 렌더링 코드 추가
        for tower in win.towers:
            if tower.upgrade_button_active:
                pygame.draw.rect(screen, upgrade_button_color, tower.upgrade_button_rect)

        # draw players health and money
        player.draw_player_info(screen)
        # draw wave number
        wave_controller.draw_wave_info(screen)
        # draw towers to buy
        coordinate_manager.show_tower_buy(screen, win)
        
        # set framerate to 60 
        # clock.tick(60)
        # Flip the display
        pygame.display.flip()
    
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def menu():
    # set display caption
    pygame.display.set_caption("menu")
    while True:
        # blit background
        screen.blit(menu_background._image, menu_background._rect)
        # get mouse position
        mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(60).render("CANYON DEFENDERS", True, (152, 213, 234))
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 200), 
                                text_input="PLAY", font=get_font(45), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 600), 
                                text_input="QUIT", font=get_font(45), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        score_button = Button(image=pygame.image.load("assets/Score Rect.png"), pos=(640, 400), 
                                text_input="SCORE", font=get_font(45), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        screen.blit(menu_text, menu_rect)

        for button in [play_button, quit_button, score_button]:
                button.change_color(mouse_pos)
                button.update(screen)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(mouse_pos):
                    print("Play button clicked")
                    play()
                elif quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif score_button.check_for_input(mouse_pos):
                #else:
                    print("Score button clicked")
                    show_scoreboard()
        pygame.display.update()
menu()
