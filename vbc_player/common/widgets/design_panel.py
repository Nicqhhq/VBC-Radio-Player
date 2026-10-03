"""Elementos do Figma em painéis Qt, com controles nativos nos seus slots."""
import json
from copy import deepcopy

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPainter, QPen
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QPushButton, QWidget

from vbc_player.theme import ASSETS, DESIGN


def descendants(node):
    yield node
    for child in node.get("c", []):
        yield from descendants(child)


class DesignPanel(QWidget):
    _components = None
    _asset_map = None
    _renderers = {}

    def __init__(self, component_id, parent=None):
        super().__init__(parent)
        if DesignPanel._components is None:
            components = [
                node
                for i in range(4)
                for node in json.loads(
                    (DESIGN / f"geometry-{i}.json").read_text(encoding="utf-8")
                )
            ]
            DesignPanel._components = {node["id"]: node for node in components}
            DesignPanel._asset_map = json.loads((DESIGN / "assets.json").read_text())
            for asset in set(DesignPanel._asset_map.values()):
                path = ASSETS / "figma" / asset
                renderer = QSvgRenderer(str(path))
                if not path.is_file() or not path.stat().st_size or not renderer.isValid():
                    raise RuntimeError(f"SVG inválido ou ausente: {path}")
                DesignPanel._renderers[asset] = renderer
        self.design = deepcopy(self._components[component_id])
        self.nodes = {n["id"]: n for n in descendants(self.design)}
        self.origin_x, self.origin_y, self.design_width, self.design_height = self.design["b"]
        self.hidden = set()
        self.overlays = []
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def local_rect(self, node_id, rendered=False):
        node = self.nodes[node_id]
        x, y, w, h = node.get("r" if rendered else "b") or node["b"]
        return QRectF(x - self.origin_x, y - self.origin_y, w, h)

    def set_text(self, node_id, text):
        self.nodes[node_id]["t"] = str(text)
        self.update()

    def add_control(self, widget, rect):
        widget.setParent(self)
        self.overlays.append((widget, QRectF(*rect) if isinstance(rect, tuple) else QRectF(rect)))
        self._place_controls()
        return widget

    def button(self, label, rect, callback, checkable=False):
        button = QPushButton(self)
        button.setAccessibleName(label)
        button.setToolTip(label)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setCheckable(checkable)
        button.setStyleSheet("QPushButton {background: transparent; border: 1px solid transparent; padding:0;} QPushButton:hover {background:rgba(100,160,230,24); border:1px solid #345c92;} QPushButton:pressed {background:rgba(100,160,230,50);} QPushButton:focus {border:1px solid #60a5fa;} QPushButton:checked {border:1px solid #4ce0ae;}")
        button.clicked.connect(callback)
        return self.add_control(button, rect)

    def _place_controls(self):
        sx, sy = self.width() / self.design_width, self.height() / self.design_height
        for widget, rect in self.overlays:
            widget.setGeometry(round(rect.x()*sx), round(rect.y()*sy), round(rect.width()*sx), round(rect.height()*sy))

    def resizeEvent(self, event):
        self._place_controls()
        super().resizeEvent(event)

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.scale(self.width() / self.design_width, self.height() / self.design_height)
        try:
            self._paint_node(painter, self.design)
        finally:
            painter.end()

    def _paint_node(self, painter, node):
        if node["id"] in self.hidden:
            return
        painter.save()
        painter.setOpacity(painter.opacity() * node.get("o", 1))
        rect = self.local_rect(node["id"])
        asset = self._asset_map.get(node["id"])
        if asset:
            self._renderers[asset].render(painter, self.local_rect(node["id"], rendered=True))
        elif node["type"] == "TEXT":
            font = QFont(node.get("f", "Inter"))
            font.setPixelSize(round(node.get("s", 12)))
            font.setWeight(QFont.Weight(node.get("w", 400)))
            painter.setFont(font)
            painter.setPen(QColor(node.get("fill") or "#cbd5e1"))
            metrics = QFontMetricsF(font)
            text = metrics.elidedText(node["t"], Qt.TextElideMode.ElideRight, rect.width()+2)
            flags = {"LEFT": Qt.AlignmentFlag.AlignLeft, "CENTER": Qt.AlignmentFlag.AlignHCenter, "RIGHT": Qt.AlignmentFlag.AlignRight}.get(node.get("a"), Qt.AlignmentFlag.AlignLeft)
            painter.drawText(rect.adjusted(0, -1, 2, 2), flags | Qt.AlignmentFlag.AlignVCenter, text)
        elif node.get("fill") or node.get("stroke"):
            painter.setBrush(QColor(node["fill"]) if node.get("fill") else Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(node["stroke"]), node.get("sw", 1)) if node.get("stroke") else Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, node.get("radius", 0), node.get("radius", 0))
        if not asset:
            for child in node.get("c", []):
                self._paint_node(painter, child)
        painter.restore()
