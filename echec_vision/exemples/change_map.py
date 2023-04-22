import inspect
import sys
import os
import cv2


def main(currentdir):

    previous_image_name = "2.jpg"
    next_image_name = "3.jpg"

    path = os.path.join(currentdir, 'images', previous_image_name)
    frame1 = cv2.imread(path)

    path = os.path.join(currentdir, 'images', next_image_name)
    frame2 = cv2.imread(path)

    if frame1 is None or frame2 is None:
        print("Erreur, une des images n'existe pas dans le repertoire 'images/'")
        return

    standard_image1 = image_resize(frame1, height=700)
    extracted_plate1 = extract_plate(standard_image1)

    standard_image2 = image_resize(frame2, height=700)
    extracted_plate2 = extract_plate(standard_image2)

    if extracted_plate1 is None:
        print("Aucune extraction valide n'a été trouvé ! (Image 1)")
        return

    if extracted_plate2 is None:
        print("Aucune extraction valide n'a été trouvé ! (Image 2)")
        return

    extracted_plate1.show("Now-1 image")
    extracted_plate2.show("Now image")

    map = from_histogram(extracted_plate1, extracted_plate2)
    img = map_to_image(map, 8)

    plt.imshow(img, cmap='Greens', vmin=0, vmax=255)
    plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':

    # Import parent core module
    currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

    from core.plate.extract import extract_plate
    from core.utils.image import image_resize
    from core.movement.change_map import from_histogram, map_to_image
    from matplotlib import pyplot as plt

    main(currentdir)
