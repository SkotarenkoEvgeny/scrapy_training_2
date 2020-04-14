import scrapy


from datetime import datetime
import re
import json

from tauntondeeds.formdata_storage import formdata, formdata_1

class BristolSpider(scrapy.Spider):
    name = 'bristol'

    start_urls = ['http://www.tauntondeeds.com/Searches/ImageSearch.aspx']

    def none_molder(data):
        if data == '\xa0':
            data = None
        return data

    def parse(self, response):

        for form in [formdata, formdata_1]:

            yield scrapy.FormRequest(url=BristolSpider.start_urls[0],
                                               formdata=form,
                                               callback=self.parse_item)

    def parse_item(self, response):
        pagination_selector = """//*[@onmouseover="this.originalClass=this.className;this.className='gridHighlight'"]"""

        page_list = response.xpath(pagination_selector)

        for item in page_list:
            raw_data = {'date': None, 'type': None, 'book': None,
                        'page_num': None,
                        'doc_num': None, 'city': None, 'description': None,
                        'cost': None, 'street_address': None, 'state': None,
                        'zip': None}

            # get the date
            raw_data['date'] = datetime.strptime(
                item.xpath('td[2]/text()').get(),
                '%M/%d/%Y').date()

            # get the type
            raw_data['type'] = item.xpath('td[3]/text()').get()

            # get the book
            raw_data['book'] = BristolSpider.none_molder(
                item.xpath('td[4]/text()').get())

            # get the page_num
            raw_data['page_num'] = BristolSpider.none_molder(
                item.xpath('td[5]/text()').get())

            # get the page_num
            raw_data['doc_num'] = item.xpath(
                'td[6]/text()').get()  # get the doc_num

            # get the page_num
            raw_data['city'] = item.xpath('td[7]/text()').get()  # get the city

            raw_description = item.xpath('td/span/text()').get()

            # get the description
            raw_data['description'] = raw_description

            # get the cost
            raw_cost = raw_description.find('$')
            if raw_cost != -1:
                raw_data['cost'] = float(
                    raw_description[raw_cost + 1:])

            # get the street_adress
            raw_street = re.search(
                r"(ST|RD|AVE|WAY|LANE|AS).+(ST|RD|AVE|WAY|LANE)",
                raw_description)
            if raw_street !=None:
                temp = re.search(r"\d+.+(ST|RD|AVE|WAY|LANE|AS\s)",
                                 raw_street.group(0))
            else:
                temp = re.search(r"[0-9\-]+[A-Z\s]+(ST|RD|AVE|WAY|LANE|AS\s)",
                                 raw_description)

            if temp != None:
                raw_data['street_address'] = temp.group(0)
            else:
                temp = re.search(r"(ST|RD|AVE|WAY|LANE|AS\s).+",
                                 raw_street.group(0))
                raw_data['street_address'] = temp.group(0)

            # get the state
            raw_state = re.search(r"\((STATE .*)\)", raw_description)

            if raw_state != None:
                raw_data['state'] = raw_state.group(1)

            # get the zip
            # I did not found zip in this request data

            # for i in raw_data.keys():
            #     print(i, '=', raw_data[i])

            # print json file

            print(json.dumps(raw_data, default=str))



        # formdata_1['__EVENTARGUMENT'] = 'Page${}'.format(curent_page + 1)


        #
        # yield scrapy.FormRequest.from_response(response=response,
        #                                        formdata=formdata_1,
        #                                        callback=self.parse_item)

# this code is worked

# def parse_item(self, response):
#     pagination_selector = """//*[@onmouseover="this.originalClass=this.className;this.className='gridHighlight'"]/td"""
#
#     print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#     page_list = response.xpath(pagination_selector)
#
#     for item in page_list:
#         print(item.xpath('text()').extract())
#         print(item.xpath('span/text()').extract())
#     yield response
