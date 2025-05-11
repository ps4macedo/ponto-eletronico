from datetime import datetime, timedelta
from typing import List, Tuple
from ponto_eletronico.models import UserConfig, ShiftTimes

class TimeClockCalculator:
    def __init__(self, cfg: UserConfig):
        self.cfg = cfg

    def expected_exit(self, entry: datetime) -> datetime:
        if self.cfg.two_shifts:
            half = timedelta(hours=self.cfg.total_work_hours / 2)
            start_break = entry + half
            end_break = start_break + timedelta(minutes=self.cfg.break_duration or 0)
            return end_break + half
        return entry + timedelta(hours=self.cfg.total_work_hours)

    def worked_and_overtime(
        self, entries: List[datetime], exit_time: datetime
    ) -> Tuple[timedelta, timedelta]:
        total = timedelta()
        for idx, ent in enumerate(entries):
            nxt = entries[idx+1] if idx+1 < len(entries) else exit_time
            total += nxt - ent
        if self.cfg.two_shifts and self.cfg.break_duration:
            total -= timedelta(minutes=self.cfg.break_duration)
        standard = timedelta(hours=self.cfg.total_work_hours)
        if not self.cfg.overtime_allowed or total <= standard:
            return total, timedelta()
        extra = total - standard
        if self.cfg.max_overtime_hours is not None:
            limit = timedelta(hours=self.cfg.max_overtime_hours)
            extra = min(extra, limit)
        return total, extra

    def calculate_shift_times(self, entry: datetime) -> ShiftTimes:
        exit_dt = self.expected_exit(entry)
        if self.cfg.two_shifts:
            half = timedelta(hours=self.cfg.total_work_hours / 2)
            bs = entry + half
            be = bs + timedelta(minutes=self.cfg.break_duration or 0)
            return ShiftTimes(entry, bs, be, exit_dt)
        return ShiftTimes(entry, None, None, exit_dt)
