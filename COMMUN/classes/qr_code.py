import qrcode
import pygame
import io

# Génère un QR Code à partir d'une chaîne donnée
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    return qr.make_image(fill_color="white", back_color="black")

# Convertit l'image du QR Code en une surface Pygame
def qr_image_to_pygame_surface(img):
    data = io.BytesIO()
    img.save(data, 'PNG')
    data.seek(0)
    return pygame.image.load(data)