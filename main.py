from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json

app = Ursina()

with open("config.json", "r") as configuration:
    data = json.load(configuration)
    jump_height = data['jump_height']
    jump_duration = data['jump_duration']
    jump_fall_after = data['jump_fall_after']
    gravity_scale = data['gravity_scale']
    run_speed = data['run_speed']
    window.fps_counter.enabled = data['fps_counter']
    window.exit_button.visible = data['exit_button']


mouse_sensitivity = Vec2(40,40) # Default: (40,40)

punch = Audio('assets/punch', autoplay=False)

blocks = [
    load_texture('assets/grass.png'),
    load_texture('assets/grass.png'),
    load_texture('assets/stone.png'),
    load_texture('assets/gold.png'),
    load_texture('assets/lava.png'),
]

block_id = 1

def input(key):
    global block_id, hand
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        hand.texture = blocks[block_id]

sky = Entity(
    parent=scene,
    model='sphere',
    texture=load_texture('assets/sky.jpg'),
    scale=500,
    double_sided=True
)

hand = Entity(
    parent=camera.ui,
    model='assets/block',
    texture=blocks[block_id],
    scale=0.2,
    rotation=Vec3(-10, -10, 10),
    position=Vec2(0.6, -0.6)
)

def update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        punch.play()
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='assets/grass.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                Voxel(position=self.position + mouse.normal, texture=blocks[block_id])
            elif key == 'right mouse down':
                destroy(self)

for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x, 0, z))

player = FirstPersonController()

player.jump_height = jump_height
player.jump_up_duration = jump_duration
player.mouse_sensitivity = mouse_sensitivity
player.speed = run_speed
player.gravity = gravity_scale

app.run()
