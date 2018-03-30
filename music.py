from __future__ import unicode_literals
import youtube_dl
import sys
import urllib.request
import urllib.parse
import re

def print_all_links(search_results):
	"""
		@param:
			search_results: a list of links
		returns
			None
	"""
	for link in search_results:
		print("http://www.youtube.com/watch?v=" + link)

def get_links(song_name):
	"""
		@param
			song_name: a string
		returns
			A list of youtube links
	"""

	ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

	print("searching...")
	query_string = urllib.parse.urlencode({"search_query" : song_name})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)

	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	return search_results


def display_information(search_results):
	"""
		@param:
			A list of links
		returns:
			None
	"""
	ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
	with ydl:
		result = ydl.extract_info(
			search_results,
			download=False # We just want to extract the info
		)
	if 'entries' in result:
	    # Can be a playlist or a list of videos
	    video = result['entries'][0]
	else:
	    # Just a video
	    video = result

	print(video)
	video_url = video['url']
	print(video_url)	


def query_and_download():
	"""
		@param
			None
		returns
			None
	"""
	
	song_name = input("Enter a song name: ").strip()
	
	search_results = get_links(song_name)

	# display_information(search_results)
	print_all_links(search_results)
	
	print("{} results found. Downloading the first one.".format(len(search_results)))
	ydl_opts = {'preferredcodec':'mp3'}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		link = []
		link.append(search_results[0])
		ydl.download(link)


def main():
	"""
	 The main program
	"""

	query_and_download()



if __name__ == '__main__':
	main()
