from __future__ import unicode_literals
import youtube_dl
import sys
import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup


def print_all_links(search_results):
	"""
		@param:
			search_results: a list of links
		returns
			None
	"""
	for link in search_results:
		# print("http://www.youtube.com/watch?v=" + link)
		print(link)

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

	youtube_string = "http://www.youtube.com/watch?v=";
	for i in range(0,len(search_results)):
		search_results[i] = youtube_string + search_results[i]
	return search_results


def display_information(search_results):
	"""
		Prints the details of the video.
		@param:
			A list of links
		returns:
			None
	"""
	ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
	video_titles = []
	# len(search_results)
	for i in range(0, min(len(search_results), 10)):
		try:
			with ydl:
				result = ydl.extract_info(
					search_results[i],
					download=False # We just want to extract the info
				)
			if 'entries' in result:
			    # Can be a playlist or a list of videos
			    video = result['entries'][0]
			else:
			    # Just a video
			    video = result				
			# print(video)
			video_titles.append(video['title'])
			# video_url = video['webpage_url']
			# print(video_url)	
		except Exception as e:
			continue
	for i in range(0, len(video_titles)):
		print(str(i+1) + " -> " + video_titles[i])


def query_and_download():
	"""
		@param
			None
		returns
			None
	"""
	
	song_name = input("Enter a song name: ").strip()
	
	search_results = get_links(song_name)
	display_information(search_results)
	# print_all_links(search_results)

	num = input("which one would you like to download ? : ").strip()
	print("{} results found. Downloading song number {}.".format(len(search_results), int(num)))

	# url = urllib.request.urlopen("https://youtubemp3api.com/@api/button/mp3/cH4E_t3m3xM")
	# content = url.read()
	# soup = BeautifulSoup(content, "html.parser")
	# print(soup)
	# for a in soup.findAll('a',href=re.compile('http.*\.mp3')):
	# 	print ("URL:", a['href'])

	ydl_opts = {
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		link = []
		link.append(search_results[int(num)-1])
		ydl.download(link)


def main():
	"""
	 The main program
	"""
	query_and_download()



if __name__ == '__main__':
	main()
