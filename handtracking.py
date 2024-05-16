import cv2
import mediapipe as mp

mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils

maos = mp_maos.Hands()

camera = cv2.VideoCapture(0)
resolucao_x = 1280
resolucao_y = 720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolucao_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolucao_y)

while True:
    sucesso, img = camera.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    resultado = maos.process(img_rgb)

    if resultado.multi_hand_landmarks:
        for marcacao_maos in resultado.multi_hand_landmarks:
            mp_desenho.draw_landmarks(img,
                                      marcacao_maos,
                                      mp_maos.HAND_CONNECTIONS)
    cv2.imshow('Imagem', img)
    tecla = cv2.waitKey(1)
    if tecla == 27:
        break
