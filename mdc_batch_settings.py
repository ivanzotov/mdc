file_or_dir = "o:/project/scenes/Episode_01_Scene_01.mb"
template = "//snowqueen/03_characters/characters/?/builds/dynamic/build_?_cache.mb"
refs = {"vegard":template} # will search ref by *key*, and replace to template
set_names = {'vegard':['*vegard*:cache_set']}
save_cache_to = "o:/project/data/Episode_01_Scene_01"
start = False # get Timeslider min if False
end = False # get Timeslider max if False