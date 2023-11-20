from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt5.QtGui import QPixmap, QPen
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsLineItem, QGraphicsEllipseItem, \
    QMessageBox


class HandleItem(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super().__init__(-10, -10, 20, 20, parent)
        self.setBrush(Qt.red)

    def mousePressEvent(self, event):
        self.setSelected(True)
        super().mousePressEvent(event)


class DraggableLineItem(QGraphicsLineItem):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.handle = HandleItem(self)
        self.__initUi()
        self.updateHandlePosition()

    def updateHandlePosition(self):
        line = self.line()
        center_x = (line.x1() + line.x2()) / 2
        center_y = (line.y1() + line.y2()) / 2

        self.handle.setPos(center_x, center_y)

    def __initUi(self):
        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setPen(QPen(Qt.black, 10, Qt.DashDotLine))

    def updateHeight(self, new_height):
        self.setLine(self.line().x1(), 0, self.line().x2(), new_height)
        self.updateHandlePosition()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.updateHandlePosition()
        cur_x = self.scene().itemsBoundingRect().x()
        new_x = self.x()
        if new_x > self.scene().sceneRect().width():
            new_x = self.scene().sceneRect().width()
            self.setPos(new_x, 0)
        elif cur_x < 0:
            new_x = 0
            self.setPos(new_x, 0)
        else:
            self.setPos(new_x, 0)


from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPainterPath


class ClippablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, line_item, side, parent=None):
        super().__init__(pixmap, parent)
        self.line_item = line_item
        self.side = side  # 'left' or 'right'

    def updateLine(self, line_item):
        self.line_item = line_item

    def paint(self, painter, option, widget):
        # Create a path that represents the visible area of this pixmap
        clip_path = QPainterPath()
        line_x = self.line_item.x()
        scene_rect = self.scene().sceneRect()

        if self.side == 'left':
            clip_rect = QRectF(scene_rect.topLeft(), QPointF(line_x, scene_rect.bottom()))
            clip_path.addRect(clip_rect)
        elif self.side == 'right':
            clip_rect = QRectF(QPointF(line_x, scene_rect.top()), scene_rect.bottomRight())
            clip_path.addRect(clip_rect)

        painter.setClipPath(clip_path)
        super().paint(painter, option, widget)


class SplittedImageView(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__aspectRatioMode = Qt.KeepAspectRatio
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__scene = QGraphicsScene(self)
        self.__p_left = QPixmap()
        self.__p_right = QPixmap()
        self.__item_left = ''
        self.__item_right = ''
        self.__line = None
        self.__min_width = 300
        self.__min_height = 300

    def __initUi(self):
        self.setMinimumSize(self.__min_width, self.__min_height)
        self.__scene.setSceneRect(0, 0, self.__min_width, self.__min_height)

        self.__line = DraggableLineItem(0, 0, 0, self.height())
        self.__line.setZValue(1)
        self.__scene.addItem(self.__line)
        self.setScene(self.__scene)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def __refresh_scene_size(self):
        new_scene_width = max(self.__p_left.width(), self.__p_right.width())
        new_scene_height = max(self.__p_left.height(), self.__p_right.height())
        self.__scene.setSceneRect(0, 0, new_scene_width, new_scene_height)

    def __refresh_line(self):
        if self.__line:
            if self.__line.x() > self.__scene.width():
                self.__line.setX(0)
            self.__line.setLine(self.__line.line().x1(), 0, self.__line.line().x2(), self.__scene.height())
            self.__line.updateHandlePosition()

    def setFilenameToLeft(self, filename):
        pixmap = QPixmap(filename)
        if pixmap.width() < self.__min_width or pixmap.height() < self.__min_height:
            QMessageBox.information(self, 'Notification', f'Image is too small. Must be at least {self.__min_width}x{self.__min_height}.')
            return

        if self.__item_left:
            self.__scene.removeItem(self.__item_left)

        self.__p_left = pixmap
        self.__item_left = ClippablePixmapItem(self.__p_left, self.__line, 'left')
        self.__scene.addItem(self.__item_left)
        self.__item_left.setTransformationMode(Qt.SmoothTransformation)
        self.__item_left.setPos(0, 0)

        self.__refresh_scene_size()
        self.__refresh_line()

        self.setScene(self.__scene)
        self.fitInView(self.__scene.sceneRect(), self.__aspectRatioMode)

    def setFilenameToRight(self, filename):
        pixmap = QPixmap(filename)
        if pixmap.width() < self.__min_width or pixmap.height() < self.__min_height:
            QMessageBox.information(self, 'Notification', f'Image is too small. Must be at least {self.__min_width}x{self.__min_height}.')
            return

        if self.__item_right:
            self.__scene.removeItem(self.__item_right)

        self.__p_right = pixmap
        self.__item_right = ClippablePixmapItem(self.__p_right, self.__line, 'right')
        self.__scene.addItem(self.__item_right)
        self.__item_right.setTransformationMode(Qt.SmoothTransformation)
        self.__item_right.setPos(0, 0)

        self.__refresh_scene_size()
        self.__refresh_line()

        self.setScene(self.__scene)
        self.fitInView(self.__scene.sceneRect(), self.__aspectRatioMode)

    def removeItemOnTheLeft(self):
        if self.__item_left:
            self.__scene.removeItem(self.__item_left)
            self.__item_left = ''

    def removeItemOnTheRight(self):
        if self.__item_right:
            self.__scene.removeItem(self.__item_right)
            self.__item_right = ''

    def setAspectRatioMode(self, mode):
        self.__aspectRatioMode = mode

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if self.__line or self.__item_left or self.__item_right:
            self.fitInView(self.sceneRect(), self.__aspectRatioMode)