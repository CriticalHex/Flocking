import pygame
from flock import Flock


def main():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    running = True
    clock = pygame.time.Clock()

    count = 200
    flock = Flock(count)

    while running:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                running = False

            if keys[pygame.K_LSHIFT]:
                flock = Flock(count)

        screen.fill((0, 0, 0))

        flock.draw()

        pygame.display.flip()


if __name__ == "__main__":
    main()
