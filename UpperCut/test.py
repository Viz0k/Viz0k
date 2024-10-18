import pygame

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))

running = True
key_pressed = False  # To track the first press

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Detect single press of the SPACE key
    if keys[pygame.K_SPACE] and not key_pressed:
        print("Spacebar pressed!")
        key_pressed = True  # Mark that the key has been pressed

    # Reset when the key is released
    if not keys[pygame.K_SPACE]:
        key_pressed = False

    # Update the display (optional for this example)
    pygame.display.flip()

pygame.quit()