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
    sub_category = span[-2].text
    category = span[-3].text

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

def main():
    # Write csv file
    with open('./tiki_products.csv', 'w', encoding='utf-8-sig') as output:
        writer = csv.writer(output)
        writer.writerow(["Category","Sub Category","Product_id","Product_name","Price","Rating_value","Rating_count","Also_viewed_items"])

        page_number = 1
        PAGE_LIMIT = 2
        
        while page_number < PAGE_LIMIT:
            sauce = urllib.request.urlopen(LINK_PAGE + '?page=' + str(page_number)).read()
            soup = bs.BeautifulSoup(sauce, 'lxml')
            
            product_box_list = soup.find('div', class_='product-box-list')
            for a in product_box_list.find_all('a'):
                record = crawl_data_to_record(a.get('href'))
                writer.writerow(record)
            page_number += 1

main()
    









