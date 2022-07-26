import math as mt


def _calc_oil_density(gamma_oil, rs, gamma_gas, bo):
    return 1000 * (gamma_oil + rs * gamma_gas * 1.2217 / 1000) / bo


def _calc_bo(rs, gamma_gas, gamma_oil, t):
    return 0.972 + 0.000147 * ((5.614583333333334 * rs * (
        (gamma_gas / gamma_oil)**0.5) + 2.25 * t - 574.5875)**1.175)


def _calc_bg(p, t, z):
    gas_fvf = t * z * 350.958 / p
    return gas_fvf


def _calc_rs(gamma_gas, gamma_oil, t, p):
    yg = 1.2254503 + 0.001638 * t - 1.76875 / gamma_oil
    rs = gamma_gas * (1.9243101395421235e-06 * p / 10**yg)**1.2048192771084338
    return rs


def _calc_gas_density(gamma_gas, bg):
    m = 28.97 * gamma_gas
    return m / (24.04220577350111 * bg)


def _calc_rho_mix(rho_oil, rho_gas, rho_wat, wct, gas_fraction):
    rho_liq = rho_oil * (1 - wct) + rho_wat * wct
    rho_mix = rho_liq * (1 - gas_fraction) + gas_fraction * rho_gas
    return rho_mix


def _calc_qg(q_fluid, wct, rp, rs, bg):
    return bg * (q_fluid * (1 - wct) * (rp - rs))


def _calc_qw(q_fluid, wct):
    return q_fluid * wct


def _calc_qo(q_fluid, wct, bo):
    return q_fluid * (1 - wct) * bo


def _calc_ql(qw, qo):
    return qw + qo


def _calc_qm(ql, qg):
    return ql + qg


def _calc_gf(qg, qm):
    return qg / qm


def _oil_deadviscosity_beggs(gamma_oil, t):
    """
    Метод расчета вязкости дегазированной нефти по корреляции Beggs
    Parameters
    ----------
    :param gamma_oil: относительная плотность нефти, доли,
    (относительно воды с плотностью 1000 кг/м3 при с.у.)
    :param t: температура, К
    :return: вязкость дегазированной нефти, сПз
    -------
    """
    # Ограничение плотности нефти = 58 API для корреляции Beggs and Robinson
    gamma_oil = min((141.5 / gamma_oil - 131.5), 58)

    # Ограничение температуры = 295 F для корреляции Beggs and Robinson
    t = min(((t - 273.15) * 1.8 + 32), 295)

    if t < 70:
        # Корректировка вязкости дегазированной нефти для температуры ниже 70 F
        # Расчет вязкости дегазированной нефти для 70 F
        oil_deadviscosity_beggs_70 = (10**(
            (10**(3.0324 - 0.02023 * gamma_oil)) * (70**(-1.163)))) - 1
        # Расчет вязкости дегазированной нефти для 80 F
        oil_deadviscosity_beggs_80 = (10**(
            (10**(3.0324 - 0.02023 * gamma_oil)) * (80**(-1.163)))) - 1
        # Экстраполяция вязкости дегазированной нефти по двум точкам
        c = mt.log10(oil_deadviscosity_beggs_70 /
                     oil_deadviscosity_beggs_80) / mt.log10(80 / 70)
        b = oil_deadviscosity_beggs_70 * 70**c
        oil_deadviscosity_beggs = 10**(mt.log10(b) - c * mt.log10(t))
    else:
        x = (10**(3.0324 - 0.02023 * gamma_oil)) * (t**(-1.163))
        oil_deadviscosity_beggs = (10**x) - 1
    return oil_deadviscosity_beggs


def _oil_liveviscosity_beggs(oil_deadvisc, rs):
    """
    Метод расчета вязкости нефти, насыщенной газом, по корреляции Beggs
    Parameters
    ----------
    :param oil_deadvisc: вязкость дегазированной нефти, сПз
    :param rs: газосодержание, (м3/м3)
    :return: вязкость, насыщенной газом нефти, сПз
    -------
    """
    # Конвертация газосодержания в куб. футы/баррель
    rs_new = rs / 0.17810760667903522

    a = 10.715 * (rs_new + 100)**(-0.515)
    b = 5.44 * (rs_new + 150)**(-0.338)
    oil_liveviscosity_beggs = a * oil_deadvisc**b
    return oil_liveviscosity_beggs


def _gas_viscosity_lee(t: float, gamma_gas: float, rho_gas: float) -> float:
    """
    Метод расчета вязкости газа по корреляции Lee
    Parameters
    ----------
    :param t: температура, К
    :param gamma_gas: относительная плотность газа, доли,
    (относительно в-ха с плотностью 1.2217 кг/м3 при с.у.)
    :param rho_gas: плотность газа при данном давлении температуре, кг/м3
    :return: вязкость газа, сПз
    -------
    """
    t_r = t * 1.8

    a = (7.77 + 0.183 * gamma_gas) * t_r**1.5 / (122.4 + 373.6 * gamma_gas +
                                                 t_r)
    b = 2.57 + 1914.5 / t_r + 0.275 * gamma_gas
    c = 1.11 + 0.04 * b
    gas_viscosity = 10**(-4) * a * mt.exp(b * (rho_gas / 1000)**c)
    return gas_viscosity


def _calc_mul(muo, muw, wc_rc):
    return muo * (1 - wc_rc) + muw * wc_rc


def _calc_mum(mul, mug, gf):
    return gf * mug + (1 - gf) * mul


def calc_pvt(p, t, gamma_gas, gamma_oil, gamma_wat, wct, rp, q_fluid):
    q_fluid /= 86400
    rp *= gamma_oil
    rs = _calc_rs(gamma_gas, gamma_oil, p, t)
    bo = _calc_bo(rs, gamma_gas, gamma_oil, t)
    rho_oil = _calc_oil_density(gamma_oil, rs, gamma_gas, bo)

    bg = _calc_bg(p, t, 1)
    rho_gas = _calc_gas_density(gamma_gas, bg)
    muod = _oil_deadviscosity_beggs(gamma_oil, t)
    muo = _oil_liveviscosity_beggs(muod, rs)
    mug = _gas_viscosity_lee(t, gamma_gas, rho_gas)

    qg = _calc_qg(q_fluid, wct, rp, rs, bg)
    qo = _calc_qo(q_fluid, wct, bo)
    qw = _calc_qw(q_fluid, wct)
    ql = _calc_ql(qw, qo)
    qm = _calc_qm(ql, qg)

    gf = _calc_gf(qg, qm)
    wc_rc = qw / ql
    mul = _calc_mul(muo, 1, wc_rc)
    mum = _calc_mum(mul, mug, gf)
    rho_mix = _calc_rho_mix(rho_oil, rho_gas, gamma_wat * 1000, wct, gf)
    return qm, rho_mix, mum
