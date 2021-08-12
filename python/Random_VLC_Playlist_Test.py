from Series import Playlist, Series, SeriesPlaylistRandomizer, SERIES_LOCATION_DICT
import subprocess, os, platform
from typing import List
import xml.etree.ElementTree as xml

def fill_playlist(p1:Playlist, xml_list:List[str]) -> Playlist:
    for x in xml_list:
        p1.add_track(x)
    return p1

def write_playlist_to_file(p1:Playlist, filename:str) -> None:
    playlist_xml = p1.get_playlist()
    with open(f'{filename}.xspf','w') as mf:
	    mf.write(xml.tostring(playlist_xml).decode('utf-8'))

def run_file(filename:str):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(filepath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', filepath))

        
series_1 = Series() # Cowboy Bebop
series_1.collect_files(SERIES_LOCATION_DICT['Cowboy Bebop'])
series_2 = Series() # Samurai Champloo
series_2.collect_files(SERIES_LOCATION_DICT['Samurai Champloo'])
series_3 = Series() # Samurai Champloo
series_3.collect_files(SERIES_LOCATION_DICT['Gundam Wing'])

print("Series Collected")

randomizer = SeriesPlaylistRandomizer()
randomizer.add_series('Cowboy Bebop',series_1)
randomizer.add_series('Samurai Champloo',series_2)
randomizer.add_series('Gundam Wing',series_3)
randomized_xml_list = randomizer.get_randomized_playlist()

print("Series Randomized")

playlist1 = Playlist()
playlist1 = fill_playlist(playlist1, randomized_xml_list)

print('Playlist filled')

write_playlist_to_file(playlist1, 'test_playlist')

filepath = 'test_playlist.xspf'
print('Playlist Written')


