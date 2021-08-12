import os
import random
from create_playlist import Playlist
from typing import List
import xml.etree.ElementTree as xml

# Main caveat is that this program assumes Series are entirely contained in their directories and it's subdirectories and that they are in order

SERIES_LOCATION_DICT = {
    'Cowboy Bebop':r'C:\Users\Cameron Phillips\Downloads\Movies\[CBM] Cowboy Bebop 1-26 Complete (Dual Audio) [BDRip-720p-8bit]',
    'Samurai Champloo':r'C:\Users\Cameron Phillips\Downloads\Movies\[a-S] Samurai Champloo (01-26) (1080p)',
    "Gundam Wing":r'C:\Users\Cameron Phillips\Downloads\Movies\GUNDAM Series (Pack 3)\A-MS Gundam Wing (1995-96)'
}

class Movies:
    def __init__(self):
        self.file = ''
        
    def collect_files(self, direc):
         pass


class Series:
    """Manages the video files for a group of related sequential media files"""
    def __init__(self):
        self.files = []
        
    def remove_nonvideo_files(self, file_list):
    #Removes files whose extension is not mentioned in ext_list from list of files.
        ext_list = ['.mp4', '.mkv', '.avi', '.flv', '.mov', '.wmv', '.vob', '.mpg','.3gp', '.m4v']
        for index, file_name in enumerate(file_list[:]):
            if file_name.endswith(tuple(ext_list)) or file_name.endswith(tuple(ext.upper() for ext in ext_list)):
                pass
            else:
                file_list.remove(file_name)
        return file_list
    
    def get_edited_paths(self):
    #Add path and prefix to files as required in vlc playlist file. 
        video_files = self.files
        for index in range(len(video_files)):
            video_files[index] =( 
            'file:///' + os.path.join(video_files[index])).replace('\\','/')
        return video_files

    def get_edited_path(self, file_path):
    #Add path and prefix to files as required in vlc playlist file. 
        file_path =('file:///' + os.path.join(file_path)).replace('\\','/')
        return file_path
    
    def collect_files(self, direc, check_subdirs = True):
        cur_dir = os.getcwd()
        os.chdir(direc)
        if check_subdirs == True:
            pathlist = [os.getcwd()]
            for root, dirs, files in os.walk(os.getcwd()):
                for name in dirs:
                    subdir_path = os.path.join(root, name)
                    if subdir_path.find('\.') != -1:
                        pass
                    else:
                        pathlist.append(subdir_path)
            for path in pathlist:
                all_files = os.listdir(path)
                for f in self.remove_nonvideo_files(all_files):
                    location = path + '\\' + f
                    self.files.append(location)
        else:
            all_files = os.listdir(direc)
            for f in self.remove_nonvideo_files(all_files):
                location = os.getcwd() + '\\' + f
                self.files.append(location)
        os.chdir(cur_dir)

class SeriesPlaylistRandomizer:
    """Class to randomly choose and produce an ordered Playlist
    from 1+ series in a random order, but sequential within each series"""
    def __init__(self):
        self.seriesPlaceDict = dict()
        self.seriesDict = dict()
        self.seriesLengthDict = dict()
    
    def add_series(self, seriesName:str, series:Series):
        self.seriesDict[seriesName] = series
        self.seriesPlaceDict[seriesName] = 0
        self.seriesLengthDict[seriesName] = len(series.files)
    
    def _increment_series_place(self, seriesName):
        self.seriesPlaceDict[seriesName] += 1
    
    def _get_next_track(self, seriesName):
        # Get filepath for next track in series according to the current series place
        return self.seriesDict[seriesName].files[self.seriesPlaceDict[seriesName]]
    
    def get_randomized_playlist(self):
        # Randomly choose from each series until seriesPlace = seriesLength
        playlist_videos_xml = []
        finished_series = []
        while finished_series != list(self.seriesDict.keys()):
            series = random.choice(list(self.seriesDict.keys()))
            # series = random.choice(list(set(self.seriesDict.keys()) - set(finished_series)))
            if series in finished_series:
                continue
            else:
                next_track = self._get_next_track(series)
                edited_path = self.seriesDict[series].get_edited_path(next_track)
                playlist_videos_xml.append(edited_path)
                self._increment_series_place(series)
                if self.seriesPlaceDict[series] == self.seriesLengthDict[series]:
                    finished_series.append(series)
        return playlist_videos_xml

