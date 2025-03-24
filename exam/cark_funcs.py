from buildings.comm_across import *
import random


def devide_v(ss, t, file, postfix='.wmv', au_channel=0, vi_channel=0):
    # cmd = 'ffmpeg -ss %s -t %s -accurate_seek -i "%s" -codec copy "%s"'
    input_f = file + postfix
    container = '-codec copy'
    if postfix in ['.rmvb', '.mpg', '.avi', '.mkv']:
        container = ''
    if postfix in ['.rmvb', '.mpg', '.avi', '.mkv']:  #
        postfix = '.mp4'
    au_state = f'-map 0:{au_channel} -c:a copy' if au_channel >= 0 else ''  # 音轨参数，默认第一个也可以不写
    vi_state = f'-map 0:{vi_channel} -c:v copy'
    output_f = file + '_cut_' + time.strftime('%Y%m%d_%H%M%S') + postfix
    cmd = f'ffmpeg -ss {ss} -t {t} -accurate_seek -i "{input_f}" {vi_state} {container} {au_state} "{output_f}"'
    print(cmd)
    try_cmd(cmd)
    # print(os.popen(cmd).read())
    # os.popen(output_f).read()
    return output_f


def gen_dev_v(f_name, time_str='000010', format_='.mp4', dev_secs=60, f_dir="C:\\迅雷下载\\16278482\\cut2", au_channel=0,
              vi_channel=0):
    os.chdir(f_dir)
    time_str = time_str[-6:]
    return devide_v('%s:%s:%s' % (time_str[:2], time_str[2:4], time_str[4:]), dev_secs, f_name, format_,
                    au_channel=au_channel, vi_channel=vi_channel)


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


def mv_concat3(process_dir, mv_nums=5, postfix='.mp4', ts_dir='', with_shuffle=False):
    """

    :param process_dir:
    :param mv_nums:
    :param postfix:
    :param ts_dir:
    :param with_shuffle:
    :return:
    """
    mv_li = findall_in_dir(postfix, path=process_dir, include_dir=True)
    if with_shuffle:
        random.shuffle(mv_li)
    cmd_to_ts_ = 'ffmpeg -i "%s" -c copy -bsf:v h264_mp4toannexb -f mpegts %s -y'
    ts_dir = ts_dir if ts_dir else f'{process_dir}\\ts_video\\'
    iter_mkdir(ts_dir)
    for i in range(mv_nums):
        cmd_s = cmd_to_ts_ % (mv_li[i], f'{ts_dir}f{i}.ts')
        print(i, cmd_s)
        try_cmd(cmd_s)
    concat_vi_ss = '|'.join([f'{ts_dir}f{i}.ts' for i in range(mv_nums)])
    out_ = f'{ts_dir}join_' + time.strftime('%Y%m%d_%H%M%S') + '.mp4'
    # cmd_ss = f'ffmpeg -i "concat:{concat_vi_ss}"  -c copy -bsf:a aac_adtstoasc -movflags +faststart {out_}'
    # cmd_ss = f'ffmpeg -i "concat:{concat_vi_ss}"  -c copy -bsf:a aac_adtstoasc {out_}'
    cmd_ss = f'ffmpeg -i "concat:{concat_vi_ss}"  -c copy {out_}'
    return try_cmd(cmd_ss)
