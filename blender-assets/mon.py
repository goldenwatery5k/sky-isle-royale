import bpy,math
from mathutils import Vector
def clear():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete()
def mat(n,c,r=.6,em=None):
    k=bpy.data.materials.new(n);k.use_nodes=True
    b=next(x for x in k.node_tree.nodes if x.type=='BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=r
    if em:
        b.inputs['Emission Color'].default_value=(*em,1);b.inputs['Emission Strength'].default_value=2
    return k
M={'Skin':mat('Skin',(.28,.12,.45),.7),'Belly':mat('Belly',(.5,.28,.65),.7),'Eye':mat('Eye',(1,.8,.1),.3,(1,.7,.1)),'Tooth':mat('Tooth',(.95,.95,.9),.4),'Dark':mat('Dark',(.05,.02,.1),.8),'Horn':mat('Horn',(.9,.85,.7),.5)}
clear();objs=[]
def sph(loc,sc,m,seg=24,rot=(0,0,0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=seg//2,location=loc,rotation=rot);o=bpy.context.object;o.scale=sc;bpy.ops.object.transform_apply(scale=True,rotation=True);o.data.materials.append(M[m]);bpy.ops.object.shade_smooth();objs.append(o);return o
def cone(loc,r,h,m,rot=(0,0,0),v=10,r2=0):
    bpy.ops.mesh.primitive_cone_add(vertices=v,radius1=r,radius2=r2,depth=h,location=loc,rotation=rot);o=bpy.context.object;o.data.materials.append(M[m]);bpy.ops.object.shade_smooth();objs.append(o);return o
# body/head
sph((0,0,1.9),(1.75,1.25,1.45),'Skin',32)
# belly
sph((0,-.55,1.25),(1.15,.85,1.0),'Belly',24)
# ears (pointed, tilted outward)
for sx in(-1,1):
    cone((sx*1.15,-.05,3.25),.5,1.3,'Skin',(0,sx*.45,0),12)
    cone((sx*1.15,-.18,3.2),.3,.9,'Dark',(0,sx*.45,0),12)
# crown spikes
for i,(x,z,h) in enumerate([(-.5,3.1,.85),(0,3.35,1.05),(.5,3.1,.85)]):
    cone((x,.15,z),.28,h,'Skin',(0,0,0),10)
# back spikes
for i in range(5):
    z=1.2+i*.45;cone((0,1.15-i*.02,z),.25,.9-i*.05,'Skin',(-1.9,0,0),10)
# tail
cone((0,1.35,.55),.35,1.1,'Skin',(-2.2,0,0),10)
# eyes (slanted)
for sx in(-1,1):
    sph((sx*.7,-1.05,2.35),(.42,.1,.2),'Eye',16,(0,sx*.55,0))
    sph((sx*.7,-1.12,2.35),(.06,.04,.14),'Dark',8)
# mouth: dark wide ellipse + teeth
sph((0,-1.0,1.65),(1.15,.2,.55),'Dark',20)
for i in range(-4,5):
    x=i*.24;cone((x,-1.17,1.98-abs(i)*.02),.1,.28,'Tooth',(math.pi,0,0),6)
for i in range(-3,4):
    x=i*.28;cone((x,-1.17,1.32+abs(i)*.03),.09,.22,'Tooth',(0,0,0),6)
# arms with claws
for sx in(-1,1):
    sph((sx*1.9,-.35,1.7),(.5,.5,.95),'Skin',16,(0,sx*.35,0))
    for k in(-1,0,1):
        cone((sx*(2.1+abs(k)*.04),-.45+k*.2,.8),.09,.35,'Tooth',(math.pi,0,0),6)
# legs
for sx in(-1,1):
    sph((sx*.8,-.1,.55),(.7,.75,.55),'Skin',16)
    sph((sx*.8,-.45,.2),(.62,.7,.22),'Skin',16)
bpy.ops.object.select_all(action='DESELECT')
for o in objs:o.select_set(True)
bpy.context.view_layer.objects.active=objs[0]
bpy.ops.object.join();o=bpy.context.object;o.name='Ghoul'
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
print('DIM',o.dimensions)
bpy.ops.export_scene.gltf(filepath='/private/tmp/claude-501/glb2/Ghoul.glb',export_format='GLB',use_selection=True,export_yup=True)
