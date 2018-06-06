import scrapy
import time
import os
from UniPLan.crawler.crawler import HTMLToJson
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    """
    This spider extracts all the links which contains the data of a course, and dumps them all in a list
    """
    name = "spiderUnil"
    target_json_file = os.path.normpath('../JSON_output_files/Courses.json')
    target_html_file = os.path.normpath('../HTML_output_files/Courses.html')

    def start_requests(self):
        """
        this function initiate the crawling by using the starting url
        :return: None
        """
        urls = [
            "https://applicationspub.unil.ch/interpub/noauth/php/Ud/index.php?v_langue=fr&v_isinterne=&v_ueid=174"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        """
        Called by callback by start_request on every response the spider gets, this function parses the html code of
        the response object and looks for links with the title 'Horaire HTML', it then adds it to a list of urls on
        which it starts crawling again.
        :param response: a Scrapy.response object
        :return:
        """
        responses = []

        for resp in response.xpath("//tr/td/a[@title='Horaire HTML']"):
            responses.append(resp.xpath("@href").extract())

        courses_urls = []

        for resp in responses:
            courses_urls.append("https://applicationspub.unil.ch/interpub/noauth/php/Ud/"+resp[0])

        if courses_urls is not None:

            try:
                output_json_file = open(self.target_json_file, 'a')
                output_json_file.write("[\n")
                output_json_file.close()
            except IOError:
                print("Initial Json writing error")

            for url in courses_urls:
                yield scrapy.Request(url, callback=self.parse_courses)
                time.sleep(1)

            try:
                output_json_file = open(self.target_json_file, 'a')
                output_json_file.write("\n]")
                output_json_file.close()
            except IOError:
                print("Secondary Json writing error")


    def parse_courses(self, response):
        """
        Called by callback by parse on every response it gets, this function parses the html code of the response object
        and looks for the 'UniDocContent' div, which contains the required data, it then uses HTMLToJson to create
        a .json file that contains all the data we want.
        :param response: a Scrapy.response object
        :return: None
        """
        output_json = ""
        # this loops on the divs that have an id of 'UniDocContent' (normally one by page, but you never know)
        for resp in response.xpath("//div[@id='UniDocContent']"):
            target_file = os.path.normpath('../HTML_output_files/Courses.html')
            # this then tries to open the Courses.html file, write the current html page in it, and calls
            # HTMLToJson to create a json formatted string
            try:
                output_html_file = open(target_file, 'w')
                output_html_file.write(resp.extract())
                output_html_file.close()
                output_json += HTMLToJson.recoverTimePlaceNameAndTeacher(target_file)
            except IOError:
                print("HTMLWrinting failure, file does not exist or is write-protected")

        target_file = os.path.normpath('../JSON_output_files/Courses.json')
        # finally, we try to open the Courses.json file and append the json file in it.
        try:
            output_json_file = open(target_file, 'a')
            output_json_file.write(output_json)
            output_json_file.close()
        except:
            print("JSONWriting failure, file does not exist or is write-protected")



"""
This part of the code simulate a terminal box and launches the spider automatically when this file is run
"""
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(QuotesSpider)
process.start() # the script will block here until the crawling is finished