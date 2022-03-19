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
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import logging
import time

def web():
 global driver
# Add headless option to make it work without Chrome popup
 op = webdriver.ChromeOptions()
 op.add_argument('--ignore-certificate-errors')
 op.add_argument("--start-maximized")
# Below 8 statements is needed to make the script work at linux
 op.add_argument('--headless')
 op.add_argument('--disable-gpu')
 op.add_argument("--no-sandbox")
 op.add_argument("--disable-dev-shm-usage")
 from pyvirtualdisplay import Display
 display = Display(visible=0, size=(1920, 1080))
 display.start()
 driver = webdriver.Chrome("/usr/bin/chromedriver",options=op)
# Below is for windows
# driver = webdriver.Chrome(options=op)

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

def checkheader(xpath,statement):

  inputElement = driver.find_element_by_id("tab-1")
  driver.execute_script("arguments[0].click();", inputElement)

  WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.XPATH,"//div[contains(text(),'csp')]")))

  org_rows = driver.find_elements_by_xpath("//*[contains(@id,'csfWidgets-tree-leafNode')]")

  q=0
  for element in org_rows:
      
    org_element = element.find_element_by_class_name("node-text")
    q+= 1
    if q==2:
       selectedorg=org_element.text
       
       
       hover = ActionChains(driver).move_to_element(org_element)
       hover.perform()
       time.sleep(1)
       icon= driver.find_element_by_class_name("node-menu")
       icon.click()
       time.sleep(1)
       option= driver.find_element_by_xpath(xpath)
       
       option.click()     
       
       time.sleep(15)
   
       orgname=driver.find_element_by_class_name("parentOrganizationHeaderLayout")
       header=((((orgname.text).split("\n"))[1])[1:])
       statement=statement.ljust(85,".")
       
       if header==selectedorg:
          print(statement,"complied")
       else:
          print(statement,"Not complied!")
       break        

if __name__ == "__main__":

 # Set the log file
 logging.basicConfig(filename='/tmp/whitelabeltest4.log',level=logging.INFO, format='%(asctime)s %(levelname)s  %(message)s')
 logging.info('Started')

 # Parses the /tmp/test4.properties file to get the url and the credentials
 f = open("/tmp/test4.properties","r")
 
 A=f.readlines()
 numberofapps=len(A) // 5


 # Loops to execute the process to all apps
 
 for i in range (0,numberofapps):

  web()

  appname=A[i*5].partition("=")[2].replace('\n', '')
  url=A[i*5+1].partition("=")[2].replace('\n', '')
  username=A[i*5+2].partition("=")[2].replace('\n', '')
  password=A[i*5+3].partition("=")[2].replace('\n', '')
  org=A[i*5+4].partition("=")[2].replace('\n', '')
  logging.info('Credentials parsed for '+appname)

  print()
  print("Application:",appname)
  print("-----------------------------------------------------------------------------------------------")

  
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

  # First get the norm enterpise-nsg table from the inventory tab

  WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.XPATH,"//div[contains(text(),'csp')]")))

  if appname=="NSG-Upgrade":

    checkheader("//li[@id='branchInventory']","Criteria-1 Selected enterprise name matched with the INVENTORY tab header")
    checkheader("//li[@id='branchUpgrade']","Criteria-2 Selected enterprise name matched with the UPGRADE tab header")
    checkheader("//li[@id='branchOperations']","Criteria-3 Selected enterprise name matched with the OPERATIONS tab header")
    

  if appname=="Extended-Config":

    checkheader("//li[@id='borderRouterAlarmsPage']","Criteria-1 Selected enterprise name matched with the UBR ALARMS tab header")
    checkheader("//li[@id='borderRouterAssignmentPage']","Criteria-2 Selected enterprise name matched with the UBR ASSIGNMENT tab header")
    checkheader("//li[@id='borderRouterGroupAssignmentPage']","Criteria-3 Selected enterprise name matched with the UBR GROUP ASSIGNMENT tab header")
    checkheader("//li[@id='nsgGroupManagementPage']","Criteria-4 Selected enterprise name matched with the NSG GROUP MANAGEMENT tab header")
    checkheader("//li[@id='borderRouterPortManagement']","Criteria-5 Selected enterprise name matched with the UBR PORT MANAGEMENT tab header")

  print()

  logging.info(appname + 'checks are done')

  # Logs out
  
  inputElement = driver.find_element_by_xpath("//div[@id='csfWidgets-banner-appBanner-userAccountSummaryButton-userAccount-content']")
  inputElement.click()

  inputElement = driver.find_element_by_xpath("//div[@id='csfWidgets-banner-appBanner-userAccountSummaryButton-logout-content']")
  inputElement.click()

  logging.info('Logged out')

  driver.close()

logging.info('Stopped')
      



