import maya.cmds as cmds
import maya.mel as mel
import maya.standalone
import sys
import os
from mdc import *
from mdc_batch_settings import *

maya.standalone.initialize()

def batch(file_or_dir_name, set_names, save_cache_to, start=False, end=False, file_or_dir=True):
  for ref, replace_to in refs.iteritems():
    replace_to = replace_to.replace("?", ref)
    if replace_ref(ref, replace_to) == False:
      print "Reference "+ref+" not found"
      continue

  for dir, sets in set_names.iteritems():
    for set in sets:
      if len(cmds.ls(set)) == 0:
        print "Set "+set+" doesn't exists"
        continue

      cmds.select(set, r=True)
    
      if start==False:
        start = cmds.playbackOptions(q=True, min=True)
      if end==False:
        end = cmds.playbackOptions(q=True, max=True)
      
      if file_or_dir:
        create(start, end, save_cache_to+"/"+dir)
      else:
        create(start, end, save_cache_to+"/"+file_or_dir_name.rstrip(".mb")+"/"+dir)
    
      print "Cache saved to " + save_cache_to

file_or_dir = file_or_dir.rstrip("/")
save_cache_to = save_cache_to.rstrip("/")

if not os.path.exists(file_or_dir):
  print "File or dir "+file_or_dir+" doesn't exists"
  exit(0)

if os.path.isfile(file_or_dir):
  cmds.file(file_or_dir, o=True)
  batch(file_or_dir, set_names, save_cache_to, start, end)

if os.path.isdir(file_or_dir):
  for file in cmds.getFileList(folder=file_or_dir+"/"):
    cmds.file(file_or_dir+"/"+file, o=True)
    batch(file, set_names, save_cache_to, start, end, False)
