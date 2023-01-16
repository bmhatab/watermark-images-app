from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/watermark', methods=['POST'])
def watermark():
    if 'image' not in request.files or 'text' not in request.form:
        return 'No image or text file uploaded'
        
    image = request.files['image']
    text = request.form.get('text', 'Watermarked')
    image = Image.open(image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial/arial.ttf', 36)
    #text = "Watermarked"
    textwidth, textheight = draw.textsize(text, font)
    image_width, image_height = image.size
    x = (image_width - textwidth) / 2
    y = (image_height - textheight) / 2
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))
    image = image.convert("RGB")
    image.save('watermarked.jpg')

    print('Image watermarked and saved as "watermarked.jpg"')
    return render_template('index.html')

@app.route('/watermark-image', methods=['POST'])
def watermark_image():
    if 'image' not in request.files:
        return 'No image file uploaded'
    image = request.files['image']
    watermark_image = request.files['watermark_image']
    image = Image.open(image)
    
    watermark_image = Image.open(watermark_image)
    watermark_image = watermark_image.convert(image.mode)

    image_width, image_height = image.size
    watermark_image = watermark_image.resize((int(image_width/5), int(image_height/5)))
    x = int((image_width - watermark_image.width) / 2)
    y = int((image_height - watermark_image.height) / 2)
    image.alpha_composite(watermark_image, (x, y))
    image = image.convert("RGB")
    image.save('watermarked.jpg')
    print('Image watermarked and saved as "watermarked.jpg"')
    return render_template('index.html')

@app.route('/download-watermarked-image', methods=['GET'])
def download_watermarked_image():
    try:
        return send_file('watermarked.jpg', as_attachment=True)
    except Exception as e:
        return str(e)



if __name__ == '__main__':
    app.run(debug=True)
