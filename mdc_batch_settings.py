file_or_dir = "o:/project/scenes/"
template = "//snowqueen/03_characters/characters/?/builds/dynamic/build_?_cache.mb"
refs = {"vegard":template, "kareta":template} # will search ref by *key*, and replace to template
set_names = {'vegard':'*vegard*:cache_set'}
save_cache_to = "o:/project/data/"
start = False # get Timeslider min if False
end = False # get Timeslider max if False
step = 1



#script.py "test1.mb" "set1" "o:/cache/test1/set1" "'vegard':'//snowqueen/vegard_build.mb', 'kareta':'/kareta_build.mb'" False False 1 
#script.py "test1.mb" "set2" "o:/cache/test1/set2" "'vegard':'//snowqueen/vegard_build.mb', 'kareta':'/kareta_build.mb'" False False 1 
#script.py "test2.mb" "set1" "o:/cache/test2/set1" "'vegard':'//snowqueen/vegard_build.mb', 'kareta':'/kareta_build.mb'" False False 1 
#script.py "test2.mb" "set2" "o:/cache/test2/set2" "'vegard':'//snowqueen/vegard_build.mb', 'kareta':'/kareta_build.mb'" False False 1 
#script.py "test3.mb" "set1" "o:/cache/test3/set1" "'vegard':'//snowqueen/vegard_build.mb', 'kareta':'/kareta_build.mb'" False False 1 
