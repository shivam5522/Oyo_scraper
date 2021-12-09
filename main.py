from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import csv
import time


class Scrape:
    def __init__(self):
        self.driver=webdriver.Chrome()

    def extract(self):
        self.driver.get('https://www.oyorooms.com/')
        time.sleep(2)

        """Enters the given location in the input"""
        self.driver.find_element_by_xpath('//*[@id="autoComplete__home"]').send_keys('Mumbai')

        time.sleep(2)

        """Selects the first option from the dropdown"""
        self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[1]/div[3]/div/div[1]/div/div[1]/div/span/div/div/div[1]/div').click()  

        time.sleep(2)

        """Clicking the Search button"""
        self.driver.find_element_by_xpath('//*[contains(text(),"Search")]').click()

        time.sleep(5)

        """Fetching all the hotels in the current page"""
        data= self.driver.find_elements_by_xpath("//*[@class='hotelCardListing__descriptionWrapper']")
        final_data=[]

        """Traversing all the hotels in the current page"""
        for hotel in data:
            name=hotel.find_element_by_xpath('.//*[@itemprop="name"]').text
            address=hotel.find_element_by_xpath('.//*[@itemprop="address"]').text
            try:
                rating=hotel.find_element_by_xpath('.//*[@itemprop="ratingValue"]').get_attribute('content')
            except:
                rating='No rating found'
            price=hotel.find_element_by_xpath('.//*[@class="listingPrice__finalPrice"]').text

            """Appending the data to a final list to be added to the csv file"""
            final_data.append([name,address,rating,price])
        self.driver.quit()

        return final_data

    def write_to_csv(self,data):
        fields=['Name','Address','Rating','Price']
        
        with open('hotels.csv','a',newline='',encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile) 
        
            csvwriter.writerow(fields) 
        
            csvwriter.writerows(data)


obj=Scrape()
data=obj.extract()
obj.write_to_csv(data)


