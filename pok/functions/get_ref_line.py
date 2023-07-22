import numpy as np

# Permet de recuperer la ligne de reference pour comparer plusieurs lignes entres elles
# axis : (0 : Verticale, 1 : Hozitontale)
# center : décalager par rapport à gauche (pour un axe verticale) ou au haut (pour un axe horizontale)  
def get_ref_line(axis, center):
    if axis == 1:
        return [[center[0], 0]]
    return [[center[1], np.pi/2]]