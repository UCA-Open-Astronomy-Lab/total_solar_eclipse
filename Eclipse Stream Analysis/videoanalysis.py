import ffmpeg
crop_dimensions = '640:480:0:0' #sets values for cropping, from left to right: Width of cropped video, height of cropped video, top left x coordinate of cropped video, top left y coordinate for cropped video
(
    ffmpeg.input("eclipse.mp4")#the video we want to extract data from
    .filter('crop', *crop_dimensions.split(':'))#crops the video
    .output('frame%d.png', vf = 'fps=1')# extracts frames from the entire video at 1 fps and saves them as pngs
    #.run()
)