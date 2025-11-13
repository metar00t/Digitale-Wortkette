import qrcode
import qrcode.image.svg

class QrCodeController:
    def __init__(self, text):
        self.text = text

    def generateQrCode(self):
        img = qrcode.make(self.text, image_factory=qrcode.image.svg.SvgPathImage)
        svg_string = img.to_string(encoding='unicode')
        return f'{svg_string}'