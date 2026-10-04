from krita import Krita, DockWidget # type: ignore
from .flowlayout import FlowLayout

try:
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QWidget, QPushButton, QScrollArea, QSizePolicy
except ImportError:  # Krita 5
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QPushButton, QScrollArea, QSizePolicy


SIZES = [ 
          2, 5, 8, 10, 
          11, 12, 13, 14, 15, 17, 20, 
          25, 30, 35, 40, 45, 50,
          60, 70, 80, 90, 100 
        ]

class BrushSizesMatrixDocker(DockWidget):

    # runs at krita startup
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brush sizes")

        root = QWidget()
        btn_layout = FlowLayout(root) # inner layout

        for size in SIZES:
            btn = QPushButton(str(size))
            btn.setFixedSize(40, 40)
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

    def run_action(self, name):
        action = Krita.instance().action(name)
        if action:
            action.trigger()

    def set_size(self, size):
        window = Krita.instance().activeWindow()
        view = window.activeView() if window else None
        if view:
            view.setBrushSize(float(size))
