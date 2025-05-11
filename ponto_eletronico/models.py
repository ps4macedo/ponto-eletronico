from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class UserConfig:
    total_work_hours: float               # só 6.0 ou 8.0
    two_shifts: bool                      # True = dois turnos
    break_duration: Optional[int] = None  # minutos (30, 60 ou 180)
    overtime_allowed: bool = False
    max_overtime_hours: Optional[float] = None  # limite diário de hora-extra

@dataclass(frozen=True)
class ShiftTimes:
    entry: datetime
    break_start: Optional[datetime]
    break_end: Optional[datetime]
    exit: datetime
