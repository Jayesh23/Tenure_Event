import os
import glob

i=1

path = os.listdir("saved/")

for filename in path:

	name, ext = filename.split('.')
	prev_name = 'saved/' + filename
	saved_name = 'saved/' + str(i) + '.' + ext
	os.rename(prev_name, saved_name)
	i+=1