import time

import scrapy


class HWZoneSpider(scrapy.Spider):
    name = "HwZone"
    start_urls = [
        "https://forums.hardwarezone.com.sg/forums/japan.271/"
    ]

    def parse(self, response):
        for thread in response.xpath("//div[@class='structItem-title']/a"):
            thread_link = thread.xpath("@href").extract()

            yield response.follow("https://forums.hardwarezone.com.sg" + thread_link[0], self.parse_thread)

        next_page = response.xpath("//a[@class='pageNav-jump pageNav-jump--next']/@href").extract()
        if next_page is not None:
            yield response.follow("https://forums.hardwarezone.com.sg" + next_page[0], self.parse)

    def parse_thread(self, response):
        title = response.xpath("//h1[@class='p-title-value']/text()").extract()
        cnt = response.xpath("//div[@class='bbWrapper']/text()").extract()
        ath = response.xpath("//a[@itemprop='name']/text()").extract()
        for post in range(len(response.xpath("//article[@class='message message--post js-post js-inlineModContainer  ']"))):
            yield {
                'title': title[0],
                'content':cnt[post],
                'author': ath[post],
            }

        next_page = response.css('a.pageNav-jump--next::attr(href)').get()
        if next_page is not None:
            yield response.follow("https://forums.hardwarezone.com.sg" + next_page, self.parse_thread)


