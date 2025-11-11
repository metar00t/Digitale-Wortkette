import qrcode
import qrcode.image.svg

class QrCodeController:
    def __init__(self, text):
        self.text = text

    def setQrCode(self):
        img = qrcode.make(self.text, image_factory=qrcode.image.svg.SvgPathImage)
        self.text = img.to_string(encoding='unicode')
        return f'{self.text}'

    def getQrCode(self):
        return f'{self.text}'