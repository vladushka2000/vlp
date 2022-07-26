import numpy as np
from src.calculations.well import calc_pwf


def calc_vlp(inclinometry: dict, casing: dict, tubing: dict, pvt: dict,
             p_wh: float, geo_grad: float, h_res: float):

    q_liq = np.linspace(0.001, 400, 20)
    p_wf = np.empty_like(q_liq)

    for i, ql in enumerate(q_liq):

        p_wf[i] = calc_pwf(inclinometry, casing, tubing, pvt, p_wh, geo_grad,
                           h_res, ql)

    result = {"q_liq": q_liq.tolist(), "p_wf": p_wf.tolist()}

    return result


if __name__ == "__main__":
    import json

    with open("../../../contracts/vlp_in.json") as f:
        data = json.load(f)
    results = calc_vlp(**data)
    print(results)
