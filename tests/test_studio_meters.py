import os
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtGui import QColor, QFontDatabase
from PySide6.QtWidgets import QApplication

from vbc_player.pages.player.widgets.clock import StudioClockWidget
from vbc_player.services.playback import PlaybackService
from vbc_player.theme import ASSETS


class StudioMetersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        QFontDatabase.addApplicationFont(str(ASSETS / "fonts/Inter.ttf"))

    def setUp(self):
        self.service = PlaybackService()
        self.clock = StudioClockWidget(self.service)
        self.clock.resize(236, 236)

    def tearDown(self):
        self.clock.close()
        self.clock.deleteLater()
        self.service.player.stop()
        self.service.deleteLater()
        self.app.processEvents()

    def advance(self, elapsed):
        now = self.clock._last_animation_time + elapsed
        with patch("vbc_player.pages.player.widgets.clock.monotonic", return_value=now):
            self.clock._animate_meters()

    def test_stereo_signal_drives_separate_bars_in_original_slots(self):
        self.assertEqual(self.clock.meter_levels, [-60, -60])
        self.service.audio.stereo_levels_changed.emit(-6, -float("inf"))
        self.advance(.2)
        self.assertGreater(self.clock.meter_levels[0], -7)
        self.assertEqual(self.clock.meter_levels[1], -60)
        image = self.clock.grab().toImage()
        self.assertEqual(image.pixelColor(70, 150), QColor("#22c55e"))
        self.assertEqual(image.pixelColor(70, 178), QColor("#1f2937"))
        self.clock.grab().save("/tmp/vbc-studio-meters.png")

    def test_silence_and_stalled_decoder_release_to_empty_bars(self):
        self.service.audio.stereo_levels_changed.emit(-6, -18)
        self.advance(.15)
        previous = list(self.clock.meter_levels)
        self.service.audio.stereo_levels_changed.emit(-float("inf"), -float("inf"))
        self.advance(.1)
        self.assertGreater(self.clock.meter_levels[0], -60)
        self.assertLess(self.clock.meter_levels[0], previous[0])
        self.advance(2)
        self.assertEqual(self.clock.meter_levels, [-60, -60])
        self.service.audio.stereo_levels_changed.emit(-3, -9)
        # Mesmo sem sinal de reset, ausência de blocos novos limpa a leitura.
        self.advance(3)
        self.assertEqual(self.clock._targets, [-60, -60])
        self.assertEqual(self.clock.meter_levels, [-60, -60])

    def test_master_label_tracks_real_volume_and_mute(self):
        self.service.output.setVolume(.5)
        self.assertEqual(self.clock.nodes["17:458"]["t"], "MASTER -6.0 dB")
        self.service.output.setVolume(0)
        self.assertEqual(self.clock.nodes["17:458"]["t"], "MASTER MUDO")


if __name__ == "__main__":
    unittest.main()
