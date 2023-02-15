import numpy as np
from functions.find_cases_between_points import *

# =====================
# Ce code permet de calculer les coordonnées de l'echiquier
#

def get_interpolate_coord(points):
    points = np.sort(points)
    max_s_find, max_ect_norm_divisor, first_point_idx = find_cases_between_points(points)

    coord = [max_s_find]
    
    print("---- get_interpolate_coord ----")

    for i, nbr_case in enumerate(max_ect_norm_divisor):
        print("Nbr de case :", nbr_case, "Idx :", i)

        if nbr_case == 0:
            continue

        current_idx = first_point_idx + i
        current_point = points[current_idx]

        print("current_idx", current_idx)
        print("current_point", current_point)

        if nbr_case == 1:
            coord.append(current_point)
        else:
            for j in range(1,nbr_case+1):
                factor = j / nbr_case
                print(factor)

                previous_point = points[current_idx - 1]
                distance = current_point - previous_point

                print("previous_point", previous_point)
                print("distance", distance)

                interpolate_point = previous_point + distance*factor

                coord.append(interpolate_point)


    return np.array(coord).astype(int)