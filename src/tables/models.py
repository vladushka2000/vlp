import sqlalchemy as sa

from src.db import Base


class WellData(Base):
    __tablename__ = "well_data"

    id = sa.Column(sa.String, primary_key=True,
                   comment="Идентификатор данных скважины")
    inclinometry = sa.Column(sa.String,
                             comment="Инклинометрия: "
                                     "измеренная по стволу глубина, м; "
                                     "вертикальная глубина, м")
    d_cas = sa.Column(sa.Float, comment="Данные по ЭК, м")
    d_tub = sa.Column(sa.Float, comment="Данные по НКТ, м")
    h_tub = sa.Column(sa.Float, comment="Глубина НКТ, м")
    wct = sa.Column(sa.Float, comment="Обводненность, %")
    rp = sa.Column(sa.Float, comment="Газовый фактор, м3/т")
    gamma_oil = sa.Column(sa.Float, comment="Отн. плотность нефти")
    gamma_gas = sa.Column(sa.Float, comment="Отн. плотность газа")
    gamma_wat = sa.Column(sa.Float, comment="Отн. плотность воды")
    t_res = sa.Column(sa.Float, comment="Пластовая температура, C")
    p_wh = sa.Column(sa.Float, comment="Буферное давление, атм")
    geo_grad = sa.Column(sa.Float, comment="Градиент температуры, C/100 м")
    h_res = sa.Column(sa.Float, comment="Глубина Верхних Дыр Перфорации, м")


class VLP(Base):
    __tablename__ = "vlp"

    id = sa.Column(sa.String, primary_key=True,
                   comment="Идентификатор VLP")
    vlp = sa.Column(sa.String,
                    comment="Дебиты жидкости, м3/сут, Забойное давление, атм")
    well_id = sa.Column(sa.String,
                        sa.ForeignKey("well_data.id"),
                        comment="Идентификатор скважины")
