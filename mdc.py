import maya.cmds as cmds
import maya.mel as mel

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
  references = cmds.ls(rf=True)

  i = 0
  for r in references:
    references[i] = r.replace(":","_")
    i = i + 1

  if len(references)==0:
    return False

  cmds.file(path, lr=references[0])

def increase_per(per):
    global completed_per
    completed_per = completed_per + per
    print completed_str % completed_per

