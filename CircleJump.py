
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 400
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Set up colors
background_color = (135, 206, 250)
bird_color = (255, 255, 0)
pipe_color = (34, 139, 34)
text_color = (255, 255, 255)

# Set up the bird
bird_radius = 20
bird_x = 100
bird_y = window_height // 2
bird_velocity = 0
gravity = 0.5

# Set up the pipes
pipe_width = 50
pipe_gap = 300  # Increased gap size
pipe_x = window_width
pipe_heights = [random.randint(50, 250) for _ in range(5)]  # Decreased maximum pipe height
pipe_speed = 2

# Set up the game clock
clock = pygame.time.Clock()

# Set up the score
score = 0
high_score = 0
score_font = pygame.font.Font(None, 36)

# Set up the start menu
start_font = pygame.font.Font(None, 48)
start_text = start_font.render("Press SPACE to Start", True, text_color)
start_text_rect = start_text.get_rect(center=(window_width // 2, window_height // 2))

# Set up the try again button
button_width = 200
button_height = 50
button_x = (window_width - button_width) // 2
button_y = window_height // 2 + 100
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
button_color = (0, 0, 255)
button_text = start_font.render("Try Again", True, text_color)
button_text_rect = button_text.get_rect(center=button_rect.center)

# Game states
START = 0
PLAYING = 1
GAME_OVER = 2
game_state = START

# Function to reset the game
def reset_game():
    global bird_y, bird_velocity, pipe_x, pipe_heights, pipe_gap, score, pipe_speed
    bird_y = window_height // 2
    bird_velocity = 0
    pipe_x = window_width
    pipe_heights = [random.randint(150, 250) for _ in range(5)]
    pipe_gap = 300
    score = 0
    pipe_speed = 2

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == START:
                    game_state = PLAYING
                elif game_state == PLAYING:
                    bird_velocity = -10
            elif event.key == pygame.K_RETURN and game_state == GAME_OVER:
                game_state = START

        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == GAME_OVER:
            if button_rect.collidepoint(event.pos):
                reset_game()
                game_state = START

    if game_state == PLAYING:
        # Update bird position
        bird_velocity += gravity
        bird_y += bird_velocity

        # Update pipe positions
        pipe_x -= pipe_speed

        # Increase speed gradually based on the score
        if score > 0 and score % 10 == 0 and pipe_speed < 10:
            pipe_speed += 0.1

        if pipe_x < -pipe_width:
            pipe_x = window_width
            pipe_heights.pop(0)
            pipe_heights.append(random.randint(50, 250))
            pipe_gap = random.randint(300, 600)

        # Check collision with pipes
        for i in range(len(pipe_heights)):
            if bird_x + bird_radius > pipe_x and bird_x - bird_radius < pipe_x + pipe_width:
                if bird_y - bird_radius < pipe_heights[i] or bird_y + bird_radius > pipe_heights[i] + pipe_gap:
                    game_state = GAME_OVER
                    if score > high_score:
                        high_score = score
                    score = 0

        # Check collision with window boundaries
        if bird_y > window_height or bird_y < 0:
            game_state = GAME_OVER
            if score > high_score:
                high_score = score
            score = 0

        # Update score
        if pipe_x + pipe_width < bird_x:
            score += 1

    # Draw background
    window.fill(background_color)

    if game_state == START:
        # Draw start menu
        window.blit(start_text, start_text_rect)
    elif game_state == PLAYING:
        # Draw bird
        pygame.draw.circle(window, bird_color, (bird_x, int(bird_y)), bird_radius)

        # Draw pipes
        for i in range(len(pipe_heights)):
            pygame.draw.rect(window, pipe_color, (pipe_x, 0, pipe_width, pipe_heights[i]))
            pygame.draw.rect(window, pipe_color, (pipe_x, pipe_heights[i] + pipe_gap, pipe_width, window_height - (pipe_heights[i] + pipe_gap)))

        # Draw score
        score_text = score_font.render(f"Score: {score}", True, text_color)
        window.blit(score_text, (10, 10))
        # Draw high score
        high_score_text = score_font.render(f"High Score: {high_score}", True, text_color)
        window.blit(high_score_text, (10, 50))
    elif game_state == GAME_OVER:
        # Draw game over message
        game_over_font = pygame.font.Font(None, 48)
        game_over_text = game_over_font.render("Game Over", True, text_color)
        game_over_text_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(game_over_text, game_over_text_rect)
        # Draw current score
        current_score_text = score_font.render(f"Score: {score}", True, text_color)
        current_score_rect = current_score_text.get_rect(center=(window_width // 2, window_height // 2 + 50))
        window.blit(current_score_text, current_score_rect)
        # Draw high score
        high_score_text = score_font.render(f"High Score: {high_score}", True, text_color)
        high_score_rect = high_score_text.get_rect(center=(window_width // 2, window_height // 2 + 90))
        window.blit(high_score_text, high_score_rect)
        # Draw the try again button
        pygame.draw.rect(window, button_color, button_rect)
        window.blit(button_text, button_text_rect)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(90)

# Quit the game
pygame.quit()