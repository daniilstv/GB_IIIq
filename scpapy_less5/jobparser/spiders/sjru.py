# -*- coding: utf-8 -*-
import scrapy
#from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D0%BE%D0%BB%D0%BE%D0%B3']

    def parse(self, response):
        next_page = response.css('a.f-test-link-dalshe::attr(href)').extract_first()  # Переход на следю страницу
        yield response.follow(next_page, callback=self.parse)  # Переходим на следующую страницу и возвращаемся

        vacansy = response.css(
            'div.display div._2g1F- div._3zucV a.icMQ_ _1QIBo::attr(href)'
        ).extract()  # Извлекаем ссылки на все вакансии

        for link in vacansy:
            yield response.follow(link, self.vacansy_parse) #Переходим на страницы вакансий

    def vacansy_parse(self, response):  # Собираем информацию со страницы
        name = response.css('div._3MVeX h1.header::text').extract_first()

        vacansy_description = response.css('div._1Tjoc script.application/ld+json').extract()
#        jsonresponse = json.loads(vacansy_description)
#        salary_max = jsonresponse['maxValue']
#        salary_min = jsonresponse['minValue']

        print(name)
#        yield JobparserItem(name=name, salary=salary)  # Формируем item

        pass
