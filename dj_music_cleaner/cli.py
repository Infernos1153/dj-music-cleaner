#!/usr/bin/env python3
import os
import re
import time
import glob
import subprocess
import argparse
from mutagen.mp3 import MP3

def remove_bracket_numbers(filename):
    """Remove numbers in square brackets from the filename."""
    base, ext = os.path.splitext(filename)
    base = re.sub(r'^\[.*?\]\s*', '', base)
    base = re.sub(r'\s*\[.*?\]$', '', base)
    return base + ext

def get_newly_downloaded_mp3s(since_time):
    """Return a list of mp3 files modified since a given time."""
    return [file for file in glob.glob("*.mp3") if os.path.getmtime(file) >= since_time]

def get_duration(file):
    """Return the duration (in seconds) of the mp3 file."""
    try:
        audio = MP3(file)
        return audio.info.length
    except Exception as e:
        print(f"Error reading duration for {file}: {e}")
        return None

def process_file(file, song_db, clean_names):
    """Process the file: clean filename, check for duplicates, and log the song."""
    formatted_name = remove_bracket_numbers(file)
    if clean_names:
        print(f"Processing file: {file}")
        print(f"Proposed new filename: {formatted_name}")
        new_file = formatted_name
        if new_file != file:
            try:
                os.rename(file, new_file)
                print(f"Renamed '{file}' to '{new_file}'")
                file = new_file
            except Exception as e:
                print(f"Error renaming file '{file}': {e}")
    else:
        print(f"Skipping filename cleanup for: {file}")
    
    # Check for duplicates.
    song_title = os.path.splitext(file)[0]
    check_title = song_title[10:] if song_title.startswith("DUPLICATE ") else song_title

    if check_title in song_db:
        if not file.startswith("DUPLICATE "):
            dup_file = "DUPLICATE " + file
            try:
                os.rename(file, dup_file)
                print(f"Duplicate detected. Renamed '{file}' to '{dup_file}'")
                file = dup_file
            except Exception as e:
                print(f"Error renaming duplicate file '{file}': {e}")
    else:
        song_db.add(check_title)
        with open("song_list.txt", "a") as db_file:
            db_file.write(check_title + "\n")
        print(f"Recorded '{check_title}' in song_list.txt")
    return file

def download_playlist(playlist_link):
    """Save the playlist link and execute the download command."""
    with open("links.txt", "a") as f:
        f.write(playlist_link + "\n")
    print("Playlist link saved to links.txt.")
    print("Downloading playlist. Please wait...")

    if "spotify.com" in playlist_link:
        command = f'spotdl "{playlist_link}"'
    elif "soundcloud.com" in playlist_link:
        command = f'yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 --yes-playlist "{playlist_link}"'
    else:
        print("Unrecognized link. Only Spotify and SoundCloud are supported.")
        return False
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print("Download failed. Please check your link and try again.")
        return False
    print("Download complete!")
    return True

def main():
    parser = argparse.ArgumentParser(description="DJ Music Cleaner & Downloader App")
    parser.add_argument('--playlist', '-p', type=str, help="Playlist link to download songs")
    parser.add_argument('--clean', '-c', action='store_true', help="Automatically clean filenames (remove bracketed numbers)")
    parser.add_argument('--delete-truncated', '-d', action='store_true', help="Automatically delete truncated files (<30 seconds)")
    args = parser.parse_args()

    print("==============================================")
    print("     DJ Music Cleaner & Downloader App")
    print("==============================================\n")

    new_files = []
    start_time = time.time()

    playlist_link = args.playlist
    if not playlist_link:
        playlist_link = input("Please paste the playlist link (or press Enter to skip download): ").strip()

    if playlist_link:
        if not download_playlist(playlist_link):
            return
        new_files = get_newly_downloaded_mp3s(start_time)
        if not new_files:
            print("No new mp3 files found after download.")
    else:
        print("No playlist link provided. Skipping download.")

    print(f"\nFound {len(new_files)} mp3 file(s) to process.")

    song_db = set()
    if os.path.exists("song_list.txt"):
        with open("song_list.txt", "r") as db_file:
            for line in db_file:
                title = line.strip()
                if title:
                    song_db.add(title)

    clean_names = args.clean
    if not args.clean:
        choice = input("\nWould you like to remove numbers enclosed in [] from the mp3 filenames? (y/n): ").strip().lower()
        clean_names = (choice == 'y')

    processed_files = []
    for file in new_files:
        processed_file = process_file(file, song_db, clean_names)
        processed_files.append(processed_file)

    print("\nChecking for truncated files (duration < 30 seconds)...")
    for file in processed_files:
        duration = get_duration(file)
        if duration is not None:
            print(f"File: {file} | Duration: {duration:.2f} seconds")
            if duration < 30:
                if args.delete_truncated:
                    delete_choice = 'y'
                else:
                    delete_choice = input("This file appears truncated. Delete it? (y/n): ").strip().lower()
                if delete_choice == 'y':
                    try:
                        os.remove(file)
                        print(f"Deleted {file}.")
                    except Exception as e:
                        print(f"Error deleting {file}: {e}")
                else:
                    print("File retained.")

    print("\nAll files processed. Enjoy your music!")

if __name__ == "__main__":
    main()