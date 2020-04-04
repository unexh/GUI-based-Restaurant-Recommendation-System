from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd

csvFileLink = r'C:\Users\Unex H\Desktop\Ai Project\GUI-based-Restaurant-Recommendation-System\zomato.csv'

global DataFieldWhole 
DataFieldWhole = pd.read_csv(csvFileLink,encoding='latin')

backgroundImageLink = r'C:\Users\Unex H\Desktop\Ai Project\GUI-based-Restaurant-Recommendation-System\images\sizller-with-noodles22.jpg'
searchIconLink = r'C:\Users\Unex H\Desktop\Ai Project\GUI-based-Restaurant-Recommendation-System\images\icons8-search-50(2).png'

class Ui_MainWindow(object):
    selectedCityName=selectedLocalityName=selectedRestaurantName=str("")
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1180, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1180, 700))
        MainWindow.setMaximumSize(QtCore.QSize(1180, 700))
        MainWindow.setMouseTracking(False)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(243, 243, 243);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.centralwidget.setFont(font)

        self.LBackgroundImage = QtWidgets.QLabel(self.centralwidget)
        self.LBackgroundImage.setGeometry(QtCore.QRect(0, 0, 1180, 511))
        self.LBackgroundImage.setToolTip("")
        self.LBackgroundImage.setText("")
        self.LBackgroundImage.setPixmap(QtGui.QPixmap(backgroundImageLink))
        self.LBackgroundImage.setScaledContents(True)
        self.LBackgroundImage.setObjectName("LBackgroundImage")

        self.LMainBanner = QtWidgets.QLabel(self.centralwidget)
        self.LMainBanner.setGeometry(QtCore.QRect(190, 80, 791, 161))
        self.LMainBanner.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"Microsoft YaHei UI\";")
        self.LMainBanner.setObjectName("LMainBanner")

        self.cBCity = QtWidgets.QComboBox(self.centralwidget)
        self.cBCity.setGeometry(QtCore.QRect(60, 360, 231, 31))
        self.cBCity.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.cBCity.setStyleSheet("font: 9pt \"Microsoft YaHei UI\";\n"
"border: 1px solid gray;\n"
"border-radius: 5px;\n"
"padding: 3px 3px 3px 3px;")
        self.cBCity.setEditable(True)
        self.cBCity.setIconSize(QtCore.QSize(16, 16))
        self.cBCity.setFrame(False)
        self.cBCity.setObjectName("cBCity")
        self.cBCity.addItem("")

        self.cBlocality = QtWidgets.QComboBox(self.centralwidget)
        self.cBlocality.setGeometry(QtCore.QRect(330, 360, 251, 31))
        self.cBlocality.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.cBlocality.setStyleSheet("font: 9pt \"Microsoft YaHei UI\";\n"
"border: 1px solid gray;\n"
"border-radius: 5px;\n"
"padding: 3px 3px 3px 3px;")
        self.cBlocality.setEditable(True)
        self.cBlocality.setFrame(False)
        self.cBlocality.setObjectName("cBlocality")
        self.cBlocality.addItem("")

        self.cBRestaurant = QtWidgets.QComboBox(self.centralwidget)
        self.cBRestaurant.setGeometry(QtCore.QRect(630, 360, 441, 31))
        self.cBRestaurant.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.cBRestaurant.setStyleSheet("font: 9pt \"Microsoft YaHei UI\";\n"
"border: 1px solid gray;\n"
"border-radius: 5px;\n"
"padding: 3px 3px 3px 3px;")
        self.cBRestaurant.setEditable(True)
        self.cBRestaurant.setFrame(False)
        self.cBRestaurant.setObjectName("cBRestaurant")
        self.cBRestaurant.addItem("")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(90, 510, 981, 351))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.LTopRestaurants = QtWidgets.QLabel(self.frame)
        self.LTopRestaurants.setGeometry(QtCore.QRect(30, 20, 891, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setFamily("Microsoft YaHei UI")
        self.LTopRestaurants.setFont(font)
        self.LTopRestaurants.setStyleSheet("color: rgb(36, 36, 36);\n"
"")
        self.LTopRestaurants.setObjectName("LTopRestaurants")

        self.LRestaurantStar1 = QtWidgets.QLabel(self.frame)
        self.LRestaurantStar1.setGeometry(QtCore.QRect(100, 130, 47, 13))
        self.LRestaurantStar1.setObjectName("LRestaurantStar1")
        self.LRestaurantStar2 = QtWidgets.QLabel(self.frame)
        self.LRestaurantStar2.setGeometry(QtCore.QRect(290, 130, 47, 13))
        self.LRestaurantStar2.setObjectName("LRestaurantStar2")
        self.LRestaurantStar3 = QtWidgets.QLabel(self.frame)
        self.LRestaurantStar3.setGeometry(QtCore.QRect(470, 130, 47, 13))
        self.LRestaurantStar3.setObjectName("LRestaurantStar3")
        self.LRestaurantStar4 = QtWidgets.QLabel(self.frame)
        self.LRestaurantStar4.setGeometry(QtCore.QRect(650, 130, 47, 13))
        self.LRestaurantStar4.setObjectName("LRestaurantStar4")
        self.LRestaurantStar5 = QtWidgets.QLabel(self.frame)
        self.LRestaurantStar5.setGeometry(QtCore.QRect(840, 130, 47, 13))
        self.LRestaurantStar5.setObjectName("LRestaurantStar5")

        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 100, 881, 26))
        self.layoutWidget.setObjectName("layoutWidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.BRestaurant1 = QtWidgets.QPushButton(self.layoutWidget)
        self.BRestaurant1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BRestaurant1.setObjectName("BRestaurant1")
        self.horizontalLayout.addWidget(self.BRestaurant1)
        self.BRestaurant2 = QtWidgets.QPushButton(self.layoutWidget)
        self.BRestaurant2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BRestaurant2.setObjectName("BRestaurant2")
        self.horizontalLayout.addWidget(self.BRestaurant2)
        self.BRestaurant3 = QtWidgets.QPushButton(self.layoutWidget)
        self.BRestaurant3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BRestaurant3.setObjectName("BRestaurant3")
        self.horizontalLayout.addWidget(self.BRestaurant3)
        self.BRestaurant4 = QtWidgets.QPushButton(self.layoutWidget)
        self.BRestaurant4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BRestaurant4.setObjectName("BRestaurant4")
        self.horizontalLayout.addWidget(self.BRestaurant4)
        self.BRestaurant5 = QtWidgets.QPushButton(self.layoutWidget)
        self.BRestaurant5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BRestaurant5.setObjectName("BRestaurant5")

        self.horizontalLayout.addWidget(self.BRestaurant5)
        self.lineSeparator = QtWidgets.QFrame(self.frame)
        self.lineSeparator.setGeometry(QtCore.QRect(20, 60, 921, 16))
        self.lineSeparator.setStyleSheet("")
        self.lineSeparator.setFrameShape(QtWidgets.QFrame.HLine)
        self.lineSeparator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineSeparator.setObjectName("lineSeparator")

        self.bSearch = QtWidgets.QPushButton(self.centralwidget)
        self.bSearch.setGeometry(QtCore.QRect(1070, 350, 41, 51))
        self.bSearch.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bSearch.setToolTip("")
        self.bSearch.setStyleSheet("border-radius: 5px;\n"
"background-color: rgb(0, 0, 0);")
        self.bSearch.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(searchIconLink), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bSearch.setIcon(icon)
        self.bSearch.setIconSize(QtCore.QSize(30, 30))
        self.bSearch.setObjectName("bSearch")
        self.frame.raise_()
        self.LBackgroundImage.raise_()
        self.LMainBanner.raise_()
        self.cBCity.raise_()
        self.cBlocality.raise_()
        self.bSearch.raise_()
        self.cBRestaurant.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Brasserie"))

        self.LMainBanner.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; font-weight:600; color:#55aa00;\">B</span><span style=\" font-size:36pt; font-weight:600; color:#ffffff;\">rasserie</span></p><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; color:#55aa00; vertical-align:sub;\">Ai</span><span style=\" font-size:18pt; font-weight:600; color:#ffffff; vertical-align:sub;\">-powered Restaurant </span><span style=\" font-size:18pt; font-weight:600; color:#55aa00; vertical-align:sub;\">recommendation engine</span></p></body></html>"))
        
        self.cBCity.setToolTip(_translate("MainWindow", "Enter City Name !"))
        self.cBCity.setCurrentText(_translate("MainWindow", "City"))
        self.cBCity.setItemText(0, _translate("MainWindow", "City"))
        self.cBCity.addItems(self.ReturnCityName())
        self.cBCity.currentTextChanged.connect(self.UpdateLocalityName)

        self.cBlocality.setToolTip(_translate("MainWindow", "Enter Locality Name in that City !"))
        self.cBlocality.setCurrentText(_translate("MainWindow", "Locality"))
        self.cBlocality.setItemText(0, _translate("MainWindow", "Locality"))
        self.cBlocality.addItems(self.ReturnLocalityName())
        self.cBlocality.currentTextChanged.connect(self.UpdateRestaurantName)
        
        self.cBRestaurant.setToolTip(_translate("MainWindow", "Enter Restaurant Name !"))
        self.cBRestaurant.setCurrentText(_translate("MainWindow", "Restaurant Name"))
        self.cBRestaurant.setItemText(0, _translate("MainWindow", "Restaurant Name"))
        self.cBRestaurant.addItems(self.ReturnRestaurantName())

        self.bSearch.clicked.connect(self.ShowResults)

        self.LTopRestaurants.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; font-weight:600; color:#1b1b1b;\">Top </span><span style=\" font-size:20pt; font-weight:600; color:#55aa00;\">Restaurants</span></p></body></html>"))

        self.LRestaurantStar1.setText(_translate("MainWindow", "Stars"))
        self.LRestaurantStar2.setText(_translate("MainWindow", "Stars"))
        self.LRestaurantStar3.setText(_translate("MainWindow", "Stars"))
        self.LRestaurantStar4.setText(_translate("MainWindow", "Stars"))
        self.LRestaurantStar5.setText(_translate("MainWindow", "Stars"))

        self.BRestaurant1.setText(_translate("MainWindow", "Restaurant Name"))
        self.BRestaurant2.setText(_translate("MainWindow", "Restaurant Name"))
        self.BRestaurant3.setText(_translate("MainWindow", "Restaurant Name"))
        self.BRestaurant4.setText(_translate("MainWindow", "Restaurant Name"))
        self.BRestaurant5.setText(_translate("MainWindow", "Restaurant Name"))

        
    def ReturnCityName(self):
        CityData = list(DataFieldWhole['City'].unique())
        #print(CityData)
        CityData.sort()
        #print(CityData)
        return CityData

    def UpdateLocalityName(self):
        self.cBlocality.clear()
        self.cBlocality.addItems(self.ReturnLocalityName())

    def ReturnLocalityName(self):
        self.selectedCityName = str(self.cBCity.currentText())
        """
        if(cityNameSelected == 'City'):
            #throwError
            print("CityName value can't be == City")
        """
        print(self.selectedCityName)
        DataFieldWholeTemp = DataFieldWhole[DataFieldWhole['City']==self.selectedCityName]
        localityData = list(DataFieldWholeTemp['Locality'].unique())
        #print(localityData)
        localityData.sort()
        #print(localityData)
        return localityData

    def UpdateRestaurantName(self):
        self.cBRestaurant.clear()
        self.cBRestaurant.addItems(self.ReturnRestaurantName())

    def ReturnRestaurantName(self):
        self.selectedCityName = str(self.cBCity.currentText())
        self.selectedLocalityName = str(self.cBlocality.currentText())
        """
        if(cityNameSelected == 'City'):
            #throwError
            print("CityName value can't be == City")
        """
        #print(self.selectedCityName)
        #print(self.selectedLocalityName)
        DataFieldWholeTemp = DataFieldWhole[(DataFieldWhole['City']==self.selectedCityName) & (DataFieldWhole['Locality']==self.selectedLocalityName)]
        RestaurantData = list(DataFieldWholeTemp['Restaurant Name'].unique())
        #print(RestaurantData)
        RestaurantData.sort()
        #print(RestaurantData)
        return RestaurantData

    def ShowResults(self):
        self.selectedRestaurantName = str(self.cBRestaurant.currentText())
        print("button clicked printing results")
        self.CheckValues()

    def CheckValues(self):
        print("City : ",self.selectedCityName)
        print("Locality : ",self.selectedLocalityName)
        print("Restaurant Name : ",self.selectedRestaurantName)

        if(self.selectedCityName=='City'or self.selectedCityName==''\
            or self.selectedLocalityName == 'Locality' or self.selectedLocalityName == ''\
            or self.selectedRestaurantName == 'Restaurant Name' or  self.selectedRestaurantName == ''):
            print("Error, unknownValues/invalidValues found")
        elif(self.selectedRestaurantName not in self.ReturnRestaurantName()):
            print("Error, no Restaurant Found")
        else:
            print("Safe To enter")
            self.ClearScreen()


    def ClearScreen(self):
        print("Resetting All widgets")
        self.centralwidget2 = QtWidgets.QWidget(MainWindow)
        self.centralwidget2.setObjectName("centralwidget2")
        MainWindow.setCentralWidget(self.centralwidget2)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
