import requests
import pandas as pd

# Define the API URLs
api_urls = [
    "https://fptshop.com.vn/apiFPTShop/Product/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Fmay-say-quan-ao&s=842df55283db001e5111732116ed1942670bdf525f627e02d4f43716812c5c58",
    "https://fptshop.com.vn/apiFPTShop/Product/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Fmay-giat&s=e93eac6a30a7175ec072d5e070159c6416f18b15b5c3477d885991ec408b6e88",
    "https://fptshop.com.vn/apiFPTShop/Product/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Ftu-lanh&s=161e0c694ab71b863e6da319402573d3862ce9648d495dd72bd228c6395acb02",
    "https://fptshop.com.vn/apiFPTShop/Product/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Fmay-lanh-dieu-hoa%3Fsort%3Dban-chay-nhat%26trang%3D100%26pagetype%3D1&s=9a048e37eb40c57ed19dfa607d2e65a254a97a731495f292196d5f12f65b4c1d",
    "https://fptshop.com.vn/apiFPTShop/Product/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Ftivi%3Fsort%3Dban-chay-nhat%26trang%3D100%26pagetype%3D1&s=40e46f6cd75e4b3ff25cdea90b761167be9b96815a4e39ba98069a79da8cafb0",
    "https://fptshop.com.vn/apiFPTShop/Product/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Fsmartwatch%3Fsort%3Dban-chay-nhat%26trang%3D100%26pagetype%3D1&s=3a2611476de4eba083c3f29e46af4b4431b766b203e601a932b48c54be6d8b92",
    "https://fptshop.com.vn/apiFPTShop/Product/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Fmay-chieu%3Fsort%3Dban-chay-nhat%26trang%3D100%26pagetype%3D1&s=f5aad47da4e58c91b938f896bd654ab9a50fdab48c081f25619d09e1360f69d2",
    "https://fptshop.com.vn/apiFPTShop/Product/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Fman-hinh%3Fsort%3Dban-chay-nhat%26trang%3D100%26pagetype%3D1&s=e298984c73e176fb68a2a6a0ba5c353675045dd1e320dcf5f305892c7a780259",
    "https://fptshop.com.vn/apiFPTShop/ProductPC/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Fmay-tinh-de-ban%3Fsort%3Dban-chay-nhat%26trang%3D100%26pagetype%3D1&s=439262a804490092f2ec17498e35732d5470ddb6d2a52cd02881a6a3fb92dc85",
    "https://fptshop.com.vn/apiFPTShop/Product/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Fmay-tinh-bang%3Fsort%3Dban-chay-nhat%26trang%3D100%26pagetype%3D1&s=6c83f97c400f7470cbf56769ab794a5f466f0c27a16d2cc08a29792913ab9f1e",
    "https://fptshop.com.vn/apiFPTShop/Product/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Fdien-thoai%3Fsort%3Dban-chay-nhat%26trang%3D100%26pagetype%3D1&s=1d320458510837a35116f8bb20300d287b4ec1a53371725b8101ccefd1410d32",
    "https://fptshop.com.vn/apiFPTShop/Product/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Fmay-tinh-xach-tay%3Fsort%3Dban-chay-nhat%26trang%3D100%26pagetype%3D1&s=cf17cd2830b7c5f08ba2242265c7d7224642fcf58081358c9f5f71eedeb0bdb3"
]


def crawl_data(api_urls):
    # Initialize an empty list to store products
    all_products = []

    # Loop through each API URL
    for url in api_urls:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Navigate to the desired part of the JSON structure
            products = data.get('datas', {}).get('filterModel', {}).get('listDefault', {}).get('list', [])
            # Loop through the products to extract name and price
            for product in products:
                category = data.get('datas', {}).get('filterModel', {}).get('listDefault', {}).get('categoryName', 'N/A')
                brand = product.get('brandName', 'N/A')
                name = product.get('nameAscii', 'N/A')
                price = product.get('productVariant', {}).get('price', 'N/A')
                all_products.append({ 'category': category, 'product brand': brand, 'product name': name, 'price': price})
        else:
            print(f"Failed to retrieve data from {url}")

    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(all_products)

    # Remove special characters from the name product column
    df['product name'] = df['product name'].str.replace('-', ' ')
    # Format the 'price' column with periods as thousand separators
    df['price'] = df['price'].apply(lambda x: '{:,.0f}'.format(int(x))).str.replace(',', '.')

    print("total product", len(df))
    # Display the DataFrame and convert to excel
    print(df.head(20))

    df.to_excel('fpt_shop.xlsx')

crawl_data(api_urls) 
