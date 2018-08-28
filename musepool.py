import datetime
import numpy as np
import os
import pandas as pd
import re
import sys

# Count the number of entries in a DataFrame, then output as a string.
def count(dataframe):
    return str(len(dataframe.index))

# Function to add a track to an output list.
def add(artist, title, output):
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

# Auxiliary mode toggler for keymatcher (below).
def toggle(v):
    if v == 'A': return 'B'
    elif v == 'B': return 'A'

# Keymatching function.
def keymatch(key):
    num, mode = re.findall('\d+|\D+', key)
    inum = int(num)

    key_ccw = str(((inum - 2) % 12) + 1) + mode
    key_cw = str((inum % 12) + 1) + mode
    key_swap = num + toggle(mode)

    return [key, key_ccw, key_cw, key_swap]

# Converts a time in MM:SS format to seconds only.
def get_sec(time):
    mm, ss = time.split(':')
    return (int(mm) * 60) + int(ss)

# Compare two lists, then return False if one value matches between both lists.
def compare(a, b):
    return not bool(set(a) & set(b))

# Create a yes/no prompt from a single string.
def yn(string):
    while True:
        prompt = input(string + ' [Y/n] ')
        if prompt.lower() in ('yes', 'ye', 'y', ''):
            return True
        elif prompt.lower() in ('no', 'n'):
            return False
        else:
            print('\nPlease respond with "yes/y" or "no/n".')
            continue

# Converts a time in seconds to MM:SS format (string).
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

# -----------------------------------------------------------------------------
# Begin an input prompt loop for the user.
# -----------------------------------------------------------------------------

os.system('clear')

print(

    '╔═════════════════════╤═══════════════════╗\n' + \
    '║  musepool 0.1.0-b2  │    ' + count(tf_muse) + '  /  ' + count(df) + '    ║\n' + \
    '╟─────────────────────┴───────────────────╢\n' + \
    '║  Type \'z\' to create a short playlist.   ║\n' + \
    '║  Type \'x\' to create a long playlist.    ║\n' + \
    '║  Type \'c\' to insert a new track.        ║\n' + \
    '║  Press enter to exit the program.       ║\n' + \
    '╚═════════════════════════════════════════╝\n'
)

while True:
    try:
        selector = input('>>> ')
    
    except ValueError:
        print('\nIncorrect operation specified. Please retry.\n')
        continue

    # ---------------------------------------------------------------------
    # Initialize important values, then begin the playlist's creation by
    # adding the first track that appears in df_muse.
    # ---------------------------------------------------------------------

    if selector in ('z', 'x'):
        if selector == 'z':
            r_min = 20 * 60
            r_max = 21 * 60
            part = 'A'
        elif selector == 'x':
            r_min = 27 * 60
            r_max = 28 * 60
            part = 'B'    

        muse_out = []
        runtime = 0

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
            all_idx = [cur_idx]
            runtime = get_sec(df_muse['time'].iloc[0])

            add(cur_artist, df_muse['title'].iloc[0], muse_out)
            df_muse.drop([cur_idx], inplace=True)

            # -----------------------------------------------------------------
            # Filter keys, lengths, and artists accordingly.
            # -----------------------------------------------------------------

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
                        all_idx.extend([cur_idx])
                        runtime += get_sec(song['time'])
                        add(cur_artist, song['title'], muse_out)
                        df_muse.drop([cur_idx], inplace=True)
                        break
                    else:
                        failsafe -= 1

        # ---------------------------------------------------------------------
        # Ask the user if they are okay with saving the generated playlist,
        # then ask for an episode number for the filename.
        # ---------------------------------------------------------------------

        print('\nYour generated playlist (runs for ' + inv_sec(runtime) + '):\n')

        for line in muse_out:
            print(line)

        yn_save = yn('\nIs this okay?')

        if yn_save == False:
            print('\nExiting...\n')
            break
        
        episode = input('\nPlease select an episode number to identify your file: ')

        # ---------------------------------------------------------------------
        # Flag and update the CSV, then save the playlist to an MD file.
        # ---------------------------------------------------------------------

        for idx in all_idx:
            df['flag'].iloc[idx] = 'P'

        df.to_csv('data.csv',index=False)

        day = datetime.date.today()
        year = day.strftime('%y')
        year_day = int(day.strftime('%j'))

        if year_day > 183:
            semester = 'F'
        else:
            semester = 'S'
        
        production_code = semester + year + episode.zfill(2) + part

        with open('output/' + production_code + '.md', 'w') as md_out:
            md_out.write('# **' + production_code + ' (' + inv_sec(runtime) + ')** #\n')
            for line in muse_out:
                md_out.write('- ' + line + '\n')
        md_out.close()

        print('\nPlaylist \"' + production_code + '.md\" successfully compiled!\n')

    # -------------------------------------------------------------------------
    # Prompt the user to insert a track into the CSV, then do so if requested.
    # -------------------------------------------------------------------------

    elif selector is 'c':
        input_artist = input('\nEnter a list of artists featured in this song, separated by a \'|\': ')
        input_title = input('\nEnter the full title of this song: ')
        input_len = input('\nEnter the length of this song in [mm:ss] format: ')
        input_key = input('\nEnter the key of the song in Camelot format: ')

        yn_input = yn('\nIs this okay?')

        if yn_input == False:
            print('\nExiting...\n')
            break

        insertion = pd.DataFrame([[input_artist, input_title, input_len, input_key, 'N']], columns=['artist', 'title', 'time', 'key', 'flag'])
        df = df.append(insertion, ignore_index=True)
        df.sort_values(['artist', 'title'], inplace=True)
        df.to_csv('data.csv',index=False)

        print('\nDatabase successfully updated!\n')

    # -------------------------------------------------------------------------
    # Miscellaneous input responses.
    # -------------------------------------------------------------------------

    elif selector is '':
        print('\nExiting...\n')
        sys.exit()
    else:
        print('\nIncorrect operation specified. Please retry.\n')