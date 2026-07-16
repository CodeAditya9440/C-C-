import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 200, 200)

# Game variables
FPS = 60
GRAVITY = 0.6
JUMP_STRENGTH = -12
PIPE_GAP = 130
PIPE_WIDTH = 50
PIPE_VELOCITY = -5
SPAWN_PIPE_EVERY = 90

# Bird dimensions
BIRD_SIZE = 20
BIRD_X = 50

class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.size = BIRD_SIZE
        self.alive = True
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Check boundary collision
        if self.y + self.size >= SCREEN_HEIGHT or self.y <= 0:
            self.alive = False
    
    def jump(self):
        self.velocity = JUMP_STRENGTH
    
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.size)
        # Draw eye
        pygame.draw.circle(screen, BLACK, (int(self.x + 7), int(self.y - 5)), 3)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(PIPE_GAP + 50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.passed = False
    
    def update(self):
        self.x += PIPE_VELOCITY
    
    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, GREEN, 
                        (self.x, 0, PIPE_WIDTH, self.gap_y - PIPE_GAP // 2))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, 
                        (self.x, self.gap_y + PIPE_GAP // 2, PIPE_WIDTH, SCREEN_HEIGHT))
    
    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0
    
    def check_collision(self, bird):
        bird_right = bird.x + bird.size
        bird_left = bird.x - bird.size
        bird_bottom = bird.y + bird.size
        bird_top = bird.y - bird.size
        
        # Check top pipe collision
        if (bird_right > self.x and bird_left < self.x + PIPE_WIDTH and
            bird_top < self.gap_y - PIPE_GAP // 2):
            return True
        
        # Check bottom pipe collision
        if (bird_right > self.x and bird_left < self.x + PIPE_WIDTH and
            bird_bottom > self.gap_y + PIPE_GAP // 2):
            return True
        
        return False
    
    def check_pass(self, bird):
        if not self.passed and bird.x > self.x + PIPE_WIDTH:
            self.passed = True
            return True
        return False

class FlappyBirdGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)
        self.reset_game()
    
    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.started = False
        self.pipe_counter = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.started:
                        self.started = True
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.bird.jump()
        return True
    
    def update(self):
        if not self.started or self.game_over:
            return
        
        self.bird.update()
        
        # Spawn pipes
        self.pipe_counter += 1
        if self.pipe_counter >= SPAWN_PIPE_EVERY:
            self.pipes.append(Pipe(SCREEN_WIDTH))
            self.pipe_counter = 0
        
        # Update pipes
        for pipe in self.pipes:
            pipe.update()
            
            # Check collision
            if pipe.check_collision(self.bird):
                self.game_over = True
            
            # Check score
            if pipe.check_pass(self.bird):
                self.score += 1
        
        # Remove off-screen pipes
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]
        
        # Check if bird is dead
        if not self.bird.alive:
            self.game_over = True
    
    def draw(self):
        self.screen.fill(CYAN)
        
        if not self.started:
            # Draw start screen
            title = self.font_large.render("FLAPPY BIRD", True, BLACK)
            instruction = self.font_small.render("Press SPACE to start", True, BLACK)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 
                                    SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 
                                          SCREEN_HEIGHT // 2 + 50))
        else:
            # Draw pipes
            for pipe in self.pipes:
                pipe.draw(self.screen)
            
            # Draw bird
            self.bird.draw(self.screen)
            
            # Draw score
            score_text = self.font_small.render(f"Score: {self.score}", True, BLACK)
            self.screen.blit(score_text, (10, 10))
            
            if self.game_over:
                # Draw game over screen
                game_over_text = self.font_large.render("GAME OVER", True, RED)
                final_score = self.font_small.render(f"Final Score: {self.score}", True, BLACK)
                restart = self.font_small.render("Press SPACE to restart", True, BLACK)
                
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                                 SCREEN_HEIGHT // 2 - 100))
                self.screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2, 
                                              SCREEN_HEIGHT // 2))
                self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 
                                          SCREEN_HEIGHT // 2 + 80))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()
