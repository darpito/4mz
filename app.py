from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_product_info', methods=['POST'])
def get_product_info():
    asin = request.form['asin']
    product_info = scrape_amazon(asin)
    return render_template('product_info.html', product_info=product_info)

def scrape_amazon(asin):
    # Di sini Anda bisa memanggil fungsi scrape_amazon dari file amazon_scraper.py
    # Gantikan ini dengan kode untuk mengambil data dari Amazon berdasarkan ASIN
    return {
        'name': 'Product Name',
        'price': '$100',
        'description': 'Product Description',
        'image_url': 'https://example.com/product_image.jpg'
    }

if __name__ == '__main__':
    app.run(debug=True)