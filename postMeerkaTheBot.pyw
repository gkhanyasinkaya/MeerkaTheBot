from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from urllib.request import urlretrieve
from PIL import Image
import time
import schedule
import os.path
import re

## Getting Ready Webdriver ##

options = Options()
options.add_argument(r"--user-data-dir=C:\Users\gokli\AppData\Local\Google\Chrome\User Data")
options.add_argument(r'--profile-directory=pinbot')
#options.add_argument('--headless')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
time.sleep(1)

## Drop File System by: florentbr/#wd-drop-file.py ##


JS_DROP_FILES = "var k=arguments,d=k[0],g=k[1],c=k[2],m=d.ownerDocument||document;for(var e=0;;){var f=d.getBoundingClientRect(),b=f.left+(g||(f.width/2)),a=f.top+(c||(f.height/2)),h=m.elementFromPoint(b,a);if(h&&d.contains(h)){break}if(++e>1){var j=new Error('Element not interactable');j.code=15;throw j}d.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var l=m.createElement('INPUT');l.setAttribute('type','file');l.setAttribute('multiple','');l.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');l.onchange=function(q){l.parentElement.removeChild(l);q.stopPropagation();var r={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:l.files,setData:function u(){},getData:function o(){},clearData:function s(){},setDragImage:function i(){}};if(window.DataTransferItemList){r.items=Object.setPrototypeOf(Array.prototype.map.call(l.files,function(x){return{constructor:DataTransferItem,kind:'file',type:x.type,getAsFile:function v(){return x},getAsString:function y(A){var z=new FileReader();z.onload=function(B){A(B.target.result)};z.readAsText(x)},webkitGetAsEntry:function w(){return{constructor:FileSystemFileEntry,name:x.name,fullPath:'/'+x.name,isFile:true,isDirectory:false,file:function z(A){A(x)}}}}}),{constructor:DataTransferItemList,add:function t(){},clear:function p(){},remove:function n(){}})}['dragenter','dragover','drop'].forEach(function(v){var w=m.createEvent('DragEvent');w.initMouseEvent(v,true,true,m.defaultView,0,0,0,b,a,false,false,false,false,0,null);Object.setPrototypeOf(w,null);w.dataTransfer=r;Object.setPrototypeOf(w,DragEvent.prototype);h.dispatchEvent(w)})};m.documentElement.appendChild(l);l.getBoundingClientRect();return l"

def drop_files(element, files, offsetX=0, offsetY=0):
    driver = element.parent
    isLocal = not driver._is_remote or '127.0.0.1' in driver.command_executor._url
    paths = []
    
    # ensure files are present, and upload to the remote server if session is remote
    for file in (files if isinstance(files, type(list)) else [files]) :
        if not os.path.isfile(file) :
            raise FileNotFoundError(file)
        paths.append(file if isLocal else element._upload(file))
    
    value = '\n'.join(paths)
    elm_input = driver.execute_script(JS_DROP_FILES, element, offsetX, offsetY)
    elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})

WebElement.drop_files = drop_files

## Pinterest Photo Select ##

def photoSelect(driver):
    flag = True
    while flag:
        
        time.sleep(2)
        driver.get("https://tr.pinterest.com")


        resimler = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='XiG zI7 iyn Hsu']/img[@srcset]")))


        linkler = []
        a,b,c,d = resimler.get_attribute('srcset').split(',')
        linkler.append(d[:-3])
        urlretrieve(linkler[0], f"resim0.png")
        time.sleep(2)

        # photo checking
        image1= Image.open(r"C:\Users\gokli\Desktop\jup\resim0.png")

        width, height= image1.size
        
        if (width >= 1000 and height >= 800)or(width >= 800 and height >=1000):
            flag = False
            pinNum = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-test-id='pin']"))).get_attribute('data-test-pin-id')
            currentURL = "Source Pin Num: " + pinNum
            return(currentURL)

stop_words = set(stopwords.words('english'))

def parserNormal(text):
  text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
  words = text.split()
  lemmed = [WordNetLemmatizer().lemmatize(w) for w in words]
  lemmed = [w for w in lemmed if not w in stop_words]
  firstList = []
  for i in lemmed:
    firstList.append(i)
  return firstList

def hastagMaker(aList):
    str = ""
    for i in aList:
        str = str+"#"+i+" "
    return(str)

def postMeerkatTheBot(driver):
    
    ######################################### Getting a fact #########################################
    time.sleep(0.5)
    driver.get("https://www.mentalfloss.com/amazingfactgenerator")
    
    a = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[@class='_qsor55']"))).text
    facts = "#fact "+ a +"\n\n"
    
    currentURL = photoSelect(driver)
    facts = facts + currentURL
    
    ######################################### Posting Image #########################################
    
    driver.get("https://www.instagram.com/?hl=tr")

    # btn1 = 
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_acub']"))).click()
    
    dropzone = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='rq0escxv l9j0dhe7 du4w35lb']")))
    dropzone.drop_files(r"C:\Users\gokli\Desktop\jup\resim0.png")
    
    for _ in range(3):
        time.sleep(0.5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9- _abaa']/button"))).click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[@class='_aacl _aacr _aact _aacx _aad6 _aadb']")))
    
    ######################################### Editing Image #########################################
    
    #time.sleep(5)
    driver.get("https://www.instagram.com/meerkathebot/")
    
    alt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[@class='_aagt']"))).get_attribute('alt')
    hastag = hastagMaker(parserNormal(alt))
    
    postDesc = ".\n" + facts + " \n\n" + hastag
    
    for xpath in ["//div[@class='_aagu']","//div[@class='_aasm']","//div[@class='_a9-z']/button[@class='_a9-- _a9_1']","//textarea[@class='_ablz _aaeg']"]:
        btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath ))).click()
    
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//textarea[@class='_ablz _aaeg focus-visible']"))).send_keys(postDesc)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_ac7b _ac7d']"))).click()
    
    time.sleep(2)
    
    driver.close()
    
postMeerkatTheBot(driver)