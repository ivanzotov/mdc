import maya.cmds as cmds
import maya.mel as mel
import maya.standalone
import sys
import os
from mdc import *

if sys.argv[1] == "file_settings":
  from mdc_batch_settings import *
else:
  file_or_dir = sys.argv[1]
  refs = {}
  for arg in sys.argv[2].split(","):
    key, value = sys.argv[2].split(":", 1)
    refs[key] = value
  set_names = {}
  for arg in sys.argv[3].split(","):
    key, value = sys.argv[3].split(":", 1)
    set_names[key] = value
  save_cache_to = sys.argv[4]
  start = False
  if sys.argv[5] != "False": start = int(sys.argv[5])
  end = False
  if sys.argv[6] != "False": end = int(sys.argv[6])
  step = sys.argv[7]

maya.standalone.initialize()

def batch(file_or_dir_name, set_names, save_cache_to, start=False, end=False, file_or_dir=True):
  for ref, replace_to in refs.iteritems():
    replace_to = replace_to.replace("?", ref)
    if replace_ref(ref, replace_to) == False:
      cmds.warning("Reference "+ref+" not found")
      continue

  for dir, set in set_names.iteritems():
    if len(cmds.ls(set)) == 0:
      cmds.warning("Set "+set+" doesn't exists")
      continue

    cmds.select(set, r=True)
  
    if start==False:
      start = cmds.playbackOptions(q=True, min=True)
    if end==False:
      end = cmds.playbackOptions(q=True, max=True)
    
    if file_or_dir:
      create(start, end, save_cache_to+"/"+dir, step)
    else:
      create(start, end, save_cache_to+"/"+file_or_dir_name.rstrip(".mb")+"/"+dir, step)
  
    print "Cache saved to " + save_cache_to

file_or_dir = file_or_dir.rstrip("/")
save_cache_to = save_cache_to.rstrip("/")

if not os.path.exists(file_or_dir):
  cmds.warning("File or dir "+file_or_dir+" doesn't exists")
  exit(0)

if os.path.isfile(file_or_dir):
  cmds.file(file_or_dir, o=True)
  batch(file_or_dir, set_names, save_cache_to, start, end)
  cmds.file(file_or_dir, mf=False)

if os.path.isdir(file_or_dir):
  for file in cmds.getFileList(folder=file_or_dir+"/"):
    cmds.file(file_or_dir+"/"+file, o=True)
    batch(file, set_names, save_cache_to, start, end, False)
    cmds.file(file_or_dir+"/"+file, mf=False)
