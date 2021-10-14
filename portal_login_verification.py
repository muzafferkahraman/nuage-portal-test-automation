##################################################################
#
# JIRA2 NCMSDWANT-109
# Develop UI QA test automation for framework apps
# Subtask-1 v1.1
#
# by Muzaffer Kahraman Nokia IPO NME June 2021
#
##################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.action_chains import ActionChains
import logging 

def web():
 global driver
# Add headless option to make it work without Chrome popup
 op = webdriver.ChromeOptions()
# op.add_argument('--headless')
 op.add_argument('--ignore-certificate-errors')
# Below 7 statements is needed to make the script work at linux
 op.add_argument('--disable-gpu')
 op.add_argument("--no-sandbox") 
 op.add_argument("--disable-dev-shm-usage")
 from pyvirtualdisplay import Display
 display = Display(visible=0, size=(800, 800))  
 display.start()
 driver = webdriver.Chrome("/usr/bin/chromedriver",options=op)
# Below is for windows
# driver = webdriver.Chrome(options=op)

if __name__ == "__main__":


 # Set the log file
 logging.basicConfig(filename='/tmp/whitelabeltest1.log',level=logging.INFO, format='%(asctime)s %(levelname)s  %(message)s')
 logging.info('Started')

 # Parses the /tmp/test.properties file to get the url and the credentials
 try:
  f = open("/tmp/test.properties","r")
 except FileNotFoundError:
  print("There is no test.properties file found under /temp")

 A=f.readlines()
 numberofapps=len(A) // 5


 # Loops to execute the process to all apps
 
 for i in range (0,numberofapps):

  web()
  
  appname=A[i*5].partition("=")[2].replace('\n', '')
  if appname=="Portal":
      continue
  url=A[i*5+1].partition("=")[2].replace('\n', '')
  username=A[i*5+2].partition("=")[2].replace('\n', '')
  password=A[i*5+3].partition("=")[2].replace('\n', '')
  org=A[i*5+4].partition("=")[2].replace('\n', '')
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
  
  inputElement = driver.find_element_by_xpath("//button[@id='tab-1']")
  s=inputElement.text
  statement="Criteria-1 (Overview tab page is opened after login)".ljust(85,".")
  if s=="OVERVIEW":
    print(statement,"complied")
  else:
    print(statement,"Not complied!")
     
  WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.XPATH,"//label[normalize-space()='Count:']")))

  # Checks if the Parent Org shows the correct info

  inputElement = driver.find_elements_by_class_name("node-text")
  s=inputElement[0].text
  statement="Criteria-2 (Parent organization shows correct info)".ljust(85,".")
  if s==org:
    print(statement,"complied")
  else:
    print(statement,"Not complied!")

  # Checks if the Org and Username parameters are the same as input credentials

  inputElement = driver.find_element_by_xpath("//header[@role='presentation']")
  s=inputElement.text
  Arr=s.split("\n")

  s=Arr[3]
  statement="Criteria-3 (Username shows correctly in the top right of page)".ljust(85,".")
  if username=="Admin":
      username="admin"
  if s==username:  
    print(statement,"complied")
  else:
    print(statement,"Not complied!")

  s=Arr[2]
  statement="Criteria-4 (Org name shows correctly in the top right of page)".ljust(85,".")
  if s==org: 
    print(statement,"complied")
  else:
    print(statement,"Not complied!")
    
  # Takes screnshot with the same name as the app under /tmp for evidence 

  logging.info('End of verification checks')
  
  driver.save_screenshot("/tmp/"+appname+".png")
  print("Screenshot taken and copied as /temp/"+appname+".png")

  logging.info('Screenshot is taken as /tmp/'+appname+'.png')

  # Logs out
  
  inputElement = driver.find_element_by_xpath("//div[@id='csfWidgets-banner-appBanner-userAccountSummaryButton-userAccount-content']")
  inputElement.click()

  inputElement = driver.find_element_by_xpath("//div[@id='csfWidgets-banner-appBanner-userAccountSummaryButton-logout-content']")
  inputElement.click()

  logging.info('Logged out')

  driver.close()
 
 logging.info('Stopped')
 
 





