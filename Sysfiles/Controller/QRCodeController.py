import qrcode
import qrcode.image.svg


class QrCodeController:
    def __init__(self, text):
        self.text = text

    def generateQrCode(self) -> str:
        """
        Generates the QRCode PathImage
        :return: Image Path for the QRCode
        :rtype: str
        """
        img = qrcode.make(self.text, image_factory=qrcode.image.svg.SvgPathImage, version=1)
        svg_string : str = img.to_string(encoding='unicode')
        return svg_string
