
import scrapy
import openpyxl
from scrapy.http import HtmlResponse

from ..items import PersonDataItem
import time


class PersonDataSpider(scrapy.Spider):
    name = 'person_data_spider'

    def start_requests(self):
        # 从unique_product_ids.xlsx文件中读取product_id
        wb = openpyxl.load_workbook('movies_list.xlsx')
        sheet = wb.active

        product_ids = []
        for row in sheet.iter_rows(values_only=True):
            product_id = row[0]
            product_ids.append(product_id)

        # 生成对应的URL并爬取数据
        for product_id in product_ids:
            url = f'https://www.amazon.com/dp/{product_id}/'
            yield scrapy.Request(url, callback=self.parse, meta={'product_id': product_id})

    #start_urls = ['https://www.amazon.com/dp/B004EPYZQM/']
    def process_request(self, request, spider):
        self.driver.get(request.url + "/?language=en_US")
        self.driver.refresh()
        # 检测机器人
        robot_sentence = "Sorry, we just need to make sure you're not a robot. For best results, please make sure your browser is accepting cookies."
        if robot_sentence in self.driver.page_source:
            from lxml import etree
            html = etree.HTML(self.driver.page_source)

            from amazoncaptcha import AmazonCaptcha
            link = html.xpath("/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img/@src")[0]
            captcha = AmazonCaptcha.fromlink(link)
            solution = captcha.solve()

            from selenium.webdriver.common.by import By
            input_element = self.driver.find_element(By.ID, "captchacharacters")
            input_element.send_keys(solution)

            button = self.driver.find_element(By.XPATH, "//button")
            button.click()
            time.sleep(3)

        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding='utf-8')
        return response

    def parse(self, response, *args, **kwargs):

        with open('output.json', 'w') as f:
            pass

        item = PersonDataItem()
            #return
        movie_genre_selectors=[
            '//span[contains(text(),"Genre")]/../following-sibling::td/span/text()',
            '//a[contains(text(),"Movies & TV")]/../../following-sibling::li[last()]/span/a/text()',
            '//span[@data-testid="genre-texts"][last()]/@aria-label'
        ]
        item['genre']=[]
        for movie_genre_selector in movie_genre_selectors:
            res = response.xpath(movie_genre_selector).extract()
            if res is not None and len(res) > 0 and len(res[0].strip())>0:
                item['genre'] = res[0].strip().split(", ")
                break

        # if(len(item['genre'])==0):
        #     print("#################")
            #yield response.follow(response.request.url, callback=self.parse, meta=response.meta)#重爬


        movie_directors_selectors = [
            '//span[contains(text(),"Directors")]/../following-sibling::dd/a/text()',
            #首先找到包含文本"Directors"的<span>元素，然后通过/..返回到其父元素，
            # 接着使用following-sibling::dd/a/text()找到该父元素的后续兄弟元素中的<a>标签，并提取其中的文本内容
            '//span[contains(text(),"Director")]/following-sibling::span/text()',
        ]
        item['directors'] = []
        for movie_directors_selector in movie_directors_selectors:
            res = response.xpath(movie_directors_selector).extract()#找到xpath对应的内容，填进res
            if res is not None and len(res) > 0:
                item['directors'] = res[0].split(", ")
                break

        movie_starring_selectors = [
            '//span[contains(text(),"Starring")]/../following-sibling::dd/a/text()',
            '//*[@id="acrPopover"]/span[1]/a/span/text()'
        ]
        item['starring'] = []
        for movie_starring_selector in movie_starring_selectors:
            res = response.xpath(movie_starring_selector).extract()
            if res is not None and len(res) > 0:
                item['starring'] = res[0].split(", ")
                break

        movie_actors_selectors = [
            '//span[contains(text(),"Actors")]/following-sibling::span/text()',
            '//span[contains(text(),"(Actor)")]/../../a/text()'#找(actor)
        ]
        item['actors'] = []
        for movie_actors_selector in movie_actors_selectors:
            res = response.xpath(movie_actors_selector).extract()
            if res is not None and len(res) > 0:
                item['actors'] = res[0].split(", ")
                break
        if len(item['actors'])>0 or len(item['genre'])>0 or len(item['directors'])>0 or len(item['starring'])>0:
            yield item

        # movie_name_selectors = ['//div[@id="titleSection"]/h1/span/text()',
        #                         '//h1[@data-automation-id="title"]/text()']
        # item['movie_name'] = ''
        # for movie_name_selector in movie_name_selectors:
        #     res = response.xpath(movie_name_selector).get()
        #     if res is not None and len(res) > 0:
        #         item['movie_name'] = res.strip()
        #         break
        #
        # movie_format_selectors = ['//span[contains(text(), "Format")]/following-sibling::span[1]',
        #                           '//span[(contains(text(), "Rent") or contains(text(), "Buy")) and span[@class="dv-conditional-linebreak"]]/strong/text()']
        # item['movie_format'] = ''
        # for movie_format_selector in movie_format_selectors:
        #     res = response.xpath(movie_format_selector).get()
        #     if res is not None and len(res) > 0:
        #         item['movie_format'] = res.strip()
        #         break

       # yield item
