from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QTimer
import sys, random


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.rocketX = 250
        self.rocketY = 570
        self.scores = 0
        self.setFixedSize(600, 600)
        self.setWindowTitle('Rocket')
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()
        self.attack()

    def mainDesign(self):
        self.rocket = QLabel()
        self.rocket.setStyleSheet("background-color:black;")
        self.rocket.setMaximumSize(100, 50)

        self.defenseBtn = QPushButton()
        self.defenseBtn.clicked.connect(self.defense)
        self.defenseBtn.hide()

        self.timer = QTimer()
        self.timer.setInterval(4500)
        self.timer.timeout.connect(self.attack)
        self.timer.start()

        self.collisionDetection = QTimer()
        self.collisionDetection.setInterval(100)
        self.collisionDetection.timeout.connect(self.funcDetectCollision)
        self.collisionDetection.start()


        self.frame1 = QWidget()
        self.frame1.setStyleSheet("background-color:black; border-radius:15px;")

        self.frame2 = QWidget()
        self.frame2.setStyleSheet("background-color:red; border-radius:15px;")

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QVBoxLayout()

        self.bottomLayout.addStretch()
        self.bottomLayout.addWidget(self.frame1)
        self.bottomLayout.addWidget(self.frame2)
        self.bottomLayout.addWidget(self.rocket)

        self.mainLayout.addLayout(self.topLayout, 5)
        self.mainLayout.addLayout(self.bottomLayout, 95)
        self.setLayout(self.mainLayout)

    
    def keyPressEvent(self, e):
        speed = 15
        if self.rocketX <= self.width() - 110:
            if e.key() == Qt.Key_Right:
                self.rocketX += speed
                self.rocket.move(self.rocketX, self.rocketY)
        if self.rocketX >= 0:
            if e.key() == Qt.Key_Left:
                self.rocketX -= speed
                self.rocket.move(self.rocketX, self.rocketY)
        
        if e.key() == Qt.Key_A:     #press 'a' to attack square
            self.defenseBtn.click()

    def defense(self):
        self.animation1 = QPropertyAnimation(self.frame1, b"geometry")
        self.animation1.setDuration(1000)
        self.animation1.setStartValue(QRect(self.rocketX + 30, self.rocketY, 30, 30))
        self.animation1.setEndValue(QRect(self.rocketX + 30, -70, 30, 30))
        self.animation1.start()

    def attack(self):
        randX = random.randint(40, 560)
        self.animation2 = QPropertyAnimation(self.frame2, b"geometry")
        self.animation2.setDuration(4500)
        self.animation2.setStartValue(QRect(randX,  0, 50, 50))
        self.animation2.setEndValue(QRect(randX, 1000, 50, 50))
        self.animation2.start()

    def funcDetectCollision(self):
        if ((self.frame2.x() + 30 >= self.frame1.x() and self.frame2.x() - 30 <= self.frame1.x()) and (self.frame2.y() + 30 >= self.frame1.y() and self.frame2.y() - 30 <= self.frame1.y())):
            self.scores += 1
            self.attack()
        elif self.frame2.y() >= 600:
            self.timer.stop()
            self.collisionDetection.stop()
            QMessageBox.information(self, "Game over", f"You lost! Your scores: {self.scores}")
            sys.exit()          


def main():
    app = QApplication(sys.argv)
    window = Window()
    app.exec_()

if __name__ == '__main__':
    main()