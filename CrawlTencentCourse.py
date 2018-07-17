#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
import re
import json
import time
import random
import os
import urllib
import urllib2
from multiprocessing import Pool
import contextlib
import sys
reload(sys)
sys.setdefaultencoding("utf8")


from commonUtils import headers

video_page_url='https://ke.qq.com/webcourse/index.html#course_id={course_id}&'
video_page_base_uri = 'term_id=%s&taid=%s&vid=%s'
course_url = 'https://ke.qq.com/course/{course_id}'

get_info_url='https://h5vv.video.qq.com/getinfo?platform=11001&charge=1&otype=json&auth_from=260001&auth_ext=PMRGG33VOJZWKX3JMQRDUMRTGU2DGMRMEJ2GK4TNL5UWIIR2GEYDAMRXG43DENBMEJ2HS4DFEI5DELBCONXXK4TDMURDUMZMEJRW633LNFSSEORCEJ6Q&vids={vids}&defaultfmt=auto'
video_url = '{base_url}{filename}?sdtfrom=v1101&vkey={vkey}'


def crawl_tencent_course(url, course_id=None):
    course_id = course_id if course_id else get_course_id_from_url(url)
    r = requests.get(url, headers=headers)

    metadataPatten = re.compile('var\s+metaData\s+=\s+(.*);')
    metaData = metadataPatten.findall(r.content)[0]
    json_metadata =  json.loads(metaData)

    course_title = json_metadata['name']
    courses = json_metadata['terms'][0]['chapter_info']

    course_results = {'title': course_title, 'items': []}

    for course in courses:
        course_name = course['name']

        items = course['sub_info']
        for item in items:
            item_name = item['name']
            tasks = item['task_info']
            for task in tasks:
                term_id = task['term_id']
                taid = task['taid']
                video = task['video']
                video_name = video['name']
                vid = video['vid']

                ext, v_url = get_video_url(vid)
                v_name, _ = os.path.splitext(video_name)
                v_name = '%s%s'%(v_name, ext)
                course_results['items'].append({
                    'name': v_name,
                    'url': v_url
                })


    return course_results

def get_video_url(vids):
    url = get_info_url.format(vids=vids)
    r = requests.get(url, headers=headers)
    c = r.content
    p = re.compile('\s*Json\s*=\s*(.*);')
    d = p.findall(c)[0]
    v_url=''
    ext = ''
    if d:
        data = json.loads(d)
        ip = data['ip']
        vs = data['vl']['vi']
        for vi in vs:
            filename = vi['fn']
            _,ext = os.path.splitext(filename)
            vkey=vi['fvkey']
            baseUrl = vi['ul']['ui'][0]['url']

            if filename and vkey and baseUrl:
                v_url = video_url.format(base_url=baseUrl, filename=filename, vkey=vkey)
                break
    return ext, v_url


def get_course_id_from_url(url):
    courseId = None
    if (re.match(r'^\d*$', url)):
        courseId = url
    elif ('http' in url or 'https' in url) and 'course' in url:
        courseId = re.findall(r'course/(\w*)', url)[0]
    else:
        print '%s 中不包含 courseId 信息, 请复制带courseId的 URL'

    return courseId


def download_course(course_id, save_as_markdown_file=False, download_videos=True, dir=None):
    url = course_url.format(course_id=course_id)
    data = crawl_tencent_course(url)

    if len(data['items']) == 0:
        print 'No course video crawled'
        sys.exit(0)

    if save_as_markdown_file:
        genreate_markdown_file(data)

    if download_videos:
        download_to_local(course_id,data,  dir)


def genreate_markdown_file(video_data):
    """
    Create markdown file
    :param video_data: the param data from crawl_tencent_course function returned
    :return:
    """
    if len(video_data['items']) == 0:
        print "No Course video crawled"
        sys.exit(0)

    title = video_data['title']
    items = video_data['items']

    c_title = '# %s' % title
    c_item = '- [{v_name}]({v_url})'

    c_items = []

    for item in items:
        v_name = item['name']
        v_url = item['url']

        c_items.append(c_item.format(v_name=v_name, v_url=v_url))


    f_content = '%s \n %s' % (c_title, '\n'.join(c_items))

    filename = '%s.md'% title
    with open(filename, 'w') as f:
        f.write(f_content)

    print 'The markdown file [%s] created done!'%filename


def download_videos(item):
    dir, filename, url = item['dir'], item['name'], item['url']
    print('正在下载: %s' % filename)
    host = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url)
    filename = os.path.join(dir, filename)
    urllib.urlretrieve(url, filename)
    # req = urllib2.Request(url)
    # req.add_header("User-Agent", headers['User-Agent'])
    # req.add_header("Upgrade-Insecure-Requests", "1")
    # if host and len(host) > 0:
    #     req.add_header("Host", host[0])
    # # req.add_header("Referer", 'https://ke.qq.com/webcourse/index.html')
    # resp = urllib2.urlopen(req)
    # content = resp.read()
    # with open(filename, 'wb') as local_file:
    #     local_file.write(content)


    # resp = requests.get(url, headers={
    #     "User-Agent": headers['User-Agent'],
    #     'Host':host[0],
    #     'Upgrade-Insecure-Requests': "1"
    # }, stream=True)
    #
    # # resp = requests.get(url, stream=True)
    # with open(filename, 'wb') as local_file:
    #     for chunk in resp.iter_content(chunk_size=1024 * 1024):
    #         if chunk:
    #             local_file.write(chunk)


def download_to_local(course_id, video_data, dir=None):
    """
    Save the videos to local
    :param video_data: the param data from crawl_tencent_course function returned
    :return:
    """

    if len(video_data['items']) == 0:
        print "No Course video crawled"
        sys.exit(0)

    course_name = video_data['title']
    items = video_data['items']

    if not dir:
        dir = os.path.expanduser("~/Downloads/")

    course_folder_name = '%s_%s' % (course_name, course_id)
    dir = os.path.join(dir, course_folder_name)

    if not os.path.exists(dir):
        os.makedirs(dir)

    for item in items:
        item['dir']=dir

    print('共找到了该课程[%s]的 共[%d]个视频.' % (course_name, len(items)))
    # num_processes = len(items) / 2
    num_processes = len(items) / len(items)
    with contextlib.closing(Pool(processes=num_processes)) as p:
        p.map(download_videos, items)

    print("关于课程[%s]的 共[%d]个视频 下载完毕" % (course_name, len(items)))

import argparse
# if __name__ == '__main__':
#     parameters = sys.argv[1:]
#
#     helper_text = """
#             Usage:
#                python CrawlTencentCourse.py 235432
#                python CrawlTencentCourse.py https://ke.qq.com/course/235432
#         """
#
#     if len(parameters) == 0:
#         print helper_text
#         sys.exit(0)
#
#     parser = argparse.ArgumentParser(description="网易云课堂视频下载(收费的不能下载)")
#     parser.add_argument('course', metavar='course', help='course id or course url')
#     parser.add_argument('-d', '--dir', help='视频下载存放在本地的路径')
#     parser.add_argument('-i', action='store_true', help='不生成markdown file')
#     parser.add_argument('--info', action='store_true', help='生成markdown file')
#     parser.add_argument('--notdownload', action='store_true', help='不下载视频文件到本地')
#
#     args = parser.parse_args()
#
#     course_id = get_course_id_from_url(args.course)
#
#     if not course_id:
#         print helper_text
#         sys.exit(0)
#
#     _download_course_videos = not args.notdownload
#     _generate_markdown_file = args.info
#     _store_dir = None
#
#     if args.dir:
#         _store_dir = os.path.expanduser(args.dir)
#
#     download_course(course_id, _generate_markdown_file, _download_course_videos, _store_dir)
#     print '^_^下载完毕!^_^'

# data =  crawl_tencent_course('https://ke.qq.com/course/235432')
# download_course(235432, save_as_markdown_file=True)

download_course('235432')

