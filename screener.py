from re import S
from selenium import webdriver
import requests
import time
from bs4 import BeautifulSoup
import numpy as np
import os
import traceback
import statistics
import copy
import RoboFund.technical_func as technicals

sectors = {
   "Basic Materials":[
      "Agricultural Inputs",
      "Building Materials",
      "Chemicals",
      "Specialty Chemicals",
      "Lumber & Wood Production",
      "Paper & Paper Products",
      "Aluminum",
      "Copper",
      "Other Industrial Metals & Mining",
      "Gold",
      "Silver",
      "Other Precious Metals & Mining",
      "Coking Coal",
      "Steel"
   ],
   "Consumer Cyclical":[
      "Auto & Truck Dealerships",
      "Auto Manufacturers",
      "Auto Parts",
      "Recreational Vehicles",
      "Furnishings, Fixtures & Appliances",
      "Residential Construction",
      "Textile Manufacturing",
      "Apparel Manufacturing",
      "Footwear & Accessories",
      "Packaging & Containers",
      "Personal Services",
      "Restaurants",
      "Apparel Retail",
      "Department Stores",
      "Home Improvement Retail",
      "Luxury Goods",
      "Internet Retail",
      "Specialty Retail",
      "Gambling",
      "Leisure",
      "Lodging",
      "Resorts & Casinos",
      "Travel Services"
   ],
   "Financial Services":[
      "Asset Management",
      "Banks—Diversified",
      "Banks—Regional",
      "Mortgage Finance",
      "Capital Markets",
      "Financial Data & Stock Exchanges",
      "Insurance—Life",
      "Insurance—Property & Casualty",
      "Insurance—Reinsurance",
      "Insurance—Specialty",
      "Insurance Brokers",
      "Insurance—Diversified",
      "Shell Companies",
      "Financial Conglomerates",
      "Credit Services"
   ],
   "Real Estate":[
      "Real Estate—Development",
      "Real Estate Services",
      "Real Estate—Diversified",
      "REIT—Healthcare Facilities",
      "REIT—Hotel & Motel",
      "REIT—Industrial",
      "REIT—Office",
      "REIT—Residential",
      "REIT—Retail",
      "REIT—Mortgage",
      "REIT—Specialty",
      "REIT—Diversified"
   ],
   "Consumer Defensive":[
      "Beverages—Brewers",
      "Beverages—Wineries & Distilleries",
      "Beverages—Non-Alcoholic",
      "Confectioners",
      "Farm Products",
      "Household & Personal Products",
      "Packaged Foods",
      "Education & Training Services",
      "Discount Stores",
      "Food Distribution",
      "Grocery Stores",
      "Tobacco"
   ],
   "Healthcare":[
      "Biotechnology",
      "Drug Manufacturers—General",
      "Drug Manufacturers—Specialty & Generic",
      "Healthcare Plans",
      "Medical Care Facilities",
      "Pharmaceutical Retailers",
      "Health Information Services",
      "Medical Devices",
      "Medical Instruments & Supplies",
      "Diagnostics & Research",
      "Medical Distribution"
   ],
   "Utilities":[
      "Utilities—Independent Power Producers",
      "Utilities—Renewable",
      "Utilities—Regulated Water",
      "Utilities—Regulated Electric",
      "Utilities—Regulated Gas",
      "Utilities—Diversified"
   ],
   "Communication Services":[
      "Telecom Services",
      "Advertising Agencies",
      "Publishing",
      "Broadcasting",
      "Entertainment",
      "Internet Content & Information",
      "Electronic Gaming & Multimedia"
   ],
   "Energy":[
      "Oil & Gas Drilling",
      "Oil & Gas E&P",
      "Oil & Gas Integrated",
      "Oil & Gas Midstream",
      "Oil & Gas Refining & Marketing",
      "Oil & Gas Equipment & Services",
      "Thermal Coal",
      "Uranium"
   ],
   "Industrials":[
      "Aerospace & Defense",
      "Specialty Business Services",
      "Consulting Services",
      "Rental & Leasing Services",
      "Security & Protection Services",
      "Staffing & Employment Services",
      "Conglomerates",
      "Engineering & Construction",
      "Infrastructure Operations",
      "Building Products & Equipment",
      "Farm & Heavy Construction Machinery",
      "Industrial Distribution",
      "Business Equipment & Supplies",
      "Specialty Industrial Machinery",
      "Metal Fabrication",
      "Pollution & Treatment Controls",
      "Tools & Accessories",
      "Electrical Equipment & Parts",
      "Airports & Air Services",
      "Airlines",
      "Railroads",
      "Marine Shipping",
      "Trucking",
      "Integrated Freight & Logistics",
      "Waste Management"
   ],
   "Technology":[
      "Information Technology Services",
      "Software—Application",
      "Software—Infrastructure",
      "Communication Equipment",
      "Computer Hardware",
      "Consumer Electronics",
      "Electronic Components",
      "Electronics & Computer Distribution",
      "Scientific & Technical Instruments",
      "Semiconductor Equipment & Materials",
      "Semiconductors",
      "Solar"
   ]
}
sector_num_list = ["Basic Materials","Consumer Cyclical","Financial Services","Real Estate","Consumer Defensive","Healthcare","Utilities","Communication Services","Energy","Industrials","Technology"]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


def getDriver(url):
    # CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
    # GOOGLE_CHROME_BIN = "/app/.apt/usr/bin/google-chrome"
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = GOOGLE_CHROME_BIN
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--window-size=1920,1080")
    # driver = webdriver.Chrome(CHROMEDRIVER_PATH,chrome_options=chrome_options)
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(os.getcwd() + "/RoboFund/chromedriver",chrome_options=chrome_options)
    driver.get(url)
    return driver


def start(user_sector=None,user_sub_sector=None):
    sectors_list = list(sectors)
    if not (user_sector and user_sub_sector):
        have_error = True
        while have_error:
            print("Hello there, please select the sector you want:")
            counter = 1
            for i in sectors:
                print(str(counter) + ". " + i)
                counter += 1
            try:
                user_sector = int(input("Please type in the number corresponding to your sector: ")) - 1
                have_error = False
            except:
                print("Please type in a number.")
                have_error = True
        have_error = True
        
        while have_error:
            print("Please choose your sub-sector:")
            counter = 1
            for i in sectors[sectors_list[user_sector]]:
                print(str(counter) + ". " + i)
                counter += 1
            try:
                user_sub_sector = int(input("Please type in the number corresponding to your sub sector: ")) - 1
                have_error = False
            except:
                print("Please type in a number")
                have_error = True
        
    return get_stocks(sectors_list[user_sector] ,sectors[sectors_list[user_sector]][user_sub_sector])


def get_stocks(sector):
    stocks_from_yf = []    

    driver = getDriver("https://finance.yahoo.com/screener/new")
    # with open("myfile.html","w",encoding='utf-8') as f:
    #     f.write(driver.page_source)
    

    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/button[3]').click()
    driver.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/button[4]').click()
    driver.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[4]/div/div[1]/div[2]/ul/li/div').click()
    time.sleep(1)
    dropdown = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/div[4]/div/div[1]/div[2]/ul/li/div/div[2]/div/div[2]/ul')
    time.sleep(1)
    for i in sector:
        driver.implicitly_wait(10)
        dropdown.find_element_by_xpath(f'//*[text()="{i}"]').click()

        # archive
        #click_span = driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/div[4]/div/div[1]/div[2]/ul/li/div/div[2]/div/div[2]/ul/li[{sector_num_list.index(i) + 1}]/label')
        #print(dropdown.find_element_by_xpath(f'//span[text()="{i}"]').find_element_by_xpath("..").get_attribute('innerHTML'))
        #ActionChains(driver).move_to_element(click_span).click(click_span).perform()
        #dropdown.find_element_by_xpath(f'//span[text()="{i}"]').click()
        # click_span=WebDriverWait(elem, 60).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/div[4]/div/div[1]/div[2]/ul/li/div/div[2]/div/div[2]/ul/li[{sector_num_list.index(i) + 1}]/label')))
        # click_span.click()
        #driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/div[4]/div/div[1]/div[2]/ul/li/div/div[2]/div/div[2]/ul/li[{sector_num_list.index(i) + 1}]/label/input').click()
        # dropdown.find_element_by_xpath(f'//span[text()="{i}"]').find_element_by_xpath("..").click()
    
    driver.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]').click()

    # get subsector
    # driver.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[4]/div/div[3]/div[2]/ul/li/div').click()
    # time.sleep(1)
    # dropdown = driver.find_element_by_xpath('//*[@id="dropdown-menu"]/div/div/ul')
    
    # dropdown.find_element_by_xpath(f'//span[text()="{sub_sector}"]').click()

    # driver.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]').click()
    # end get subsector

    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]/div[3]/button[1]').click()
    time.sleep(5)
    driver.implicitly_wait(20)
    driver.get(driver.current_url + '&count=100')
    driver.implicitly_wait(5)
    
    print(">>> Get stocks")
    # with open("myfile.html","w",encoding='utf-8') as f:
    #     f.write(driver.page_source)
    try:
        table = driver.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table')
        table_data = table.find_elements_by_tag_name('tr')
        for i in range(1,len(table_data)):
            if "-" not in driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{i}]/td[1]').text:
                stocks_from_yf.append(driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{i}]/td[1]').text)
    except Exception as e:
        print(f"No results for {sector} sector.")
        print(f"{str(e)}\n\n{''.join(traceback.format_tb(e.__traceback__))}")
        driver.quit()
        return None

    driver.quit()
    return stocks_from_yf

def get_stocks_from_finviz(stocks_from_yf):
    not_found = []
    no_multiple = []
    finviz_stats = {}
    avg_pb_mul = {}
    avg_pe_mul = {}

    print(">>> Starting finviz section")
    print(f">>> {stocks_from_yf}")
    for ticker in stocks_from_yf:
        print(f">>> started {ticker}")
        validityCheck = requests.get(f"https://finviz.com/quote.ashx?t={ticker}", allow_redirects=False, headers=headers)
        if validityCheck.status_code == 200:
            #finviz
            print(">>> going into stocks")
            soupf = BeautifulSoup(validityCheck.content, "html.parser")
            sectorData = soupf.find_all("table",class_="fullview-title")
            td3 = sectorData[0].find_all('td')[2]
            stock_sector = td3.find_all('a')[0].text
            if stock_sector not in finviz_stats:
                finviz_stats[stock_sector] = {}
            if stock_sector not in avg_pb_mul:
                avg_pb_mul[stock_sector] = 0
            if stock_sector not in avg_pe_mul:
                avg_pe_mul[stock_sector] = 0

            tableData = soupf.find_all("td",class_="snapshot-td2")
            #get 52 week high and low
            highlowStr = tableData[34].text
            highlowyRange = highlowStr.split("-")
            
            try:
                print(ticker)
                low = float(highlowyRange[0].strip()) 
                high = float(highlowyRange[1].strip())
                print(ticker + " range passed")
                #get price
                price = float(tableData[65].text)
                print(ticker + " price passed")
                #price to book
                pb = float(tableData[25].text)
                print(ticker + " pb passed")
                #price to earnings
                pe = float(tableData[1].text)
                print(ticker + " pe passed")   
                avg_pb_mul[stock_sector] += pb
                avg_pe_mul[stock_sector] += pe
                finviz_stats[stock_sector][ticker] = {"high":high,"low":low,"price":price,"pb":pb,"pe":pe}
            except:
                print("fail")
                no_multiple.append(ticker)

        else:
            print(">>> not found")
            not_found.append(ticker)
    
    if not_found:
        print(f">>> Could not find the following stock tickers:\n{', '.join(not_found)}")
    if no_multiple:
        print(f">>> These stocks have no multiples:\n{', '.join(no_multiple)}")
    
    print("Iterating through all the stock multiples")
    
    stonks = []
    refined_stonks = []
    
    #FINANCIALS TO HAVE OWN FUNCTION
    # if sector == "Financial Services":
    #     if len(finviz_stats) > 0:
    #             avg_pb_mul = avg_pb_mul/len(finviz_stats)
    #             stonks = [(i,j['price']) for i,j in finviz_stats.items() if j['pb'] < avg_pb_mul]
    #             print(f">>> Here are the stocks that I recommend: {', '.join([x[0] for x in stonks])}")
    #             print("Refining based on technicals...")
    #             refined_stonks = technicals.get_refined_stocks(stonks)
    #
    #     else:
    #         print(">>> No stocks in list")
    # else:

    for z in finviz_stats:
        if len(finviz_stats[z]) > 0:
            avg_pb_mul[z] = avg_pb_mul[z]/len(finviz_stats[z])
            avg_pe_mul[z] = avg_pe_mul[z]/len(finviz_stats[z])

            std_pb_mul = {}
            std_pe_mul = {}

            std_pb_mul[z] = statistics.stdev([j["pb"] for i,j in finviz_stats[z].items()])
            std_pe_mul[z] = statistics.stdev([j["pe"] for i,j in finviz_stats[z].items()])

            print("Avg PB:",avg_pb_mul[z])
            print("Avg PE:",avg_pe_mul[z])

            notable_stocks = []
            temp_finviz_stats = copy.deepcopy(finviz_stats[z])

            # find outliers using stdev
            for i,j in temp_finviz_stats.items():
                if j['pb'] > std_pb_mul[z] * 2 + avg_pb_mul[z] or j['pe'] > std_pe_mul[z] * 2 + avg_pe_mul[z]:
                    finviz_stats[z].pop(i)
                
            std_pb_mul[z] = statistics.stdev([j["pb"] for i,j in finviz_stats[z].items()])
            std_pe_mul[z] = statistics.stdev([j["pe"] for i,j in finviz_stats[z].items()])
            
            avg_pb_mul[z] = sum([j['pb'] for i,j in finviz_stats[z].items()])/len(finviz_stats[z])
            avg_pe_mul[z] = sum([j['pe'] for i,j in finviz_stats[z].items()])/len(finviz_stats[z])

            for i,j in finviz_stats[z].items():
                if j['pb'] < avg_pb_mul[z] - std_pb_mul[z] * 2 or j['pe'] < avg_pe_mul[z] - std_pe_mul[z] * 2:
                    notable_stocks.append(i)

            print(f"Avg PB:{avg_pb_mul[z]:.2f}")
            print(f"Avg PE:{avg_pe_mul[z]:.2f}")
            print(finviz_stats[z])
            print(f">>> Avg PB: {avg_pb_mul[z]}\nAvg PE: {avg_pe_mul[z]}")
            stonks += [(i,j['price']) for i,j in finviz_stats[z].items() if j['pb'] < avg_pb_mul[z] or j['pe'] < avg_pe_mul[z]]
            print(f">>> Here are the stocks that I recommend: \n{', '.join([x[0] for x in stonks])}\n\n*Undervalued Stocks*\n{' ,'.join(notable_stocks) if len(notable_stocks) > 0 else 'No undervalued stocks in sector'}") if len(stonks) > 0 else print(f">>> No stocks to recommend.")
            
        else:
            print(">>> No stocks in list")
    
    return stonks

def get_refined_stonks(stonks):
    print(">>> stonks")
    print(stonks)
    refined_stonks = []
    refined_stonks = technicals.get_refined_stocks(stonks)

    #return list(set(refined_stonks + [x for x,y in stonks]))
    return list(set(refined_stonks + [x[0] for x in stonks]))
