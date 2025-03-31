from setuptools import setup, find_packages

setup(
    name='dj-music-cleaner',
    version='0.1.0',
    description='A CLI tool to download and clean up music files from playlists',
    author='Andrew Miley',
    packages=find_packages(),
    install_requires=[
        'mutagen',
        'setuptools'
    ],
    entry_points={
        'console_scripts': [
            'dj-music-cleaner=dj_music_cleaner.cli:main',
        ],
    },
)