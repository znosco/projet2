#importation des packages
import csv
from bs4 import BeautifulSoup
from requests import get


#copie le contenu de la page web dans la variable page et on 'parse' le contenu dans la variable soup

x=1
nombre_Page_a_scrape = True
l=[]
liste_titre1=[]
while nombre_Page_a_scrape == True:
    url="http://books.toscrape.com/catalogue/category/books/food-and-drink_33/page-"+str(x)+".html"
    page = get(url)
    if page.ok:
        soup = BeautifulSoup(page.content,'html.parser')
        
        liste_titres=soup.find_all("h3")
       
      
        
        for truc in liste_titres:
           
            a = truc.find('a')
            link = a['href']
            liste_titre1.append(link)
        
        l = [element.replace('../../../','http://books.toscrape.com/catalogue/') for element in liste_titre1] 
        
        x+=1
    
    else:
        nombre_Page_a_scrape = False


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
        
    
for i in range(len(l)):
    
    url=l[i]
    page = get(url)
    if page.ok:
        soup = BeautifulSoup(page.content,'html.parser')
        

        



        product_page_url.append(url)
        liste_title.append(soup.find('h1').string)
        

        category.append('Food and Drink')
        
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
       

        a=soup.find('div' , id='product_description').next_sibling.next_sibling.string
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

with open ('Food_and_Drink.csv',"w") as fichier_csv:
    var = csv.writer(fichier_csv,delimiter=',')
    var.writerow(en_tete)
    for x1,x2,x3,x4,x5,x6,x7,x8,x9,x10 in zip (liste_title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url,product_page_url,
universal_product_code):
        var.writerow([x1,x2,x3,x4,x5,x6,x7,x8,x9,x10])
    

        

        
        


  
    
    
    
    
    