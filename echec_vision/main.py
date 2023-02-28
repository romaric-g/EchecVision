import os
import numpy as np
import cv2 as cv2
import chess.engine
from matplotlib import pyplot as plt
from get_chess_plate import *
from scipy import signal
from skimage.metrics import structural_similarity
from classes.game import *
from classes.video_capture import *
from classes.image_logger import *


def difference(frame1_source, frame2_source):

    chess_plate_1 = get_chess_plate(frame1_source)
    before = chess_plate_1.get_chess_plate_img()

    chess_plate_2 = get_chess_plate(frame2_source)
    after = chess_plate_2.get_chess_plate_img()

    before = before[100:200, :100, :]
    after = after[100:200, :100, :]

    print(before.shape)
    print(after.shape)

    before = frame1_source
    after = frame2_source

    # Convert images to grayscale
    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between the two images
    (score, diff) = structural_similarity(before_gray, after_gray, full=True)
    print("Image Similarity: {:.4f}%".format(score * 100))

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1]
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")
    diff_box = cv2.merge([diff, diff, diff])

    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(
        diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(before.shape, dtype='uint8')
    filled_after = after.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 80:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(before, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(after, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(diff_box, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.drawContours(mask, [c], 0, (255, 255, 255), -1)
            cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)

    cv2.imshow('before', before)
    cv2.imshow('after', after)
    cv2.imshow('diff', diff)
    cv2.imshow('diff_box', diff_box)
    cv2.imshow('mask', mask)
    cv2.imshow('filled after', filled_after)
    cv2.waitKey()

    # diff = cv2.absdiff(frame1, frame2)

    # cv2.imshow("diff", diff)
    # cv2.waitKey(0)

    # gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    # dilated = cv2.dilate(thresh, None, iterations=3)
    # contours, _ = cv2.findContours(
    #     dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for contour in contours:
    #     (x, y, w, h) = cv2.boundingRect(contour)
    #     if cv2.contourArea(contour) < 500:
    #         continue
    #     cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #     #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    # cv2.imshow("feed", frame1)
    # cv2.waitKey(0)


def main(image_path='./images/sources/2.jpg'):
    chess_plates_img_path = [
        './images/sources/1.jpg',
        './images/sources/2.jpg',
        './images/sources/3.jpg',
        './images/sources/4.jpg',
        './images/sources/5.jpg',
        './images/sources/6.jpg',
        './images/sources/7.jpg',
        './images/sources/8.jpg',
        './images/sources/9.jpg',
        './images/sources/10.jpg',
        './images/sources/11.jpg',
        './images/sources/12.jpg',
        './images/sources/13.jpg',
    ]

    export_path = 'C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/generated/datasets_2'

    image_ref = cv2.imread(image_path)

    chess_plate = get_chess_plate(image_ref)
    chess_plate.show()

    # chess_plate_img = chess_plate.get_chess_plate_img()

    # sobel_64 = cv2.Sobel(chess_plate_img, cv2.CV_64F, 1, 0, ksize=3)
    # abs_64 = np.absolute(sobel_64)
    # sobel_8u = np.uint8(abs_64)

    # for i in range(0, 8):
    #     for j in range(0, 8):
    #         case = chess_plate.get_case(i, j)
    #         case_sobel = chess_plate.get_case_on_img(sobel_8u, i, j)

    #         case_filename = "case_" + str(i) + "_" + str(j) + ".png"
    #         case_sobel_filename = "case_" + \
    #             str(i) + "_" + str(j) + "_sobel.png"

    #         cv2.imwrite(os.path.join(export_path, case_filename), case)
    #         cv2.imwrite(os.path.join(
    #             export_path, case_sobel_filename), case_sobel)

    #center = tuple([int(case.shape[0]/2), int(case.shape[1]/2)])

    #a = get_ref_line(0, center)
    #b = get_ref_line(1, center)

    # show_line(case,a,(255,0,0))
    # show_line(case,b,(0,255,0))

    # cv2.imshow('sobel_8u',case)
    # cv2.waitKey(0)

    # cv2.imwrite(os.path.join(export_path, "source.png"), image_ref)


def get_change_map():

    frame1 = cv2.imread(
        "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/Suivis/1.png")
    frame2 = cv2.imread(
        "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/Suivis/2.png")

    # difference(frame1, frame2)

    values = np.zeros((8, 8))

    plate1 = get_chess_plate(frame1)
    plate2 = get_chess_plate(frame2)

    plate1_img = plate1.get_chess_plate_img()
    plate2_img = plate2.get_chess_plate_img()

    plate1_img = cv2.medianBlur(plate1_img, 3)
    plate2_img = cv2.medianBlur(plate2_img, 3)

    for i in range(0, 8):
        for j in range(0, 8):

            case_to_compare = (i, j)

            case1 = plate1.get_case_on_img(plate1_img, *case_to_compare)
            case2 = plate2.get_case_on_img(plate2_img, *case_to_compare)

            case1 = cv2.cvtColor(case1, cv2.COLOR_BGR2GRAY)
            case2 = cv2.cvtColor(case2, cv2.COLOR_BGR2GRAY)

            # cv2.imshow('case 1', case1)
            # cv2.imshow('case 2', case2)

            resized1 = cv2.resize(
                case1, (10, 10), interpolation=cv2.INTER_AREA)
            resized2 = cv2.resize(
                case2, (10, 10), interpolation=cv2.INTER_AREA)

            array1 = resized1.astype(np.int16, copy=False)
            array2 = resized2.astype(np.int16, copy=False)

            array1 = array1[1:9, 1:9]
            array2 = array2[1:9, 1:9]

            # minref = array1.min()
            # maxref = array1.max()

            # array1 = (array1 - minref) / (maxref - minref)
            # array2 = (array2 - minref) / (maxref - minref)

            diff = np.abs(np.subtract(array1, array2))

            diff = np.ones(array1.shape)[diff > 25]

            # print(diff)

            value = np.sum(diff)

            values[i, j] = value

            print("[value]", value)

            # fig, axs = plt.subplots(3)
            # im = axs[0].pcolor(array1, cmap=plt.cm.Blues)
            # im = axs[1].pcolor(array2, cmap=plt.cm.Blues)
            # im = axs[2].pcolor(diff, cmap=plt.cm.Blues)

            # plt.show()

            # cv2.waitKey()

    return values
    # fig, ax = plt.subplots()
    # ax.pcolor(values, cmap=plt.cm.Blues)
    # plt.show()
    # cv2.waitKey()

    # print("Test type", arr.dtype)

    # print("My type", array1.dtype)
    # print("array1", array1)
    # print("array2", array2)
    # print("diff", diff)

    # fig, axs = plt.subplots(3)
    # im = axs[0].pcolor(array1, cmap=plt.cm.Blues)
    # im = axs[1].pcolor(array2, cmap=plt.cm.Blues)
    # im = axs[2].pcolor(diff, cmap=plt.cm.Blues)

    # plt.show()

    # cv2.waitKey()


def find_best_moove_from_change_map(change_map):

    ind = np.unravel_index(np.argsort(change_map, axis=None), change_map.shape)

    for i in reversed(range(0, len(ind[0]))):
        x = ind[0][i]
        y = ind[1][i]
        print(x, y)


if __name__ == '__main__00':
    frame0 = cv2.imread(
        "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_saves/plate_change_orientation/0.png")
    frame1 = cv2.imread(
        "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_saves/plate_change_orientation/1.png")
    frame2 = cv2.imread(
        "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_saves/plate_change_orientation/2.png")
    frame3 = cv2.imread(
        "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_saves/plate_change_orientation/3.png")
    frame4 = cv2.imread(
        "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_saves/plate_change_orientation/4.png")
    frame5 = cv2.imread(
        "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_saves/plate_change_orientation/5.png")
    # frame6 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_saves/plate_change_orientation/6.png")
    # frame7 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_saves/plate_change_orientation/7.png")
    # frame8 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_saves/plate_change_orientation/8.png")
    # frame9 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_saves/plate_change_orientation/9.png")
    # frame10 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_saves/plate_change_orientation/10.png")
    # frame11 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/log_saves/plate_change_orientation/11.png")

    # Init

    plate = get_chess_plate(frame0)
    game = Game(plate)
    print(game.board)

    plate.show()
    cv2.waitKey(0)

    # #1

    plate = get_chess_plate(frame1)
    game.play_from_plate(plate)
    print(game.board)

    plate.show()
    cv2.waitKey(0)

    # #2

    plate = get_chess_plate(frame2)
    game.play_from_move(chess.Move(
        chess.square(3, 6), chess.square(3, 4)), plate)
    print(game.board)

    plate.show()
    cv2.waitKey(0)

    # #3

    plate = get_chess_plate(frame3)
    game.play_from_plate(plate)
    print(game.board)

    plate.show()
    cv2.waitKey(0)

    # #4

    plate = get_chess_plate(frame4)
    game.play_from_move(chess.Move(
        chess.square(2, 6), chess.square(2, 4)), plate)
    print(game.board)

    plate.show()
    cv2.waitKey(0)

    # #5

    plate = get_chess_plate(frame5)
    game.play_from_plate(plate)
    print(game.board)

    plate.show()
    cv2.waitKey(0)

    # #6

    # plate = get_chess_plate(frame6)
    # game.play_from_move(chess.Move(
    #     chess.square(1, 6), chess.square(2, 4)), plate)
    # print(game.board)

    # plate.show()
    # cv2.waitKey(0)


# if __name__ == '__main__':
#     frame1 = cv2.imread(
#         "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/difference/1.png")

#     plate1 = get_chess_plate(frame1)
#     plate1.show()
#     cv2.waitKey(0)

# if __name__ == '__main__00':
#     url = "http://172.20.10.9:8080/video"
#     cap = VideoCapture(url)

#     frame1 = cap.read()

#     cv2.imshow("frame1", frame1)
#     cv2.waitKey(0)

#     plate1 = get_chess_plate(frame1)
#     plate1.show()
#     cv2.waitKey(0)

#     cv2.destroyAllWindows()


if __name__ == "__main__":

    url = "http://10.112.91.130:8080/video"
    cap = VideoCapture(url)

    played = input("Ready to start ?")

    frame = cap.read()

    export_path = 'C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/logs'
    img_logger = ImageLogger(export_path)
    cropped_logger = ImageLogger(export_path, 'cropped')

    initial_plate = get_chess_plate(frame)

    img_logger.log(frame)
    cropped_logger.log(initial_plate.plate_img)

    initial_plate.show()
    cv2.waitKey(0)

    game = Game(initial_plate)
    engine = chess.engine.SimpleEngine.popen_uci(
        r"C:\Users\Romaric\DataScience\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

    board = game.board

    while not board.is_game_over():

        # Le joueur joue

        played = input("Press Enter to confirm your play...")

        frame = cap.read()
        plate = get_chess_plate(frame)

        img_logger.log(frame)
        cropped_logger.log(plate.plate_img)

        plate.show()
        cv2.waitKey(0)

        game.play_from_plate(plate)
        print(game.board)

        # L'IA joue

        result = engine.play(board, chess.engine.Limit(time=0.1))

        print("L'IA a joué : ", result.move)
        played = input("Press Enter to confirm you report IA's play...")

        frame = cap.read()
        plate = get_chess_plate(frame)

        img_logger.log(frame)
        cropped_logger.log(plate.plate_img)

        plate.show()
        cv2.waitKey(0)

        game.play_from_move(result.move, plate)
        print(game.board)

    engine.quit()
    cap.release()
    cv2.destroyAllWindows()

    # frame1 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/Suivis 2/1.jpg")
    # frame2 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/Suivis 2/2.jpg")
    # frame3 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/Suivis 2/3.jpg")
    # frame4 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/Suivis 2/4.jpg")
    # frame5 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/Suivis 2/5.jpg")
    # frame6 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/Suivis 2/6.jpg")
    # frame7 = cv2.imread(
    #     "C:/Users/Romaric/DataScience/Echecs Vision/echec_vision/images/Suivis 2/7.jpg")

    # plate1 = get_chess_plate(frame1)
    # plate2 = get_chess_plate(frame2)
    # plate3 = get_chess_plate(frame3)
    # plate4 = get_chess_plate(frame4)
    # plate5 = get_chess_plate(frame5)
    # plate6 = get_chess_plate(frame6)
    # plate7 = get_chess_plate(frame7)

    # # Debut
    # game = Game(plate1)

    # print("DEBUT")
    # print(game.board)

    # # [Tour 1 : Blanc] Le joueur comencer
    # game.play_from_plate(plate2)

    # print("[Tour 1 : Blanc]")
    # print(game.board)

    # # [Tour 1 : Noir] L'IA joue son premier coup
    # move_ia = chess.Move(chess.square(3, 6), chess.square(3, 4))
    # game.play_from_move(move_ia, plate3)

    # print("[Tour 1 : Noir]")
    # print(game.board)

    # # [Tour 2 : Blanc]
    # game.play_from_plate(plate4)

    # print("[Tour 2 : Blanc]")
    # print(game.board)

    # # [Tour 2 : Noir]
    # move_ia = chess.Move(chess.square(2, 6), chess.square(2, 4))
    # game.play_from_move(move_ia, plate5)

    # print("[Tour 2 : Noir]")
    # print(game.board)

    # # [Tour 3 : Blanc]
    # game.play_from_plate(plate6)

    # print("[Tour 3 : Blanc]")
    # print(game.board)

    # print("END")


# W : White
# B : Black

# -1 : Empty
# 1 : Pawn
# 2 : Knight
# 3 : Bishop
# 4 : Rook
# 5 : Queen
# 6 : King
