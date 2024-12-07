from math import pi
from random import Random, randint, random
from typing import overload, Optional
import pygame


def mathMap(x: float, in_min: float, in_max: float, out_min: float, out_max: float):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


@overload
def random2DVector() -> pygame.Vector2:
    ...


@overload
def random2DVector(x1: float, y1: float) -> pygame.Vector2:
    ...


def random2DVector(
    x1: Optional[float] = None, y1: Optional[float] = None, x2: Optional[float] = None, y2: Optional[float] = None
) -> pygame.Vector2:
    if x1 is None and x2 is None and y1 is None and y2 is None:
        vect = pygame.Vector2(1, 0)
        vect.rotate_rad_ip(random() * 2 * pi)
        return vect
    elif x2 is None and y2 is None:
        a = 0
        b = x1
        c = 0
        d = y1
    elif x1 is not None and x2 is not None and y1 is not None and y2 is not None:
        a = x1
        b = y1
        c = x2
        d = y2
    else:
        raise ValueError()
    if b is None or d is None:
        raise ValueError()
    rng = Random()
    return pygame.Vector2(
        mathMap(rng.random(), 0, 1, a, b), mathMap(rng.random(), 0, 1, c, d)
    )


def hsvToRgb(hue: int, saturation: float = 1.0, value: float = 1.0):
    if hue < 0 or hue > 359:
        raise ValueError
    if saturation < 0 or saturation > 1.0:
        raise ValueError
    if value < 0 or value > 1.0:
        raise ValueError

    c = value * saturation
    x = c * (1 - abs((hue / 60) % 2 - 1))
    m = value - c

    if 0 <= hue < 60:
        rp, gp, bp = c, x, 0
    elif 60 <= hue < 120:
        rp, gp, bp = x, c, 0
    elif 120 <= hue < 180:
        rp, gp, bp = 0, c, x
    elif 180 <= hue < 240:
        rp, gp, bp = 0, x, c
    elif 240 <= hue < 300:
        rp, gp, bp = x, 0, c
    elif 300 <= hue < 360:
        rp, gp, bp = c, 0, x
    else:
        rp, gp, bp = 0, 0, 0
    r, g, b = (rp + m) * 255, (gp + m) * 255, (bp + m) * 255
    return (int(r), int(g), int(b))


class Firework:
    class Particle:
        @property
        def __rect(self):
            return pygame.Rect(0, 0, self.size, self.size)

        @property
        def done(self):
            return self.lifespan < 1

        @property
        def __color(self):
            if self.lifespan < 0:
                self.lifespan = 0
            return pygame.Color(self.r, self.g, self.b, self.lifespan)

        @property
        def Color(self):
            return (self.r, self.g, self.b)

        def __init__(self, x: float, y: float, firework: bool, size: float = 4, color: tuple[int, int, int] = (255, 255, 255), canvasHeight: int = 480) -> None:
            if firework:
                maxSpeed = canvasHeight * 0.017437365 + 3.670064875
                self.vel = pygame.Vector2(0, -randint(int(maxSpeed * 0.75), int(maxSpeed)))
            else:
                self.vel = random2DVector()
                self.vel *= randint(1, 20)
            self.firework = firework
            self.lifespan = 255
            self.acc = pygame.Vector2(0, 0)
            self.size = size
            self.pos = pygame.Vector2(x, y - self.size)
            self.r = color[0]
            self.g = color[1]
            self.b = color[2]

        def applyForce(self, force: pygame.Vector2):
            self.acc += force

        def update(self):
            if not self.firework:
                self.vel *= 0.85
                self.lifespan -= 4
            self.vel += self.acc
            self.pos += self.vel
            self.acc.x = 0
            self.acc.y = 0

        def show(self, window: pygame.Surface | pygame.surface.Surface):
            surf = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.rect(surf, self.__color, self.__rect)
            window.blit(surf, self.pos)

    @property
    def offScreen(self) -> bool:
        return self.exploded and not self.particles

    def __getRandomColor(self) -> tuple[int, int, int]:
        return hsvToRgb(randint(0, 359))

    def __init__(self, width: int, height: int, gravity: pygame.Vector2):
        self.canvasWidth = width
        self.canvasHeight = height
        self.gravity = gravity
        self.size = 4
        self.firework = Firework.Particle(
            randint(0, self.canvasWidth),
            self.canvasHeight,
            True,
            self.size,
            self.__getRandomColor(),
            height
        )
        self.exploded = False
        self.particles: list[Firework.Particle] = []

    def update(self):
        self.firework.applyForce(self.gravity)
        self.firework.update()
        if not self.exploded:
            if self.firework.vel.y >= 0:
                self.exploded = True
                self.explode()
        for particle in self.particles:
            particle.applyForce(self.gravity)
            particle.update()
            if particle.done:
                self.particles.pop(self.particles.index(particle))

    def explode(self):
        self.particles = []
        for _ in range(100):
            self.particles.append(
                Firework.Particle(
                    self.firework.pos.x,
                    self.firework.pos.y,
                    False,
                    self.size,
                    self.firework.Color,
                    self.canvasHeight,
                )
            )

    def show(self, window: pygame.Surface | pygame.surface.Surface):
        if not self.exploded:
            self.firework.show(window)
        for particle in self.particles:
            particle.show(window)
