# version 1.0
# written by Huy Le

import bs4 as bs
import urllib.request
import csv
import json

PAGES = ['https://www.lazada.vn/phu-kien-may-vi-tinh']
##PAGES = ['https://www.lazada.vn/phu-kien-dien-thoai-may-tinh-bang','https://www.lazada.vn/thiet-bi-mang','https://www.lazada.vn/linh-kien-may-tinh','https://www.lazada.vn/phu-kien-may-anh-may-quay-phim','https://www.lazada.vn/thiet-bi-deo-cong-nghe','https://www.lazada.vn/thiet-bi-luu-tru','https://www.lazada.vn/thiet-bi-choi-game','https://www.lazada.vn/may-in-phu-kien','https://www.lazada.vn/phu-kien-may-tinh-bang','https://www.lazada.vn/tivi','https://www.lazada.vn/phu-kien-cho-tv','https://www.lazada.vn/he-thong-giai-tri-cho-tai-gia','https://www.lazada.vn/gia-dung-nha-bep','https://www.lazada.vn/do-gia-dung-nha-bep','https://www.lazada.vn/quat-may-nong-lanh','https://www.lazada.vn/choi-cay-lau-san-nha','https://www.lazada.vn/thiet-bi-cham-soc-quan-ao','https://www.lazada.vn/cham-soc-ca-nhan','https://www.lazada.vn/thiet-bi-do-gia-dung','https://www.lazada.vn/trang-diem','https://www.lazada.vn/san-pham-cham-soc-toc','https://www.lazada.vn/dung-cu-cham-soc-sac-dep','https://www.lazada.vn/nuoc-hoa','https://www.lazada.vn/cham-soc-cho-nam-gioi','https://www.lazada.vn/san-pham-tam-cham-soc-co-the','https://www.lazada.vn/thuc-pham-bo-sung','https://www.lazada.vn/thiet-bi-y-te','https://www.lazada.vn/cham-soc-ca-nhan','https://www.lazada.vn/cham-soc-tre-so-sinh-tre-nho','https://www.lazada.vn/do-dung-bu-sua-an-dam','https://www.lazada.vn/quan-ao-phu-kien-cho-be','https://www.lazada.vn/ta-dung-cu-ve-sinh','https://www.lazada.vn/dung-cu-cham-soc-co-the-tre-em','https://www.lazada.vn/xe-ghe-em-be','https://www.lazada.vn/do-choi-cho-tre-so-sinh-chap-chung','https://www.lazada.vn/do-choi-bo-suu-tap-nhan-vat','https://www.lazada.vn/the-thao-tro-choi-ngoai-troi','https://www.lazada.vn/do-an-sang','https://www.lazada.vn/do-hop-do-kho-thuc-pham-dong-goi','https://www.lazada.vn/cac-loai-do-uong','https://www.lazada.vn/thuc-uong-co-con','https://www.lazada.vn/giat-giu-cham-soc-nha-cua','https://www.lazada.vn/keo-socola','https://www.lazada.vn/nau-an-lam-banh','https://www.lazada.vn/phu-kien-hut-thuoc','https://www.lazada.vn/snack-do-an-vat','https://www.lazada.vn/do-dung-bep-phong-an','https://www.lazada.vn/cac-loai-den','https://www.lazada.vn/do-dung-phong-ngu-gia-dinh','https://www.lazada.vn/do-dung-phu-kien-phong-tam','https://www.lazada.vn/san-pham-noi-that','https://www.lazada.vn/san-pham-trang-tri-nha-cua','https://www.lazada.vn/tan-trang-nha-cua','https://www.lazada.vn/van-phong-pham-va-nghe-thu-cong','https://www.lazada.vn/sach','https://www.lazada.vn/nhac-cu-moi','https://www.lazada.vn/trang-phuc-nu','https://www.lazada.vn/giay-nu-thoi-trang','https://www.lazada.vn/tui-cho-nu','https://www.lazada.vn/phu-kien-cho-nu','https://www.lazada.vn/do-ngu-noi-y','https://www.lazada.vn/trang-phuc-cua-be-gai','https://www.lazada.vn/thoi-trang-giay-danh-cho-be-gai','https://www.lazada.vn/phu-kien-danh-cho-be-gai','https://www.lazada.vn/tui-danh-cho-tre-em','https://www.lazada.vn/trang-phuc-nam','https://www.lazada.vn/do-lot-nam','https://www.lazada.vn/giay-nam-thoi-trang','https://www.lazada.vn/tui-nam','https://www.lazada.vn/phu-kien-thoi-trang-nam','https://www.lazada.vn/trang-phuc-cua-be-trai','https://www.lazada.vn/thoi-trang-giay-cho-be-trai','https://www.lazada.vn/phu-kien-danh-cho-be-trai','https://www.lazada.vn/tui-danh-cho-tre-em','https://www.lazada.vn/dong-ho-nu-thoi-trang','https://www.lazada.vn/dong-ho-nam-gioi','https://www.lazada.vn/kinh-mat','https://www.lazada.vn/kinh-deo-mat','https://www.lazada.vn/san-pham-cham-soc-mat','https://www.lazada.vn/trang-suc-nu','https://www.lazada.vn/trang-suc-nam','https://www.lazada.vn/kinh-phu-kien','https://www.lazada.vn/dung-cu-de-tap-the-hinh','https://www.lazada.vn/hoat-dong-da-ngoai','https://www.lazada.vn/do-the-thao-nam','https://www.lazada.vn/do-the-thao-nu','https://www.lazada.vn/cac-mon-the-thao-vot','https://www.lazada.vn/cac-mon-tap-luyen-doi-khang','https://www.lazada.vn/dam-boc-vo-thuat-danh-mma','https://www.lazada.vn/cac-mon-the-thao-duoi-nuoc','https://www.lazada.vn/phu-kien-the-thao','https://www.lazada.vn/xe-may','https://www.lazada.vn/thiet-bi-phu-kien-o-to-xe-may','https://www.lazada.vn/dich-vu-lap-dat-xe','https://www.lazada.vn/do-bao-ho-mo-to','https://www.lazada.vn/dau-nhot-mo-to','https://www.lazada.vn/bo-phan-mo-to-phu-tung-thay-the-cho-mo-to','https://www.lazada.vn/cham-soc-ngoai-xe','https://www.lazada.vn/dau-nhot-o-to-xe-may','https://www.lazada.vn/phu-kien-ngoai-o-to-xe-may','https://www.lazada.vn/lap-dat-lop-mam-xe']
def get_data_from(item):
    
    product = []

    category = item['categories'][0]
    product.append(category)
    
    sub_category = item['categories'][1]
    product.append(sub_category)
    
    product_id = item['itemId']
##    print(product_id)
    product.append(product_id)
    
    product_name = item['name']
##    print(product_name)
    product.append(product_name)

    
    product_price = item['price']
##    print(product_price)
    product.append(product_price)

    rating_value = item['ratingScore']
##    print(rating_value)
    product.append(rating_value)

    rating_count = item['review']
##    print(rating_count)
    product.append(rating_count)
    
    return product
    

def main():

    
##    print('key:',data.keys())
    
##    print('Name:',data['mods']['listItems'][0]['name'])
    for page in PAGES:
        # Write csv file
        print('Getting page', page)
        with open('./' + page[22:] + '.csv', 'w', newline='', encoding='utf-8-sig') as output:
            writer = csv.writer(output)
    ##        ,,"Frequently_bought_together"
            writer.writerow(["Category","Sub Category","Product_id","Product_name","Price","Rating_value","Rating_count"])

            CURRENT_PAGE = 1
            LIMIT_PAGE = 103
            while CURRENT_PAGE < LIMIT_PAGE:
                sauce = urllib.request.urlopen(page + '?page=' + str(CURRENT_PAGE)).read()
                soup = bs.BeautifulSoup(sauce, 'lxml')
                script = soup.find_all("script")[2].text[16:]
    ##            print(script)
    ##            CURRENT_PAGE += 50
                try:
                    data = json.loads(script)
                    print('GETTING PAGE ' + str(CURRENT_PAGE))
                    products = data['mods']['listItems']
                    for item in products:
                        product = get_data_from(item)
                        writer.writerow(product)
                    CURRENT_PAGE += 1
                except Exception as e:
                    print(e)
                    CURRENT_PAGE += LIMIT_PAGE
                    pass
            
            

main()

    









