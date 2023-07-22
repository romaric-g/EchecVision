import numpy as np

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