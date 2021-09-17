#importation des packages
import csv
from bs4 import BeautifulSoup
from requests import get


# 1) Obtenir tous les url de chaque page et les stocker dans une liste de listes de chaque catégorie


home_url="http://books.toscrape.com/"
page = get(home_url)

soup = BeautifulSoup(page.content,'html.parser')


soup_find=soup.find("a",href='catalogue/category/books_1/index.html').next_sibling.next_sibling.contents


 
category_url=[]
category_name = []
category_name_in_url=[]
counter = 0


for x in soup_find:
   
    if x == '\n':
        continue
    else:
        
        y=x.find('a')
        z="http://books.toscrape.com/"+y['href']
        category_url.append(z)
        z = z.replace('http://books.toscrape.com/catalogue/category/books/',"").replace('/index.html',"")
        category_name_in_url.append(z)
        
        counter += 1
        if counter<9:
            scissors = 2
        else:
            scissors = 3
        
        z = z[:(len(z)-scissors)]
        category_name.append(z)

 

 

list_of_liste_of_urlCategory_of_book=[]        
        
for name , name_url in zip(category_name , category_name_in_url):


    
#url = "http://books.toscrape.com/catalogue/category/books/" +name_url+ "/page-"+str(x)+".html"     

    x=1
    nomber_Page_for_scrape = True
    l=[]
    l_page=[]
    end_url="/index.html"
        
    while nomber_Page_for_scrape == True:



        url = "http://books.toscrape.com/catalogue/category/books/" + name_url + end_url
       
        page = get(url)


        if page.ok:

            soup = BeautifulSoup(page.content,'html.parser')
            liste_titres = soup.find_all("h3")
        
        
            liste_titre1=[] # à vider avant de parcourir la boucle , sinon la méthode append le remplie
            
            for truc in liste_titres:

                a = truc.find('a')
                link = a['href']
                liste_titre1.append(link)
                
            l_page = [element.replace('../../../','http://books.toscrape.com/catalogue/') for element in liste_titre1] 

            

            test = "http://books.toscrape.com/catalogue/category/books/" + name_url + "/page-"+str(x+1)+".html"
            
            page_test = get(test)
            
            
            if page_test.ok:
                x+=1
                end_url = "/page-"+str(x)+".html"
                l = l + l_page
            else:
                l = l + l_page
                list_of_liste_of_urlCategory_of_book.append(l)
                nomber_Page_for_scrape = False
 
  

counter = -1        



for listo_category in list_of_liste_of_urlCategory_of_book:
    
    counter +=1
    
    product_page_url =[]
    liste_title =[]
    price_including_tax =[]
    universal_product_code =[]
    price_excluding_tax  =[]
    number_available  =[]
    product_description  =[]
    category  = []
    review_rating  =[]
    image_url  =[] 
    
       
    for listo_element in listo_category:
    
            
   
        category.append(category_name[counter])
        
        url=listo_element
        print(url)
        page = get(url)
        
        if page.ok:
            soup = BeautifulSoup(page.content,'html.parser')



            product_page_url.append(url)

            liste_title.append(soup.find('h1').string)


            box = soup.find_all('tr')

            def recup_produc_info(mot_cle):

                for element in box:
                    if (mot_cle) in str(element):
                        a = element.find('td').string

                        return(a)



            price_including_tax.append(recup_produc_info("incl"))

            universal_product_code.append(recup_produc_info("UPC"))

            price_excluding_tax.append(recup_produc_info("excl"))

            number_available.append(recup_produc_info("Availability"))

            
            
            if 'id="product_description"' in str(soup.find('div' , id='product_description')):

                a=soup.find('div' , id='product_description').next_sibling.next_sibling.string
            
            else:
                a ='NONE'
            
            
            product_description.append(a)     


            a=soup.find("p",class_= "star-rating")
            link = a['class']
            b=link[0]+'='+link[1]

            review_rating.append(b)


            a=soup.find('img')
            link = a['src']
            b=link.replace('../../','http://books.toscrape.com/')

            image_url.append(b)

            
            
            
            
            
    en_tete = ['title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url','product_page_url',
    'universal_ product_code']

    with open (str(category_name[counter]) + '.csv',"w",encoding ='utf-8') as fichier_csv:
        var = csv.writer(fichier_csv,delimiter=',')
        var.writerow(en_tete)
        for x1,x2,x3,x4,x5,x6,x7,x8,x9,x10 in zip (liste_title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url,product_page_url,
    universal_product_code):
            var.writerow([x1,x2,x3,x4,x5,x6,x7,x8,x9,x10])

