import cv2
import mediapipe as mp

mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils
maos = mp_maos.Hands()

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

            print(lado_mao.classification[0].label)

            mp_desenho.draw_landmarks(img,
                                      marcacoes_maos,
                                      mp_maos.HAND_CONNECTIONS)

    return img, todas_maos


while True:
    sucesso, img = camera.read()
    img = cv2.flip(img, 1)

    img, todas_maos = encontra_coordenadas_maos(img)

    cv2.imshow("Imagem", img)
    tecla = cv2.waitKey(1)
    if tecla == 27:
        break