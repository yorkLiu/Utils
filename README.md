# Utils
记录自己所总结或所使用的一些工具

1. [CrawlWangYiYunCourse.py](CrawlWangYiYunCourse.py) 下载[网易云课堂](http://study.163.com/)的视频
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
    
    | 参数 | 说明|
    | :---: | :---: |
    | -d, --dir| 视频下载存放在本地的路径, 默认为 "~/Downloads/"路径下|
    | -i| 不生成markdown file, 默认为 True|
    | --info| 生成markdown file, 默认为 False|
    | --notdownload| 不下载视频文件到本地, 默认为 False|
    
    ```bash
        python CrawlWangYiYunCourse.py [courseId]/[course url] [-d ~/Downloads/] [--info] [--notdownload]
    ```