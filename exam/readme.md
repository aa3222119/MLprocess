# ffmpeg 笔记
## win10
#### 0 安装
    
#### 1 图片 + 音频 双输入 拼接输出：
    ffmpeg -i ./shengteng2yaren/xihongshishoufu-2018_1_%6d.png -i ../src/shenteng/xihongshishoufu-2018_1.mkv -c:v libx264 -vf "fps=25,format=yuv420p" -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 shengteng2yaren.mp4
    ffmpeg -i ./shengteng2tony/xihongshishoufu-2018_2_%6d.png -i ../src/shenteng/xihongshishoufu-2018_2.mkv -c:v libx264 -vf "fps=25,format=yuv420p" -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 2_shengteng2tony.mp4
    

https://www.zhihu.com/question/300182407

#### 2 截取片段
