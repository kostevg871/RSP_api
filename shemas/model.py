from pydantic import BaseModel


class Geometry(BaseModel):
    d_in_t: float
    d_out_t: float
    s_hor: float
    s_vert: float
    n_ryad_vert: int
    a_avg: float
    D_avg: float
    L_t: float
    n_t: int
    F_he_in_t: float
    F_he_out_t: float
    F_in_t: float
    F_out_t: float


class CoilHe(BaseModel):
    lambda_w: float
    T_in_t_in: float
    T_out_t_in: float
    P_in_t_in: float
    P_out_t_in: float
    G_in_t_in: float
    G_out_t_in: float
    n_razb: int
    mode: int = 1
    geometry: Geometry
    alw_in_t: float = 4500
    alw_out_t: float = 5500
