import maya.cmds as cmds
import maya.mel as mel
import re
import math

# TODO Auto find near objects to blend

completed_str = "Completed: %d percents"
completed_per = 0

# Prepare selected objects for cache
def prepare(setname="cache_set", groupname="cache_group", prefix="cache_"):
    selection = cmds.ls(sl=True, l=True)
    
    if len(selection) == 0:
        cmds.warning("Please select objects!")
        return
        
    cmds.duplicate()
    dup = cmds.ls(sl=True, l=True)
    
    if cmds.objExists(groupname):
        cmds.parent(dup, groupname)
    else:
        cmds.group(w=True, n=groupname)
    
    cmds.select(groupname)
    dup = get_shapes()
    add_to_set_of_shapes(setname, dup)
    
    i = 0
    for obj in dup:
        cmds.blendShape([selection[i], obj], w=(0, 1),o="world", foc=True)
        objects = []
        objects.append(obj)
        addattr(objects, prefix+str(i))
        i=i+1

# Prepare selected objects for attach
def prepare_for_attach(setname, sel=False):
    add_to_set_of_shapes(setname, sel)

# Create shapes's set of selected objects
def add_to_set_of_shapes(setname, sel=False):    
    if sel == False:
        sel = get_shapes()

    if cmds.objExists(setname):
        cmds.sets(sel, add=setname)    
    else:
        cmds.sets(sel, n=setname)

# Return shapes of selected objects
def get_shapes(sel=False):
    if sel == False:
        sel = cmds.ls(sl=True, l=True)
        
    return cmds.ls(sel, s=True, dag=True, ni=True, l=True)

# Blend in world coords
def blend():
    sel = cmds.ls(sl=True)
    cmds.blendShape([sel[0], sel[1]], w=(0, 1),o="world", foc=True)
    cmds.hide(sel[0])
               
# Add attribute for selected objects       
def addattr(objects=False, name="cache", attrcachefile="cachefile"):
    if objects == False:
        objects = cmds.ls(sl=True, l=True)
        
    for obj in objects:       
        cmds.addAttr(obj, ln=attrcachefile, dt="string")
        cmds.setAttr(obj+"."+attrcachefile, name, type="string")

# Delete attribute from selected objects
def delattr(attrcachefile="cachefile"):
    objects = cmds.ls(sl=True, l=True)
    for obj in objects:
        cmds.select(obj)
        cmds.deleteAttr(obj+"."+attrcachefile)

#Caching selected shapes
def create(start, end, dir, smr=1, attrcachefile="cachefile", per=False):
    set = cmds.ls(sl=True, l=True)

    len_set = float(len(set))
    if len_set == 0:
        cmds.warning("Please select objects!")
        return
    
    i = 0
    for shape in set:
        cachefile = cmds.getAttr(shape+"."+attrcachefile)
        cmds.cacheFile(f=cachefile, staticCache=0, st=start, et=end, points=shape, smr=smr, dir=dir, format='OneFile')
        if not per == False:
          increase_per(per/len_set)
        i=i+1

#Connect cache to selected shapes
def attach(dir, attrcachefile="cachefile"):
    set = cmds.ls(sl=True, l=True)
    
    for shape in set:
        cachefile = cmds.getAttr(shape+"."+attrcachefile)
        switch = mel.eval('createHistorySwitch("'+shape+'",false)')
        cacheNode = cmds.cacheFile(f=cachefile+".xml", ia='%s.inp[0]' % switch , directory=dir, attachFile=True)
        cmds.setAttr( '%s.playFromCache' % switch, 1 )

# Replace ref
def replace_ref(ref, path):
  refs = cmds.ls(rf=True)
  references = []

  for r in refs:
    if re.match(".*"+ref+".*", r):
      references.append(r)

  if len(references)==0:
    return False
  
  cmds.file(path, lr=references[0])

# Incease percents ( used for batch )
def increase_per(per):
    global completed_per
    completed_per = completed_per + per
    cmds.warning(completed_str % int(round(completed_per)))

# Ls set by regular
def ls_set(set_re, all_sets=False):
  if all_sets == False:
    all_sets = cmds.ls(set=True)

  sets = []
  for s in all_sets:
    if re.match(set_re, s):
      sets.append(s)

  return sets
  

# Objects that will be blendshaped 
origin_objects = []

# Objects where need find
other_objects = []

# Load origin objects
def get_origin():
    global origin_objects
    origin_objects = cmds.ls(sl=True)

# Load other objects
def get_other():
    global other_objects
    other_objects = cmds.ls(sl=True)
    

# Blend same objects
def blend_same(r=0, step=0.1):   
    count = 0
    
    o_objects = other_objects
    or_objects = origin_objects  
    
    i = 0  

    while i < r:    
        for org_obj in or_objects:       
            org_min = cmds.getAttr(org_obj+'.boundingBoxMin')[0]
            org_max = cmds.getAttr(org_obj+'.boundingBoxMax')[0]
    
            org_parent_transform = cmds.getAttr(org_obj+'.parentMatrix')        
            
            org_min = plus_parent_transform(org_min, org_parent_transform)
            org_max = plus_parent_transform(org_max, org_parent_transform)
    
            for obj in o_objects:
                min = cmds.getAttr(obj+'.boundingBoxMin')[0]
                max = cmds.getAttr(obj+'.boundingBoxMax')[0]           
                parent_transform = cmds.getAttr(obj+'.parentMatrix')
        
                min = plus_parent_transform(min, parent_transform)
                max = plus_parent_transform(max, parent_transform)           
    
                comp_min = point_distance(org_min, min)
                comp_max = point_distance(org_max, max)
                   
                if comp_min <= i and comp_max <= i:
                    cmds.select(org_obj)
                    cmds.select(obj, add=True)                
                    blend()
                    o_objects.remove(obj)
                    or_objects.remove(org_obj)
                    
                    count = count + 1
    
        i = i + step

    print "Blended " + str(count)
        

def plus_parent_transform(transform, parent_transform):
    return (transform[0]+parent_transform[12], transform[1]+parent_transform[13], transform[2]+parent_transform[14])
    

# Return distance of two points
def point_distance(p1, p2):
  return math.sqrt(math.pow(p2[0]-p1[0], 2)+math.pow(p2[1]-p1[1], 2)+math.pow(p2[2]-p1[2], 2))




