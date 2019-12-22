from os import listdir, unlink
from os.path import isdir, join
from shutil import rmtree

infn = "keepers.txt"
local_lib = "c:\\Users\\Derik Stiller\\Music"

with open(infn, "r") as inf:
	tracks = [ln.strip() for ln in inf]
	albums = []
	for t in tracks:
		last_slash = t.rfind("\\")
		a = t[:last_slash]
		if not a in albums:
			albums.append(a)
		
	print("We have", len(albums), "keeper albums with", len(tracks), "tracks.")
	
	del_count = 0
	
	for a in [a for a in listdir(local_lib) if not "desktop.ini" in a and not "MusicBee" in a]:
		for al in [al for al in listdir(join(local_lib, a)) if isdir(join(local_lib, a)) and not "DS_Store" in al]:	
			audio_files = [t for t in listdir(join(local_lib, a, al)) if not "DS_Store" in t and t.endswith(".mp3") or t.endswith(".m4a")]
			other_files = [f for f in listdir(join(local_lib, a, al)) if not f in audio_files]
			
			if len(other_files) > 0:
				print("\tDealing with", len(other_files), "non-audio files for album", al)
				for f in other_files:
					try:
						unlink(join(local_lib, a, al, f))
					except:
						print("\t\tCan't delete", f, "!")
						try:
							rmtree(join(local_lib, a, al, f))
							print("\t\tGot rid of", f, "as a directory.")
						except:
							print("\t\tWasn't able to treat", f, "as a directory, either!")
						
			if join(local_lib, a, al) in albums:
				continue
				
			for t in audio_files:
				fn = join(local_lib, a, al, t)
				try:
					#unlink(fn)
					del_count += 1
				except:
					print("\t\tFailure: we couldn't delete", t, "by", a, "from album", al)
					
print("I deleted", del_count, "audio files.")

empty_count = 0

def removeEmptyFolders(path, removeRoot=True):
	#based on https://www.jacobtomlinson.co.uk/posts/2014/python-script-recursively-remove-empty-folders/directories/	
	if not isdir(path):
		return
	
	files = listdir(path)
	if len(files):
		for f in files:
			fullpath = join(path, f)
			if isdir(fullpath):
				removeEmptyFolders(fullpath)
	
	global empty_count	
	files = listdir(path)
	if len(files) == 0 and removeRoot:
		empty_count += 1
		try:
			rmtree(path) #changed from os.rmdir for consistency with my code above
		except:
			print("Couldn't delete the directory", path)
		
removeEmptyFolders(local_lib)
print("I removed", empty_count, "empty directories.")