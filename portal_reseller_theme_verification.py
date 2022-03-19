##################################################################
#
# Develop UI QA test automation for framework apps
#
# by Muzaffer Kahraman
#
##################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging



def web():
 global driver
# Add headless option to make it work without Chrome popup
 op = webdriver.ChromeOptions()
 op.add_argument('--headless')
 op.add_argument('--ignore-certificate-errors')
# Below 6 statements is needed to make the script work at linux
 op.add_argument('--disable-gpu')
 op.add_argument("--no-sandbox") 
 op.add_argument("--disable-dev-shm-usage")
 from pyvirtualdisplay import Display
 display = Display(visible=0, size=(800, 800))  
 display.start()
 driver = webdriver.Chrome("/usr/bin/chromedriver",options=op)

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) 

if __name__ == "__main__":

 web()

 # Set the log file
 logging.basicConfig(filename='/tmp/whitelabeltest6.log',level=logging.INFO, format='%(asctime)s %(levelname)s  %(message)s')
 logging.info('Started')

 # Parses the /tmp/test6.properties file to get the url and the credentials
 f = open("/tmp/test6.properties","r")

 Configlines=f.readlines()
 numberofapps=len(Configlines) // 5
 
 appname=Configlines[0].partition("=")[2].replace('\n', '')
 url=Configlines[1].partition("=")[2].replace('\n', '')
 username=Configlines[2].partition("=")[2].replace('\n', '')
 password=Configlines[3].partition("=")[2].replace('\n', '')
 org=Configlines[4].partition("=")[2].replace('\n', '')
 logging.info('Credentials parsed for '+appname)
 
 # Connects to the page
 driver.get(url)

 # Waits until the page title 
 WebDriverWait(driver,5060).until(ec.element_to_be_clickable((By.XPATH,"//input[@name='username']")))                                                                 

 # Types the credentials
 inputElement = driver.find_element_by_xpath("//input[@name='username']")
 inputElement.send_keys(username)

 inputElement = driver.find_element_by_xpath("//input[@name='password']")
 inputElement.send_keys(password)

 inputElement = driver.find_element_by_xpath("//input[@name='orgName']")
 inputElement.send_keys(org)

 # Waits for the SIGN IN button be activated
 WebDriverWait(driver,60).until(ec.element_to_be_clickable((By.XPATH,"//span[@class='MuiButton-label-206']")))

 # Clicks an the SIGN IN button
 submit= driver.find_element_by_xpath("//button[@type='submit']")
 submit.click()

 # Waits for the new page
 WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.XPATH,"//span[normalize-space()='Subscribers']")))

 rgb =driver.find_element_by_class_name("MuiAppBar-colorPrimary").value_of_css_property('background-color')
 
 img =driver.find_element_by_xpath("//div[@class='MuiToolbar-root MuiToolbar-regular']//div//img").get_attribute("src")

 time.sleep(5)
 page=driver.page_source

 j=page.index("ag-center-cols-container")
 page=page[j:j+15000]

 A=list(find_all(page,'sc-fzXfLS bZKWDs'))

 Subscribers=[]

 for i in A:
     s=page[i+18:i+150]
     if s.find("parentName") > 0:
       j=s.find("tabindex")
       Subscribers.append(s[0:j-36])
 logging.info('Reference Data Collected from the Portal')

 inputElement = driver.find_element_by_xpath("//span[normalize-space()='admin']")
 inputElement.click()

 WebDriverWait(driver,5060).until(ec.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Sign Out']")))

 inputElement = driver.find_element_by_xpath("//span[normalize-space()='Sign Out']")
 inputElement.click()

 logging.info('Logged out')

 driver.close()

 for i in range (1,numberofapps):

  web()
 
  appname=Configlines[i*5].partition("=")[2].replace('\n', '')
  url=Configlines[i*5+1].partition("=")[2].replace('\n', '')
  username=Configlines[i*5+2].partition("=")[2].replace('\n', '')
  password=Configlines[i*5+3].partition("=")[2].replace('\n', '')
  org=Configlines[i*5+4].partition("=")[2].replace('\n', '')
  logging.info('Credentials parsed for '+appname)

  # Connects to the page
  driver.get(url)
  logging.info('URL '+url+'requested')
  # Waits until the page title 
  WebDriverWait(driver,5060).until(ec.element_to_be_clickable((By.XPATH,"//input[@name='username']")))
                                                                 
  # Types the credentials
  inputElement = driver.find_element_by_xpath("//input[@name='username']")
  inputElement.send_keys(username)

  inputElement = driver.find_element_by_xpath("//input[@name='password']")
  inputElement.send_keys(password)

  inputElement = driver.find_element_by_xpath("//input[@name='orgName']")
  inputElement.send_keys(org)
 
  # Waits for the SIGN IN button be activated
  WebDriverWait(driver,60).until(ec.element_to_be_clickable((By.XPATH,"//span[@class='MuiButton-label-206']")))

  # Clicks an the SIGN IN button
  inputElement = driver.find_element_by_xpath("//button[@type='submit']")
  inputElement.click()
 
  # Waits for the new page
  WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.XPATH,"//h1[normalize-space()='SD-WAN']")))
 
  logging.info('Logged in')

  print("Application:",appname)
  print("------------------------------------------------------------------------------------------")                     

  # Checks if the OVERVIEW TAB is visible

  logging.info('Verification checks started')

  # rgb =driver.find_element_by_class_name("MuiAppBar-colorPrimary").value_of_css_property('background-color')
  rgbnew =driver.find_element_by_xpath("//header[@role='presentation']").value_of_css_property('background-color')
  if rgb==rgbnew:
    statement="Criteria-1 (Colour scheme is applied and matches what is configured in portal)".ljust(80,".")
    print(statement,"complied")
  else:
    print(statement,"Not complied!")
      

  # img =driver.find_element_by_xpath("//div[@class='MuiToolbar-root MuiToolbar-regular']//div//img").get_attribute("src")
  imgnew =driver.find_element_by_class_name("app-banner__logo__img--custom-logo").get_attribute("src")
  if rgb==rgbnew:
    statement="Criteria-2 (Custom logos are applied just the same as portal)".ljust(80,".")
    print(statement,"complied")
  else:
    print(statement,"Not complied!")

  time.sleep(5)
  page=driver.page_source

  j=page.index("node-text")
  page=page[j:j+5000]

  A=list(find_all(page,'node-text'))

  Newsubscribers=[]

  for i in A:
     s=page[i+11:i+30]
     j=s.find("</div>")
     Newsubscribers.append(s[0:j])
     
  if (Newsubscribers[0]==org) and (driver.find_element_by_xpath("//div[contains(text(),'Overview')]").is_displayed()):
    statement="Criteria-3 (The reseller with custom branding can be successfully loaded)".ljust(80,".")
    print(statement,"complied")
  else:
    print(statement,"Not complied!")
  
  Newsubscribers.pop(0)
  
  Set1=set(Subscribers)
  Set2=set(Newsubscribers)
  
  if Set1==Set2:
    statement="Criteria-4 (Subscribers at the portal and the application are identical)".ljust(80,".")
    print(statement,"complied")
  else:
    print(statement,"Not complied!")  

  driver.save_screenshot("/tmp/test6-"+appname+".png")
  print("Screenshot taken and copied as /tmp/test6-"+appname+".png")

  logging.info('Screenshot is taken as /tmp/test6-'+appname+'.png')
  print()

  inputElement = driver.find_element_by_xpath("//div[@id='csfWidgets-banner-appBanner-userAccountSummaryButton-userAccount-content']")
  inputElement.click()

  inputElement = driver.find_element_by_xpath("//div[@id='csfWidgets-banner-appBanner-userAccountSummaryButton-logout-content']")
  inputElement.click()

  logging.info('Logged out')
  
  driver.close()

 logging.info('Stopped')  

















