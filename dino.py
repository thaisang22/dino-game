import pygame
pygame.init()
clock = pygame.time.Clock()

# Title
pygame.display.set_caption("Dino Game")
icon = pygame.image.load(r'./assets/dinosaur.png')
pygame.display.set_icon(icon)

# Window game
screen = pygame.display.set_mode((600, 300))

# Images
bg = pygame.image.load(r'./assets/background.jpg')
tree = pygame.image.load(r'./assets/tree.png')
dino = pygame.image.load(r'./assets/dinosaur.png')

# Font for score and game over text
font = pygame.font.Font(None, 36)

# Create variables
bg_x, bg_y = 0, 0
tree_x, tree_y = 550, 230
dino_x, dino_y = 50, 230
x_default = 5
jump = False
jump_height = 15
jump_count = 0
score = 0
game_over = False

def reset_game():
    global bg_x, tree_x, dino_y, jump, jump_count, score, game_over, x_default
    bg_x, tree_x = 0, 550
    dino_y = 230
    jump = False
    jump_count = 0
    score = 0
    game_over = False
    x_default = 5

def increase_speed(score):
    return 5 + (score // 5)  # Increase speed every 5 points

# Game loop
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and jump_count < 2 and not game_over:
                jump = True
                jump_vel = jump_height
                jump_count += 1
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse_x, mouse_y):
                reset_game()

    if not game_over:
        # Adjust speed based on score
        x_default = increase_speed(score)
        
        # Background movement
        bg_hcn = screen.blit(bg, (bg_x, bg_y))
        bg2_hcn = screen.blit(bg, (bg_x + 600, bg_y))
        bg_x -= x_default
        if bg_x == -600:
            bg_x = 0

        # Tree movement
        tree_hcn = screen.blit(tree, (tree_x, tree_y))
        tree_x -= x_default
        if tree_x < -tree.get_width():
            tree_x = 600
            score += 1  # Increment score when the tree passes the dinosaur

        # Dino jump
        if jump:
            dino_y -= jump_vel
            jump_vel -= 1
            if jump_vel < -jump_height:
                jump = False
                dino_y = 230
                jump_count = 0  # Reset jump count after the dinosaur lands

        # Dino position
        dino_hcn = screen.blit(dino, (dino_x, dino_y))

        # Collision detection
        if dino_hcn.colliderect(tree_hcn):
            game_over = True

    else:
        # Display Game Over message
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        screen.blit(game_over_text, (250, 130))
        
        # Display Restart button
        restart_button = pygame.Rect(250, 160, 100, 40)
        pygame.draw.rect(screen, (0, 255, 0), restart_button)
        restart_text = font.render('Restart', True, (255, 255, 255))
        screen.blit(restart_text, (260, 170))

    # Display score
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
