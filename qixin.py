'''
 http://www.qixin.com/search?key=%E4%B8%8A%E6%B5%B7%E6%99%A8%E9%95%BF%E4%BF%A1%E6%81%AF%E6%8A%80%E6%9C%AF%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&page=1
http://www.qixin.com/search?key=上海晨长信息技术有限公司
 '''

import requests
from pyquery import PyQuery

base_url = "http://www.qixin.com"
search_url = "http://www.qixin.com/search?key="
company = "上海晨长信息技术有限公司"
UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
header = { "User-Agent" : UA, "Referer": "http://www.qixin.com" }
#proxy = {'http':'211.136.127.125:80'}
proxy = {'http':'139.224.24.26:8888'}
cache = {}

def fetch(url):
    '''
    查看缓存，存在命中，直接返回。
    '''
    response = requests.get(url=url,headers=header,proxies=proxy) 
    return response.text

def getCompanyUrl(company_name):
    url = search_url + company_name
    qxdoc = PyQuery(fetch(url))
    return getCompany(qxdoc)[company_name]
    
def getCompany(doc):
    company_list={}
    for data in doc('a[href*=company]'):
        pdata = PyQuery(data)
        company_list[pdata.text()]=base_url+pdata.attr("href")
    print(company_list.keys())
    return company_list

def getPerson(doc):
    person_list={}
    for data in doc('a[href*=name-detail\/]'):
        pdata = PyQuery(data)
        person_list[pdata.text()]=pdata.attr("href")
    #print(person_list.keys())
    return person_list

def getCompanyDetail(company_url):
    return getCompanyDetailFromDoc(PyQuery(fetch(company_url)))
    


def loadDocFromFile(filename):
    return PyQuery(file=filename)

def getCompanyDetailFromDoc(qxdoc):
    employees = qxdoc('#employees,#newOTCEmployees')    
    employee_list = getPerson(employees)

    partner = qxdoc('#partners,#newOTCPartners')  
    partner_companys=getCompany(partner)
    partner_persons = getPerson(partner)
    partner_managers = {}
    for comp,comp_url in partner_companys.items():
        p_employees,p_partner_persons,_,_=getCompanyDetail(comp_url)
        #p_employees,p_partner_persons,_,_=getCompanyDetailFromFile(comp)
        partner_managers.update(p_employees)
        partner_managers.update(p_partner_persons)

    return employee_list,partner_persons,partner_companys,partner_managers

def getCompanyDetailFromFile(company):
    if company in files.keys():
        return getCompanyDetailFromDoc(PyQuery(filename=files[company]))
    else:
        return {},{},{},{}

def qxb_login():
    '''
    {"acc":"18721289690","pass":"misas2018@qxb","captcha":{"isTrusted":true},"keepLogin":true}
    Cookie: aliyungf_tc=AQAAAEvzki7GlAwAXq6dtANjz88DVzyA; Hm_lvt_52d64b8d3f6d42a2e416d59635df3f71=1535796848; cookieShowLoginTip=1; sid=s%3AsV7rWJa9zMbCTvPBvLGbHcJPaDzBzpA1.WyDzPbsX%2B7zMgIm8h3eU4rraDJgDZmkadnEH11%2BQEsg; responseTimeline=16; _zg=%7B%22uuid%22%3A%20%2216594a025e6169-05142cb05c2ce3-34677908-fa000-16594a025e765b%22%2C%22sid%22%3A%201535936248.764%2C%22updated%22%3A%201535936775.2%2C%22info%22%3A%201535796848108%2C%22cuid%22%3A%20%22d3909546-64ac-43e0-beee-1c733eb58f4e%22%7D; Hm_lpvt_52d64b8d3f6d42a2e416d59635df3f71=1535936775
dc49417fe4f34f86b0fe: a1bb9bc076f5fb9e63386079cd0f53e7f0fa0f73c2f1a7ef4f66ae84189104098981b43155e924c04e66fec2034cd1e63e8320c8464b266720a132517a6af4f6
    '''
    loginurl = "https://www.qixin.com/api/user/login" 
    loginpayload = {"acc":"18721289690","pass":"misas2018@qxb","keepLogin":"true"}
    response = requests.post(loginurl,data=loginpayload,headers=header)
    print(response.text)
    return

def get_keys(dict_list):
    keys=""
    for key in dict_list.keys():
        keys +=key+","
    return keys


def test_file():    

    #qxb_login()
    company_url = 'https://www.qixin.com/company/45029850-a83d-485e-80eb-742679d415c3'
    company_url2 = "https://www.qixin.com/company/a7584eb5-cddb-4b16-b045-35421a0c4b62"
    filename1 = "/Users/administrator/Downloads/上海晨辉科技股份有限公司联系方式_信用报告_工商信息－启信宝.htm"
    filename2 = "/Users/administrator/Downloads/上海晨长信息技术有限公司联系方式_信用报告_工商信息－启信宝.htm"
    files = {"上海晨辉科技股份有限公司":filename1,"上海晨长信息技术有限公司":filename2}
    #employees,partner_persons,partner_companys,partner_managers = getCompanyDetail(company_url)
    #employees,partner_persons,partner_companys,partner_managers = getCompanyDetailFromDoc(PyQuery(filename=filename1))
    employees,partner_persons,partner_companys,partner_managers = getCompanyDetailFromDoc(PyQuery(filename=filename2))
    print("高管：",get_keys(employees))
    print("自然人股东：",get_keys(partner_persons))
    print("法人股东：",get_keys(partner_companys))
    print("法人股东高管：",get_keys(partner_managers))

companys=[
"上海艾策通讯技术有限公司",
"上海艾瑞市场咨询有限公司",
"上海爱可生信息技术股份有限公司",
"上海安方信息科技有限公司",
"上海奥典广告有限公司",
"上海奥林匹克制冷装璜工程有限公司",
"上海白领房产管理有限公司",
"上海犇众信息技术有限公司",
"上海伯特管理咨询有限公司",
"上海博达数据通信有限公司",
"上海博湾建设(集团)有限公司",
"上海博为峰软件技术股份有限公司",
"上海晨长信息技术有限公司",
"上海传际信息技术有限公司",]

for company in companys:
    company_url = getCompanyUrl(company)
    employees,partner_persons,partner_companys,partner_managers = getCompanyDetail(company_url)
    print(company)
    print("高管：",get_keys(employees))
    print("自然人股东：",get_keys(partner_persons))
    print("法人股东：",get_keys(partner_companys))
    print("法人股东高管：",get_keys(partner_managers))


