# -*- coding: utf-8 -*-
import scrapy
import copy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
from ..items import CompanyItem
from parsel import Selector


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['nasdaqomxnordic.com']
    start_urls = ['http://www.nasdaqomxnordic.com/aktier']

    def __init__(self, market=None, segment=None, other=None, sector=None, *args, **kwargs):
        super(SpiderSpider, self).__init__(*args, **kwargs)
        self.market = market
        self.segment = segment
        self.other = other
        self.sector = sector

        # 下面这句话只是为了pycharm的智能提示
        # from selenium import webdriver
        # self.driver = webdriver.Chrome()

    def __del__(self):
        self.driver.quit()

    def parse(self, response):
        # Market 部分
        xpath_market_nordic = """//*[@id="NOR"]/.."""
        xpath_market_cph = """//*[@id="CPH"]/.."""
        xpath_market_sto = """//*[@id="STO"]/.."""
        xpath_market_hel = """//*[@id="HEL"]/.."""
        xpath_market_ice = """//*[@id="ICE"]/.."""
        # market 参数处理
        if self.market is None:
            self.market = ["nordic"]
        else:
            self.market = copy.deepcopy(str(self.market).lower().split(";"))
        # market 按钮
        self.driver.find_element_by_xpath(xpath_market_nordic).click()
        self.driver.find_element_by_xpath(xpath_market_cph).click()
        self.driver.find_element_by_xpath(xpath_market_sto).click()
        self.driver.find_element_by_xpath(xpath_market_hel).click()
        self.driver.find_element_by_xpath(xpath_market_ice).click()
        time.sleep(1)
        for market in self.market:
            if market == "nordic":
                self.driver.find_element_by_xpath(xpath_market_nordic).click()
            if market == "cph":
                self.driver.find_element_by_xpath(xpath_market_cph).click()
            if market == "sto":
                self.driver.find_element_by_xpath(xpath_market_sto).click()
            if market == "hel":
                self.driver.find_element_by_xpath(xpath_market_hel).click()
            if market == "ice":
                self.driver.find_element_by_xpath(xpath_market_ice).click()

        # Segment 部分
        xpath_segment_largecap = """//*[@id="largeCap"]/.."""
        xpath_segment_midcap = """//*[@id="midCap"]/.."""
        xpath_segment_smallcap = """//*[@id="smallCap"]/.."""
        xpath_segment_norwegianshares = """//*[@id="OSLO"]/.."""
        # segment 参数处理
        if self.segment is None:
            self.segment = ["mid", "small"]
        else:
            self.segment = copy.deepcopy(str(self.segment).lower().split(";"))
        # segment 按钮
        self.driver.find_element_by_xpath(xpath_segment_largecap).click()
        time.sleep(1)
        for segment in self.segment:
            if segment == "large":
                self.driver.find_element_by_xpath(xpath_segment_largecap).click()
            if segment == "mid":
                self.driver.find_element_by_xpath(xpath_segment_midcap).click()
            if segment == "small":
                self.driver.find_element_by_xpath(xpath_segment_smallcap).click()
            if segment == "nws":
                self.driver.find_element_by_xpath(xpath_segment_norwegianshares).click()

        # Other 部分
        xpath_other_observationstatus = """//*[@id="obs"]/.."""
        xpath_other_externallist = """//*[@id="extern"]/.."""
        xpath_other_liquidityprovider = """//*[@id="lp"]/.."""
        # other 参数处理
        if self.other is None:
            self.other = []
        else:
            self.other = copy.deepcopy(str(self.other).lower().split(";"))
        # other 按钮
        for other in self.other:
            if other == "obs":
                self.driver.find_element_by_xpath(xpath_other_observationstatus).click()
            if other == "extlist":
                self.driver.find_element_by_xpath(xpath_other_externallist).click()
            if other == "lp":
                self.driver.find_element_by_xpath(xpath_other_liquidityprovider).click()

        # Sector 部分
        xpath_sector_energy = """//*[@id="energy"]/.."""
        xpath_sector_materials = """//*[@id="materials"]/.."""
        xpath_sector_industrials = """//*[@id="industrials"]/.."""
        xpath_sector_goods = """//*[@id="consumer-goods"]/.."""
        xpath_sector_services = """//*[@id="consumer-services"]/.."""
        xpath_sector_health = """//*[@id="health-care"]/.."""
        xpath_sector_telecom = """//*[@id="telecom"]/.."""
        xpath_sector_utilities = """//*[@id="utilities"]/.."""
        xpath_sector_financials = """//*[@id="financials"]/.."""
        xpath_sector_technology = """//*[@id="technology"]/.."""
        # sector 参数处理
        if self.sector is None:
            self.sector = []
        else:
            self.sector = copy.deepcopy(str(self.sector).lower().split(";"))
        # sector 按钮
        for sector in self.sector:
            if sector == "energy":
                self.driver.find_element_by_xpath(xpath_sector_energy).click()
            if sector == "mat":
                self.driver.find_element_by_xpath(xpath_sector_materials).click()
            if sector == "industry":
                self.driver.find_element_by_xpath(xpath_sector_industrials).click()
            if sector == "goods":
                self.driver.find_element_by_xpath(xpath_sector_goods).click()
            if sector == "services":
                self.driver.find_element_by_xpath(xpath_sector_services).click()
            if sector == "health":
                self.driver.find_element_by_xpath(xpath_sector_health).click()
            if sector == "telecom":
                self.driver.find_element_by_xpath(xpath_sector_telecom).click()
            if sector == "utility":
                self.driver.find_element_by_xpath(xpath_sector_utilities).click()
            if sector == "finance":
                self.driver.find_element_by_xpath(xpath_sector_financials).click()
            if sector == "tech":
                self.driver.find_element_by_xpath(xpath_sector_technology).click()

        # 解析table
        xpath_result_table_rows = """//*[@id="searchSharesListTable"]/tbody/tr"""
        xpath_result_company_industry = """//td[1]/@title"""
        xpath_result_company_fullname = """//td[2]/a/text()"""
        xpath_result_company_ccy = """//td[3]/text()"""
        xpath_result_company_last = """//td[4]/text()"""
        xpath_result_company_positive_or_negative = """//td[5]/*/text()"""
        xpath_result_company_percent = """//td[6]/*/text()"""
        xpath_result_company_bid = """//td[7]/text()"""
        xpath_result_company_ask = """//td[8]/text()"""
        xpath_result_company_volume = """//td[9]/text()"""
        xpath_result_company_turnover = """//td[10]/text()"""
        xpath_result_company_pdflink = """//td[2]/*[2]/*/@href"""
        try:
            WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located((By.ID, "searchSharesListTable"))
            )
        except:
            self.driver.quit()
            logging.error("Check your network connection")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4);")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4);")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4);")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4);")

        companies = Selector(text=self.driver.page_source).xpath(xpath_result_table_rows).extract()
        for company in companies:
            item = CompanyItem()
            item['industry'] = Selector(text=company).xpath(xpath_result_company_industry).extract_first()
            item['fullname'] = Selector(text=company).xpath(xpath_result_company_fullname).extract_first()
            item['ccy'] = Selector(text=company).xpath(xpath_result_company_ccy).extract_first()
            item['last'] = Selector(text=company).xpath(xpath_result_company_last).extract_first()
            item['positiveornegative'] = Selector(text=company).xpath\
                (xpath_result_company_positive_or_negative).extract_first()
            item['percent'] = Selector(text=company).xpath(xpath_result_company_percent).extract_first()
            item['bid'] = Selector(text=company).xpath(xpath_result_company_bid).extract_first()
            item['ask'] = Selector(text=company).xpath(xpath_result_company_ask).extract_first()
            item['volume'] = Selector(text=company).xpath(xpath_result_company_volume).extract_first()
            item['turnover'] = Selector(text=company).xpath(xpath_result_company_turnover).extract_first()
            item['pdflink'] = Selector(text=company).xpath(xpath_result_company_pdflink).extract_first()
            yield item




