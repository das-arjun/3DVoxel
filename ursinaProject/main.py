from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Create the player controller with reduced mouse sensitivity
player = FirstPersonController(
    mouse_sensitivity=Vec2(50, 50),  # Reduced sensitivity
    position=(0, 5, 0)
)

# Lock the mouse cursor to the center of the screen
window.cursex = window.center[0]
window.cursory = window.center[1]
window.exit_button.enabled = False  # Disable the exit button to prevent user from quitting by accident
window.fullscreen = False  # Optionally you can enable fullscreen to improve immersion but you might have to shut down and restart your PC for exit since that's what happened during playtest and I can't fix it.

# Create the ground block
ground = Entity(
    model="plane",
    scale=(100, 1, 100),
    texture="grass",
    texture_scale=(10, 10),
    collider="box"
)

# List to keep track of placed blocks
placed_blocks = []

class Voxel(Entity):
    def __init__(self, position=(0, 0, 0), texture='white_cube', **kwargs):
        super().__init__(
            model='cube',
            texture=texture,
            color=color.white,
            position=position,
            **kwargs
        )
        self.collider = 'box'  # Add a collider to the voxel

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":  # Place a block
                # Snapping position to a grid (e.g., 1 unit grid)
                new_pos = self.position + mouse.normal
                new_pos = Vec3(round(new_pos.x), round(new_pos.y), round(new_pos.z))

                # Avoid placing blocks where other blocks are already placed
                if not any([block.position == new_pos for block in placed_blocks]):
                    new_block = Voxel(position=new_pos, texture='grass')  # Change texture as needed
                    placed_blocks.append(new_block)  # Keep track of placed blocks

            elif key == "right mouse down":  # Break a block
                destroy(self)
                placed_blocks.remove(self)  # Remove the block from the list when destroyed


# Make the first voxel the center for easy placement
initial_block = Voxel(position=(0, 0, 0), texture='stone')
placed_blocks.append(initial_block)

# Adding more world generation (procedural terrain)
def generate_world():
    for x in range(-10, 10):
        for z in range(-10, 10):
            y = 0  # Flat ground for now
            block = Voxel(position=(x, y, z), texture='grass')
            placed_blocks.append(block)

# Generate initial world
generate_world()

# Run the application
app.run()
