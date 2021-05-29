from pygame.image import load
from pygame.math import Vector2

def load_sprite(name):
    path = f"assets/sprites/Ships/{name}.png"
    loaded_sprite = load(path)

    return loaded_sprite.convert_alpha()

def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)