from flask import request, Blueprint
import cv2

router = Blueprint('router', __name__)

@router.route('/envio', methods=['POST'])
def upload():
    webcam = cv2.VideoCapture(0)

    ret, frame = webcam.read()

    path = './imagens/oi_nicola.jpg'

    webcam.release()

    cv2.imwrite(path, frame)

    return 'Salvamento realizado com sucesso!'