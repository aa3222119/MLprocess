from buildings.comm_across import *
import random
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def gen_dev_v2(f_name, time_str='000000', format_='.mp4', dev_secs=60, f_dir=None, format_o='.mp4'):
    s1_ = 0
    h_, m_, s_ = 0, 0, 0
    if len(time_str) == 6 and '.' not in time_str:
        h_, m_, s_ = int(time_str[:2]), int(time_str[2:4]), int(time_str[4:6])
    # todo about s1_

    if f_dir and os.sep not in f_name:
        f_name = f'{f_dir}{os.sep}{f_name}'
    f_name_li = f_name.split(os.sep)
    f1_name = f_name_li[-1]
    if '.' in f1_name[-5:]:
        *file_name, format_ = f1_name.split('.')
        # 文件名还有.的简单处理
        if type(file_name) is list and len(file_name):
            file_name = file_name[-1]
    else:
        file_name = f1_name
        f1_name = f1_name + format_
        # todo format_ 仍然不给信息时尝试智能判断？
    if f_dir is None and os.sep in f_name:
        f_dir = os.sep.join(f_name_li[:-1])
    print(f'{f_name_li=} {f1_name=} {file_name=}')

    start_time = h_ * 3600 + m_ * 60 + s_ * 1 + s1_
    # video_path = "135950408.mp4"
    # start_time = 3  # 起始时间（以秒为单位）
    # end_time = 8  # 结束时间（以秒为单位）
    # target_path = "135950408_05.mp4"
    # ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=target_path)
    if format_o is None:
        format_o = format_
    file_name_o = file_name + '_cu_' + time.strftime('%Y%m%d_%H%M%S') + format_o
    vc = VideoFileClip(f'{f_dir}{os.sep}{f1_name}').subclip(start_time, start_time + dev_secs)  # 加载视频, 并截取前5秒
    # print(video.size); //视频长宽
    return vc.write_videofile(f'{f_dir}{os.sep}{file_name_o}')


def devide_v(ss, t, file, postfix='.wmv', au_channel=0):
    # cmd = 'ffmpeg -ss %s -t %s -accurate_seek -i "%s" -codec copy "%s"'
    input_f = file + postfix
    container = '-codec copy'
    if postfix == '.rmvb':
        postfix = '.mp4'
        container = ''
    au_state = f'-map 0:a:{au_channel}'  # 音轨参数，默认第一个也可以不写
    vi_state = '-map 0:v'
    output_f = file + '_cut_' + time.strftime('%Y%m%d_%H%M%S') + postfix
    cmd = f'ffmpeg -ss {ss} -t {t} -accurate_seek -i "{input_f}" {vi_state} {au_state} {container} "{output_f}"'
    print(os.popen(cmd).read())
    # os.popen(output_f).read()
    return output_f


def gen_dev_v(f_name, time_str='000010', format_='.mp4', dev_secs=60, f_dir="C:\\迅雷下载\\16278482\\cut2"):
    os.chdir(f_dir)
    return devide_v('%s:%s:%s.01' % (time_str[:2], time_str[2:4], time_str[4:]), dev_secs, f_name, format_)


def write_sth_in_file(content, file_name, mode='w'):
    """
    :param content: 写入的内容
    :param file_name: 文件名
    :param mode: r+/a/w
    :return:
    """
    with open(file_name, mode) as f_handel:
        f_handel.write(content)


def mv_concat2(process_dir, mv_nums=5, postfix='.mp4'):
    """

    :param process_dir:
    :param mv_nums:
    :param postfix:
    :return:
    """
    mv_li = findall_in_dir(postfix, path=process_dir, include_dir=True)
    random.shuffle(mv_li)
    content_ = '\n'.join([f"file '{x}'" for x in mv_li[:mv_nums]])
    input_txt_name = f'{process_dir}\\tmp.txt'
    write_sth_in_file(content_, input_txt_name)
    # concat_mv_ss = '|'.join(mv_li[:mv_nums])
    out_ = 'C:\\迅雷下载\\16278482\\cut2\\join_' + time.strftime('%Y%m%d_%H%M%S') + postfix
    cmd_ss = f"ffmpeg -f concat -safe 0 -i {input_txt_name} -c copy {out_} "
    return try_cmd(cmd_ss)


def mv_concat3(process_dir, mv_nums=5, postfix='.mp4', ts_dir=''):
    """

    :param process_dir:
    :param mv_nums:
    :param postfix:
    :param ts_dir:
    :return:
    """
    mv_li = findall_in_dir(postfix, path=process_dir, include_dir=True)
    random.shuffle(mv_li)
    cmd_to_ts_ = 'ffmpeg -i "%s" -c copy -bsf:v h264_mp4toannexb -f mpegts %s -y'
    ts_dir = ts_dir if ts_dir else f'{process_dir}\\ts_video\\'
    iter_mkdir(ts_dir)
    for i in range(mv_nums):
        print(i, )
        try_cmd(cmd_to_ts_ % (mv_li[i], f'{ts_dir}f{i}.ts'))
    concat_vi_ss = '|'.join([f'{ts_dir}f{i}.ts' for i in range(mv_nums)])
    out_ = f'{ts_dir}join_' + time.strftime('%Y%m%d_%H%M%S') + postfix
    # cmd_ss = f'ffmpeg -i "concat:{concat_vi_ss}"  -c copy -bsf:a aac_adtstoasc -movflags +faststart {out_}'
    # cmd_ss = f'ffmpeg -i "concat:{concat_vi_ss}"  -c copy -bsf:a aac_adtstoasc {out_}'
    cmd_ss = f'ffmpeg -i "concat:{concat_vi_ss}"  -c copy {out_}'
    return try_cmd(cmd_ss)
