from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects
from buildings.comm_across import *

# 加载用来指定区域的图像
im = ImageClip("Y:\\素材图片\\frame1.png")

# 加载这些区域返回一个ImageClip列表
regions = findObjects(im)
video_dir = 'Y:\\番剧相关'

charade = VideoFileClip(f"{video_dir}{os.sep}clips{os.sep}0006.mp4")
tfreeze = cvsecs(19.21)  # Time of the freeze, 19'21
clip_before = charade.subclip(tfreeze - 7, tfreeze)
clip_after = charade.subclip(tfreeze, tfreeze + 7)
# 被定格的一帧画面
im_freeze = charade.to_ImageClip(tfreeze)
# painting = (charade.fx(vfx.painting, saturation=1.6, black=0.006)
#             .to_ImageClip(tfreeze))
# # 签名的TextClip
# txt = TextClip('Antony', fontsize=35)
#
# painting_txt = (CompositeVideoClip([painting, txt.set_pos((10, 180))])
#                 .add_mask()
#                 .set_duration(3)
#                 .crossfadein(0.5)
#                 .crossfadeout(0.5))

# # FADEIN/FADEOUT EFFECT ON THE PAINTED IMAGE
#
# painting_fading = CompositeVideoClip([im_freeze, painting_txt])

final_clip = concatenate_videoclips([clip_before,
                                     # painting_fading.set_duration(3),
                                     clip_after])

final_clip.write_videofile(f"{video_dir}{os.sep}clips{os.sep}00000-.mp4", fps=charade.fps, codec="mpeg4", audio_bitrate="3000k")


clips = [VideoFileClip(n, audio=False) for n in [f"{video_dir}{os.sep}clips{os.sep}000{x}.mp4" for x in range(1, 8)]]
# 把每一个clip都放置在对应的图片中的区域
comp_clips = [c.resize(r.size).set_mask(r.mask).set_pos(r.screenpos) for c, r in zip(clips, regions)]
cc = CompositeVideoClip(comp_clips, im.size)
cc.write_videofile(f"{video_dir}{os.sep}clips{os.sep}00000-.mp4")



dir_ = 'Z:\\process_area\\5.4\\ft_done1\\'
file_name_li = findall_in_dir('mp4', dir_)
try_cmd('shutdown.exe -s -t 3344')

for x in file_name_li:
    name, _ = x.split('.mp4')
    print(name, _)
    clip = VideoFileClip(x)
    frame = clip.get_frame(2)
    if frame.shape[0] > frame.shape[1]:
        clip_ = clip.rotate(90)
        # clip_.ipython_display()
        clip_.write_videofile(name + '_r.mp4')


video_data = VideoFileClip(f'{video_dir}{os.sep}你的名字HD.mp4')
video_new = video_data.subclip(150, 200)
video_new.write_videofile(f'{video_dir}{os.sep}clips{os.sep}0001.mp4')
video_data.reader.close()

video_data = VideoFileClip(f'{video_dir}{os.sep}[HoneyGod] 言叶之庭 言の葉の庭 The Garden of Words[x264_10bit][粤日双语][BDrip_1080p]_cut_20200411_150949.mkv')
video_new = video_data.subclip(29, 79)
video_new.write_videofile(f'{video_dir}{os.sep}clips{os.sep}0002.mp4')
video_data.reader.close()

name_ = "[Moozzi2] Re Zero Kara Hajimeru Isekai Seikatsu - OVA [ Memory Snow ] (BD 1920x1080 x.264 FLACx2).mkv"
video_data = VideoFileClip(f'{video_dir}{os.sep}{name_}')
video_new = video_data.subclip((54, 20), (55, 10))
video_new.write_videofile(f'{video_dir}{os.sep}clips{os.sep}0003.mp4')
video_data.reader.close()

video_data = VideoFileClip(f'{video_dir}{os.sep}{name_}')
video_new = video_data.subclip((42, 40), (43, 30))
video_new.write_videofile(f'{video_dir}{os.sep}clips{os.sep}0004.mp4')
video_data.reader.close()

name_ = 'MV - Grand Escape.mkv'
video_data = VideoFileClip(f'{video_dir}{os.sep}{name_}')
video_new = video_data.subclip(123, 173)
video_new.write_videofile(f'{video_dir}{os.sep}clips{os.sep}0007.mp4')
video_data.reader.close()


