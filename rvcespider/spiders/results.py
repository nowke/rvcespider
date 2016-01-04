# -*- coding: utf-8 -*-
import scrapy
from rvcespider.items import ResultItem
from config import Config_dict

class ResultsSpider(scrapy.Spider):
    name = "results"
    allowed_domains = ["173.255.199.232"]
    start_urls = (
        'http://173.255.199.232:8001/results/getresult',
    )

    def parse(self, response):
    	self.config = Config_dict

        self.branch = (self.config['CUR_BRANCH_CODE'], self.config['CUR_BRANCH_FULL'])
        self.sem = (self.config['CUR_SEM_VAL'], self.config['CUR_SEM'])
        
        self.auth_token = str(response.xpath('//input[@name="authenticity_token"]/@value').extract()[0])
        self.year = '2015'

        year_short = self.config['CUR_USN_YEAR']
        start = int(self.config['CUR_USN_START'])
        end = int(self.config['CUR_USN_END']) + 1
        self.usns = [
            '1RV' +  year_short + self.config['CUR_BRANCH'] + "%03d" % x for x in range(start, end) 
        ]

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