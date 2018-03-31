#############################################################
# Imports
#############################################################

from __future__ import unicode_literals
import os
from bs4 import BeautifulSoup as bs
import requests


try:
    from Tkinter import Entry, Frame, Label, StringVar
    from Tkconstants import *
except ImportError:
    from tkinter import Entry, Frame, Label, StringVar
    from tkinter.constants import *
from tkinter import ttk

import youtube_dl
import sys
import urllib.request
import urllib.parse
import re

#############################################################
# Global Variables
#############################################################

quality="192" 
search_results = []

#############################################################
# Utility functions
#############################################################

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
    query_string = urllib.parse.urlencode({"search_query": song_name})
    html_content = urllib.request.urlopen(
        "http://www.youtube.com/results?" + query_string)

    search_results = re.findall(
        r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

    youtube_string = "http://www.youtube.com/watch?v="
    for i in range(0, len(search_results)):
        search_results[i] = youtube_string + search_results[i]
    search_results = list(set(search_results))
    return search_results


def display_information(search_results):
    """
        Prints the details of the video.
        @param:
            A list of links
        returns:
            titles of videos as a list
    """
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    video_titles = []
    for i in range(0, min(len(search_results),5)):
        try:
            with ydl:
                result = ydl.extract_info(
                    search_results[i],
                    download=False  # We just want to extract the info
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
    return video_titles


def query_and_download(text):
    """
        @param
            text: Receive a string from user from gui
        returns
            None
    """
    global search_results
    song_name = text.strip()

    search_results = get_links(song_name)
    video_titles = display_information(search_results)
    show_titles(video_titles)


#############################################################
# GUI Functionality
#############################################################


class filterit:
    value_of_combo = '192'


    def __init__(self, parent):
        self.parent = parent
        self.combo()

    def newselection(self, event):
        global quality
        self.value_of_combo = self.box.get()
        quality = self.value_of_combo


    def combo(self):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value)
        self.box['values'] = ('192', '256', '320')
        self.box.bind("<<ComboboxSelected>>", self.newselection)
        self.box.current(0)
        self.box.pack()

def hex2rgb(str_rgb):
    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color."% str_rgb)

    return tuple(int(v, 16) for v in (r, g, b))

class Placeholder_State(object):
     __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'contains_placeholder'

def add_placeholder_to(entry, placeholder, color="grey", font=None):
    normal_color = entry.cget("fg")
    normal_font = entry.cget("font")
    
    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color=normal_color
    state.normal_font=normal_font
    state.placeholder_color=color
    state.placeholder_font=font
    state.placeholder_text = placeholder
    state.contains_placeholder=True

    def on_focusin(event, entry=entry, state=state):
        if state.contains_placeholder:
            entry.delete(0, "end")
            entry.config(fg = state.normal_color, font=state.normal_font)
        
            state.contains_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get() == '':
            entry.insert(0, state.placeholder_text)
            entry.config(fg = state.placeholder_color, font=state.placeholder_font)
            
            state.contains_placeholder = True

    entry.insert(0, placeholder)
    entry.config(fg = color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")
    
    entry.placeholder_state = state

    return state

class SearchBox(Frame):
    """
        This class is  search box changes colour when we write and other 
        functionality to look like a search box
    """
    def __init__(self, master, entry_width=30, entry_font=None, entry_background="white", entry_highlightthickness=1, button_text="Search", button_ipadx=10, button_background="#009688", button_foreground="white", button_font=None, opacity=0.8, placeholder=None, placeholder_font=None, placeholder_color="grey", spacing=3, command=None):
        Frame.__init__(self, master)
        
        self._command = command

        self.entry = Entry(self, width=entry_width, background=entry_background, highlightcolor=button_background, highlightthickness=entry_highlightthickness)
        self.entry.pack(side=LEFT, fill=BOTH, ipady=1, padx=(0,spacing))
        
        if entry_font:
            self.entry.configure(font=entry_font)

        if placeholder:
            add_placeholder_to(self.entry, placeholder, color=placeholder_color, font=placeholder_font)

        self.entry.bind("<Escape>", lambda event: self.entry.nametowidget(".").focus())
        self.entry.bind("<Return>", self._on_execute_command)

        opacity = float(opacity)

        if button_background.startswith("#"):
            r,g,b = hex2rgb(button_background)
        else:
            # Color name
            r,g,b = master.winfo_rgb(button_background)

        r = int(opacity*r)
        g = int(opacity*g)
        b = int(opacity*b)

        if r <= 255 and g <= 255 and b <=255:
            self._button_activebackground = '#%02x%02x%02x' % (r,g,b)
        else:
            self._button_activebackground = '#%04x%04x%04x' % (r,g,b)

        self._button_background = button_background

        self.button_label = Label(self, text=button_text, background=button_background, foreground=button_foreground, font=button_font)
        if entry_font:
            self.button_label.configure(font=button_font)
            
        self.button_label.pack(side=LEFT, fill=Y, ipadx=button_ipadx)
        
        self.button_label.bind("<Enter>", self._state_active)
        self.button_label.bind("<Leave>", self._state_normal)

        self.button_label.bind("<ButtonRelease-1>", self._on_execute_command)

    def get_text(self):
        entry = self.entry
        if hasattr(entry, "placeholder_state"):
            if entry.placeholder_state.contains_placeholder:
                return ""
            else:
                return entry.get()
        else:
            return entry.get()
        
    def set_text(self, text):
        entry = self.entry
        if hasattr(entry, "placeholder_state"):
            entry.placeholder_state.contains_placeholder = False

        entry.delete(0, END)
        entry.insert(0, text)
        
    def clear(self):
        self.entry_var.set("")
        
    def focus(self):
        self.entry.focus()

    def _on_execute_command(self, event):
        text = self.get_text()
        self._command(text)

    def _state_normal(self, event):
        self.button_label.configure(background=self._button_background)

    def _state_active(self, event):
        self.button_label.configure(background=self._button_activebackground)
###################search box ends##################


def show_titles(video_titles):
    video_titles.reverse()
    for items in video_titles:
        listbox.insert(0,items)

def Downloadit(event):
    global search_results
    global quality
    index = listbox.get(0, "end").index(listbox.get('active'))
    print(index)
    print("{} results found. Downloading song number {}.".format(len(search_results), int(index)))
    ydl_opts={
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality':quality,
        }],
    }
    print("quality: " + str(quality))
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        link = []
        link.append(search_results[int(index)])
        ydl.download(link)

    return index

def  similarsong(event):
    global search_results
    global quality
    index = listbox.get(0, "end").index(listbox.get('active'))
    youtube_string = "http://www.youtube.com"
    link = []
    link.append(search_results[int(index)])
    print(link)
    r = requests.get(link[0])
    page = r.text
    soup = bs(page, 'html.parser')
    res = soup.find_all('a', {'class': "content-link"})
    search_results.clear()
    listbox.delete(0, END)
    for l in res:
        p = l.get("href")
        if p.startswith('/watch'):
            search_results.append(youtube_string + p)

    video_titles = display_information(search_results)
    show_titles(video_titles)


def latesthindi(event):
    global search_results
    youtube_string = "http://www.youtube.com"
    r = requests.get("https://www.youtube.com/watch?v=SAcpESN_Fk4&list=RDQMrdSrjvg9Z0s")
    page = r.text
    soup = bs(page, 'html.parser')
    res = soup.find_all('a', {'class': "content-link"})
    search_results.clear()
    listbox.delete(0, END)
    for l in res:
        p = l.get("href")
        if p.startswith('/watch'):
            search_results.append(youtube_string + p)

    video_titles = display_information(search_results)
    show_titles(video_titles)


if __name__ == "__main__":
    from  tkinter.messagebox import showinfo
    from tkinter import *
    from tkinter.filedialog import askdirectory
    root = Tk()
    root.minsize(700,700)
    v = StringVar()
    def command(text):
        query_and_download(text)
    SearchBox(root, command=command, placeholder="Type and press enter", entry_highlightthickness=0).pack(pady=6, padx=3)
    label = Label(root, text="Select Quality")
    label.pack()

    Filterit = filterit(root)
    
    listbox = Listbox(root, width=90, height=600)
    listbox.pack(side="right", padx=5)
    
    Downloadbutton = Button(root, text='Download',height=1, width=10)
    Downloadbutton.pack()
    Downloadbutton.bind("<Button-1>", Downloadit)
    Downloadbutton1 = Button(root, text='Similar songs', height=1, width=10)
    Downloadbutton1.pack()
    Downloadbutton1.bind("<Button-1>",similarsong)
    Downloadbutton2 = Button(root, text='Latest Hindi', height=1, width=10)
    Downloadbutton2.pack()
    Downloadbutton2.bind("<Button-1>", latesthindi)
    # Downloadbutton = Button(root, text='Latest English',height=1, width=10)
    # Downloadbutton.pack()
    # Downloadbutton.bind("<Button-1>", latestenglish)
    
    root.mainloop()




