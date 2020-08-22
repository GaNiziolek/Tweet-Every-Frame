import os
import traceback
from time import sleep
from pathlib import Path

try:
    import tweepy
except ModuleNotFoundError:
    os.system("pip install tweepy")

try:
    import cv2
except ModuleNotFoundError:
    os.system("pip install opencv-python")

def clear_console():
    os.system('cls')

# video_Path = r'test_videos\achei-redstone-minecraft-em-busca-da-casa-automatica-2.mp4'
def main():
    while True:
        while True:
            clear_console()
            try:
                video_Path = Path(input('Digite o caminho para o video que você quer extrair os frames (sem "):\n'))
                break
            except:
                print('Digite corretamente o caminho para o arquivo')

        video_Name = os.path.basename(os.path.splitext(video_Path)[0])

        cap = cv2.VideoCapture(str(video_Path))


        cap_fps = int(round(cap.get(cv2.CAP_PROP_FPS)))

        if cap_fps == 0:
            print('Vídeo inválido ou não foi possível ler o arquivo.')
        else:
            break

    while True:
        clear_console()
        print(f'O frame rate do video é {cap_fps} fps')
        try:
            takes_by_second = int(input('quantos frames deseja extrair por segundo?\n'))
            break
        except:
            print('Digite um número inteiro')

    while True:
        clear_console()
        try:
            frame_pos = int(input('Deseja extrair o frame em qual momento? (Digite o número) \n1 - Final do segundo \n2 - Metade do segundo \n'))

            if frame_pos in [1, 2]:
                break
            else:
                pass
        except:
            print('Selecione uma das opções acima')

    frame_num = 0
    cont_time = 0

    clear_console()


    while True:
        
        sucess, frame = cap.read()

        if not sucess:
            break

        frame_num += 1

        if frame_pos == 1 and frame_num % (cap_fps / takes_by_second) == 0:
            cont_time += 1
            print(f'Salvando frame {frame_num} do segundo: {cont_time}')
            cv2.imwrite(f'Frames/{video_Name} ; {cont_time}.jpg', frame)

        if frame_pos == 2 and ((frame_num + (cap_fps / 2)) % (cap_fps / takes_by_second)) == 0:
            cont_time += 1
            print(f'Salvando frame {frame_num} do segundo: {cont_time}')
            cv2.imwrite(f'Frames/{video_Name} ; {cont_time}.jpg', frame)

    print('Tudo pronto!')
    print(f'Foram criadas {cont_time} imagens na pasta Frames')

if __name__ == '__main__':
    try:
        main()
    except:
        clear_console()

        for i in range(5):
            print('Houve um problema, por favor verifique o arquivo log.txt')
            print(f'O programa será finalizado em { 5 - i }')
            sleep(1)
            clear_console()

        log = open('log.txt', 'w')

        log.writelines(traceback.format_exc())

        log.close()