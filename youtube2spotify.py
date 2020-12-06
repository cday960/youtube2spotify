from pytube import YouTube
import time
from youtubesearchpython import SearchVideos
import ast
import PySimpleGUI as sg
import string
import os, shutil, getpass, sys

#First window
layout = [[sg.Text("Enter song title: ")], [sg.InputText(key='song name')], [sg.Button("Ok", bind_return_key=True), sg.Button("Cancel")]]
window = sg.Window("Youtube to spotify", layout, margins=(200, 200))

#Window Event
while True:
	event, values = window.read()
	#Assigns searchTitle to the input of the text box
	if event == "Ok":
		searchTitle = values["song name"]
		window.close()
	if event == sg.WIN_CLOSED or event=="Cancel":
		break

#searches youtube for a video with that title and returns the top 20 results
search = SearchVideos(searchTitle, offset = 1, mode = "json", max_results = 20)
#converts it into a dictionary
search = ast.literal_eval(search.result())

#This is all of the printable characters by the utf-8 codec, this will be used to filter out any non english words
#or special characters when displaying them in the second window to prevent errors
printable = set(string.printable)

#Creates a list of all of the results that were given and assigns them to a button for the user to press
layout = []
layout += [ [sg.Text("Click one to download")] ]
for i in range(20):
	temp = str(search["search_result"][i]["title"])
	temp = ''.join(filter(lambda x: x in printable, temp))
	layout += [sg.Text(f'{i+1}. '), sg.Button(temp, key=str(i+1))],	
layout += [ [sg.Button("Cancel")] ]

#Results page, assigns songLink and songName to their respective values
window = sg.Window("Youtube to Spotify: Results", layout)
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event=="Cancel":
		sys.exit()
		break
	for i in range(20):
		if event == str(i+1):
			songLink = ''.join(filter(lambda x: x in printable, str(search["search_result"][i]["link"])))
			songName = ''.join(filter(lambda x: x in printable, str(search["search_result"][i]["title"])))
			break
	break

#Downloads the first available version from the link and gets rid of the video so there is only audio
#you need an audio only file to import to spotify
YouTube(songLink).streams.filter(only_audio=True).first().download()

#Declares the new path which is the music file (mac) and the old path which is the current working directory
newPath = '/Users/{name}/Music/Music/{musicFile}.mp4'.format(name=getpass.getuser(), musicFile=songName)
oldPath = ('{dir}/{musicFile}.mp4').format(dir=os.getcwd(), musicFile=songName)
#Moves the file so spotify can read it
shutil.move(str(oldPath), str(newPath))
window.close()

#Done box
layout = [[sg.Text("Done :)"), sg.Button("Ok", key="exit")]]
window = sg.Window("All done", layout, margins=(100, 100))
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event=="exit":
		break

window.close()