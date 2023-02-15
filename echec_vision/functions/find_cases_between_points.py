import numpy as np
import cv2 as cv2

# =====================
# L'objectif de ce code est d'aller chercher la meilleur premiere ligne de l'echiquier
# Pour cela, on calcule deja l'ecart median pour determiner la taille d'une case
# Puis on vient avec different calcule determiné combien de case peuvent être contenu entre 2 lignes en partant d'un
# point de départ "s"
# L'objectif est de maximiser ce nombre de case

def find_cases_between_points(points, tolerance=.1):
    points = np.sort(points)
    departs = points.copy()
    max_p = np.max(points)

    # On defini le depart sur le point 0
    s = 0
    points = np.insert(points, 0, s)
    
    print(points)

    max_s_find = -1
    max_ect_norm_divisor = np.array([])
    first_point_idx = 0
    
    idx = 0

    while s < max_p:
        
        print("S :", s)

        rlt_points = points - s
        rlt_points = rlt_points[rlt_points >= 0]

        # Si il n'y a plus de point dans la zone de recherche, on arrete la recherche
        if rlt_points.shape[0] == 0:
            break


        print("rlt_points", rlt_points)
        print("rlt_points roll", np.roll(rlt_points, 1))

        rlt_points_ect = rlt_points - np.roll(rlt_points, 1)

        # On supprime la premiere colonne qui n'est pas utile
        rlt_points_ect = rlt_points_ect[1:]

        print("rlt_points_ect", rlt_points_ect)

        # On recuperer la distance median entre 2 lignes (on considera cette distance comme la taille d'une case)
        ect_median = np.median(rlt_points_ect)
        print("ect_median", ect_median)

        # On normalise nos distances sur la base de la taille d'une case
        ect_norm = np.divide(rlt_points_ect, ect_median)

        print("ect_norm", ect_norm)

        # On vient recuperer le reste de la division par 1 de nos distances normaliser
        ect_norm_rst = np.abs((ect_norm % 1)) 
        # Puis on utilise ce reste pour connaire le nombre de case presente entre 2 lignes
        ect_norm_divisor = (ect_norm - ect_norm_rst).astype(int)

        print("ect_norm_rst", ect_norm_rst)
        print("ect_norm_divisor", ect_norm_divisor)

        # Certaine case peuvent être legrement plus petite que 1 mais existe quand même
        # On compabilise une case si elle font au moins 90% de la taile d'une case
        mask_add = ect_norm_rst >= (1 - tolerance)
        ect_norm_divisor[mask_add] = ect_norm_divisor[mask_add] + 1 
        
        
        # Certain element peuvent contenir 1 case et une parti d'une autre, ce qui n'est pas valide dans notre cas
        mask_remove = (ect_norm_rst < (1 - tolerance)) & (ect_norm_rst > tolerance)
        ect_norm_divisor[mask_remove] = 0
        
        print("mask_remove", mask_remove)
        

        print("ect_norm_divisor with added case", ect_norm_divisor)

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
            break;

        # Sinon, on chnage le point de depart
        s = departs[0]
        departs = departs[1:]

        idx = idx + 1
        
    return (
        max_s_find,
        max_ect_norm_divisor,
        first_point_idx
    )