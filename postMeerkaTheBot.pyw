from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from PIL import Image
import time
import schedule
import os.path


###################################################
## drop file system : florentbr/#wd-drop-file.py ##
###################################################

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

def photoSelect(driver):
    flag = True
    while flag:
        driver.get("https://tr.pinterest.com")
        time.sleep(3)

        resimler = driver.find_elements(By.XPATH, "//div[@class='XiG zI7 iyn Hsu']/img[@srcset]")
        time.sleep(2)

        linkler = []
        resim = resimler[0]
        a,b,c,d = resim.get_attribute('srcset').split(',')
        linkler.append(d[:-3])
        time.sleep(2)

        urlretrieve(linkler[0], f"resim0.png")
        time.sleep(3)

        # photo checking
        image1= Image.open(r"C:\Users\gokli\Desktop\jup\resim0.png")

        width, height= image1.size

        if (width >= 1000 and height >=1000):
            flag = False
            
            driver.find_element(By.XPATH, "//div[@class='XiG zI7 iyn Hsu']/img[@srcset]").click()
            time.sleep(2)

            currentURL = "Source Pin Num: "+driver.current_url.split("/")[-2]
            time.sleep(2)
            return(currentURL)
    
def hastager(str2):
    hastag = " "
    if "May be" in str2:
        list = str2.split("May be an image of")
        str2 = list[-1]
        list2 = str2.split()
        for i in list2:
            if "," in i:
                hastag = hastag + "#" + i[:-1]+" "
            elif "." == i[-1]:
                hastag = hastag + "#" + i[:-1]
            elif i == "and":
                pass
            else:
                hastag = hastag + "#" + i + " "
        return(hastag)


def postMeerkatTheBot():
    options = Options()
    options.add_argument(r"--user-data-dir=C:\Users\gokli\AppData\Local\Google\Chrome\User Data")
    options.add_argument(r'--profile-directory=pinbot')
    options.add_argument('--headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    time.sleep(3)

    currentURL = photoSelect(driver)
    
    driver.get("https://www.mentalfloss.com/amazingfactgenerator")
    time.sleep(5)
    facts = "#fact "+driver.find_element(By.XPATH, "//p[@class='_qsor55']").text+"\n\n"+currentURL

    driver.get("https://www.instagram.com/?hl=tr")
    time.sleep(5)
    
    postButton = driver.find_elements(By.XPATH, "//div[@class='_acub']")
    postButton[0].click()
    time.sleep(2)

    dropzone = driver.find_elements(By.XPATH, "//div[@class='rq0escxv l9j0dhe7 du4w35lb']")
    dropzone[0].drop_files(r"C:\Users\gokli\Desktop\jup\resim0.png")
    time.sleep(2)
    
    postButton3 = driver.find_element(By.XPATH, "//div[@class='_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9- _abaa']").click()
    time.sleep(2)

    postButton4 = driver.find_element(By.XPATH, "//div[@class='_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9- _abaa']").click()
    time.sleep(2)
    
    postButton5 = driver.find_element(By.XPATH, "//div[@class='_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9- _abaa']").click()
    time.sleep(3)
    
    driver.get("https://www.instagram.com/meerkathebot/")
    time.sleep(2)

    hastag = driver.find_element(By.XPATH, "//img[@class='_aagt']").get_attribute('alt')
    hastag = hastager(hastag)
    postDesc = ".\n" + facts + "\n\n" + hastag
    
    driver.find_element(By.XPATH, "//div[@class='_aagu']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='_aasm']").click()
    time.sleep(2) 
    driver.find_element(By.XPATH, "//button[@class='_a9-- _a9_1']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//textarea[@class='_ablz _aaeg']").click()

    
    time.sleep(2)
    driver.find_element(By.XPATH, "//textarea[@class='_ablz _aaeg focus-visible']").send_keys(postDesc)
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='_ac7b _ac7d']").click()   
    time.sleep(5)
    
    driver.close()
    
postMeerkatTheBot() 