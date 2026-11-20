import bpy,bmesh,math,random
from mathutils import Vector
random.seed(4)
def clear():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete()
def mat(n,c,r=.7,m=0,em=None):
    k=bpy.data.materials.new(n);k.use_nodes=True
    b=next(x for x in k.node_tree.nodes if x.type=='BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=r;b.inputs['Metallic'].default_value=m
    if em:
        b.inputs['Emission Color'].default_value=(*em,1);b.inputs['Emission Strength'].default_value=3
    return k
def done(objs,name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:o.select_set(True)
    bpy.context.view_layer.objects.active=objs[0]
    bpy.ops.object.join();o=bpy.context.object;o.name=name
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    bpy.ops.export_scene.gltf(filepath=f'/private/tmp/claude-501/glb2/{name}.glb',export_format='GLB',use_selection=True,export_yup=True)
    clear()
def cyl(r,h,loc,m,v=16,r2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=v,radius1=r,radius2=r if r2 is None else r2,depth=h,location=loc);o=bpy.context.object;o.data.materials.append(m);return o
def box(s,loc,m,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc,rotation=rot);o=bpy.context.object;o.scale=s;o.data.materials.append(m);bpy.ops.object.transform_apply(scale=True);return o
def bev(o,w=.02):
    bpy.context.view_layer.objects.active=o;md=o.modifiers.new('b','BEVEL');md.width=w;md.segments=2
    bpy.ops.object.modifier_apply(modifier='b')
clear()
# Campfire / brazier: ring of stones + logs + flame
stone=mat('Stone',(.35,.33,.32),.9);wood=mat('Wood',(.2,.1,.05),.8);fl=mat('Flame',(1,.45,.08),.5,0,(1,.4,.05));fl2=mat('Flame2',(1,.8,.2),.5,0,(1,.7,.1))
ob=[]
for i in range(9):
    a=i/9*6.283;o=box((.28,.22,.2),(math.cos(a)*.62,math.sin(a)*.62,.11),stone,(0,0,a+random.random()*.4));bev(o,.05);ob.append(o)
for i in range(5):
    a=i/5*3.14+.3;ob.append(box((.9,.12,.12),(0,0,.2+(i%2)*.1),wood,(0,.25,a)))
bpy.ops.mesh.primitive_cone_add(vertices=8,radius1=.28,radius2=0,depth=.9,location=(0,0,.7));o=bpy.context.object;o.data.materials.append(fl);ob.append(o)
bpy.ops.mesh.primitive_cone_add(vertices=8,radius1=.14,radius2=0,depth=.6,location=(0,0,.65));o=bpy.context.object;o.data.materials.append(fl2);ob.append(o)
done(ob,'Campfire')
# Banner on pole
cloth=mat('Cloth',(.55,.08,.1),.85);gold=mat('Gold',(.9,.7,.2),.35,.9);dark=mat('Dark',(.1,.08,.07),.6)
ob=[box((.9,.06,.06),(0,0,2.1),gold),box((.06,.06,.06),(-.46,0,2.1),gold),box((.06,.06,.06),(.46,0,2.1),gold)]
for o in ob[1:]:o.scale=(2,2,2)
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,1.2));c=bpy.context.object;c.scale=(.72,.03,1.7);c.data.materials.append(cloth)
bpy.ops.object.transform_apply(scale=True);ob.append(c)
bm=bmesh.new();bm.from_mesh(c.data)
for v in bm.verts:
    if v.co.z<1.2-.5:v.co.y+=math.sin(v.co.x*6)*.03
bm.to_mesh(c.data);bm.free()
ob.append(box((.5,.04,.04),(0,-.03,1.85),gold))
bpy.ops.mesh.primitive_cone_add(vertices=3,radius1=.17,radius2=0,depth=.3,location=(0,-.04,.2),rotation=(3.14159,0,0));t=bpy.context.object;t.data.materials.append(gold);ob.append(t)
bpy.ops.mesh.primitive_torus_add(major_radius=.17,minor_radius=.035,location=(0,-.035,1.3),rotation=(1.5708,0,0));t=bpy.context.object;t.data.materials.append(gold);ob.append(t)
done(ob,'Banner')
# Mossy rock
rock=mat('Rock',(.32,.31,.3),.95);moss=mat('Moss',(.18,.38,.1),.95)
ob=[]
for i,(x,y,s) in enumerate([(0,0,.8),(.6,.2,.5),(-.5,.3,.45)]):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=s,location=(x,y,s*.6));o=bpy.context.object
    bm=bmesh.new();bm.from_mesh(o.data)
    for v in bm.verts:v.co*=Vector((1+random.random()*.3,1+random.random()*.3,.75+random.random()*.25))
    bm.to_mesh(o.data);bm.free();o.data.materials.append(rock);o.data.materials.append(moss)
    for p in o.data.polygons:
        n=p.normal
        p.material_index=1 if (n.z>.35 and random.random()<.85) or random.random()<.12 else 0
    ob.append(o)
done(ob,'MossRock')
# Floor grate (flat)
met=mat('Metal',(.12,.12,.13),.5,.8)
ob=[box((1.6,1.6,.06),(0,0,.03),dark)]
for i in range(-3,4):ob.append(box((.07,1.6,.12),(i*.22,0,.07),met))
ob.append(box((1.7,.1,.14),(0,.8,.07),met));ob.append(box((1.7,.1,.14),(0,-.8,.07),met))
done(ob,'Grate')
# Lamp post
ob=[cyl(.28,.15,(0,0,.075),met,12,.2),cyl(.09,2.6,(0,0,1.45),met,10)]
ob.append(cyl(.18,.18,(0,0,2.6),gold,10,.22))
lamp=mat('Glow',(1,.8,.4),.3,0,(1,.7,.25))
ob.append(box((.32,.32,.4),(0,0,2.9),lamp))
ob.append(cyl(.32,.18,(0,0,3.2),met,4,.05))
for sx in(-1,1):
    for sy in(-1,1):ob.append(box((.04,.04,.42),(sx*.17,sy*.17,2.9),met))
ob.append(box((.5,.04,.04),(0,0,2.1),met))
done(ob,'LampPost')
