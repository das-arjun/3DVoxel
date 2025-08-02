from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Block types and selection
block_types = ['grass', 'stone', 'brick', 'white_cube']
current_block_index = 0

# Track placed blocks using dictionary
placed_blocks = {}

# UI Title
title = Text(
    text='Pycraft 2.7',
    position=(0.46, 0.02),
    origin=(44.9, 0),
    scale=0.08,
    color=color.orange
)

# Player setup
player = FirstPersonController(
    mouse_sensitivity=Vec2(50, 50),
    position=(0, 5, 0)
)

# Lock mouse and configure window
mouse.locked = True
window.exit_button.enabled = True
window.fullscreen = False

# Ground plane (optional)
ground = Entity(
    model="plane",
    scale=(100, 1, 100),
    texture="grass",
    texture_scale=(10, 10),
    collider="box"
)

# Voxel block class
class Voxel(Entity):
    def __init__(self, position=(0, 0, 0), texture='white_cube', is_terrain=False, **kwargs):
        super(Voxel, self).__init__(
            model='cube',
            texture=texture,
            color=color.white,
            position=position,
            **kwargs
        )
        self.collider = 'box'
        self.is_terrain = is_terrain

# Unified input handling
def input(key):
    global current_block_index

    # Change selected block type
    if key.isdigit() and 1 <= int(key) <= len(block_types):
        current_block_index = int(key) - 1
        print("Selected block:", block_types[current_block_index])

    # Block placement
    if mouse.hovered_entity and isinstance(mouse.hovered_entity, Voxel):
        hovered_block = mouse.hovered_entity

        if key == "left mouse down":
            # Place block on top of the face you're pointing at
            new_pos = hovered_block.position + mouse.normal
            new_pos = Vec3(round(new_pos.x), round(new_pos.y), round(new_pos.z))
            pos_key = tuple(new_pos)

            if pos_key not in placed_blocks:
                new_block = Voxel(position=new_pos, texture=block_types[current_block_index])
                placed_blocks[pos_key] = new_block

        elif key == "right mouse down":
            # Prevent destroying terrain blocks
            if hasattr(hovered_block, 'is_terrain') and hovered_block.is_terrain:
                return
            destroy(hovered_block)
            placed_blocks.pop(tuple(hovered_block.position), None)

# Generate terrain blocks
def generate_world():
    for x in range(-10, 10):
        for z in range(-10, 10):
            y = 0
            block = Voxel(position=(x, y, z), texture='grass', is_terrain=True)
            placed_blocks[(x, y, z)] = block

# Generate terrain
generate_world()
app.run()
