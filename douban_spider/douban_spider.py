"""
一个简单的Python爬虫, 用于抓取豆瓣电影Top前100的电影的名称

Anthor: JiangTao11
Version: 0.0.0
Date: 2016/10/15
Language: Python3.4
Editor: Sublime Text2
"""
import re
import urllib.request


class DouBanSpider:
    """
    豆瓣top100爬虫类说明
    Attributes:
        page:表示当前所处地抓取页面
        cur_url:当前抓取页面的url
        datas:用于储存已经抓取到的电影的名称
        _top_num:用于记录当前电影的top号
    """

    def __init__(self):
        self.page = 1
        self.cur_url = "http://movie.douban.com/top250?start={page}&filter=&type="
        self.datas = []
        self._top_num = 1

    def get_page_content(self, cur_page):
        """
        爬取当前页面的内容
        Args:
            cur_page: 当前页面的页码

        Returns:
            返回当前页面的内容
        """
        url = self.cur_url
        try:
            page_content = urllib.request.urlopen(url.format(page=(cur_page - 1) * 25)).read().decode("utf-8")
        except urllib.error as e:
            if hasattr(e, "code"):
                print("The server couldn't fulfill the request.")
                print("Error code: %s" % e.code)
            elif hasattr(e, "reason"):
                print("We failed to reach a server. Please check your url and read the Reason")
                print("Reason: %s" % e.reason)
        return page_content

    def find_movie_name(self, page_content):
        """
        从爬取的页面中解析出电影名称
        Args:
            page_content: 爬取页面的html
        """
        temp_data = []
        movie_name = re.findall(r'<span.*?class="title">(.*?)</span>', page_content, re.S)
        for index, item in enumerate(movie_name):
            if item.find("&nbsp") == -1:
                temp_data.append("Top "+str(self._top_num)+"  "+item)
                self._top_num += 1
        self.datas.extend(temp_data)

    def start_spider(self):
        """
        爬虫入口控制已经爬取数量限制
        由于豆瓣每页的电影title显示数是25个
        因此要爬取电影top100,只需要爬取前四页即可
        """
        while self.page <= 4:
            page_content = self.get_page_content(self.page)
            self.find_movie_name(page_content)
            self.page += 1

def main():
    mySpider = DouBanSpider()
    mySpider.start_spider()
    for item in mySpider.datas:
        print(item)
if __name__=="__main__":
    main()