import ffmpeg
#Testing 
#t_0 = 1:56:50
#t_f = 1:57:10
eclipse_mp4 = "EclipseStreamAnalysis/2024 April 8, 4k Live Stream of the Solar Eclipse from the UCA Observatory [lrWkmZvI3JY].mp4"
start_time = "01:56:50"
end_time = "01:57:10"
crop_dimensions = '1300:1300:1300:500' #sets values for cropping, from left to right: Width of cropped video, height of cropped video, top left x coordinate of cropped video, top left y coordinate for cropped video
(
    ffmpeg.input(eclipse_mp4, ss=start_time, to=end_time)#the video we want to extract data from
    .filter('crop', *crop_dimensions.split(":"))#crops the video
    .filter('fps', fps=1, round='up')
    .output('EclipseStreamAnalysis/capturedFrames/frame%d.png')# extracts frames and saves them as pngs
    .run()
)