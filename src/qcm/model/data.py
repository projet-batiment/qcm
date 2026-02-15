from dataclasses import dataclass, field

from qcm.model.qcm import Qcm
from qcm.model.tentative import Tentative


@dataclass
class QcmData:
    """
    Représente un qcm accompagné de ses tentatives.
    """

    qcm: Qcm = field(default_factory=Qcm)
    tentatives: list[Tentative] = field(default_factory=list)
