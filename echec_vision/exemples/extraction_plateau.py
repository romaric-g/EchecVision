import inspect
import sys
import os
import cv2

# ------------------------------------------------------------
# Exemple d'extraction de plateau depuis une photo
# -> Vous pouvez ajouter des images dans le repertoire /images
# ------------------------------------------------------------

def main(currentdir):

    print("Nom de l'image ?")
    image_name = input()
    print('Extraction de ' + image_name + "...")

    path = os.path.join(currentdir, 'images', image_name)
    frame = cv2.imread(path)

    if frame is None:
        print("Erreur, l'image n'existe pas dans le repertoire 'images/'")
        return

    standard_image = image_resize(frame, height=700)
    extracted_plate = extract_plate(standard_image)

    if extracted_plate is None:
        print("Aucune extraction valide n'a été trouvé !")
        return

    extracted_plate.show()

    cv2.waitKey(0)


if __name__ == '__main__':

    # Import parent core module
    currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

    from core.plate.extract import extract_plate
    from core.plate.plate import Plate
    from core.movement.difference import compute_difference_score
    from core.game import Game
    from core.utils.image import image_resize
    from core.utils.image_logger import ImageLogger
    from core.server.types import GameLog, ChessBoardState

    main(currentdir)
