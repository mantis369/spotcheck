from time import sleep
from os import listdir
from os.path import isdir, join
from re import compile

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from credentials import client_id as cid, client_secret as secret

ofn = "keepers.txt"
local_lib = "c:\\Users\\Derik Stiller\\Music"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def cleanUpFn(fn):
	replacements = [
		"\[.*\]", #brackets
		"\(.*\)", #parentheticals
		"^[0-9]* ", #track number
		"^[0-9]*\-[0-9]* ", #disc and track
		"Compilations",
		"Various Artists",
		"\.mp3$",
		"\.m4a$"
	]
	whitespace = [
		"_", #underscores
		"  " #double spaces
	]
	for r in replacements:
		x = compile(r)
		fn = x.sub("", fn)
	for w in whitespace:
		x = compile(w)
		fn = x.sub(" ", fn)		
	return fn
	
with open(ofn, "w") as outf:
	for a in [a for a in listdir(local_lib) if not "desktop.ini" in a and not "MusicBee" in a]:
		print("Artist", a)
		for al in [al for al in listdir(join(local_lib, a)) if isdir(join(local_lib, a)) and not "DS_Store" in al]:
			al_clean = cleanUpFn(al)
			print("\tAlbum", al_clean)
			for t in [t for t in listdir(join(local_lib, a, al)) if not "DS_Store" in t and t.endswith(".mp3") or t.endswith(".m4a")]:
				t_clean = cleanUpFn(t)
				print("\t\t", t_clean)
				s = " ".join([cleanUpFn(a), al_clean, t_clean])
				print("\t\t\t", s)
				results = sp.search(q=s, limit=5)
				tracks = results["tracks"]["items"]
				print("\t\t\tFound", len(tracks))
				if (len(tracks) == 0):
					outf.write(join(local_lib, a, al, t) + "\n")
				sleep(0.5)	
