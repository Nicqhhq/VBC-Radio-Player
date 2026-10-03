from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DESIGN = ROOT / "design"

STYLESHEET = """
QWidget { background: #0b0f17; color: #cbd5e1; font-family: Inter; font-size: 12px; }
QDialog, QStackedWidget { background: #111827; }
QPushButton { background: #1e293b; border: 1px solid #2b3b52; border-radius: 7px; padding: 9px 14px; }
QPushButton:hover { background: #263750; }
QPushButton:pressed { background: #162238; }
QPushButton:focus { border: 1px solid #60a5fa; }
QLineEdit, QDateTimeEdit, QComboBox, QListWidget, QTableWidget { background: #162238; border: 1px solid #2a3a54; border-radius: 6px; padding: 7px; }
QHeaderView::section { background: #182335; border: 0; padding: 8px; color: #94a3b8; }
QSlider::groove:horizontal { height: 6px; background: #26344a; border-radius: 3px; }
QSlider::sub-page:horizontal { background: #38a3ee; border-radius: 3px; }
QSlider::handle:horizontal { width: 18px; margin: -6px 0; background: #60a5fa; border-radius: 9px; }
QLabel { background: transparent; }
QToolTip { background: #182335; color: #f4f7fc; border: 1px solid #345c92; }
"""
