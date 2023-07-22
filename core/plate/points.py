import numpy as np
from core.utils.image import get_image_center
from core.plate.lines import extract_points_from_lines


def extract_valid_points(image_board, segmented_lines):
    i_lines = segmented_lines[0]
    j_lines = segmented_lines[1]

    center = get_image_center(image_board)

    # Les lignes detecté sont ici soit verticale, soit horizontale (homographie qui suit le plateau)
    # On cherches les points de croisement, si la ligne de croissement est parallele aux lignes, on inverse l'axe de croissement
    try:
        v_points = np.array(
            extract_points_from_lines(i_lines, center, axis=0))
        h_points = np.array(
            extract_points_from_lines(j_lines, center, axis=1))
    except:
        # En cas d'inversion, les lignes horizontales determinent alors les points verticale et inversement
        try:
            v_points = np.array(
                extract_points_from_lines(j_lines, center, axis=0))
            h_points = np.array(
                extract_points_from_lines(i_lines, center, axis=1))
        except:
            return None

    # On extrait la taille du plateau
    im_dst_w = image_board.shape[0]
    im_dst_h = image_board.shape[1]

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

    return v_coord, h_coord


def mean_similar_points(points, tolerence):
    next_group_id = 0
    keys_groups = dict()

    for i, value in enumerate(points):
        mask = np.absolute(points-value) < tolerence
        similars = points[mask]
        if value in keys_groups:
            for s in similars:
                keys_groups[s] = keys_groups[value]
        else:
            for s in similars:
                keys_groups[s] = next_group_id
            next_group_id = next_group_id + 1

    inv_map = {}
    for k, v in keys_groups.items():
        inv_map[v] = inv_map.get(v, []) + [k]

    mean_points = []
    for i in inv_map:
        i_list = inv_map[i]
        i_mean = int(sum(i_list) / len(i_list))
        mean_points.append(i_mean)

    return mean_points


# ===================================================
# Ce code permet de calculer les coordonnées de l'echiquier
#

def get_interpolate_coord(points):
    points = np.sort(points)
    max_s_find, max_ect_norm_divisor, first_point_idx = find_cases_between_points(
        points)

    # TEST !!
    # while first_point_idx + np.sum(max_ect_norm_divisor) + 1 <= len(points):
    #     first_point_idx = len(points) - 1

    coord = [max_s_find]

    # print("---- get_interpolate_coord ----")

    for i, nbr_case in enumerate(max_ect_norm_divisor):
        # print("Nbr de case :", nbr_case, "Idx :", i)

        if nbr_case == 0:
            continue

        current_idx = first_point_idx + i + 1
        current_point = points[current_idx]

        # print("current_idx", current_idx)
        # print("current_point", current_point)

        if nbr_case == 1:
            coord.append(current_point)
        else:
            for j in range(1, nbr_case+1):
                factor = j / nbr_case
                # print(factor)

                previous_point = points[current_idx - 1]
                distance = current_point - previous_point

                # print("previous_point", previous_point)
                # print("distance", distance)

                interpolate_point = previous_point + distance*factor

                coord.append(interpolate_point)

    return np.array(coord).astype(int)


# ==========================================================================================
# L'objectif de ce code est d'aller chercher la meilleur premiere ligne de l'echiquier
# Pour cela, on calcule deja l'ecart median pour determiner la taille d'une case
# Puis on vient avec different calcule determiné combien de case peuvent être contenu entre 2 lignes en partant d'un
# point de départ "s"
# L'objectif est de maximiser ce nombre de case

def find_cases_between_points(points, tolerance=.2):
    points = np.sort(points)
    departs = points.copy()
    max_p = np.max(points)

    # On defini le depart sur le point 0
    s = points[0]

    # print(points)

    max_s_find = -1
    max_ect_norm_divisor = np.array([])
    first_point_idx = 0

    idx = 0

    while s < max_p:

        # print("S :", s)

        rlt_points = points - s
        rlt_points = rlt_points[rlt_points >= 0]

        # Si il n'y a plus de point dans la zone de recherche, on arrete la recherche
        if rlt_points.shape[0] == 0:
            break

        # print("rlt_points", rlt_points)
        # print("rlt_points roll", np.roll(rlt_points, 1))

        rlt_points_ect = rlt_points - np.roll(rlt_points, 1)

        # On supprime la premiere colonne qui n'est pas utile
        rlt_points_ect = rlt_points_ect[1:]

        # print("rlt_points_ect", rlt_points_ect)

        # On recuperer la distance median entre 2 lignes (on considera cette distance comme la taille d'une case)
        ect_median = np.median(rlt_points_ect)
        # print("ect_median", ect_median)

        # On normalise nos distances sur la base de la taille d'une case
        ect_norm = np.divide(rlt_points_ect, ect_median)

        # print("ect_norm", ect_norm)

        # On vient recuperer le reste de la division par 1 de nos distances normaliser
        ect_norm_rst = np.abs((ect_norm % 1))
        # Puis on utilise ce reste pour connaire le nombre de case presente entre 2 lignes
        ect_norm_divisor = (ect_norm - ect_norm_rst).astype(int)

        # print("ect_norm_rst", ect_norm_rst)
        # print("ect_norm_divisor", ect_norm_divisor)

        # Certaine case peuvent être legrement plus petite que 1 mais existe quand même
        # On compabilise une case si elle font au moins 90% de la taile d'une case
        mask_add = ect_norm_rst >= (1 - tolerance)
        ect_norm_divisor[mask_add] = ect_norm_divisor[mask_add] + 1

        # Certain element peuvent contenir 1 case et une parti d'une autre, ce qui n'est pas valide dans notre cas
        mask_remove = (ect_norm_rst < (1 - tolerance)
                       ) & (ect_norm_rst > tolerance)
        ect_norm_divisor[mask_remove] = 0

        # print("mask_remove", mask_remove)

        # print("ect_norm_divisor with added case", ect_norm_divisor)

        # =============================
        # Le meilleur point de depart ne garanti pas que toutes les lignes puissent être inclus dans la grille, si ce n'est pas le cas,
        # if first_point_idx + np.sum(max_ect_norm_divisor) + 1 <= len(points):
        #     break

        # =============================
        # On vient comparer notre resultat avec les prevedents

        if np.sum(max_ect_norm_divisor) <= np.sum(ect_norm_divisor):
            max_s_find = s
            max_ect_norm_divisor = ect_norm_divisor
            first_point_idx = idx

        # =============================
        # Optimisation : Si toutes les zones entre 2 lignes contiennent au moins une case, on s'arrete
        if ect_norm_divisor[ect_norm_divisor == 0].shape[0] == 0:
            break

        # =============================
        # Changement du point de depart

        # Si il n'y a plus d'autre point de depart, on arrete la recherche
        if (departs[0] is None):
            break

        # Sinon, on chnage le point de depart
        departs = departs[1:]
        s = departs[0]

        idx = idx + 1

    return (
        max_s_find,
        max_ect_norm_divisor,
        first_point_idx
    )
