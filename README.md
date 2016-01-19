# theatresignage-player-pi
Raspberry Pi Player will display the content on a Raspberry Pi.
Content is managed by the theatresignage-server project.


## Notes
This will use:
* uzbl
 * for image display (and possibly web content).
* hello_video.bin
 * for very efficient video playback, but needs videos in raw h264 so the server would need to convert media.
* omxplayer
 * general video player
* python
 * managing assets and playlist
* supervisord
 * keep main process running
* scrot
 * screenshots for remote monitoring
* hamachi
 * vpn for management
