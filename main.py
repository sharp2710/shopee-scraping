from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import bs4
import time
import pandas as pd
import json
from pythainlp.tokenize import word_tokenize
 

location = r"./chromedriver.exe"
service = Service(location)
service.start()
keyword = "ลูกชิ้น"
driver = webdriver.Remote(service.service_url)
location = "https://shopee.co.th/search?keyword=" + keyword
driver.get(location)
data = []



def get_data():
    # รอ 5 วินาที
     def set_data():
         time.sleep(5)
         page_source = driver.page_source
         soup = bs4.BeautifulSoup(page_source)
         link = soup.find_all('a', {'data-sqe': 'link'})
         image = soup.find_all('img', {'class': '_7DTxhh vc8g9F'}) 
         price = soup.find_all('div', {'class': 'vioxXd rVLWG6'})
         name = soup.find_all('div', {'class': 'ie3A+n bM+7UW Cve6sh'})
         sold = soup.find_all('div', {'class': 'ZnrnMl'})
 
         for i in range(len(link)):
             data.append({
                 'link':  link[i]['href'] if link[i]['href'].startswith('https://shopee.co.th') else 'https://shopee.co.th' + link[i]['href'],
                 'image': image[i]['src'] if image[i]['src'] is not None else 'None',
                 'price': price[i].text if price[i].text is not None else 'None',
                 'sold': sold[i].text if sold[i].text is not None else 'None',
                 'name': word_tokenize(name[i].text, engine='newmm') if name[i].text is not None else 'None'
           })
           
     while True:
            try:
                set_data()
                break
            except:
                try:
                    set_data()
                    break
                except:
                  if driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/img') is not None:
                    print('stop')
                    file = pd.DataFrame(data)
                    file.to_csv('shopee.csv', index=False)
                    # create filr json utf-8
                    with open('shopee.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                        
                        

                    driver.quit()
                    break
                  else:
                    pass

    
      
def loop_data():
     i = 0
     while True:
        try:
            i += 1
            driver.get(location + "&page=" + str(i))
            driver.execute_script('document.body.style.zoom="10%"')
            get_data()
 
        except:
            driver.quit()
            break
    

def main():
    try:
      thai_button = driver.find_element('xpath', '/html/body/div[2]/div[1]/div[1]/div/div[3]/div[1]/button')
      thai_button.click()
      driver.execute_script('document.body.style.zoom="10%"')
    except:
       driver.execute_script('document.body.style.zoom="10%"')

    get_data()
    loop_data()
    

  






main()
 
