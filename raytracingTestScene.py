import numpy as np
import matplotlib.pyplot as plt


def create_ray(origine,
               direction) -> dict:
    ray = {'Origine': np.array(origine), 'Direction': np.array(direction)}
    return ray


def create_sphere(centre, rayon, ambient, diffuse, specular, reflexion, index):
    sphere = {'Type': 'sphere', 'Centre': np.array(centre), 'Rayon': float(rayon), 'Ambient': np.array(ambient), 'Diffuse': np.array(diffuse), 'Specular': np.array(specular), 'Reflexion': float(reflexion), 'Index': int(index)}
    return sphere


def create_plane(P, n, a, d, s, cr, i):
    plane = {'Type': 'plan', 'Position': np.array(P), 'Normale': np.array(n), 'Ambient': np.array(a),
             'Diffuse': np.array(d), 'Specular': np.array(s), 'Reflexion': float(cr), 'Index': int(i)}
    return plane


def normalize(x):
    return x / np.linalg.norm(x)


def get_Normal(obj, M):
    if obj['Type'] == 'plan':
        return obj['Normale']
    if obj['Type'] == 'sphere':
        C = obj['Centre']
        return normalize(M - C)


def rayAt(ray, t):
    O = ray['Origine']
    D = ray['Direction']
    return O + t * D


def intersect_Plane(ray, plane):
    O = ray['Origine']
    D = ray['Direction']
    n = plane['Normale']
    P = plane['Position']
    num = np.dot((O - P), n)
    den = np.dot(D, n)
    if abs(den) < 10 ** -6:
        return np.inf
    t = -num / den
    if t < 0:
        return np.inf
    return t


def intersect_Sphere(ray, sphere):
    O = ray['Origine']
    d = ray['Direction']
    C = sphere['Centre']
    r = sphere['Rayon']
    a = np.linalg.norm(d) ** 2
    b = 2 * np.dot(O - C, d)
    c = np.dot(O - C, O - C) - r ** 2
    delta = b ** 2 - 4 * a * c
    if delta <= 0:
        return np.inf
    t1 = (-b - np.sqrt(delta)) / (2 * a)
    t2 = (-b + np.sqrt(delta)) / (2 * a)
    if t1 > 0 and t2 > 0:
        return min(t1, t2)
    else:
        return np.inf


def intersect_Scene(ray, obj):
    if obj['Type'] == 'plan':
        return intersect_Plane(ray, obj)
    if obj['Type'] == 'sphere':
        return intersect_Sphere(ray, obj)


def Is_in_Shadow(obj_min, P, N):
    LIntersect = []
    LP = normalize(L - P)
    Pe = P + (acne_eps) * N
    rayTest = create_ray(Pe, LP)
    for obj in scene:
        if obj_min['Index'] != obj['Index']:
            tobj = intersect_Scene(rayTest, obj)
            if tobj < np.inf:
                LIntersect.append(obj)
    if LIntersect:
        return True
    return False


def eclairage(obj, light, P):
    Ka = obj['Ambient']
    la = Light['ambient']
    Kd = obj['Diffuse']
    ld = Light['diffuse']
    l = normalize(L - P)
    n = get_Normal(obj, P)
    n = normalize(n)

    Ks = obj['Specular']
    ls = Light['specular']
    beta = materialShininess
    c = normalize(C - P)

    cd = Ka * la + Kd * ld * max(np.dot(l, n), 0)
    ct = cd + Ks * ls * max(np.dot(normalize(l + c), n), 0) ** (beta / 4)

    return cd + ct


def reflected_ray(dirRay, N):
    dref = normalize(dirRay - 2 * np.dot(dirRay, N) * N)
    return dref


def compute_reflection(rayTest, depth_max, col):
    dirRay = rayTest['Direction']
    cr = 1
    for i in range(1, depth_max):
        tobj = trace_ray(rayTest)
        if not tobj:
            break
        obj, M, N, col_ray = tobj
        col = col + col_ray * cr
        Me = M + acne_eps * N
        dirRay = reflected_ray(dirRay, N)
        rayTest = create_ray(Me, dirRay)
        cr = cr * obj['Reflexion']
    return col


def trace_ray(ray):
    tmin = np.inf
    objmin = None
    for obj in scene:
        t = intersect_Scene(ray, obj)
        if t <= tmin:
            tmin = t
            objmin = obj

    if tmin == np.inf:  # objmin==None
        return None
    else:
        P = rayAt(ray, tmin)
        N = get_Normal(objmin, P)
        if Is_in_Shadow(objmin, P, N):
            return None
        col_ray = eclairage(objmin, Light, P)

        return objmin, P, N, col_ray


# Taille de l'image
w = 800
h = 600
acne_eps = 1e-4
materialShininess = 50

img = np.zeros((h, w, 3))  # image vide : que du noir
# Aspect ratio
r = float(w) / h
# coordonnées de l'écran : x0, y0, x1, y1.
S = (-1., -1. / r, 1., 1. / r)

# Position et couleur de la source lumineuse
Light = {'position': np.array([5, 5, 0]),
         'ambient': np.array([0.05, 0.05, 0.05]),
         'diffuse': np.array([1, 1, 1]),
         'specular': np.array([1, 1, 1])}

L = Light['position']

col = np.array([0.2, 0.2, 0.7])  # couleur de base
C = np.array([0., 0.1, 1.1])  # Coordonée du centre de la camera.
Q = np.array([0, 0.3, 0])  # Orientation de la caméra
img = np.zeros((h, w, 3))  # image vide : que du noir
materialShininess = 50
skyColor = np.array([0.321, 0.752, 0.850])
whiteColor = np.array([1, 1, 1])
depth_max = 10

scene = [create_sphere([.75, -.3, -1.],  # Position
                       .6,  # Rayon
                       np.array([1., 0.6, 0.]),  # ambiant
                       np.array([1., 0.6, 0.]),  # diffuse
                       np.array([1, 1, 1]),  # specular
                       0.2,  # reflection index
                       1),  # index
         create_plane([0., -.9, 0.],  # Position
                      [0, 1, 0],  # Normal
                      np.array([0.145, 0.584, 0.854]),  # ambiant
                      np.array([0.145, 0.584, 0.854]),  # diffuse
                      np.array([1, 1, 1]),  # specular
                      0.7,  # reflection index
                      2),  # index
         ]

# Loop through all pixels.
for i, x in enumerate(np.linspace(S[0], S[2], w)):
    if i % 10 == 0:
        print(i / float(w) * 100, "%")
    for j, y in enumerate(np.linspace(S[1], S[3], h)):
        col = np.zeros((3))
        Q[:2] = (x, y)
        d = normalize(Q - C)
        raytest = create_ray(C, d)
        traced = trace_ray(raytest)
        if traced:
            obj, P, N, colRay = traced
            if depth_max > 0:
                col = compute_reflection(raytest, depth_max, col)
            col = col + colRay
        img[h - j - 1, i, :] = np.clip(col, 0, 1)  # la fonction clip permet de "forcer" col a être dans [0,1]

plt.imsave('figRaytracing.png', img)
