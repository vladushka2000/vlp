from src.tables.models import WellData, VLP


def get_check_well_data_exists(session, well_data_hash):
    """
    Checks if the well_data table exists.
    
    :param session:
    :param well_data:
    :return:
    """
    well_id = session.query(WellData.id).filter(
        WellData.id == well_data_hash).scalar()

    return well_id


def get_check_vlp_exists(session, well_id):
    """
    Check if the well_id exists in the session
    :param well_id:
    :return:
    """
    vlp = session.query(VLP.vlp).filter(VLP.well_id == well_id).scalar()
    return vlp


def save_init_data(session, init_data, well_data_id):
    well_data = WellData(
        id=well_data_id,
        inclinometry=str(init_data["inclinometry"]),
        d_cas=init_data["casing"]["d"],
        d_tub=init_data["tubing"]["d"],
        h_tub=init_data["tubing"]["h_mes"],
        wct=init_data["pvt"]["wct"],
        rp=init_data["pvt"]["rp"],
        gamma_oil=init_data["pvt"]["gamma_oil"],
        gamma_gas=init_data["pvt"]["gamma_gas"],
        gamma_wat=init_data["pvt"]["gamma_wat"],
        t_res=init_data["pvt"]["t_res"],
        p_wh=init_data["p_wh"],
        geo_grad=init_data["geo_grad"],
        h_res=init_data["h_res"]
    )
    session.add(well_data)
    session.commit()


def save_vlp_data(session, vlp, vlp_id, init_data_id):
    vlp = VLP(
        id=vlp_id,
        vlp=vlp,
        well_id=init_data_id
    )
    session.add(vlp)
    session.commit()
