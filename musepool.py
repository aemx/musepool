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

def check_key(key):
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
sf = df.reindex(np.random.permutation(df.index)).copy()
tf = sf['flag'] != 'P'
df_muse = sf[tf].copy()

print('CSV successfully loaded.')
print(count(df_muse) + '/' + count(df) + ' songs available for use.')

# -----------------------------------------------------------------------------
# Initialize important values, then begin the playlist's creation by adding the
# first track that appears in df_muse.
# -----------------------------------------------------------------------------

muse_out = []
cur_artist = df_muse['artist'].iloc[0]
all_artist = cur_artist.split('|')
cur_key = df_muse['key'].iloc[0]
cur_idx = df_muse.iloc[0].name
runtime = 0

add(cur_artist, df_muse['title'].iloc[0], muse_out)
df_muse.drop([cur_idx], inplace=True)

print('Creating playlist...')

# -----------------------------------------------------------------------------
# Filter keys, lengths, and artists accordingly, finishing the playlist.
# -----------------------------------------------------------------------------

failsafe = 100
r_min = 21 * 60
r_max = 22 * 60

while runtime < r_min:
    tf_key = df_muse['key'].isin(check_key(cur_key))
    df_key = df_muse[tf_key].copy()

    for idx, song in df_key.iterrows():
        if runtime + get_sec(song['time']) < r_max:
            cur_artist = song['artist']
            all_artist.extend(song['artist'].split('|'))
            cur_key = song['key']
            cur_idx = song.name
            runtime += get_sec(song['time'])
            add(cur_artist, song['title'], muse_out)
            df_muse.drop([cur_idx], inplace=True)
            break
        elif failsafe == 0:
            runtime += r_min
            break
        else:
            failsafe -= 1
            continue

if failsafe == 0:
    print(inv_sec(runtime - r_min), muse_out)
else:
    print(inv_sec(runtime), muse_out)