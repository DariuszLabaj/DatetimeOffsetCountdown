import datetime
import math
import pygame
import random


class Particle:
    def __init__(self, x: float, y: float) -> None:
        self.__x = random.randint(0, 800)
        self.__y = random.randint(0, 600)
        self.__target_x = x
        self.__target_y = y

    @staticmethod
    def lerp(start: float, stop: float, amt: float):
        return (1-amt)*start+stop*amt

    def update(self):
        self.__x = Particle.lerp(self.__x, self.__target_x, 0.1)
        self.__y = Particle.lerp(self.__y, self.__target_y, 0.1)

    def scatter(self, radius: float):
        randomAngle = random.uniform(0, math.pi * 2)
        self.__x += math.cos(randomAngle) * radius
        self.__y += math.sin(randomAngle) * radius

    def setTarget(self, x: float, y: float):
        self.__target_x = x
        self.__target_y = y

    def draw(self, surface: pygame.surface.Surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.__x), int(self.__y)), 2)


class Gui:
    @property
    def Width(self) -> int:
        return self.__screen.get_width()

    @property
    def Height(self) -> int:
        return self.__screen.get_height()

    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__isFullScreen = False
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption("Gui")

        # Colors
        self.__black = (0, 0, 0)
        self.__white = (255, 255, 255)

        # Font setup
        pygame.font.init()
        self.font = pygame.font.Font(None, 120)

        self.__particles: list[Particle] = []

        self.text = self.getCurrentTime()
        self.generate_particles()

    def toggle_fullscreen(self):
        self.__isFullScreen = not self.__isFullScreen
        if self.__isFullScreen:
            self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.__screen = pygame.display.set_mode((self.__width, self.__height))

    def update_text(self):
        new_text = self.getCurrentTime()
        if new_text != self.text:
            self.text = new_text
            self.generate_particles()

    def generate_particles(self):
        # Create particles based on text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.Width // 2, self.Height // 2))

        # Get pixel data
        text_mask = pygame.mask.from_surface(text_surface)
        target_positions: list[tuple[int, int]] = []

        # Iterate through each pixel of the text mask
        for y in range(text_rect.height):
            for x in range(text_rect.width):
                if text_mask.get_at((x, y)):
                    # Check neighbors to see if this pixel is on the edge
                    if (x-1 < 0 or y-1 < 0 or x+1 >= text_rect.width or y+1 >= text_rect.height):
                        target_x = text_rect.left + x
                        target_y = text_rect.top + y
                        target_positions.append((target_x, target_y))
                        continue
                    if (
                        not text_mask.get_at((x - 1, y)) or  # Left
                        not text_mask.get_at((x + 1, y)) or  # Right
                        not text_mask.get_at((x, y - 1)) or  # Above
                        not text_mask.get_at((x, y + 1))     # Below
                    ):
                        # Add to target positions if it's an edge pixel
                        target_x = text_rect.left + x
                        target_y = text_rect.top + y
                        target_positions.append((target_x, target_y))
        for i, particle in enumerate(self.__particles):
            if i < len(target_positions):
                particle.scatter(80)
                particle.setTarget(*target_positions[i])
            else:
                # Remove extra particles
                self.__particles = self.__particles[:len(target_positions)]
                break
        for i in range(len(self.__particles), len(target_positions)):
            target_x, target_y = target_positions[i]
            self.__particles.append(Particle(target_x, target_y))

    def getCurrentTime(self):
        # return datetime.datetime.now().strftime("%H:%M:%S")
        #      "Sydney"
        return "Sydney" + datetime.datetime.now().strftime("%H:%M:%S")

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.__screen.fill(self.__black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LCTRL] and keys[pygame.K_LALT] and event.key == pygame.K_f:
                        self.toggle_fullscreen()
            self.update_text()
            for particle in self.__particles:
                particle.update()
                particle.draw(self.__screen)

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    pygame.init()
    app = Gui(800, 600)
    app.run()
