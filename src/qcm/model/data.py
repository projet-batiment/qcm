from qcm.model.qcm import Qcm
from qcm.model.tentative import Tentative

from dataclasses import dataclass, field

@dataclass
class QcmData:
    """
    Représente un qcm accompagné de ses tentatives.
    """

    qcm: Qcm = field(default_factory=Qcm)
    tentatives: list[Tentative] = field(default_factory=list)
