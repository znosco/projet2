import urllib.request
import os
import csv
from bs4 import BeautifulSoup
from requests import get


"""Part1: Get all urls of each page and store them in a list of lists 
   of each category called list_of_liste_of_urlCategory_of_book """
home_url = "http://books.toscrape.com/"

# create the directories for the csv files and the pictures
if not os.path.exists('My_csv_files'):
    os.makedirs('My_csv_files')

if not os.path.exists('pictures'):
    os.makedirs('pictures')

#copy the content of the web page into the page variable
page = get(home_url)
#we 'parse' the content into the soup variable
soup = BeautifulSoup(page.content, 'html.parser')

# the soup_find object allows us to obtain the list of alliteration category
soup_find = soup.find(
    "a", href='catalogue/category/books_1/index.html').next_sibling.next_sibling.contents


# initialization of tables and counters
category_url = []
category_name = []
category_name_with_nomber = []
counter = 0
dico_list ={}

# iteration
for x in soup_find:

    if x == '\n':
        continue
    else:

        y = x.find('a')
        z = "http://books.toscrape.com/"+y['href']
        category_url.append(z)         
        z = z.replace('http://books.toscrape.com/catalogue/category/books/',
                      "").replace('/index.html', "")
        category_name_with_nomber.append(z)
        
        #the number can have one or two digits
        counter += 1
        if counter < 9:
            scissors = 2
        else:
            scissors = 3

        z = z[:(len(z)-scissors)]
        category_name.append(z)

# bloc for user selection
print('\n Do you want to scrapte a single category ?')    
select1 = input("Enter 'y' for yes, or anything to scrape the whole site")  
if select1 == "y":

    for i in range(50):
        y = i + 1
        dico_list.update({y:category_name[i]})

    #check that the input value is an integer in the correct interval
    wrong_number = True
    while wrong_number == True:
        try:
            for i in dico_list:
                print(i,':',dico_list[i])
            select2 = input('\n please enter the number corresponding to the desired category \n')
            int_select2 = int(select2)
            if int_select2<1 or int_select2>50: 
                print('\n Oops!  That was no valid number. Try again... \n')

            else:
                print('\n You have chosen to scrape the category: '+dico_list[int_select2]+'\n')
                min = int_select2-1
                max = int_select2
                category_name = category_name[min:max]
                category_name_with_nomber = category_name_with_nomber[min:max]  
                wrong_number = False            
        except ValueError:
            print("\n Oops!  That was no valid number.  Try again... \n")
        
else:
    print('\n You have chosen to scrape the entire site \n')
#end of block

#build the list : list_of_liste_of_urlCategory_of_book 
list_of_liste_of_urlCategory_of_book = []

for name,name_url in zip(category_name,category_name_with_nomber):

    counter = 1
    l = []
    nomber_page_for_scrape = True
    l_page = []
    end_url = "/index.html"

    # take into account that there can be several pages in a category
    while nomber_page_for_scrape == True:
        
        url = "http://books.toscrape.com/catalogue/category/books/" + name_url + end_url
        print("url in process: \n" + url)
        page = get(url)

        if page.status_code == 200:

            soup = BeautifulSoup(page.content, 'html.parser')
            list_titles = soup.find_all("h3")

            #to empty before going through the loop, otherwise the method appends filled it
            liste_titre1 = []

            for truc in list_titles:
                a = truc.find('a')
                link = a['href']
                liste_titre1.append(link)
       
            for element in liste_titre1:
                element = element.replace(
                    '../../../', 'http://books.toscrape.com/catalogue/')
                l_page.append(element)
            
            test = "http://books.toscrape.com/catalogue/category/" \
                   "books/" + name_url + "/page-" + str(counter+1) + ".html"

            page_test = get(test)

            # the test to find out if there are any pages left
            if page_test.status_code == 200:
                counter += 1
                end_url = "/page-"+str(counter)+".html"
                l = l + l_page
                l_page = []
            else:
                l = l + l_page
                list_of_liste_of_urlCategory_of_book.append(l)
                nomber_page_for_scrape = False

counter = -1


# Part2 : Obtain all searched items and store them

for listo_category in list_of_liste_of_urlCategory_of_book:
    
    counter += 1

    #initialisation
    counter2 = 0
    product_page_url = []
    liste_title = []
    price_including_tax = []
    universal_product_code = []
    price_excluding_tax = []
    number_available = []
    product_description = []
    category = []
    review_rating = []
    image_url = []

    for listo_element in listo_category:

        category.append(category_name[counter])
        url = listo_element
        page = get(url)

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')

            # we find successively the 10 informations of the book
            product_page_url.append(url)
            liste_title.append(soup.find('h1').string)
            box = soup.find_all('tr')

            # use this function because there are 4 items in same place
            def recup_produc_info(keyword):
                for element in box:
                    if keyword in str(element):
                        item_found = element.find('td').string
                        return(item_found)

            price_including_tax.append(recup_produc_info("incl"))
            universal_product_code.append(recup_produc_info("UPC"))
            price_excluding_tax.append(recup_produc_info("excl"))
            number_available.append(recup_produc_info("Availability"))
               
            if 'id="product_description"' in str(soup.find('div', id='product_description')):
                soup_result = soup.find(
                    'div', id='product_description').next_sibling.next_sibling.string

            else:
                soup_result = 'NONE'

            product_description.append(soup_result)
            soup_result = soup.find("p", class_="star-rating")
            link = soup_result['class']
            item_found = link[0]+'='+link[1]
            review_rating.append(item_found)
            soup_result = soup.find('img')
            link = soup_result['src']
            item_found = link.replace('../../', 'http://books.toscrape.com/')
            image_url.append(item_found)
            # we got the 10 informations on the book

            # download and write files pictures in the good directory
            if not os.path.exists('pictures/' + category[0]):
                os.makedirs('pictures/' + category[0])

            # solved files names problems
            def replace_file_name(x):
                annoying_chars = '^*./":?<>'
                for char in annoying_chars:
                    x = x.replace(char, '_')
                return x

            title_ = replace_file_name(liste_title[counter2])
            print("title of the book"+':'+title_)

            urllib.request.urlretrieve(image_url[counter2],
                                       'pictures/' + category[0]+'/'+title_ + '.jpg')
            urllib.request.urlcleanup()

            counter2 += 1

    # write csv files
    header = ['title',
              'price_including_tax', 
              'price_excluding_tax', 
              'number_available', 
              'product_description', 
              'category', 
              'review_rating', 
              'image_url', 
              'product_page_url',
              'universal_ product_code'
              ]

    with open('My_csv_files/' + category[0] + '.csv', "w", encoding='utf-8') as fichier_csv:
        var = csv.writer(fichier_csv, delimiter=',')
        var.writerow(header)
        for x1, x2, x3, x4, x5, x6,x7, x8, x9, x10 in zip(liste_title, 
                                                           price_including_tax, 
                                                           price_excluding_tax, 
                                                           number_available, 
                                                           product_description, 
                                                           category, review_rating, 
                                                           image_url, 
                                                           product_page_url,
                                                           universal_product_code
                                                           ):
            var.writerow([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10])

print('End')
