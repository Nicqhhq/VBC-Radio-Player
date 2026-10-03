from vbc_player.common.widgets.design_panel import DesignPanel


class PlaybackModesWidget(DesignPanel):
    def __init__(self, service, parent=None):
        super().__init__("24:7", parent)
        self.service = service
        self.auto = self.button("Modo automático", self.local_rect("17:462"), lambda: self.set_automatic(True))
        self.manual = self.button("Modo manual", self.local_rect("17:465"), lambda: self.set_automatic(False))
        self.loop = self.button("Repetir lista", self.local_rect("17:474"), lambda value: setattr(service, "loop", value), True)
        self.shuffle = self.button("Reprodução aleatória", self.local_rect("17:476"), lambda value: setattr(service, "shuffle", value), True)
        satellite = self.button("Satélite: conexão externa não configurada", self.local_rect("17:478"), lambda: None)
        satellite.setEnabled(False)
        self.setToolTip("Crossfade: referência visual de 2,5 s. Processamento de mixagem ainda não implementado.")

    def set_automatic(self, enabled):
        self.service.automatic = enabled
        # Swap the existing original button assets without changing their SVGs.
        self.nodes["17:462"]["o"] = 1 if enabled else .45
        self.nodes["17:465"]["o"] = .45 if enabled else 1
        self.manual.setChecked(not enabled)
        self.service.mode_changed.emit()
        self.update()
