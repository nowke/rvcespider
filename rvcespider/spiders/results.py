# -*- coding: utf-8 -*-
import scrapy
from rvcespider.items import ResultItem

class ResultsSpider(scrapy.Spider):
    name = "results"
    allowed_domains = ["173.255.199.232"]
    start_urls = (
        'http://173.255.199.232:8001/results/getresult',
    )

    def parse(self, response):
        self.branch = ('5687f1d86e95525d0e0000b6', 'Computer Science')
        self.sem = ('Fifth', 5)
        self.usns = ['1RV13CS090', '1RV13CS091', '1RV13CS088']
        self.auth_token = str(response.xpath('//input[@name="authenticity_token"]/@value').extract()[0])
        self.year = '2015'

        for usn in self.usns:
        	yield scrapy.FormRequest.from_response(
        		response,
        		formdata = {
        			'authenticity_token': self.auth_token,
        			'result[usn]': usn,
        			'result[department]': self.branch[0],
        			'result[sem]': self.sem[0],
        			'result[year]': self.year,
        			'commit': 'Search'
        		},
        		callback=self.parse_result
        	)

    def parse_result(self, response):
    	container = response.xpath('//div[@id="wrapper"]//div[@class="container"]')[0]
    	main = container.xpath('.//div[@class="span12 main"]')[0]
    	rows = main.xpath('.//div[@class="row"]')

    	# Row 1 for USN, Name
    	first_row = rows[1]
    	first_row_data = first_row.xpath('.//p/text()').extract()

    	usn = first_row_data[1].strip()
    	name = first_row_data[3].strip()

    	if not usn:
    		return

    	# Subject rows - rows[3:-1]
    	course_data = []

    	subject_rows = rows[3:-1]
    	for subject_row in subject_rows:
    		cols = subject_row.xpath('./div//p/text()').extract()
    		course_code = cols[0].strip()
    		course_title = cols[1].strip()
    		course_grade = cols[2].strip()

    		course_data.append({
    				'sub_code': course_code,
    				'sub_title': course_title,
    				'sub_grade': course_grade,
    			})

    	# SGPA - last row
    	sgpa_row = rows[-1]
    	grade_div = sgpa_row.xpath('./div//p/b/text()').extract()
    	sgpa = grade_div[1].strip()

    	result_item = ResultItem()
    	result_item['usn'] = usn
    	result_item['name'] = name
    	result_item['sem'] = self.sem[1]
    	result_item['branch'] = self.branch[1]
    	result_item['sgpa'] = str(sgpa)
    	result_item['subjects'] = course_data

    	yield result_item