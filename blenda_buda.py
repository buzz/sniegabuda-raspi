import sys, os

import bpy
import mathutils
from mathutils import Vector

sys.path.append(os.path.dirname(__file__))
from model import coords, faces
from model import middle_sorted as leds

def create_sphere(name, origin):
    bpy.ops.mesh.primitive_uv_sphere_add(
		size=0.1,
        rotation=(0, 0, 0),
        location=origin
    )
 
    obj = bpy.context.object
    obj.name = name
    mesh = obj.data
    mesh.name = name + '-mesh'

    return obj

def make_material(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.emit = 2.0
    mat.alpha = alpha
    mat.ambient = 1
    return mat
 
def set_material(ob, mat):
    me = ob.data
    me.materials.append(mat)

red = make_material('red', (1,0,0), (1,1,1), 1)
blue = make_material('blue', (0,0,1), (0.5,0.5,0), 0.5)

mesh_name = "dome"
obj_name = "dome"

scene = bpy.context.scene

#for obj in scene.objects:
#	scene.objects.unlink(obj)

mesh = bpy.data.meshes.new(mesh_name)
obj  = bpy.data.objects.new(obj_name, mesh)
scene.objects.link(obj)
mesh.from_pydata(coords, [], faces)
mesh.update()

led_objects = []

for i, led in enumerate(leds):
	obj = create_sphere('led-%03i' % i, Vector(tuple(led)))
	led_objects.append(obj)

for obj in led_objects:
	set_material(obj, blue)
