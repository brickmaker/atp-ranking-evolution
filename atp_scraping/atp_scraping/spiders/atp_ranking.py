# -*- coding: utf-8 -*-
import scrapy


class AtpRankingSpider(scrapy.Spider):
    name = 'atp_ranking'
    start_urls = ['https://www.atptour.com/en/rankings/singles/']

    def parse(self, response):
        l = response.css('.dropdown').css('[data-value="rankDate"]')
        dates = l.css('li').css('::text').extract()
        dates = list(map(lambda s : s.strip().replace('.', '-'), dates))
        rank_range = '0-100'
        for date in dates:
            url = f'https://www.atptour.com/en/rankings/singles?rankDate={date}&rankRange={rank_range}'
            yield scrapy.Request(url, callback=self.parse_a_week)


        
    def parse_a_week(self, response):
        date = response.css('.dropdown-label').css('::text').get().strip()
        print(date)

        def get_info(row):
            terms = row.css('td')

            rank = int(terms[0].css('::text').get().strip())
            name = terms[3].css('a').css('::text').get()
            point = int(terms[5].css('a').css('::text').get().replace(',', ''))

            return {
                'rank': rank,
                'name': name,
                'point': point,
            }

        top_n = 10
        ranks_info = list(map(get_info, response.css('table').css('tbody').css('tr')[:top_n]))

        print(ranks_info)

        yield {
            'date': date,
            'ranks': ranks_info
        }
