from krita import Krita, DockWidget # type: ignore
from .flowlayout import FlowLayout

try:
    from PyQt6.QtCore import Qt, QSize, QPointF
    from PyQt6.QtWidgets import QWidget, QPushButton, QScrollArea, QSizePolicy
    from PyQt6.QtGui import QPixmap, QPainter, QIcon, QColor
except ImportError:  # Krita 5
    from PyQt5.QtCore import Qt, QSize, QPointF
    from PyQt5.QtWidgets import QWidget, QPushButton, QScrollArea, QSizePolicy
    from PyQt5.QtGui import QPixmap, QPainter, QIcon, QColor


SIZES = [ 
          3, 5, 8, 10, 11, 12, 
          13, 14, 15, 17, 20, 21,
          22, 23, 24, 25, 26, 27,
          30, 35, 40, 45, 50, 55,
          60, 70, 80, 90, 100, 120 
        ]
BTN = 40  # image and button size in pixels

class BrushSizesMatrixDocker(DockWidget):

    # runs at krita startup
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brush sizes")

        root = QWidget()
        btn_layout = FlowLayout(root) # inner layout

        for size in SIZES:
            btn = QPushButton()
            btn.setIcon(self.brush_icon(size))
            btn.setIconSize(QSize(BTN, BTN))
            btn.setFixedSize(BTN, BTN)
            btn.setToolTip(str(size))
            btn.setStyleSheet("padding: 0; border: none;")
            btn.clicked.connect(lambda _checked=False, s=size: self.set_size(s))
            btn_layout.addWidget(btn)

        scroll = QScrollArea()
        scroll.setWidget(root)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(scroll)

    # default override method
    def canvasChanged(self, canvas):
        pass
    def setGeometry(self, rect):
        super().setGeometry(rect)
        height = self._do_layout(rect, False)
        parent = self.parentWidget()
        if parent is not None and parent.minimumHeight() != height:
            parent.setMinimumHeight(height)

    def run_action(self, name):
        action = Krita.instance().action(name)
        if action:
            action.trigger()

    def set_size(self, size):
        window = Krita.instance().activeWindow()
        view = window.activeView() if window else None
        if view:
            view.setBrushSize(float(size))

    def brush_icon(self, size, max_size=max(SIZES), px=BTN):
        pm = QPixmap(px, px)
        pm.fill(QColor("black"))

        # diameter scales linearly so the biggest brush nearly fills the image
        # never go below 1px, otherwise tiny brushes would be invisible
        diameter = max(1.0, size / max_size * (px - 1))

        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("white"))
        c = px / 2
        p.drawEllipse(QPointF(c, c), diameter / 2, diameter / 2)
        p.end()  # must finish painting before using the pixmap

        return QIcon(pm)
