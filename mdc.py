import maya.cmds as cmds
import maya.mel as mel

# Prepare selected objects for cache in world coord
def prepare(setname="for_cache", groupname="for_cache_group"):
    selection = cmds.ls(sl=True, l=True)
    selection_shapes = cmds.ls(sl=True, s=True, dag=True, ni=False)
    
    if len(selection) == 0:
        cmds.warning("Please select objects for cache!")
        return
    cmds.duplicate()
    dup = cmds.ls(sl=True, l=True)
    
    if cmds.objExists(groupname):
        cmds.parent(dup, groupname)
    else:
        cmds.group(w=True, n=groupname)
    
    cmds.select(groupname)
    dup = cmds.ls(sl=True, s=True, dag=True, ni=True, l=True)
    
    if cmds.objExists(setname):
        cmds.sets(dup, add=setname)    
    else:
        set = cmds.sets(dup, n=setname)
    
    i = 0
    for obj in dup:
        cmds.blendShape([selection[i], obj], w=(0, 1),o="world", foc=True)
        objects = []
        objects.append(obj)
        addattr(objects, "cache_"+str(i))
        i=i+1
        
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
def create(start, end, dir, attrcachefile="cachefile"):
    set = cmds.ls(sl=True, l=True)
   
    if len(set) == 0:
        cmds.warning("Please select objects!")
        return
       
    i = 0
    for shape in set:
        cachefile = cmds.getAttr(shape+"."+attrcachefile)
        cmds.cacheFile(f=cachefile, staticCache=0, st=start, et=end, points=shape, dir=dir, format='OneFile')
        i=i+1

#Connect cache to selected shapes
def attach(dir, attrcachefile="cachefile"):
    set = cmds.ls(sl=True, l=True)
    
    for shape in set:
        cachefile = cmds.getAttr(shape+"."+attrcachefile)
        switch = mel.eval('createHistorySwitch("'+shape+'",false)')
        cacheNode = cmds.cacheFile(f=cachefile+".xml", ia='%s.inp[0]' % switch , directory=dir, attachFile=True)
        cmds.setAttr( '%s.playFromCache' % switch, 1 )

