import bpy,math,random
random.seed(3)
def clear():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete()
def mat(n,c,r=.45,m=.5,em=None,es=3):
    k=bpy.data.materials.new(n);k.use_nodes=True
    b=next(x for x in k.node_tree.nodes if x.type=='BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=r;b.inputs['Metallic'].default_value=m
    if em:
        b.inputs['Emission Color'].default_value=(*em,1);b.inputs['Emission Strength'].default_value=es
    return k
M={'Hull':mat('Hull',(.72,.76,.82),.4,.6),'Dark':mat('Dark',(.1,.11,.14),.5,.7),'Red':mat('Red',(.75,.12,.1),.5,.3),'Glass':mat('Glass',(.1,.3,.5),.1,.2,(.1,.4,.7),1),'Glow':mat('Glow',(.3,.7,1),.3,0,(.3,.75,1),6),'NavR':mat('NavR',(1,.1,.1),.3,0,(1,.1,.1),8),'NavG':mat('NavG',(.1,1,.2),.3,0,(.1,1,.2),8),'Gold':mat('Gold',(.85,.65,.2),.35,.9)}
clear();objs=[]
def reg(o,m):
    o.data.materials.append(M[m]);bpy.ops.object.shade_smooth();objs.append(o);return o
def box(loc,sc,m,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc,rotation=rot);o=bpy.context.object;o.scale=sc;bpy.ops.object.transform_apply(scale=True);return reg(o,m)
def cyl(loc,r,h,m,rot=(0,0,0),v=16,r2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=v,radius1=r,radius2=r if r2 is None else r2,depth=h,location=loc,rotation=rot);return reg(bpy.context.object,m)
def sph(loc,sc,m,rot=(0,0,0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=10,location=loc,rotation=rot);o=bpy.context.object;o.scale=sc;bpy.ops.object.transform_apply(scale=True);return reg(o,m)
# nose -Y, tail +Y, up +Z
X=math.pi/2
# fuselage: central tube + nose cone + rear block
cyl((0,.8,1.2),1.15,5.2,'Hull',(X,0,0))
cyl((0,-3.9,1.2),1.15,3.4,'Hull',(X,0,0),16,.12)   # nose taper (apex toward -Y)
cyl((0,-5.7,1.2),.14,.4,'Dark',(X,0,0),12,.06)
sph((0,-0.4,1.9),(1.0,1.5,.7),'Glass')                 # canopy
box((0,-.4,1.75),(.1,2.8,.1),'Dark')                   # canopy frame
for y in(-1.6,-0.4,.8):box((0,y,2.35),(1.6,.1,.12),'Dark')
# dorsal spine + greebles
box((0,2.2,2.45),(.5,3.6,.45),'Hull');box((0,2.2,2.75),(.3,3.4,.2),'Dark')
for i in range(6):
    box((0,.8+i*.55,2.95),(.35,.28,.14),'Dark')
# red stripe + panel lines on fuselage
box((0,.8,2.34),(.55,5.0,.06),'Red')
for y in(-1.8,-.9,.0,1.0,2.0,3.0):box((0,y,1.2),(2.4,.045,2.4),'Dark')
# wings (swept)
for sx in(-1,1):
    w=box((sx*3.4,1.8,1.0),(5.4,2.8,.28),'Hull',(0,0,sx*-.5))
    box((sx*3.7,1.3,1.18),(4.4,1.8,.1),'Dark',(0,0,sx*-.5))
    box((sx*4.6,2.0,.9),(.14,2.6,.8),'Red',(0,0,sx*-.5))          # wing tip fin
    box((sx*6.1,3.1,1.0),(.3,1.2,1.2),'Dark')                       # pod
    cyl((sx*5.4,.2,1.0),.28,2.2,'Dark',(X,0,0),12)                 # gun barrel
    cyl((sx*5.4,-.95,1.0),.14,.4,'Dark',(X,0,0),10)
    sph((sx*6.05,-.1,.95),(.55,.9,.45),'Hull')
    box((sx*3.4,2.6,.82),(4.6,.12,.12),'Dark',(0,0,sx*-.5))        # flap line
# nacelles / engines
for sx in(-1,1):
    cyl((sx*1.9,3.6,1.1),.8,3.2,'Dark',(X,0,0),16)
    cyl((sx*1.9,3.7,1.1),.72,3.0,'Hull',(X,0,0),16)
    cyl((sx*1.9,5.3,1.1),.62,.5,'Dark',(X,0,0),16)
    cyl((sx*1.9,5.62,1.1),.5,.22,'Glow',(X,0,0),16)
    cyl((sx*1.9,2.3,1.1),.84,.12,'Gold',(X,0,0),16)
    for k in range(5):
        a=k/5*6.283
        box((sx*1.9+math.cos(a)*.78,4.2,1.1+math.sin(a)*.78),(.06,1.6,.06),'Dark')
    box((sx*1.1,2.5,1.1),(.9,1.6,.5),'Hull')                        # strut
# central engine
cyl((0,3.6,1.2),.6,2.6,'Dark',(X,0,0),20);cyl((0,5.1,1.2),.55,.3,'Glow',(X,0,0),20)
# tail fins
box((0,4.4,3.0),(.2,1.8,2.0),'Hull',(.35,0,0));box((0,4.5,3.2),(.22,1.0,1.0),'Red',(.35,0,0))
for sx in(-1,1):box((sx*1.0,4.8,2.0),(1.2,1.2,.14),'Hull',(0,0,sx*.4))
# belly details
box((0,.6,.1),(1.4,3.0,.35),'Dark')
for sx in(-1,1):
    for y in(-.6,1.8):
        cyl((sx*.9,y,.0),.12,.8,'Dark',(0,0,0),10);sph((sx*.9,y,-.45),(.35,.35,.12),'Dark')
# antenna + nav lights + lamps
cyl((.5,2.0,3.5),.04,1.4,'Dark',(0,0,0),6);sph((.5,2.0,4.25),(.1,.1,.1),'NavR')
cyl((-.5,3.2,3.2),.03,1.0,'Dark',(0,0,0),6)
sph((-7.0,3.3,1.05),(.18,.18,.18),'NavR');sph((7.0,3.3,1.05),(.18,.18,.18),'NavG')
sph((0,-5.3,1.2),(.09,.09,.09),'Glow')
# rivet rows on hull top
for i in range(12):
    for sx in(-1,1):
        sph((sx*.5,-.9+i*.45,2.28),(.06,.06,.04),'Dark')
bpy.ops.object.select_all(action='DESELECT')
for o in objs:o.select_set(True)
bpy.context.view_layer.objects.active=objs[0]
bpy.ops.object.join();o=bpy.context.object;o.name='Escort'
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
print('DIM',o.dimensions,len(o.data.polygons))
bpy.ops.export_scene.gltf(filepath='/private/tmp/claude-501/glb2/Ship.glb',export_format='GLB',use_selection=True,export_yup=True)
