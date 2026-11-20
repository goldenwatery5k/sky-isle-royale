import bpy,bmesh,math,random
from mathutils import Vector
random.seed(7)
def clear():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete()
def mat(n,c,r=.45,m=.5,em=None,es=3):
    k=bpy.data.materials.new(n);k.use_nodes=True
    b=next(x for x in k.node_tree.nodes if x.type=='BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=r;b.inputs['Metallic'].default_value=m
    if em:
        b.inputs['Emission Color'].default_value=(*em,1);b.inputs['Emission Strength'].default_value=es
    return k
M={'Hull':mat('Hull',(.86,.88,.92),.4,.3),'Dark':mat('Dark',(.1,.11,.14),.5,.7),'Red':mat('Red',(.8,.1,.08),.45,.3),'Glass':mat('Glass',(.1,.3,.5),.1,.2,(.1,.45,.8),1.2),'Glow':mat('Glow',(.3,.7,1),.3,0,(.3,.75,1),6),'NavR':mat('NavR',(1,.1,.1),.3,0,(1,.1,.1),8),'NavG':mat('NavG',(.1,1,.2),.3,0,(.1,1,.2),8),'Gold':mat('Gold',(.9,.68,.2),.3,.9),'Blue':mat('Hull',(.86,.88,.92),.4,.3)}
clear();objs=[]
def reg(o,m,smooth=True):
    o.data.materials.append(M[m])
    if smooth: bpy.ops.object.shade_smooth()
    objs.append(o);return o
X=math.pi/2
def lathe(profile,m,steps=40,grow=0):
    me=bpy.data.meshes.new('l');bm=bmesh.new()
    vs=[bm.verts.new((r+grow if r>0 else 0,y,0)) for y,r in profile]
    for a,b in zip(vs,vs[1:]):bm.edges.new((a,b))
    bmesh.ops.spin(bm,geom=bm.verts[:]+bm.edges[:],cent=(0,0,0),axis=(0,1,0),angle=math.tau,steps=steps,use_merge=True,use_duplicate=False)
    bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=.0005)
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    bm.to_mesh(me);bm.free();o=bpy.data.objects.new('l',me);bpy.context.collection.objects.link(o)
    bpy.context.view_layer.objects.active=o;o.select_set(True);return reg(o,m)
def cyl(loc,r,h,m,rot=(0,0,0),v=24,r2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=v,radius1=r,radius2=r if r2 is None else r2,depth=h,location=loc,rotation=rot);return reg(bpy.context.object,m)
def box(loc,sc,m,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc,rotation=rot);o=bpy.context.object;o.scale=sc;bpy.ops.object.transform_apply(scale=True);return reg(o,m,False)
def tor(loc,R,r,m,rot=(0,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R,minor_radius=r,major_segments=24,minor_segments=8,location=loc,rotation=rot);return reg(bpy.context.object,m)
def poly(verts,faces,m):
    me=bpy.data.meshes.new('p');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('p',me);bpy.context.collection.objects.link(o)
    bpy.context.view_layer.objects.active=o;o.select_set(True);return reg(o,m,False)
# ---- fuselage (lathe): nose -Y, tail +Y ----
body=[(-7.7,0),(-7.55,.18),(-7.1,.45),(-6.4,.78),(-5.5,1.05),(-4.5,1.25),(-3.4,1.38),(-2.4,1.44),(3.4,1.44),(4.0,1.36),(4.7,1.22),(5.1,1.3),(5.5,1.3),(5.5,1.0)]
lathe(body,'Hull')
lathe([(-7.7,0),(-7.55,.18),(-7.1,.45),(-6.5,.74),(-6.1,.88)],'Red',grow=.018)       # red nose cap
cyl((0,-7.95,0),.05,.8,'Dark',(X,0,0),10,.02)                                          # lightning rod
# bands + panel rings
for y,w,c in((-5.6,.5,'Red'),(-5.0,.12,'Dark'),(-2.0,.16,'Dark'),(0.0,.9,'Red'),(0.7,.12,'Dark'),(3.0,.16,'Dark'),(4.4,.2,'Dark')):
    cyl((0,y,0),1.455 if y>-3 else 1.22+ (y+5.6)*.0,w,c,(X,0,0),40)
# portholes (both sides) + frames
for k in range(5):
    y=-3.6+k*1.05
    for sx in(-1,1):
        cyl((sx*1.43,y,.25),.3,.1,'Glass',(0,X,0),20)
        tor((sx*1.44,y,.25),.34,.05,'Gold',(0,X,0))
# big viewport near nose
cyl((0,-4.7,1.1),.5,.1,'Glass',(.55,0,0),20);tor((0,-4.7,1.1),.55,.07,'Dark',(.55,0,0))
# gold emblem plate + hatch
box((1.45,-0.9,.0),(.08,1.1,.7),'Gold');box((1.46,-0.9,.0),(.08,.85,.45),'Red')
cyl((-1.44,2.0,.2),.45,.09,'Dark',(0,X,0),24);tor((-1.45,2.0,.2),.45,.05,'Hull',(0,X,0))
# umbilical pipes + vents + rivet strip
for ang in(math.radians(70),math.radians(110)):
    cyl((math.cos(ang)*1.5,.4,math.sin(ang)*1.5),.07,7.2,'Dark',(X,0,0),10)
for y in(-1.2,-0.8,-0.4):
    box((0,y,1.46),(.9,.14,.08),'Dark')
for i in range(30):
    a=i/30*math.tau
# ---- 4 fins (axis aligned) ----
for k in range(4):
    a=k*math.pi/2
    pts=[(1.35,1.6,0),(1.35,5.2,0),(4.6,6.2,0),(4.3,4.4,0)]
    t=.09
    v=[(x,y,z+s*t) for s in(-1,1) for (x,y,z) in pts]
    f=[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    o=poly(v,f,'Red')
    bpy.context.view_layer.objects.active=o;o.rotation_euler=(0,a,0);bpy.ops.object.transform_apply(rotation=True)
    # dark edge strip + nav light at tip
    cx,cz=math.sin(a),math.cos(a)
    x=4.5; 
    sph_loc=(math.cos(a)*4.55,6.15,-math.sin(a)*4.55)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=.11,location=sph_loc);reg(bpy.context.object,'NavR' if k%2==0 else 'NavG')
# ---- 4 boosters (diagonal) ----
for k in range(4):
    a=math.pi/4+k*math.pi/2;R=1.98;px,pz=math.cos(a)*R,math.sin(a)*R
    cyl((px,.6,pz),.58,7.6,'Hull',(X,0,0),28)
    cyl((px,-4.0,pz),.58,1.9,'Red',(X,0,0),28,.04)
    cyl((px,-5.05,pz),.05,.3,'Dark',(X,0,0),8,.02)
    cyl((px,4.05,pz),.6,.3,'Dark',(X,0,0),28);cyl((px,1.2,pz),.595,.18,'Dark',(X,0,0),28);cyl((px,-1.6,pz),.595,.18,'Dark',(X,0,0),28)
    cyl((px,4.75,pz),.42,1.0,'Dark',(X,0,0),22,.62)
    cyl((px,5.2,pz),.4,.06,'Glow',(X,0,0),22)
    for y in(-2.2,1.8):box((px*.5,y,pz*.5),(.18,.5,.18),'Dark',(0,-a,0))
# ---- main engine ----
cyl((0,6.5,0),1.05,2.1,'Dark',(X,0,0),36,1.55)
tor((0,7.5,0),1.55,.09,'Gold',(X,0,0))
cyl((0,7.2,0),1.35,.08,'Glow',(X,0,0),36)
for k in range(8):
    a=k/8*math.tau;box((math.cos(a)*1.2,6.2,math.sin(a)*1.2),(.1,1.4,.1),'Dark',(0,-a,0))
bpy.ops.object.select_all(action='DESELECT')
for o in objs:o.select_set(True)
bpy.context.view_layer.objects.active=objs[0]
bpy.ops.object.join();o=bpy.context.object;o.name='Rocket'
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
print('DIM',o.dimensions,len(o.data.polygons))
bpy.ops.export_scene.gltf(filepath='/private/tmp/claude-501/glb2/Rocket.glb',export_format='GLB',use_selection=True,export_yup=True)
