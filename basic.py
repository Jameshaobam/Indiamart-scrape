"""
created by: @Haobam Jameskumar singh
23/05/2022
"""
from selenium import webdriver as web
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests, time ,pandas as pd

driver  = web.Chrome(service=Service(ChromeDriverManager().install()))

URL="https://dir.indiamart.com/search.mp?ss=vermicompost&prdsrc=1"
driver.get(URL)

driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
#code for automation
supplier_names = []
supplier_addresses = []
page_links = []

def writeCSV():
  """
  Generate csv to store extracted datas
  """
  datas = {
    'Name':supplier_names,
    'Address':supplier_addresses,
    'Link':page_links,
  }
  print("Putting into CSV...")
  df = pd.DataFrame(datas)
  try:
    out_file = "./output/Indiamart_vermi_data.csv"
    df.to_csv(out_file)
    time.sleep(2)
    
  except Exception as e:
    print(str(e))
  finally:
    print(f"File Created! Check the file {out_file}")

def isLinkValid(soup=None):
  if soup is not None and soup.find('a', attrs = {'class':'color6 bo pd_txu'}) is not None:
     return True
  return False


def extractDetailPage(link=None):

    """scrape name and address of the supplier from individual page
    """
    try:
      if link is not None:

        time.sleep(1)
        print("loading>>>")
        html_doc = requests.get(link)
        soup = BeautifulSoup(html_doc.text,'html.parser')
        
        if isLinkValid(soup):
          page_links.append(link)
          supplier_name = soup.find('a', attrs = {'class':'color6 bo pd_txu'}).h2.get_text().strip().upper()
          supplier_names.append(supplier_name)
          div = soup.find('div', attrs = {'class':'cmpN txtC bdr1'})
          supplier_address = div.find('div', attrs = {'class':'fs13 color1 mt5 on addrs pdg10'}).get_text().strip()
          supplier_addresses.append(supplier_address)

        else:
          print("\t Error in finding element from this link: ".upper()+f" {link}")
    except Exception as e:
        print(f"Error in getting datas from single page \n {e.message}")

def main():
  try:
      print("Process started...")
      xpath_link = "//div[@class='prd-list-name flx100']/span/a"
      div = driver.find_elements(By.XPATH,value=xpath_link)
      links = [link.get_attribute('href').strip() for link in div]
      print("Message will be shown once done extracting from all items...")
      for link in links:
        extractDetailPage(link=link)
      
  except Exception as e:
    print(f"Error-> {e.message}")    

  finally:
    print(f"Total datas extracted is {len(supplier_names)}")
    writeCSV()
    #close the browser
    driver.quit()

if __name__ == '__main__':
  main()