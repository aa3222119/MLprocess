import requests,time,re,random,os
from bs4 import BeautifulSoup


piduan_1 = """我的手机  19:38:08
http://mp.weixin.qq.com/s/30xhMVs8pxc7ywcJJwjfyg
我的手机  19:39:00
http://mp.weixin.qq.com/s/nUxG2mmxSCvKhI1hMPHQjA
我的手机  19:39:37
http://mp.weixin.qq.com/s/AlqqazhnmD0ddInp9hgkLg
我的手机  19:39:56
http://mp.weixin.qq.com/s/C2gVvTmvRmAZxcIf0Kp07g
我的手机  19:40:17
http://mp.weixin.qq.com/s/92uf9f3aL1bnp9fZqY-KSA
我的手机  19:40:43
http://mp.weixin.qq.com/s/O6lIXaTd_z2OmAlGzneMxQ
我的手机  19:41:19
http://mp.weixin.qq.com/s/nZ9FXLtoOh0L9C_LXtuX6w
我的手机  19:42:02
http://mp.weixin.qq.com/s/ScZps4y0G8K9ez4hniOVbw
我的手机  19:42:16
http://mp.weixin.qq.com/s/rAXfJh-o0tSKULBi5gEtNA
我的手机  19:42:59
http://mp.weixin.qq.com/s/l_DbL3P-XofVDOR2XD6VRg
我的手机  19:43:15
http://mp.weixin.qq.com/s/cT5p73_MP-JI_-IMev0oPw
我的手机  19:43:35
http://mp.weixin.qq.com/s/zof8PCKpa9usIiP8yA8Fcg
我的手机  19:43:56
http://mp.weixin.qq.com/s/zMH-ulZOHpK75bh8FPYQcQ
我的手机  19:44:36
http://mp.weixin.qq.com/s/QSsX82kEBAMsKtt34Hg47A
我的手机  19:44:54
http://mp.weixin.qq.com/s/6-S-fhaRu3IBuP1rPeEzlg
我的手机  19:45:12
http://mp.weixin.qq.com/s/j1DLpM-RLlTDVZg7SnWoRw
我的手机  19:45:44
http://mp.weixin.qq.com/s/rG7rr0AjUYthR0bC2-_ggw
我的手机  19:46:19
http://mp.weixin.qq.com/s/GQmUPMoInOOL1rzCvtPmWw
我的手机  19:46:42
http://mp.weixin.qq.com/s/N0WB_0PCtsG-Go8UTb_2MA
我的手机  19:47:13
http://mp.weixin.qq.com/s/eNzA34AGRWkifGvzHSCjCw
我的手机  19:47:42
http://mp.weixin.qq.com/s/hSj-MA01DwMIU_N-1Fd63Q
我的手机  19:48:08
http://mp.weixin.qq.com/s/U9c10OuxBZb6Lr6_stgbOg
我的手机  19:48:29
http://mp.weixin.qq.com/s/1AdVE-PgwtqqMh-UuYqS6g
我的手机  19:50:51
http://mp.weixin.qq.com/s/kOX1uHgmyxqvwuXbKnlVqw
我的手机  19:51:19
http://mp.weixin.qq.com/s/1bSLEZBozv7pwOapy9TWSA
我的手机  19:52:01
http://mp.weixin.qq.com/s/J7s5PPLq3-B4H3PzpuEJ0w
我的手机  19:52:39
http://mp.weixin.qq.com/s/J8IxN7V2mm8oXMUF8Z9BFA
我的手机  19:53:01
http://mp.weixin.qq.com/s/epmJJ58568qc99ETk9GlgA
我的手机  19:53:29
http://mp.weixin.qq.com/s/Ah4kKjiNFTdwBO75ySPhFA
我的手机  19:53:47
http://mp.weixin.qq.com/s/bzbFwUAGU5p4HIZq_zh9AA
"""

piduan_2 = """我的手机  15:07:30
https://mp.weixin.qq.com/s/92uf9f3aL1bnp9fZqY-KSA
我的手机  15:08:07
https://mp.weixin.qq.com/s/rAXfJh-o0tSKULBi5gEtNA
我的手机  15:08:38
https://mp.weixin.qq.com/s/l_DbL3P-XofVDOR2XD6VRg
我的手机  15:09:06
https://mp.weixin.qq.com/s/zMH-ulZOHpK75bh8FPYQcQ
我的手机  15:09:34
https://mp.weixin.qq.com/s/6-S-fhaRu3IBuP1rPeEzlg
我的手机  15:09:56
https://mp.weixin.qq.com/s/j1DLpM-RLlTDVZg7SnWoRw
我的手机  15:11:14
https://mp.weixin.qq.com/s/rG7rr0AjUYthR0bC2-_ggw
我的手机  15:11:39
https://mp.weixin.qq.com/s/N0WB_0PCtsG-Go8UTb_2MA
我的手机  15:11:58
https://mp.weixin.qq.com/s/eNzA34AGRWkifGvzHSCjCw
我的手机  15:12:12
https://mp.weixin.qq.com/s/hSj-MA01DwMIU_N-1Fd63Q
我的手机  15:14:37
https://mp.weixin.qq.com/s/1AdVE-PgwtqqMh-UuYqS6g
我的手机  15:15:02
https://mp.weixin.qq.com/s/YCOrZPkpV74MjFUjn6tc4A
我的手机  15:15:26
https://mp.weixin.qq.com/s/J7s5PPLq3-B4H3PzpuEJ0w
"""

url_list = re.findall('(https{,1}://mp.weixin.qq.com/s/[\S]{22})\n',piduan_2)
for url in url_list:
    res = requests.get(url)
    body_soup = BeautifulSoup(res.text, "html5lib")
    title_ = body_soup.find_all('h2', class_='rich_media_title')[0].get_text().strip()
    try:
        os.mkdir('./imgs_/' + title_)
    except Exception as err:
        print(err)
    img_list = body_soup.find_all('img')
    i = 0
    for img in img_list:
        imgurl = img.get('data-src')
        if imgurl:
            i += 1
            img_res = requests.get(imgurl)
            with open('./imgs_/' + title_ + '/pa_' + str(i) + '.png', 'wb') as f:
                f.write(img_res.content)

shijianxingzhuang_jiemudan = """
https://mp.weixin.qq.com/mp/homepage?__biz=MzI4MTI4MDQwNg==&hid=3&sn=9a70bf3503912a6bbc0f63e09602308d&scene=18
&devicetype=android-25&version=26060339&lang=zh_CN&nettype=WIFI&ascene=7&session_us=gh_f4320efa44e2&wx_header=1&begin=0&count=50"""
shijianxingzhuang_html = """<div class="article_list js_plugin" id="namespace_0" data-pid="3">
	
	<a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=100000033&amp;idx=1&amp;sn=ba5b152e199f82276f3acebc1ca95ed0&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz/wlqLP7LicAz4MHxicpMib8hdCktPUicp5yATaxjAWVWcsUicMprpicOwicR8nFo4vGgUYvDc0wtOo8X84dONxEdEnIx1g/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》01 - 自我吹嘘的前言</h2>
			<p class="desc">《时间的形状》作者汪洁自己给大家倾情播讲本书，不仅仅是念书，中间还穿插了很多创作感想以及延伸知识。</p>
		</div>
	</a>
	
	<a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=100000076&amp;idx=1&amp;sn=0468d68861298c5e284d9654dc6788e5&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz5Jjv2IicQKTUh4JVk7qKx1ibgMynarKDYjLRaIranldvWbltG7sSzNlPicveUgOtyzcibSvmrLeVmFoQ/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》02 - 不得不说的废话</h2>
			<p class="desc">本章的内容对于你理解相对论会有莫大的帮助，看似有点扯远的内容恰恰是教会我们如何用一种正确的思维去阅读，甚至去“挑刺”。</p>
		</div>
	</a>
	
	<a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=100000089&amp;idx=1&amp;sn=11d4d2d249a9707b95306b677a10aeea&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz6eIxhfrYV0yffeNQ6Zc7RvbI2XicnTbvP3prln9ObzRLXkbiaYmFS5L3MDjiaBqHZ7ZOenXFWaPlGtA/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》03 - 伽利略相对性原理和变换式</h2>
			<p class="desc">伽利略变换式的伟大意义就在于他用数学的方法证明了伽利略相对性原理。</p>
		</div>
	</a>
	
	<a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=100000097&amp;idx=1&amp;sn=5ee695a60149fa49c7d37246bd271ae1&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz6Wxe3Es3iaB1o8GtHgSn5k3h7N84UgXZIarv3c754YGtlysbziawFJrnicRX68uLLTy8jTUiczEuRX9Q/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》04 - 史上最牛炼金术士牛顿</h2>
			<p class="desc">牛顿的绝对时空观符合我们大多数人的日常生活体验，然而后世一次次的实验结果都在无情地推翻着绝对时空观，物理学遇到了前所未有的危机。</p>
		</div>
	</a>
	
	<a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=100000116&amp;idx=1&amp;sn=4b942fa3bfcd5d1acebd2c07619c6a84&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz5mnRPt0eNGtYxzPNuWHaPnFKXzFY0DnOTynvKb2wjiagmxniba4vtwyQJ8zcQ3wvdmjSicxj9PTZoWw/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》05 - 光的速度</h2>
			<p class="desc">说相对论就必须要谈谈人类对光的传播速度的探索历程。</p>
		</div>
	</a>
	
<a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=100000137&amp;idx=1&amp;sn=c657efe6d914f3f29c1d05c189bc90cd&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz4wakbJiaSek3YrAI8DQoT8eM7kCqYfluky0icTwU0cCEgSUJSggMEQxfnZ4Hic4rmgZ4kCicjcq9XyQw/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》06 - 科学史上最成功的失败</h2>
			<p class="desc">“麦克尔逊—莫雷实验”对于整个物理学史甚至对于整个人类的科学史都有着举足轻重的地位。</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247483822&amp;idx=1&amp;sn=f08e37bc3e9d181d5595d99257fcf954&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz7n1qsgu4XCo7MO7gt4icUscbvHnMSjmIeQthYaINczibdriaJCEerNTibChPUVz3WEXic0VbCFAoW0llw/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》07-巨星登场</h2>
			<p class="desc">两朵乌云和光速不变原理</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247483840&amp;idx=1&amp;sn=3cf6005dea11101bfeee4ff13e03ba9f&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz6araXCFP5IibSwYYlJLz0wR1t8YFvXP4uumjltXib8xOdsYlCvs8GGC68EAe2Xov0Quwj6CrUAXyAg/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》08 - 环球快车谋杀案</h2>
			<p class="desc">小爱想着想着，眼皮开始发沉，意识逐渐模糊起来。小爱睡着了，他做了一个梦，这个梦非常精彩……</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247483875&amp;idx=1&amp;sn=2856c908fff720d4b759d181f43a53e7&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_png/wlqLP7LicAz553cpGJonu7JVacb0JGDPIAlMbX7lwDLxicI38n90751RkV9pBk9B9OejCcuvByGOWPQbdfq880oA/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》09 - 同时性的相对性</h2>
			<p class="desc">请你深吸一口冷气，因为你发现了这个宇宙中最深刻的一个奥秘，这是迄今为止让人类第一次感到深深震撼的等式，这一刻，我们根深蒂固的时间观念崩溃了。</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247483963&amp;idx=1&amp;sn=053a7d40150bacfe2d5010286881bdeb&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_png/wlqLP7LicAz7zic4vBAZoicQFZOib2KibJGrOPl5WCf9UJG8Xd6oV8yeBt5Umru4TLmhmkNYxUlcRDF6Dmxu9gnB0xQ/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》10 - 空间会收缩</h2>
			<p class="desc">下面，让我来隆重介绍本书最重要的角色之一，来自荷兰的韩德瑞克·安通·洛伦兹先生。各位观众，还记得你们读中学的</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247484003&amp;idx=1&amp;sn=610c62154290384dc25e75212582cd76&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_png/wlqLP7LicAz4aBgZN4Pco9rEVmn8Fk4y1mG1kT2xZtxLRylmhIdLcguSoQKxeYl4OuXUmxgT0DM2ia0BG1ctX4wA/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》11 - 质速神剑</h2>
			<p class="desc">牛顿如果地下有知，必定又会睁大惊恐的眼睛，暴怒道：“这个世界疯了！”</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247484024&amp;idx=1&amp;sn=9f39bae7c466704ed9a62fb5e61e48dc&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_png/wlqLP7LicAz4vPKCw9Libhc7Xul8NhV0IZW91b2mxXU1JiagUqAuej3hXaoPjqkZ96AwqV9BNWOHUGpnT9564WOhQ/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》12 - 质能奇迹</h2>
			<p class="desc">爱因斯坦马上就要写下古往今来最出名、最牛，连小学生都知道的一个惊天地泣鬼神的传世公式。</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247484044&amp;idx=1&amp;sn=369dfac4d26544ee5d56be0d6797f36d&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz7n1qsgu4XCo7MO7gt4icUscbvHnMSjmIeQthYaINczibdriaJCEerNTibChPUVz3WEXic0VbCFAoW0llw/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》13 - 爱因斯坦的不满</h2>
			<p class="desc">从狭义（special）到广义（general）是文字上的一小步，却是人类对我们这个宇宙认识的一大步，其意义</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247484099&amp;idx=1&amp;sn=0e87411b1cf5e84bd6174bc0f98ac0d6&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz5rRHb1jScQKvum8YRdIqH9hKAETIL0BbBsD6ibX3FeLTpx3ROicxYW7HWfZvt6yM3YoI5U0zFfbLIQ/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》14 - 等效原理</h2>
			<p class="desc">爱因斯坦得到了他一生中最快乐的想法</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247484160&amp;idx=1&amp;sn=2ece11b408935c31940964043a7ef389&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz5IvTE5jRicXLQYEjzX1BkaLe8C7EAWUn3yEmacDcS1ArFVPMqrLDOD6piaGcFJBWkib1snIg9QPJUdw/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》15 - 时空弯曲</h2>
			<p class="desc">在圆盘引力场中，我们发现圆周率大于π，这说明这个圆盘引力场中的空间并非平直，而是——弯曲的。</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247484202&amp;idx=1&amp;sn=674930c64d2ebdef502267c9b4715059&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz4Sq1V87NXAxWU4Cbwu7pNmdmwFbZOP1YBHBqvdRffGbLQ0UHJsHtTCLNSzSvp0ibdVxvINxLxxfsw/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》16 - 双胞胎佯谬</h2>
			<p class="desc">我们关于双胞胎兄弟孰老孰少问题的答案也就水落石出了</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247484231&amp;idx=1&amp;sn=ffe5c7da3753d1eff42c7770550a06f7&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz7heLdW9t5kUQmGicibCchdFyM6QE1NMQk79cNsR9gLuYJ9ngozd5InHblybSrhWun04ylK1RH5jGVQ/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》17 - 星光实验</h2>
			<p class="desc">且看爱因斯坦是如何设计那个将在四年后震撼全世界的著名实验的。</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247484277&amp;idx=1&amp;sn=c6db6069f4f9083c860e5aba2b72c442&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz5JibPIB5cLlvlVBcJVGuaX1eNYE0onTNvS0PIDkuFYT1wmqAc9OHP7uk3XbsMVRualVbN2SxRT4mg/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》18 - 从黑洞到虫洞</h2>
			<p class="desc">黑洞就是宇宙这张大网中时间和空间形成的一个洞，越看越像一个漏斗。你有没有想过，如果宇宙中有两个这样的漏斗，刚好漏斗嘴对漏斗嘴接上了，会发生什么情况？</p>
		</div>
	</a><a class="list_item js_post" href="http://mp.weixin.qq.com/s?__biz=MzI4MTI4MDQwNg==&amp;mid=2247484339&amp;idx=2&amp;sn=4dbb52314f497488ec8e2b99b83bfd39&amp;scene=19#wechat_redirect">
		<div class="cover">
			<img class="img js_img" src="http://mmbiz.qpic.cn/mmbiz_jpg/wlqLP7LicAz4WNVhFT1LvwL8VT3Mhkic91h2I0po29eGlyBB2JkIfXMiafKw2F5UotdbCFOu8Ez1udPL8AZ6KmUPw/0" alt="">
		</div>
		<div class="cont">
			<h2 class="title js_title">《时间的形状》19 - 宇宙大爆炸</h2>
			<p class="desc">爱因斯坦在打通六脉神剑之后，很快就把目光投向了整个宇宙，他把整个宇宙当做一个整体来研究。</p>
		</div>
	</a></div>"""
url_list = re.findall('(https{,1}://mp.weixin.qq.com/s[\S]+?)">',shijianxingzhuang_html)
for url in url_list:
    res = requests.get(url)
    body_soup = BeautifulSoup(res.text, "html5lib")
    title_ = body_soup.find_all('h2', class_='rich_media_title')[0].get_text().strip()
    try:
        os.mkdir('./html_/' + title_)
    except Exception as err:
        print(err)
    with open('./html_/' + title_ + '/pa_' + title_ + '.html', 'wb') as f:
        f.write(res.content)


res = requests.get(shijianxingzhuang_jiemudan)
body_soup = BeautifulSoup(res.text, "html5lib")
url_lists = body_soup.find_all('a', class_='list_item')
[x.get('href') for x in url_lists]