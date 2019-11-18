from buildings.comm_across import *
import random


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


def mv_concat3(process_dir, mv_nums=5, postfix='.mp4'):
    """

    :param process_dir:
    :param mv_nums:
    :param postfix:
    :return:
    """
    mv_li = findall_in_dir(postfix, path=process_dir, include_dir=True)
    random.shuffle(mv_li)
    cmd_to_ts_ = 'ffmpeg -i %s -c copy -bsf:v h264_mp4toannexb -f mpegts %s -y'
    ts_dir = f'{process_dir}\\ts_video\\'
    iter_mkdir(ts_dir)
    for i in range(mv_nums):
        try_cmd(cmd_to_ts_ % (mv_li[i], f'{process_dir}\\ts_video\\f{i}.ts'))
    concat_vi_ss = '|'.join([f'{ts_dir}f{i}.ts' for i in range(mv_nums)])
    out_ = f'{ts_dir}join_' + time.strftime('%Y%m%d_%H%M%S') + postfix
    cmd_ss = f'ffmpeg -i "concat:{concat_vi_ss}"  -c copy {out_}'
    return try_cmd(cmd_ss)
