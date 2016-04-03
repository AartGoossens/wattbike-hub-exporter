# Wattbike Hub session exporter
Script to download sessions from hub.wattbike.com and merge multiple sessions into a single .tcx file.

## Introduction
This repository contains scripts to download Wattbike sessions from the [Wattbike Hub](http://hub.wattbike.com) and convert them to .tcx to be able to import them into e.g. [GoldenCheetah](http://www.goldencheetah.org) or [Strava](https://www.strava.com).
I am aware of the fact that the Wattbike Hub offers Strava synchronization and Strava offers [export functionality](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export) but there are a few drawbacks of this solution:

1. No retrospective upload of sessions: only sessions that are uploaded **after** you enable Strava synchronization in the Wattbike Hub are uploaded. There is no way to get previous sessions out of the Wattbike Hub.
2. When doing Wattbike group sessions with the Wattbike Power Cycling SE software and recording the session with the app, most of the times you (well, at least I) end up with several sessions which cannot be merged in the Wattbike Hub.

## How does it work?
The Wattbike Hub does not offer a public API. Well... to be more accurate: the API is not documented. There are a few API endpoints that are used by both the website and apps that offer some API functionality. I use one of these endpoints to download the data from a session:
> http://hub.wattbike.com/ranking/getSessionRows?sessionId=[session_id]

Example of one of my sessions: [http://hub.wattbike.com/ranking/getSessionRows?sessionId=ee6639cbe5fd1d7aa8de4d1e4c8a1415](http://hub.wattbike.com/ranking/getSessionRows?sessionId=ee6639cbe5fd1d7aa8de4d1e4c8a1415)

## Features
- Download Wattbike session
- Save Wattbike session as .tcx
- Coming soon: Save Wattbike session as .csv
- Coming soon: Merge several Wattbike sessions and export as one

## Requirements
- Python 3 (Parts of the code might work in Python 2 and I might add Python 2 support in the future)
- Wattbike Hub account set to 'publicly viewable'. Check this in your [Wattbike Hub settings](http://hub.wattbike.com/account/edit)

## Usage
Open a terminal and clone this repository with the following command:
```
git clone https://github.com/AartGoossens/wattbike-hub-exporter.git
```
`cd` into the code directory with:
```
cd wattbike-hub-exporter
```
Start a python terminal with `python3` (or `ipython` if you have it installed) and run the following Python commands line by line:
```python
from src.workout import Workout
workout = Workout(session_ids=['session_id1', 'session_id2'])
workout.export_to_tcx()]
```
The exported `.tcx` file is saved in the current directory.

## Usefull links
- [Wattbike Hub](http://hub.wattbike.com)
- [Strava export functionality](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export)
- [GoldenCheetah](http://www.goldencheetah.org)
- [My Wattbike Hub Profile](http://hub.wattbike.com/aart.goossens)
- [My Strava Profile](https://www.strava.com/athletes/2495424)

## License
The code in this repository is licensed under the [MIT License](http://choosealicense.com/licenses/mit/). GitHub [describes](http://choosealicense.com) this license as follows:
> The MIT License is a permissive license that is short and to the point. It lets people do anything they want with your code as long as they provide attribution back to you and don’t hold you liable.
My summary: Use this code for whatever you want, but give me credit everytime you implement it somewhere.
