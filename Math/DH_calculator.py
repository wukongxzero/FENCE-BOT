import sympy as sp

def get_dh_matrix(theta, d, a, alpha):
    """
    Calculates the homogeneous transformation matrix using DH parameters.
    Order: Rot_z(theta) -> Trans_z(d) -> Trans_x(a) -> Rot_x(alpha)
    """
    
    # 1. Rotation about the Z-axis by theta
    Rz = sp.Matrix([
        [sp.cos(theta), -sp.sin(theta), 0, 0],
        [sp.sin(theta),  sp.cos(theta), 0, 0],
        [0,              0,             1, 0],
        [0,              0,             0, 1]
    ])
    
    # 2. Translation along the Z-axis by d
    Tz = sp.Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, d],
        [0, 0, 0, 1]
    ])
    
    # 3. Translation along the X-axis by a
    Tx = sp.Matrix([
        [1, 0, 0, a],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    
    # 4. Rotation about the X-axis by alpha
    Rx = sp.Matrix([
        [1, 0,            0,             0],
        [0, sp.cos(alpha), -sp.sin(alpha), 0],
        [0, sp.sin(alpha),  sp.cos(alpha), 0],
        [0, 0,            0,             1]
    ])
    
    # Multiply the transformations in order
    # T = (Rz * Tz) * (Tx * Rx)
    T = Rz * Tz * Tx * Rx
    
    return sp.simplify(T)