import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Car Game")
clock = pygame.time.Clock()
FPS = 60

font_small = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 72)


class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed


class EnemyCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 7)


class Road:
    def __init__(self):
        self.offset = 0
        self.speed = 5

    def update(self):
        self.offset += self.speed
        if self.offset >= 20:
            self.offset = 0

    def draw(self, surface):
        surface.fill(GREEN)
        pygame.draw.rect(surface, BLACK, (50, 0, SCREEN_WIDTH - 100, SCREEN_HEIGHT))
        for i in range(-1, SCREEN_HEIGHT // 20 + 1):
            y = i * 20 + self.offset
            pygame.draw.line(surface, YELLOW, (SCREEN_WIDTH // 2, y), (SCREEN_WIDTH // 2, y + 10), 3)


class Game:
    def __init__(self):
        self.player = PlayerCar()
        self.enemies = [EnemyCar() for _ in range(3)]
        self.road = Road()
        self.score = 0
        self.game_over = False
        self.game_started = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_started or self.game_over:
                        self.reset_game()
        return True

    def reset_game(self):
        self.player = PlayerCar()
        self.enemies = [EnemyCar() for _ in range(3)]
        self.score = 0
        self.game_over = False
        self.game_started = True

    def update(self):
        if not self.game_started or self.game_over:
            return

        self.player.update()
        self.road.update()

        for enemy in self.enemies:
            enemy.update()
            if self.player.rect.colliderect(enemy.rect):
                self.game_over = True
            if enemy.rect.top > SCREEN_HEIGHT:
                self.score += 10
                enemy.reset_position()

    def draw(self):
        self.road.draw(screen)
        screen.blit(self.player.image, self.player.rect)

        for enemy in self.enemies:
            screen.blit(enemy.image, enemy.rect)

        score_text = font_small.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if not self.game_started:
            title = font_large.render("CAR GAME", True, YELLOW)
            sub = font_small.render("Press SPACE to Start", True, WHITE)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        if self.game_over:
            game_over_text = font_large.render("GAME OVER", True, RED)
            final_score = font_small.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = font_small.render("Press SPACE to Restart", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2, SCREEN_HEIGHT // 2))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
