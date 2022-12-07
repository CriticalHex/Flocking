import pygame
from random import randint, random
from math import dist
from colors import Color

vec = pygame.Vector2
rec = pygame.Rect


class Flock:
    class Boid:
        def __init__(self, flock):
            self.flock: Flock = flock
            self.color = Color()
            self.pos = vec(
                randint(0, self.flock.screen.get_width()),
                randint(0, self.flock.screen.get_height()),
            )
            # self.pos = vec(500, 500)
            self.vel = vec(randint(-1, 0) + random(), randint(-1, 0) + random())
            if self.vel.magnitude != 0:
                self.vel *= self.flock.max_speed / self.vel.magnitude()
            self.acc = vec(0, 0)

        def draw(self):
            pygame.draw.circle(self.flock.screen, self.color.get_color(), self.pos, 8)
            self.color.inc()

        def update(self):
            self.pos += self.vel
            self.vel += self.acc
            if self.vel.magnitude != 0:
                self.vel *= self.flock.max_speed / self.vel.magnitude()
            self.acc *= 0
            self.wrap()

        def wrap(self):
            if self.pos.x > self.flock.screen.get_width():
                self.pos.x = 0
            elif self.pos.x < 0:
                self.pos.x = self.flock.screen.get_width()

            if self.pos.y > self.flock.screen.get_height():
                self.pos.y = 0
            elif self.pos.y < 0:
                self.pos.y = self.flock.screen.get_height()

    def __init__(self, count) -> None:
        self.screen = pygame.display.get_surface()
        self.perception = 50
        self.boids: list[Flock.Boid] = []
        self.count = count
        self.max_speed = 4
        self.max_steer = 1
        self.max_alignment = 1
        self.max_cohesion = 1
        self.max_separation = 1
        for _ in range(self.count):
            self.boids.append(Flock.Boid(self))

    def draw(self):
        self.update()
        for b in self.boids:
            b.update()
            b.draw()

    def update(self):

        for b in self.boids:
            alignment = vec(0, 0)
            separation = vec(0, 0)
            cohesion = vec(0, 0)
            total = 0

            for other in self.boids:
                if other is not b:
                    d = dist(b.pos, other.pos)
                    if d < self.perception:  # if flocking
                        alignment += other.vel
                        cohesion += other.pos
                        separation += self.calc_separation(b, other, d)
                        total += 1
            if total > 0:
                alignment = self.handle(alignment, total, b)
                cohesion = self.cohese(cohesion, total, b)
                separation = self.handle(separation, total, b)

            b.acc += alignment * self.max_alignment
            b.acc += cohesion * self.max_cohesion
            b.acc += separation * self.max_separation

    def calc_separation(self, boid: Boid, other: Boid, distance: float):
        diff = boid.pos - other.pos  # vector from other to b
        if distance != 0:
            diff /= distance
        return diff

    def handle(self, steer: vec, total: int, boid: Boid):
        steer /= total  # average
        if steer.magnitude() != 0:
            steer *= self.max_speed / steer.magnitude()  # max the speed
        steer -= boid.vel  # calculate the steer
        if (x := steer.magnitude()) > self.max_steer:
            steer *= self.max_steer / x  # limit
        return steer

        steer /= total  # average
        if (x := steer.magnitude()) > self.max_separation:
            steer *= self.max_separation / x  # limit
        steer -= boid.vel  # calculate the steer
        return steer

    def cohese(self, steer: vec, total: int, boid: Boid):
        steer /= total  # average
        steer -= boid.pos  # calculate the pos vec
        if steer.magnitude() != 0:
            steer *= self.max_speed / steer.magnitude()  # max the speed
        steer -= boid.vel  # calculate the steer
        if (x := steer.magnitude()) > self.max_steer:
            steer *= self.max_steer / x  # limit
        return steer
