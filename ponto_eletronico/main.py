# ponto_eletronico/main.py

import os
from kivy.lang import Builder
from kivymd.app import MDApp
from datetime import datetime
from ponto_eletronico.models import UserConfig
from ponto_eletronico.services import TimeClockCalculator

class PontoEletronicoApp(MDApp):
    def build(self):
        # Carrega o layout KV
        kv_path = os.path.join(os.path.dirname(__file__), "ui.kv")
        return Builder.load_file(kv_path)

    def on_start(self):
        # Atacha callbacks de ativação dos checkboxes
        self.root.ids.shifts_checkbox.bind(active=self._on_shifts_toggle)
        self.root.ids.ot_checkbox.bind(active=self._on_overtime_toggle)

    def _on_shifts_toggle(self, instance, value):
        # Habilita campo de intervalo somente se marcar dois turnos
        self.root.ids.break_field.disabled = not value

    def _on_overtime_toggle(self, instance, value):
        # Habilita campo de limite de hora-extra se marcado
        self.root.ids.ot_limit_field.disabled = not value

    def show_time_picker(self, which):
        # Abre o seletor de hora do KivyMD
        from kivymd.uix.picker import MDTimePicker
        picker = MDTimePicker()
        picker.bind(on_save=lambda inst, time, dt: self._on_time_selected(which, time))
        picker.open()

    def _on_time_selected(self, which, time):
        # Salva no atributo entry_time ou exit_time
        today = datetime.today()
        dt = datetime(today.year, today.month, today.day, time.hour, time.minute)
        setattr(self, f"{which}_time", dt)
        self.root.ids.result_label.text = f"{which.capitalize()} registrado: {time.hour:02d}:{time.minute:02d}"

    def calculate(self):
        # Lê configurações da UI
        cfg = UserConfig(
            total_work_hours=float(self.root.ids.hours_field.text),
            two_shifts=self.root.ids.shifts_checkbox.active,
            break_duration=int(self.root.ids.break_field.text) if self.root.ids.break_field.text else None,
            overtime_allowed=self.root.ids.ot_checkbox.active,
            max_overtime_hours=float(self.root.ids.ot_limit_field.text) if self.root.ids.ot_limit_field.text else None,
        )
        calc = TimeClockCalculator(cfg)

        # Calcula previsão de saída
        expected = calc.calculate_shift_times(self.entry_time)

        # Se já houver self.exit_time, calcula horas trabalhadas e extras
        result = f"Previsto:\n  Entrada {expected.entry.time()}"
        if expected.break_start:
            result += f"\n  Início intervalo {expected.break_start.time()}"
            result += f"\n  Fim intervalo {expected.break_end.time()}"
        result += f"\n  Saída prevista {expected.exit.time()}"

        if hasattr(self, "exit_time"):
            worked, extra = calc.worked_and_overtime(
                [self.entry_time] + ([self.break_field if cfg.two_shifts else []]),
                self.exit_time
            )
            result += f"\n\nTrabalhado: {worked}\nHora-extra: {extra}"

        self.root.ids.result_label.text = result

if __name__ == "__main__":
    PontoEletronicoApp().run()
