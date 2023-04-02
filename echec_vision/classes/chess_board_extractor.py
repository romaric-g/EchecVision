from functions.resize_img import *
from functions.get_cropped_img_from_max_contour import *
from functions.get_lines import *
from functions.segment_by_angle_kmeans import *
from functions.get_min_max_lines import *
from functions.get_lines_cross_points import *
from functions.mean_similar_points import *
from functions.get_interpolate_coord import *
from classes.chess_plate import *
from functions.show_line import *
from functions.contour_chessboard import *
from typing import List

size = 700


def get_center(image):
    image_shape = image.shape

    # print("Shape", image_shape)
    center = np.array([image_shape[0], image_shape[1]]).astype(np.double)
    center = center / 2
    center = center.astype(np.int)
    center = tuple(center)

    return center


class ChessBoardExtractor():

    chess_plate: ChessPlate = None
    cropped_image: CroppedImage
    i_lines: List[any]
    j_lines: List[any]

    def __init__(self, frame):
        self.frame = frame
        self.standard_image = image_resize(frame, height=size)

        contours = get_contours(self.standard_image)
        max_lines = 0

        for contour in contours:
            try:
                _cropped_image = get_cropped_object_from_contour(
                    self.standard_image, contour, padding=10)

                # # On recuper les lignes presentes dans l'image
                _lines = get_lines(_cropped_image.image, threshold=110)

                if (len(_lines) <= max_lines):
                    continue

                _segmented = segment_by_angle_kmeans(_lines)

                # Si il y a bien 2 groupes
                if len(_segmented) == 2:

                    # On obtient 2 groupes de ligne (i et j)
                    self.i_lines = _segmented[0]
                    self.j_lines = _segmented[1]
                    self.cropped_image = _cropped_image

                    max_lines = len(_lines)

            except:
                continue

    def extract(self) -> ChessPlate or None:

        if self.chess_plate != None:
            return self.chess_plate

        if self.cropped_image == None:
            return ChessPlate(None, [], [])

        # On utilise les points de croisements de toute les lignes sur une lignes de reference pour trouver la premiere et la derniere
        # Par default, on definit :
        # i : axe 1
        # j : axe 0
        try:
            # on inverse 0 et 1 si erreur (2 lignes paralleles)
            min_max_i_line = get_min_max_lines(
                self.i_lines, self.cropped_image.get_center(), axis=1)
            min_max_j_line = get_min_max_lines(
                self.j_lines, self.cropped_image.get_center(), axis=0)

        # 2 lignes paralleles => erreur
        # Si erreur, on inverse l'axe de reference pour les 2 groupes
        except:
            min_max_j_line = get_min_max_lines(
                self.i_lines, self.cropped_image.get_center(), axis=0)
            min_max_i_line = get_min_max_lines(
                self.j_lines, self.cropped_image.get_center(), axis=1)

        intersections = np.array(segmented_intersections(
            [min_max_i_line, min_max_j_line]))

        # Homographie avec les coordonnées du plateau trouvées
        x, y, h, w = self.cropped_image.values
        intersections_img_ref = intersections + (x, y)

        src = np.array(intersections_img_ref)
        dst = np.array([[0, 0], [size, 0], [0, size], [size, size]])

        h, status = cv2.findHomography(src, dst)

        self.h = h.copy()

        im_dst = cv2.warpPerspective(self.standard_image, h, (size, size))

        # On recherche des lignes dans la nouvelle image

        lines = get_lines(im_dst, threshold=110)
        segmented = segment_by_angle_kmeans(lines)

        i_lines = segmented[0] if len(segmented) > 0 else []
        j_lines = segmented[1] if len(segmented) > 1 else []

        center = get_center(self.standard_image)
        # Les lignes detecté sont ici soit verticale, soit horizontale (homographie qui suit le plateau)
        # On cherches les points de croisement, si la ligne de croissement est parallele aux lignes, on inverse l'axe de croissement
        try:
            v_points = np.array(
                get_lines_cross_points(i_lines, center, axis=0))
            h_points = np.array(
                get_lines_cross_points(j_lines, center, axis=1))
        except:
            # En cas d'inversion, les lignes horizontales determinent alors les points verticale et inversement
            v_points = np.array(
                get_lines_cross_points(j_lines, center, axis=0))
            h_points = np.array(
                get_lines_cross_points(i_lines, center, axis=1))

            # print("EXCEPT")

        # On extrait la taille du plateau
        im_dst_w = im_dst.shape[0]
        im_dst_h = im_dst.shape[1]

        v_points = np.insert(v_points, 0, 0)
        h_points = np.insert(h_points, 0, 0)

        # On insert un point maximum à la liste des points (permet de detecter la derniere ligne du plateau)
        v_points = np.insert(v_points, len(v_points), im_dst_w)
        h_points = np.insert(h_points, len(h_points), im_dst_h)

        # On supprime les points qui sortent du cadre
        v_points = v_points[(v_points <= im_dst_w) & (v_points >= 0)]
        h_points = h_points[(h_points <= im_dst_h) & (h_points >= 0)]

        # On transforme les points proches par leurs moyennes (2 point à moins de 30px de distance)
        v_points = mean_similar_points(v_points, 30)
        h_points = mean_similar_points(h_points, 30)

        # Recuperation de toutes les coordonnées du plateau en fonction des points detecté
        v_coord = get_interpolate_coord(v_points)
        h_coord = get_interpolate_coord(h_points)

        # On contruit l'objet plateau
        min_x = np.min(v_coord)
        min_y = np.min(h_coord)
        max_x = np.max(v_coord)
        max_y = np.max(h_coord)

        final_x_coords = v_coord - min_x
        final_y_coords = h_coord - min_y

        final_chess_plate_ref = im_dst[min_y:max_y, min_x:max_x]

        self.chess_plate = ChessPlate(final_chess_plate_ref,
                                      final_x_coords, final_y_coords)

        return self.chess_plate
