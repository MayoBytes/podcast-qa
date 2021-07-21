# podcast-qa

This is a tool I wrote to self-host a QA version of my podcast that I can share with friends and cohosts for feedback before content goes live on my main feed.

<br>

## Dependencies

This requires **python3** to run, and **tmux** if you use the start/stop scripts.

### Ubuntu/Debain via apt

`sudo apt install python3 tmux`

### MacOS via [Homebrew](https://brew.sh/)

`brew install python tmux`

<br>

## Usage

This server simply hosts an RSS feed (one you will have to create) named "feed.xml", an image/thumbnail named image.png, and mp3 episodes. It looks for the feed and image files in the same directory it is running in and the mp3 episodes should be in a sub-directory called "episodes".

Check out [Apple's guide to RSS](https://help.apple.com/itc/podcasts_connect/#/itcb54353390) for more information on how to write your own feed.
