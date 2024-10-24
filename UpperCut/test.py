import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Three Frame Animation')

# Animation Class
class Animation:
    def __init__(self, images, pos, frame_rate):
        self.images = images  # List of frames for animation
        self.pos = pos        # Position to draw the animation
        self.frame_rate = frame_rate  # Frame rate of animation (how fast frames change)
        self.current_frame = 0        # Current frame index
        self.playing = False          # Is the animation currently playing
        self.time_accumulator = 0     # Time accumulator for frame timing

    def play(self):
        """Starts the animation playback"""
        self.playing = True
        self.current_frame = 0
        self.time_accumulator = 0

    def update(self, dt):
        """Updates the animation, advancing the frame if necessary"""
        if self.playing:
            self.time_accumulator += dt
            if self.time_accumulator >= self.frame_rate:
                self.time_accumulator = 0
                self.current_frame += 1
                if self.current_frame >= len(self.images):
                    self.playing = False  # Stop animation after it finishes

    def draw(self, screen):
        """Draws the current frame of the animation on the screen"""
        if self.playing:
            screen.blit(self.images[self.current_frame], self.pos)

# Main Game Loop
def main():
    clock = pygame.time.Clock()

    # Load the animation frames (replace these with actual image files)
    frame1 = pygame.Surface((100, 100))
    frame1.fill((255, 0, 0))
    frame2 = pygame.Surface((100, 100))
    frame2.fill((0, 255, 0))
    frame3 = pygame.Surface((100, 100))
    frame3.fill((0, 0, 255))

    frames = [frame1, frame2, frame3]

    # Create the animation object
    animation = Animation(frames, (WIDTH // 2 - 50, HEIGHT // 2 - 50), 200)

    running = True
    while running:
        dt = clock.tick(FPS)  # Get time passed since last frame in milliseconds
        screen.fill(WHITE)    # Fill screen with white background

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get key states
        keys = pygame.key.get_pressed()

        # If SPACE is pressed, play the animation
        if keys[pygame.K_SPACE] and not animation.playing:
            animation.play()

        # Update and draw the animation
        animation.update(dt)
        animation.draw(screen)

        pygame.display.flip()  # Update the display

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()