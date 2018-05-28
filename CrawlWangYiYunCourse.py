#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
- [CrawlWangYiYunCourse.py](CrawlWangYiYunCourse.py) 下载`网易云课堂`的视频
**使用方法**
```bash
	python CrawlWangYiYunCourse.py [courseId]/[course url]
```
```bash
	python CrawlWangYiYunCourse.py http://study.163.com/course/introduction.htm?courseId=1003217019
```
或者
```bash
	python CrawlWangYiYunCourse.py 1003217019
```
**参数说明**
| :---: | :---:|
| -d, --dir| 视频下载存放在本地的路径, 默认为 "~/Downloads/"路径下|
| -i| 不生成markdown file, 默认为 True|
| --info| 生成markdown file, 默认为 False|
| --notdownload| 不下载视频文件到本地, 默认为 False|

```bash
	python CrawlWangYiYunCourse.py [courseId]/[course url] [-d ~/Downloads/] [--info] [--notdownload]
```

# more download file tools please visit: https://github.com/renever/cn_mooc_dl
"""

import requests
import re
import time
import random
import os
import sys
reload(sys)
sys.setdefaultencoding("utf8")


def get_timestamp():
    """
    get_timestamp
    1. datetime.now().strftime("%s")
    2. import calendar print calendar.timegm(datetime.utcnow().utctimetuple())
    :return:
    1527233088772
    1527233829
    """
    return str(time.time()).replace(".", str(random.randint(0,9)))

def unicode2string(unicodechars):
    # s.decode('raw_unicode-escape').encode('utf-8')
    return unicodechars.encode('utf-8').decode('unicode_escape','ignore').encode('utf-8', 'ignore')


USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
]

headers = {"User-Agent": random.choice(USER_AGENTS)}

# 课程页面url
course_base_url='http://study.163.com/course/introduction.htm?courseId={courseId}#/courseDetail?tab=1'
# 作者url
creator_base_url='http://study.163.com/provider/{creatorId}/course.htm'

# 课程dwr请求
course_detail_url = 'http://study.163.com/dwr/call/plaincall/PlanNewBean.getPlanCourseDetail.dwr?%s' % get_timestamp()
# 课程中的Video dwr请求
lesson_video_url = 'http://study.163.com/dwr/call/plaincall/LessonLearnBean.getVideoLearnInfo.dwr?%s' % get_timestamp()



def get_lesson_title_creator(html):
    creatorId, _, courseName =  re.findall(r's\w*?\.creatorId=(.*?);.*?s(\w*?)\.name="(.*?)"', html)[0]
    return (creatorId, unicode2string(courseName))

def get_course_info(Cid):
    data = {'callCount': 1,
            'scriptSessionId': '${scriptSessionId}190',
            'c0-scriptName': 'PlanNewBean',
            'c0-methodName': 'getPlanCourseDetail',
            'c0-id': '0',
            'c0-param0': 'string:' + Cid,
            'c0-param1': 'number:0',
            'c0-param2': 'null:null',
            'batchId': '%s' % get_timestamp()
            }

    r = requests.post(course_detail_url, data, headers)
    html = r.text

    course_creator_and_name = get_lesson_title_creator(html)

    lessons = re.findall(r's\w*?\.id=(.*?);.*?s(\w*?)\.lessonName="(.*?)"', html)
    return course_creator_and_name, lessons

def get_course_video_urs(Cid, Lid, Lname):
    """
      get the video urls
      :param Cid: course ID
      :param Lid: Lesson ID
      :param Lname: Lesson Name
      :return:
      """
    data = {
        'callCount': '1',
        'scriptSessionId': '${scriptSessionId}190',
        'c0-scriptName': 'LessonLearnBean',
        'c0-methodName': 'getVideoLearnInfo',
        'c0-id': '0',
        'c0-param0': 'string:' + Lid,
        'c0-param1': 'string:' + Cid,
        'batchId': get_timestamp()
    }

    r = requests.post(lesson_video_url, data, headers)
    results = r.text
    try:
        Vurl = re.findall(r'flvHdUrl="(.*?)"', results)[0]
        return Vurl
    except:
        pass



def generate_markdown_file(course_creator_and_name, course_id, lessons):
    md_contents = []
    title_tpl = '# [{course_name}]({course_url})\n[关于该作者的所有课程请点这里]({creator_url})'
    videos_tpl = '- [{name}]({url})'

    creatorId, course_name = course_creator_and_name
    # course_name = course_name.encode('latin1', 'ignore').decode('utf-8', 'ignore')
    if creatorId and course_name:
        course_url = course_base_url.format(courseId=course_id)
        creator_url = creator_base_url.format(creatorId=creatorId)
        md_contents.append(title_tpl.format(course_name=course_name, course_url=course_url, creator_url=creator_url))

    for _,name,url in lessons:
        md_contents.append(videos_tpl.format(name=name, url=url))

    file_name = '%s_%s.md' % (course_name,creatorId)
    with open(file_name, 'w') as f:
        f.write('\n'.join(md_contents))


import urllib
from multiprocessing import Pool
import contextlib
def download_to_local(course_creator_and_name, Cid, lessons, dir=None):
    """
    Download video to local folder
    :param course_creator_and_name:
    :param Cid:
    :param d_lessons:
    :return:
    """
    if not dir:
        dir = os.path.expanduser("~/Downloads/")

    _, course_name =  course_creator_and_name
    course_folder_name = '%s_%s' % (course_name, Cid)
    dir = os.path.join(dir, course_folder_name)

    if not os.path.exists(dir):
        os.makedirs(dir)

    videos = []
    idx = 0
    for _, name, url in lessons:
        idx+=1
        name = unicode2string(name).encode('latin1', 'ignore').decode('utf-8','ignore')
        # name = unicode2string(name)
        name = '%d.%s' % (idx, name)
        name = name.replace('/', '_') # convert '/' to '_'
        filename = os.path.join(dir, '%s.%s' % (name, get_extension(url)))
        # urllib.urlretrieve(url, filename)
        videos.append((filename, url))

    print('共找到了该课程[%s]的 共[%d]个视频.' % (course_name, len(videos)))

    num_processes = len(videos)/4
    with contextlib.closing(Pool(processes=num_processes)) as p:
        p.map(download_videos, videos)

def download_videos(video):
    filename, url = video
    print('正在下载: %s' % filename)
    urllib.urlretrieve(url, filename)

def get_extension(url):
    base_url = url.split('?')[0]
    base_name = os.path.basename(base_url)
    names = base_name.split(".")
    return names[len(names)-1]

def download_course(Cid, save_as_markdown_file=False, download_videos=True, dir=None):
    if not Cid:
        print 'Please enter courseId'
        exit(0)

    course_creator_and_name, lessons = get_course_info(Cid)
    d_lessons = []
    for lessonId, _, lessonName in lessons:
        lessonName = unicode2string(lessonName)
        url = get_course_video_urs(Cid, lessonId, lessonName)
        d_lessons.append((lessonId, lessonName, url))

    if save_as_markdown_file:
        generate_markdown_file(course_creator_and_name, Cid, d_lessons)

    if download_videos:
        download_to_local(course_creator_and_name, Cid, d_lessons, dir)



def get_course_id_from_url(url):
    courseId = None
    if (re.match(r'^\d*$', url)):
        courseId = url
    elif('http' in url or 'https' in url) and 'courseId' in url:
        courseId = re.findall(r'courseId=(\w*)', url)[0]
    else:
        print '%s 中不包含 courseId 信息, 请复制带courseId的 URL'

    return courseId


import argparse
if __name__ == "__main__":
    parameters =sys.argv[1:]

    helper_text = """
        Usage:
           python CrawlWangYiYunCourse.py 1003217019
           python CrawlWangYiYunCourse.py http://study.163.com/course/introduction.htm?courseId=1003217019
    """

    if len(parameters) == 0:
        print helper_text
        sys.exit(0)

    parser = argparse.ArgumentParser(description="网易云课堂视频下载(收费的不能下载)")
    parser.add_argument('course', metavar='course', help='course id or course url')
    parser.add_argument('-d', '--dir', help='视频下载存放在本地的路径')
    parser.add_argument('-i', action='store_true', help='不生成markdown file')
    parser.add_argument('--info', action='store_true', help='生成markdown file')
    parser.add_argument('--notdownload', action='store_true', help='不下载视频文件到本地')

    args = parser.parse_args()

    course_Id = get_course_id_from_url(args.course)

    if not course_Id:
       print helper_text
       sys.exit(0)

    _download_course_videos = not args.notdownload
    _generate_markdown_file = args.info
    _store_dir = None

    if args.dir:
        _store_dir = os.path.expanduser(args.dir)

    download_course(course_Id, _generate_markdown_file, _download_course_videos, _store_dir)
    print '^_^下载完毕!^_^'

