import bs4 as bs
import urllib.request
import csv

LINK_PAGE = 'https://tiki.vn/nha-sach-tiki/c8322'

# crawl tiki product data by input @product_page using beautifulsoup4
# return @record
def crawl_data_to_record(product_page):
    sauce = urllib.request.urlopen(product_page).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    record = []

    # Get product_name, sub_category and category
    ul = soup.find('ul', class_='breadcrumb')
    span = ul.find_all('span')
    product_name = span[-1].text
    if len(span) > 2:
        sub_category = span[-2].text
        category = span[-3].text
    else:
        sub_category = 'None'
        category = 'None'

    record.append(category)
    record.append(sub_category)
    
    # Get product_id
    product_id =  soup.find('input', {'id': 'product_id'}).get('value')
    record.append(product_id)
    
    record.append(product_name)

    # Get price
    price =  soup.find('input', {'id': 'product_price'}).get('value')
    record.append(price)

    # Get ratingValue
    ratingValue = soup.find("meta",  itemprop="ratingValue")
    record.append(ratingValue["content"])

    # Get ratingCount
    if ratingValue["content"] == '0':
        record.append('0')
    else:
        ratingCount = soup.find("meta",  itemprop="ratingCount")
        record.append(ratingCount["content"])

    # Get other viewed products (id)
    other_items = ''
    items = soup.find('div', class_='list style-list')
    if items != None:
        item_descendants = items.descendants
        for item in item_descendants:
            if item.name == 'div' and item.get('class', '') == ['item']:
                other_items += item.get('data-id') + ';'
        record.append(other_items)
    else:
        record.append('None')

    return record

# get product pages
def get_product_pages(LINK_PAGE):
    current_page = 1
    PAGE_LIMIT = 2
    product_pages = []
    
    while current_page < PAGE_LIMIT:
        print('Getting product pages in page ' + str(current_page) + '...')
        sauce = urllib.request.urlopen(LINK_PAGE + '?page=' + str(current_page)).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        product_box_list = soup.find('div', class_='product-box-list')
        for a in product_box_list.find_all('a'):
            product_pages.append(a.get('href'))
        current_page += 1
    print('FINISH GETTING!')
    print('Already get ' + str(len(product_pages)) + ' product pages')
    return product_pages

def main():
    
    # Write csv file
    with open('./tiki_products.csv', 'w', encoding='utf-8-sig') as output:
        writer = csv.writer(output)
        writer.writerow(["Category","Sub Category","Product_id","Product_name","Price","Rating_value","Rating_count","Frequently_bought_together"])

        product_pages = get_product_pages(LINK_PAGE)
        print('Starting to crawl product info on each page...')
        for i in range(len(product_pages)):
            print("Crawling page {}: {}".format(i + 1, product_pages[i]))
            record = crawl_data_to_record(product_pages[i])
            writer.writerow(record)
        print('DONE! All data is exported to csv file.')

main()

    









