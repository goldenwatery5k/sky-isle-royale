import bpy,math
def clear():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete()
def mat(n,c,r=.55,em=None):
    k=bpy.data.materials.new(n);k.use_nodes=True
    b=next(x for x in k.node_tree.nodes if x.type=='BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=r
    if em:
        b.inputs['Emission Color'].default_value=(*em,1);b.inputs['Emission Strength'].default_value=1.6
    return k
M={'Skin':mat('Skin',(.3,.12,.55),.55),'Belly':mat('Belly',(.4,.2,.65),.55),'Eye':mat('Eye',(1,.15,.1),.3,(1,.15,.08)),'Tooth':mat('Tooth',(.97,.97,.95),.35),'Dark':mat('Dark',(.06,.02,.1),.7),'Horn':mat('Horn',(.9,.85,.7),.5)}
clear();objs=[]
def sph(loc,sc,m,seg=32,rot=(0,0,0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=seg//2,location=loc,rotation=rot);o=bpy.context.object;o.scale=sc;bpy.ops.object.transform_apply(scale=True,rotation=True);o.data.materials.append(M[m]);bpy.ops.object.shade_smooth();objs.append(o);return o
def cone(loc,r,h,m,rot=(0,0,0),v=14,r2=0):
    bpy.ops.mesh.primitive_cone_add(vertices=v,radius1=r,radius2=r2,depth=h,location=loc,rotation=rot);o=bpy.context.object;o.data.materials.append(M[m]);bpy.ops.object.shade_smooth();objs.append(o);return o
def box(loc,sc,m,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc,rotation=rot);o=bpy.context.object;o.scale=sc;bpy.ops.object.transform_apply(scale=True,rotation=True);o.data.materials.append(M[m]);objs.append(o);return o
# wide squat body+head
sph((0,0,1.8),(1.95,1.45,1.7),'Skin',40)
sph((0,.05,.95),(1.7,1.35,.95),'Skin',32)
# crown spikes: center + flanking + ear spikes
cone((0,.05,3.75),.42,1.5,'Skin',(0,0,0))
for sx in(-1,1):
    cone((sx*.7,.05,3.4),.36,1.2,'Skin',(0,sx*.25,0))
    cone((sx*1.38,.05,3.0),.4,1.25,'Skin',(0,sx*.6,0))
# arms: raised V, tapered
for sx in(-1,1):
    cone((sx*2.45,-.1,2.1),.62,1.9,'Skin',(0,sx*.95,0),14)
# eyes: angry slanted (inner end lower)
for sx in(-1,1):
    sph((sx*.85,-1.42,2.4),(.7,.12,.4),'Eye',20,(0,-sx*.6,0))
    sph((sx*.88,-1.52,2.36),(.09,.04,.2),'Dark',10,(0,-sx*.6,0))
# huge grin: dark lip then white band
sph((0,-1.33,1.3),(1.55,.1,.62),'Dark',32)
sph((0,-1.4,1.33),(1.45,.1,.52),'Tooth',32)
for i in range(-3,4):
    box((i*.36,-1.5,1.33),(.04,.03,.9),'Dark')
box((0,-1.5,1.33),(2.5,.03,.04),'Dark')
# legs
for sx in(-1,1):
    sph((sx*.95,-.2,.5),(.85,.9,.5),'Skin',20)
    for k in(-1,0,1):
        cone((sx*.95+k*.3,-.95,.12),.16,.45,'Skin',(math.pi/2+.0,0,0),10)
bpy.ops.object.select_all(action='DESELECT')
for o in objs:o.select_set(True)
bpy.context.view_layer.objects.active=objs[0]
bpy.ops.object.join();o=bpy.context.object;o.name='Ghoul'
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
print('DIM',o.dimensions)
bpy.ops.export_scene.gltf(filepath='/private/tmp/claude-501/glb2/Ghoul.glb',export_format='GLB',use_selection=True,export_yup=True)
