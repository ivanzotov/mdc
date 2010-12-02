import maya.cmds as cmds
import maya.mel as mel

# Prepare selected objects for cache
def prepare(setname="cache", groupname="cache", prefix="cache_"):
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
    setofshapes(setname)
    
    i = 0
    for obj in dup:
        cmds.blendShape([selection[i], obj], w=(0, 1),o="world", foc=True)
        objects = []
        objects.append(obj)
        addattr(objects, prefix+str(i))
        i=i+1

# Create shapes's set of selected objects
def setofshapes(setname):
    sel = shapes()
    
    if cmds.objExists(setname):
        cmds.sets(sel, add=setname)    
    else:
        cmds.sets(sel, n=setname)

# Return shapes of selected objects
def shapes()
    return cmds.ls(sl=True, s=True, dag=True, ni=True, l=True)

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
def create(start, end, dir, smr=1, sch=False, attrcachefile="cachefile"):
    set = cmds.ls(sl=True, l=True)
   
    if len(set) == 0:
        cmds.warning("Please select objects!")
        return

    if sch == True:
        cmds.cacheFile(f=attrcachefile, staticCache=0, st=start, et=end, sch=True, points=set, smr=smr, dir=dir, format='OneFile')   
        return
       
    i = 0
    for shape in set:
        cachefile = cmds.getAttr(shape+"."+attrcachefile)
        cmds.cacheFile(f=cachefile, staticCache=0, st=start, et=end, points=shape, smr=smr, dir=dir, format='OneFile')
        i=i+1

#Connect cache to selected shapes
def attach(dir, attrcachefile="cachefile"):
    set = cmds.ls(sl=True, l=True)
    
    for shape in set:
        cachefile = cmds.getAttr(shape+"."+attrcachefile)
        switch = mel.eval('createHistorySwitch("'+shape+'",false)')
        cacheNode = cmds.cacheFile(f=cachefile+".xml", ia='%s.inp[0]' % switch , directory=dir, attachFile=True)
        cmds.setAttr( '%s.playFromCache' % switch, 1 )

