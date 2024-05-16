import cv2
import mediapipe as mp
import os

mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils
maos = mp_maos.Hands()

bloco_notas = False
chrome = False
calculadora = False
resolucao_x = 1280
resolucao_y = 720
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolucao_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolucao_y)


def encontra_coordenadas_maos(img, lado_invertido=False):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resultado = maos.process(img_rgb)
    todas_maos = []

    if resultado.multi_hand_landmarks:
        for lado_mao, marcacoes_maos in zip(resultado.multi_handedness, resultado.multi_hand_landmarks):
            info_mao = {}
            coordenadas = []
            for marcacao in marcacoes_maos.landmark:
                coord_x, coord_y, coord_z = int(marcacao.x * resolucao_x), int(marcacao.y * resolucao_y), int(
                    marcacao.z * resolucao_y)
                coordenadas.append((coord_x, coord_y, coord_z))

            info_mao['coordenadas'] = coordenadas
            if lado_invertido:
                if lado_mao.classification[0].label == 'Left':
                    info_mao['lado'] = 'Right'
                else:
                    info_mao['lado'] = 'Left'
            else:
                info_mao['lado'] = lado_mao.classification[0].label
            todas_maos.append(info_mao)

            mp_desenho.draw_landmarks(img,
                                      marcacoes_maos,
                                      mp_maos.HAND_CONNECTIONS)

    return img, todas_maos


def dedos_levantados(mao):
    dedos = []
    for ponta_dedo in [8, 12, 16, 20]:
        if mao['coordenadas'][ponta_dedo][1] < mao['coordenadas'][ponta_dedo - 2][1]:
            dedos.append(True)
        else:
            dedos.append(False)
    return dedos


while True:
    sucesso, img = camera.read()
    img = cv2.flip(img, 1)

    img, todas_maos = encontra_coordenadas_maos(img)

    if len(todas_maos) == 1:
        info_dedos_mao1 = dedos_levantados(todas_maos[0])

        if todas_maos[0]['lado'] == 'Right':
            if info_dedos_mao1 == [True, False, False, False] and bloco_notas == False:
                bloco_notas = True
                os.startfile(r'C:\Windows\system32\notepad.exe')
            if info_dedos_mao1 == [True, True, False, False] and chrome == False:
                chrome = True
                os.startfile(r'C:\Program Files\Google\Chrome\Application\chrome.exe')
            if info_dedos_mao1 == [True, True, True, False] and calculadora == False:
                calculadora = True
                os.startfile(r'C:\Windows\system32\calc.exe')
            if info_dedos_mao1 == [False, False, False, False] and bloco_notas == True:
                bloco_notas = False
                os.system('TASKKILL /IM notepad.exe')
            if info_dedos_mao1 == [True, False, False, True]:
                break

    cv2.imshow("Imagem", img)
    tecla = cv2.waitKey(1)
    if tecla == 27:
        break