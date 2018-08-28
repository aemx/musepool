import numpy as np
import pandas as pd
import re

# -----------------------------------------------------------------------------
# Count the number of entries in a DataFrame, then output as a string.
# -----------------------------------------------------------------------------

def count(dataframe):
    return str(len(dataframe.index))

# -----------------------------------------------------------------------------
# Function to add a track to an output list.
# -----------------------------------------------------------------------------

def add(artist, title, output): #, dataframe):
    artist_list = artist.split('|')
    artist_return = []

    for artist in artist_list:
        if artist not in title:
            artist_return.append(artist)
    
    if len(artist_return) > 2:
        tmpstr = ''
        for idx, artist in enumerate(artist_return):
            if idx == len(artist_return) - 2:
                break
            tmpstr += artist_return[idx] + ', '
        returnstr = tmpstr + artist_return[-2] + ' & ' + artist_return[-1] + ' - ' + title
    elif len(artist_return) == 2:
        returnstr = artist_return[0] + ' & ' + artist_return[1] + ' - ' + title
    else:
        returnstr = artist_return[0] + ' - ' + title
    
    output.extend([returnstr])

# -----------------------------------------------------------------------------
# Auxiliary mode toggler for keymatcher (below).
# -----------------------------------------------------------------------------

def toggle(v):
    if v == 'A': return 'B'
    elif v == 'B': return 'A'

# -----------------------------------------------------------------------------
# Keymatching function.
# -----------------------------------------------------------------------------

def keymatch(key):
    num, mode = re.findall('\d+|\D+', key)
    inum = int(num)

    key_ccw = str(((inum - 2) % 12) + 1) + mode
    key_cw = str((inum % 12) + 1) + mode
    key_swap = num + toggle(mode)

    return [key, key_ccw, key_cw, key_swap]

# -----------------------------------------------------------------------------
# Converts a time in MM:SS format to seconds only.
# -----------------------------------------------------------------------------

def get_sec(time):
    mm, ss = time.split(':')
    return (int(mm) * 60) + int(ss)

# -----------------------------------------------------------------------------
# Compare two lists, then return False if one value matches between both lists.
# -----------------------------------------------------------------------------

def compare(a, b):
    return not bool(set(a) & set(b))

# -----------------------------------------------------------------------------
# Converts a time in seconds to MM:SS format (string).
# -----------------------------------------------------------------------------

def inv_sec(time):
    mm = str(int(time / 60))
    ss = str('%02d' % (time % 60))
    return (mm + ':' + ss)

# -----------------------------------------------------------------------------
# Load and shuffle a CSV, then create two DataFrames, one with every song
# listed in the CSV, and one with all songs that have not been flagged [P].
# -----------------------------------------------------------------------------

df = pd.read_csv('data.csv')
tf = df['flag'] != 'P'
tf_muse = df[tf].copy()

print('CSV successfully loaded.')
print(count(tf_muse) + '/' + count(df) + ' songs available for use.')

# -----------------------------------------------------------------------------
# Initialize important values, then begin the playlist's creation by adding the
# first track that appears in df_muse.
# -----------------------------------------------------------------------------

muse_out = []
runtime = 0
r_min = 21 * 60
r_max = 22 * 60

while (runtime < r_min or
runtime > r_max):

    sf = df.reindex(np.random.permutation(df.index)).copy()
    tf = sf['flag'] != 'P'
    df_muse = sf[tf].copy()
    muse_out = []

    cur_artist = df_muse['artist'].iloc[0]
    all_artist = cur_artist.split('|')
    cur_key = df_muse['key'].iloc[0]
    cur_idx = df_muse.iloc[0].name
    runtime = get_sec(df_muse['time'].iloc[0])

    add(cur_artist, df_muse['title'].iloc[0], muse_out)
    df_muse.drop([cur_idx], inplace=True)

# -----------------------------------------------------------------------------
# Filter keys, lengths, and artists accordingly, finishing the playlist.
# -----------------------------------------------------------------------------

    failsafe = int(count(df))

    while (runtime < r_min and
    failsafe > 0):
        tf_key = df_muse['key'].isin(keymatch(cur_key))
        df_key = df_muse[tf_key].copy()

        for idx, song in df_key.iterrows():
            if (runtime + get_sec(song['time']) < r_max and
            compare(song['artist'].split('|'), all_artist)):
                cur_artist = song['artist']
                all_artist.extend(cur_artist.split('|'))
                cur_key = song['key']
                cur_idx = song.name
                runtime += get_sec(song['time'])
                add(cur_artist, song['title'], muse_out)
                df_muse.drop([cur_idx], inplace=True)
                break
            else:
                failsafe -= 1
                continue

# -----------------------------------------------------------------------------
# Print the playlist.
# -----------------------------------------------------------------------------

print('\n' + inv_sec(runtime))
for song in muse_out:
    print(song)