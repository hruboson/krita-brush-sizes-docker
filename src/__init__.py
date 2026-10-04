from krita import Krita, DockWidgetFactory, DockWidgetFactoryBase # type: ignore
from .docker import BrushSizesMatrixDocker

DOCKER_ID = "brush_sizes_matrix"

Krita.instance().addDockWidgetFactory(
    DockWidgetFactory(DOCKER_ID, DockWidgetFactoryBase.DockRight, BrushSizesMatrixDocker)
)
