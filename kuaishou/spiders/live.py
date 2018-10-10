# -*- coding: utf-8 -*-
import sys
import scrapy
import re
import bs4
from kuaishou.items import KuaishouItem

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time


class LiveSpider(scrapy.Spider):
    name = 'live'
    allowed_domains = ['live.kuaishou.com']
    #start_urls = ['https://live.kuaishou.com/profile/KSG7yyyy','https://live.kuaishou.com/profile/HYH88888888','https://live.kuaishou.com/profile/xiena666']
    start_urls = ['https://live.kuaishou.com/profile/KSG7yyyy']

    def parse(self, response):
        key_num_dict = {'쾺': '7', '곚':'0', '뷊':'1', '첪':'2', '곍':'3', 'ꯋ':'4', '뷌':'5', '꾻':'6', '껿':'8', '뿯':'9'}

        def getName(item):
            try:
                item['liveName'] = response.xpath('/html//p[@class="user-info-name"]/text()').extract()
                if type(item['liveName']) is list:
                    item['liveName'] = item['liveName'][0] #如果时list则取其一
                item['liveName'] = str(item['liveName']).strip('\n').strip()
            except Exception as e:
                print('@get name error', e, file=sys.stderr)

        def getID(item):
            try:
                item['liveID'] = response.xpath('/html//p[@class="user-info-other"]/span/text()').extract()
                
                if type(item['liveID']) is list:
                    item['liveID'] = item['liveID'][0] #如果时list则取其一
                item['liveID'] = str(item['liveID']).split('：')[-1]
            except Exception as e:
                print('@get ID error', e, file=sys.stderr)
        
        def getIntroduce(item):
            try:
                item['liveIntroduce'] = response.xpath('/html//p[@class="user-info-description"]/text()').extract()
                
                if type(item['liveIntroduce']) is list:
                    item['liveIntroduce'] = item['liveIntroduce'][0] #如果时list则取其一
                item['liveIntroduce'] = str(item['liveIntroduce'])
            except Exception as e:
                print('@get Introduce error', e, file=sys.stderr)

        # 获取主播的 星座与地址
        def getInfo(item):
            try:
                data = response.xpath('/html//span[@data-v-7cea7258]/text()').extract()
                for elem in data:
                    if re.match(r'[^\s][^\s]座', elem) is not None:
                        item['liveConstellation'] = elem
                        if type(item['liveConstellation']) is list:
                            item['liveConstellation'] = item['liveConstellation'][0] #如果时list则取其一
                            item['liveConstellation'] = str(item['liveConstellation'])
                    elif re.match(r'快手ID', elem) is not None: pass
                    else:
                        item['liveLocation'] = elem
            except Exception as e:
                print('@get liveConstellation error', e.with_traceback, file=sys.stderr)

        def getSex(item):
            try:
                item['liveSex'] = response.xpath('/html//p[@class="user-info-name"]/label').extract()
                if type(item['liveSex']) is list:
                    item['liveSex'] = item['liveSex'][0] #如果时list则取其一
                if re.search(r'female', item['liveSex']) is not None:
                    item['liveSex'] = 'female'
                elif re.search(r'\smale', item['liveSex']) is not None: 
                    item['liveSex'] = 'male'
                else:
                    item['liveSex'] = 'unknown'
            except Exception as e:
                print('@get sex error', e, file=sys.stderr)
        
        def getPhoto(item):
            try:
                item['livePhoto'] = response.xpath('/html//div[@class="avatar user-info-avatar"]/img/@src').extract()  
                if type(item['livePhoto']) is list:
                    item['livePhoto'] = item['livePhoto'][0] #如果时list则取其一
                item['livePhoto'] = str(item['livePhoto'])
            except Exception as e:
                print('@get livePhoto error', e, file=sys.stderr)

        # 数字编码问题 待解决
        # ::before ::after什么情况
        def getFans(item): 
            # 쾺.뷌w 7.5
            # 첪첪뿯.쾺w 229.7
            # 뷊꾻쾺껿.ꯋ 1678.4  뷍꿍쾾껝.붪
            # 뷌곍ꯋ.쾺 534.7
            # 첪첪꾻첪 2262
            # 꾻곍곚.쾺 630.7  
            
            #global key_num_dict
            #print('#test:', key_num_dict)
            try:
                item['liveFans'] = response.xpath('/html//div[@class="user-data-item fans"]/text()').extract()  
                if type(item['liveFans']) is list:
                    item['liveFans'] = item['liveFans'][0] #如果时list则取其一
                item['liveFans'] = str(item['liveFans'])
                #print('#test:', item['liveFans'])

                for charcter in key_num_dict:
                    item['liveFans']=item['liveFans'].replace(charcter, key_num_dict[charcter])
                    #print('#test:', item['liveFans'])

                #print('#test:', item['liveFans'])

            except Exception as e:
                print('@get liveFans error', e, file=sys.stderr)
        
        def getFollows(item): 
            #print('#test:', key_num_dict)
            try:
                item['liveFollows'] = response.xpath('/html//div[@class="user-data-item follow"]/text()').extract()  
                if type(item['liveFollows']) is list:
                    item['liveFollows'] = item['liveFollows'][0] #如果时list则取其一
                item['liveFollows'] = str(item['liveFollows'])

                for charcter in key_num_dict:
                    item['liveFollows']=item['liveFollows'].replace(charcter, key_num_dict[charcter])

            except Exception as e:
                print('@get liveFollows error', e, file=sys.stderr)

        def getProductions(item): 
            #print('#test:', key_num_dict)
            try:
                item['liveProductions'] = response.xpath('/html//div[@class="user-data-item work"]/text()').extract()  
                if type(item['liveProductions']) is list:
                    item['liveProductions'] = item['liveProductions'][0] #如果时list则取其一
                item['liveProductions'] = str(item['liveProductions'])

                for charcter in key_num_dict:
                    item['liveProductions']=item['liveProductions'].replace(charcter, key_num_dict[charcter])

            except Exception as e:
                print('@get liveProductions error', e, file=sys.stderr)

        def getProductionInfo(item):
            try:
                productionList = response.xpath('/html//div[@class="work-card-info"]')
                item['liveProductionList'] = []
                for elem in productionList:
                    product = {}
                    #print('###inside elem')
                    bsobj = bs4.BeautifulSoup(elem.extract())
                    title = bsobj.find('p', {'class':'work-card-info-title'}).get_text().strip('\n')
                    product['title'] = title
                    viewer = bsobj.find('span', {'class':'work-card-info-data-play'}).get_text().strip('\n').strip()
                    product['play_times'] = viewer
                    like = bsobj.find('span', {'class':'work-card-info-data-like'}).get_text().strip('\n').strip()
                    product['like'] = like
                    comment = bsobj.find('span', {'class':'work-card-info-data-comment'}).get_text().strip('\n').strip()
                    product['comment'] = comment
                    #print(product)
                    item['liveProductionList'].append(product)
                #print('#test product list', item['liveProductionList'])
            except Exception as e:
                print('@get livePhoto error', e, file=sys.stderr)

        def displayItem(item):
            print("######################################################\n\n", file=sys.stdout)
            for elem in item:
                print("#item:", elem, item[elem], file=sys.stdout)


        item = KuaishouItem()

        getName(item)
        getID(item)
        getIntroduce(item)
        getInfo(item)
        getSex(item)
        getPhoto(item)
        getFans(item)
        getFollows(item)
        getProductions(item)
        getProductionInfo(item)

        #displayItem(item)

        url = response.url
        print(url)
        ops = Options()  # 初始化一个选项实例
        #ops.add_argument('--headless') # 无界面运行
        prefs = {  
                'profile.default_content_setting_values' :  {  
                'notifications' : 2  
                }  
                }  
        ops.add_experimental_option('prefs',prefs) # 禁止弹窗

        driver = webdriver.Chrome(chrome_options=ops)
        try:
            count = 0
            for each in getCommentFrom(driver, url):
                print('comments count:', len(each))
                count+=1
                print('count=',count)
        except Exception as e:
            print('get comment error,', e, url)
        finally:
            driver.close()

def getCommentFrom(driver, url):
    'yield 依次返回一个作品中的所有评论'
    driver.get(url)

    products = driver.find_elements_by_xpath('//div[@class="work-card"]')

    for each in products:
        try:
            each.click()
            print(each.text)
        except Exception as e:
            print('open product error,', e)

        try:
            # 两次点击使视频暂停, 有些作品不是视频，不需要停止
            driver.find_element_by_xpath('//span[@class="play-icon"]').click()
            driver.find_element_by_xpath('//span[@class="play-icon"]').click()
        except Exception as e:
            print(e, 'no play icon')
        # 运行逻辑， 每步骤间应该加入try防止异常
        # 鼠标滚到最底下
        # 打开所有的子评论
        # 开始抓取

        commentList = driver.find_element_by_xpath('//div[@class="comment"]')

        # 滚到最底下
        count = 0
        try:
            action = ActionChains(driver)
            prev_last_comment = ''
            curr_last_comment = driver.find_elements_by_xpath('//div[@class="comment-item-body"]')[-1]
            error_time = 0  # 防止网络卡导致元素未加载
            while (prev_last_comment != curr_last_comment):
                prev_last_comment = curr_last_comment
                action.drag_and_drop(commentList, prev_last_comment)
                action.perform()
                time.sleep(0.5)  # 等待元素加载
                curr_last_comment = driver.find_elements_by_xpath('//div[@class="comment-item-body"]')[-1]
                count += 1
                print(count)
        except Exception as e:
            print("rolling error", e)

        print('totally run', count)
        print('pull over')

        # 打开所有子评论， ？？？需要打开窗口，否则会失灵, 鼠标会被占用
        try:
            expands = driver.find_elements_by_xpath('//div[@class="more-sub-expand"]')
            expands_count = len(expands)
            for each in expands:
                each.click()
                time.sleep(0.1)
        except Exception as e:
            print('open sub comment error', e)
        
        # 读取所有加载出来的评论
        try:
            comments = driver.find_elements_by_xpath('//div[@class="comment-item-body"]')
            subComments = driver.find_elements_by_xpath('//div[@class="comment-sub-item"]')
        except Exception as e:
            print('read comment error', e)
        print('now have', len(comments))
        print('expand count', expands_count)
        print('now have', len(subComments))

        # 关闭当前作品
        time.sleep(2) # 暂停
        try:
            close_icon = driver.find_element_by_xpath('//div[@class="close"]')
            if type(close_icon) is list:
                close_icon[0].click()
            else:
                close_icon.click()
        except Exception as e:
            print('close product error', e)
        yield comments + subComments
           
