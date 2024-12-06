import math
import random
from typing import Literal, Optional
import pygame


class ParticleText:
    class Particle:
        @property
        def X(self):
            return self.__x

        @property
        def Y(self):
            return self.__y

        @staticmethod
        def lerp(start: float, stop: float, amt: float):
            return (1-amt)*start+stop*amt

        def __init__(self, x: float, y: float, width: int, height: int):
            self.__x = random.randint(0, width)
            self.__y = random.randint(0, height)
            self.__target_x = x
            self.__target_y = y

        def update(self):
            self.__x = ParticleText.Particle.lerp(self.__x, self.__target_x, 0.3)
            self.__y = ParticleText.Particle.lerp(self.__y, self.__target_y, 0.3)

        def scatter(self, radius: float):
            randomAngle = random.uniform(0, math.pi * 2)
            self.__x += math.cos(randomAngle) * radius
            self.__y += math.sin(randomAngle) * radius

        def setTarget(self, x: float, y: float):
            self.__target_x = x
            self.__target_y = y

    @property
    def Text(self):
        return self.__text

    def __init__(self, width: int, height: int, x: int, y: int, font: pygame.font.Font, text: str = "", align: Optional[Literal["top", "left", "bottom", "right", "topleft", "bottomleft", "topright", "bottomright", "midtop", "midleft", "midbottom", "midright", "center", "centerx", "centery"]] = None):
        self.__particles: list[ParticleText.Particle] = []
        self.__align = align
        self.__text = text
        self.__font = font
        self.__width = width
        self.__height = height
        self.__x = x
        self.__y = y
        self.generate_particles()

    def setAlignment(self, align: Optional[Literal["top", "left", "bottom", "right", "topleft", "bottomleft", "topright", "bottomright", "midtop", "midleft", "midbottom", "midright", "center", "centerx", "centery"]] = None, generate: bool = True):
        self.__align = align
        if generate:
            self.generate_particles()

    def setFont(self, font: pygame.font.Font, generate: bool = True):
        self.__font = font
        if generate:
            self.generate_particles()

    def setPosition(self, x: int, y: int, generate: bool = True):
        self.__x = x
        self.__y = y
        if generate:
            self.generate_particles()

    def setSize(self, width: int, height: int, generate: bool = True):
        self.__width = width
        self.__height = height
        if generate:
            self.generate_particles()

    def updateText(self, text: str, generate: bool = True):
        if self.__text != text:
            self.__text = text
            if generate:
                self.generate_particles()

    def update(self):
        for particle in self.__particles:
            particle.update()

    @property
    def Particles(self):
        return self.__particles

    def generate_particles(self):
        text_surface = self.__font.render(self.__text, False, (255, 255, 255))
        match self.__align:
            case "top":
                text_rect = text_surface.get_rect(top=(self.__x, self.__y))
            case "left":
                text_rect = text_surface.get_rect(left=(self.__x, self.__y))
            case "bottom":
                text_rect = text_surface.get_rect(bottom=(self.__x, self.__y))
            case "right":
                text_rect = text_surface.get_rect(right=(self.__x, self.__y))
            case "topleft":
                text_rect = text_surface.get_rect(topleft=(self.__x, self.__y))
            case "bottomleft":
                text_rect = text_surface.get_rect(bottomleft=(self.__x, self.__y))
            case "topright":
                text_rect = text_surface.get_rect(topright=(self.__x, self.__y))
            case "bottomright":
                text_rect = text_surface.get_rect(bottomright=(self.__x, self.__y))
            case "midtop":
                text_rect = text_surface.get_rect(midtop=(self.__x, self.__y))
            case "midleft":
                text_rect = text_surface.get_rect(midleft=(self.__x, self.__y))
            case "midbottom":
                text_rect = text_surface.get_rect(midbottom=(self.__x, self.__y))
            case "midright":
                text_rect = text_surface.get_rect(midright=(self.__x, self.__y))
            case "center":
                text_rect = text_surface.get_rect(center=(self.__x, self.__y))
            case "centerx":
                text_rect = text_surface.get_rect(centerx=(self.__x, self.__y))
            case "centery":
                text_rect = text_surface.get_rect(centery=(self.__x, self.__y))
            case _:
                text_rect = text_surface.get_rect()

        text_mask = pygame.mask.from_surface(text_surface)
        target_positions = [
            (text_rect.left + x, text_rect.top + y)
            for y in range(text_rect.height)
            for x in range(text_rect.width)
            if text_mask.get_at((x, y)) and (
                x == 0 or y == 0 or x == text_rect.width - 1 or y == text_rect.height - 1 or
                not text_mask.get_at((x - 1, y)) or  # Left
                not text_mask.get_at((x + 1, y)) or  # Right
                not text_mask.get_at((x, y - 1)) or  # Above
                not text_mask.get_at((x, y + 1))    # Below
            )
        ]
        target_positions = [target_positions[i] for i in range(len(target_positions)) if i % 5 != 4]
        for i, particle in enumerate(self.__particles):
            if i < len(target_positions):
                particle.scatter(self.__font.get_height())
                particle.setTarget(*target_positions[i])
            else:
                # Remove extra particles
                self.__particles = self.__particles[:len(target_positions)]
                break
        for i in range(len(self.__particles), len(target_positions)):
            target_x, target_y = target_positions[i]
            self.__particles.append(ParticleText.Particle(target_x, target_y, self.__width, self.__height))
