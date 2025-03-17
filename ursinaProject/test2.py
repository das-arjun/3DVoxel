from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

player = FirstPersonController(
    mouse_sensitivity=Vec2(100,100),
    position=(0,5,0)
)

class Block(Entity):

 ground = Entity(
    model="plane",
    scale=(100,1,100),
    texture="grass",
    texture_scale=(10,10),
    collider="box"
)

