# dlp-exe branch
this branch exists because some av's very much dont like it when an unknown exe makes connections to the internet-<br>
-and switching over to using the yt-dlp python module made it so some things like windows defender treat it like a threat.<br>
so this branch will revert back to packaging the ytdlp.exe file into the project and using that to download videos.

# youtube-dlp-gui
This is my own take on a gui for yt-dlp using dear pygui<br>
This includes both a version of yt-dlp and ffmpeg so neither have to be downloaded<br>

note if your running/compiling from source you will need to unzip ffmpeg.7z in the exe folder since its too large to to put on github uncompressed

# Options
- Rate limit
- custom Output format
- custom download location
- cookies.txt support
- Embed thumbnail
- can pick what video to start on in a playlist and what video to end on
- Video only audio only and Full video modes
