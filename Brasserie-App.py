#importing libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.tokenize import word_tokenize
import sys

#Linking essentials
csvFileLink = r'NewZomato.csv'
backgroundImageLink = r'images\sizller-with-noodles22.jpg'
searchIconLink = r'images\icons8-search-50(2).png'
backGround2ImageLink= r'images\Sitting-near-table-darkened.jpg'
backButtonImageLink =r'images\icons8-back-50.png'


#a class to contain Restaurant Related Data
class RestaurantData:
        #RestaurantData Attributes
        selectedCityName=str("")
        selectedLocalityName=str("")
        selectedRestaurantName=str("")
        DataFieldWhole = pd.read_csv(csvFileLink,encoding='latin')
        tempTopRestaurantDF = None

        #Initializes TopRestuarantDf by calling ReturnTopFiveRestaurantName()
        def __init__(self):
            self.tempTopRestaurantDF = self.ReturnTopFiveRestaurantName()

        #Returns City Name List from Database
        def ReturnCityName(self):
            CityData = list(self.DataFieldWhole['City'].unique())
            CityData.sort()
            return CityData

        #Returns Locality Name List using currentCity from Database
        def ReturnLocalityName(self,currentCity):
            self.selectedCityName = str(currentCity)
            print("SelectedCityName : {}".format(self.selectedCityName))
            DataFieldWholeTemp = self.DataFieldWhole[self.DataFieldWhole['City']==self.selectedCityName]
            localityData = list(DataFieldWholeTemp['Locality'].unique())
            localityData.sort()
            return localityData

        #Returns Restaurant Name List using currentCity,currentLocality from Database
        def ReturnRestaurantName(self,currentCity,currentLocality):
            self.selectedCityName = str(currentCity)
            self.selectedLocalityName = str(currentLocality)
            DataFieldWholeTemp = self.DataFieldWhole[(self.DataFieldWhole['City']==self.selectedCityName) & (self.DataFieldWhole['Locality']==self.selectedLocalityName)]
            RestaurantData = list(DataFieldWholeTemp['Restaurant Name'].unique())
            RestaurantData.sort()
            return RestaurantData

        #Recommendation Function for Calculation of Cosine Similarity Score
        def RestaurantRecommendFunc(self,location,title):
            data_sample = self.data_new_delphi.loc[self.data_new_delphi['Locality'] == location] # data frame

            # index will be reset for cosine similarty index because Cosine similarty index has to be same value with result of tf-idf vectorize
            data_sample.reset_index(level=0, inplace=True)
            #print(data_sample)

            #Feature Extraction
            data_sample['Split']='X'
            for i in range(0,data_sample.index[-1]+1):
                split_data=re.split(r'[,]', data_sample['Cuisines'][i])
                for k,l in enumerate(split_data):
                    split_data[k]=(split_data[k].replace(" ", ""))
                split_data=' '.join(split_data[:])
                data_sample['Split'].iloc[i]=split_data
                
            ## --- TF - IDF Vectorizer---  ##
            #Extracting Stopword
            tfidf = TfidfVectorizer(stop_words='english')

            #Replace NaN for empty string
            data_sample['Split'] = data_sample['Split'].fillna('')

            # Applying TF-IDF Vectorizer
            tfidf_matrix = tfidf.fit_transform(data_sample['Split'])
            tfidf_matrix.shape

            # Using for see Cosine Similarty scores
            feature= tfidf.get_feature_names()

            ## ---Cosine Similarity--- ##()
            # Compute the cosine similarity matrix
            cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

            # Column names are using for index
            corpus_index=[n for n in data_sample['Split']]

            #Construct a reverse map of indices
            indices = pd.Series(data_sample.index, index=data_sample['Restaurant Name']).drop_duplicates()
            #print(indices)

            #index of the restaurant matchs the cuisines
            idx = indices[title]

            #Aggregate rating added with cosine score in sim_score list.
            sim_scores=[]
            for i,j in enumerate(cosine_sim[idx]):
                k=data_sample['Aggregate rating'].iloc[i]
                if j != 0 :
                    sim_scores.append((i,j,k))

            #Sort the restaurant names based on the similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: (x[1],x[2]) , reverse=True)

            # 5 similarty cuisines
            sim_scores = sim_scores[1:6]

            rest_indices = [i[0] for i in sim_scores]

            data_x =data_sample[['Restaurant Name','Cuisines','Aggregate rating']].iloc[rest_indices]

            data_x['Cosine Similarity']=0
            for i,j in enumerate(sim_scores):
                data_x['Cosine Similarity'].iloc[i]=round(sim_scores[i][1],2)
            return data_x.reset_index(drop=True)

        #Returns a DataFrame of RestaurantRecommendFunc
        def ReturnDF(self):
            #Remove NULL values from the City column.
            self.DataFieldWhole['City'].value_counts(dropna = False)

            #user selects City : Delhi as most Restaurants are here
            data_city =self.DataFieldWhole.loc[self.DataFieldWhole['City'] == self.selectedCityName]#user-provided-data
            
            #Now get all the Restaurant Name, Cuisines, Locality, Aggregate rating in Delhi.
            self.data_new_delphi=data_city[['Restaurant Name','Cuisines','Locality','Aggregate rating']]

            #REMOVE Null values from 'Locality' column
            self.data_new_delphi['Locality'].value_counts(dropna = False).head(5)

            #selecting a locality in delhi, 
            self.data_new_delphi.loc[self.DataFieldWhole['Locality'] == 'Connaught Place']

            data_sample=[]
            return self.RestaurantRecommendFunc(self.selectedLocalityName,self.selectedRestaurantName)

        #Implements Top restaurant code
        def ReturnTopFiveRestaurantName(self):
            restaurantTopFive = self.DataFieldWhole.sort_values('Weighted Aggregate Rating',ascending=False)
            restaurantTopFive = restaurantTopFive[['City','Locality','Restaurant Name','Aggregate rating','Weighted Aggregate Rating']].head(5)
            restaurantTopFive.reset_index()
            return restaurantTopFive
        

#a class to Create/Maintain Gui
class Ui_MainWindow(object):
    Data = RestaurantData()

    #Draws Main WindowFrame
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(90,50,1180, 700)
        #MainWindow.resize(1180, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1180, 700))
        MainWindow.setMaximumSize(QtCore.QSize(1180, 700))
        MainWindow.setMouseTracking(False)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.drawFrontPage()

    #Initializes Qt Widgets
    def drawFrontPage(self):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.LBackgroundImage = QtWidgets.QLabel(self.centralwidget)
        self.LBackgroundImage.setGeometry(QtCore.QRect(0, 0, 1180, 511))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        
        self.LBackgroundImage.setFont(font)
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
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.LTopRestaurants.setFont(font)
        self.LTopRestaurants.setStyleSheet("color: rgb(36, 36, 36);\n"
                                            "")
        self.LTopRestaurants.setObjectName("LTopRestaurants")
        
        self.LRestaurantStar1 = QtWidgets.QLabel(self.frame)
        self.LRestaurantStar1.setGeometry(QtCore.QRect(80, 130, 47, 13))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.LRestaurantStar1.setFont(font)
        self.LRestaurantStar1.setStyleSheet("color: rgb(85, 170, 0);")
        self.LRestaurantStar1.setObjectName("LRestaurantStar1")
        self.LRestaurantStar2 = QtWidgets.QLabel(self.frame)
        self.LRestaurantStar2.setGeometry(QtCore.QRect(280, 130, 47, 13))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.LRestaurantStar2.setFont(font)
        self.LRestaurantStar2.setStyleSheet("color: rgb(85, 170, 0);")
        self.LRestaurantStar2.setObjectName("LRestaurantStar2")
        self.LRestaurantStar3 = QtWidgets.QLabel(self.frame)
        self.LRestaurantStar3.setGeometry(QtCore.QRect(470, 130, 47, 13))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.LRestaurantStar3.setFont(font)
        self.LRestaurantStar3.setStyleSheet("color: rgb(85, 170, 0);")
        self.LRestaurantStar3.setObjectName("LRestaurantStar3")
        self.LRestaurantStar4 = QtWidgets.QLabel(self.frame)
        self.LRestaurantStar4.setGeometry(QtCore.QRect(670, 130, 47, 13))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.LRestaurantStar4.setFont(font)
        self.LRestaurantStar4.setStyleSheet("color: rgb(85, 170, 0);")
        self.LRestaurantStar4.setObjectName("LRestaurantStar4")
        self.LRestaurantStar5 = QtWidgets.QLabel(self.frame)
        self.LRestaurantStar5.setGeometry(QtCore.QRect(870, 130, 47, 13))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.LRestaurantStar5.setFont(font)
        self.LRestaurantStar5.setStyleSheet("color: rgb(85, 170, 0);")
        self.LRestaurantStar5.setObjectName("LRestaurantStar5")
        
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 100, 951, 29))
        self.layoutWidget.setObjectName("layoutWidget")
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(40)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.BRestaurant1 = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.BRestaurant1.setFont(font)
        self.BRestaurant1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BRestaurant1.setStyleSheet("background-color: transparent;\n"
                                        "color: rgb(141, 94, 0);\n"
                                        "font: 75 10pt \"MS Shell Dlg 2\";")
        self.BRestaurant1.setObjectName("BRestaurant1")
        
        self.horizontalLayout.addWidget(self.BRestaurant1)
        
        self.BRestaurant2 = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.BRestaurant2.setFont(font)
        self.BRestaurant2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BRestaurant2.setStyleSheet("background-color: transparent;\n"
                                        "color: rgb(141, 94, 0);\n"
                                        "font: 75 10pt \"MS Shell Dlg 2\";")
        self.BRestaurant2.setObjectName("BRestaurant2")
        
        self.horizontalLayout.addWidget(self.BRestaurant2)
        
        self.BRestaurant3 = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.BRestaurant3.setFont(font)
        self.BRestaurant3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BRestaurant3.setStyleSheet("background-color: transparent;\n"
                                        "color: rgb(141, 94, 0);\n"
                                        "font: 75 10pt \"MS Shell Dlg 2\";")
        self.BRestaurant3.setObjectName("BRestaurant3")
       
        self.horizontalLayout.addWidget(self.BRestaurant3)
       
        self.BRestaurant4 = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.BRestaurant4.setFont(font)
        self.BRestaurant4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BRestaurant4.setStyleSheet("background-color: transparent;\n"
                                        "color: rgb(141, 94, 0);\n"
                                        "font: 75 10pt \"MS Shell Dlg 2\";")
        self.BRestaurant4.setObjectName("BRestaurant4")
        
        self.horizontalLayout.addWidget(self.BRestaurant4)
        
        self.BRestaurant5 = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.BRestaurant5.setFont(font)
        self.BRestaurant5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BRestaurant5.setStyleSheet("background-color: transparent;\n"
                                        "color: rgb(141, 94, 0);\n"
                                        "font: 75 10pt \"MS Shell Dlg 2\";")
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

    #Implements Qt Widgets
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Brasserie"))
        
        self.LMainBanner.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; font-weight:600; color:#55aa00;\">B</span><span style=\" font-size:36pt; font-weight:600; color:#ffffff;\">rasserie</span></p><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; color:#55aa00; vertical-align:sub;\">AI</span><span style=\" font-size:18pt; font-weight:600; color:#ffffff; vertical-align:sub;\">-powered Restaurant </span><span style=\" font-size:18pt; font-weight:600; color:#55aa00; vertical-align:sub;\">recommendation engine</span></p></body></html>"))
        
        self.cBCity.setToolTip(_translate("MainWindow", "Enter City Name !"))
        self.cBCity.setCurrentText(_translate("MainWindow", "City"))
        self.cBCity.setItemText(0, _translate("MainWindow", "City"))
        self.cBCity.addItems(self.Data.ReturnCityName())
        self.cBCity.currentTextChanged.connect(self.UpdateLocalityName)

        self.cBlocality.setToolTip(_translate("MainWindow", "Enter Locality Name in that City !"))
        self.cBlocality.setCurrentText(_translate("MainWindow", "Locality"))
        self.cBlocality.setItemText(0, _translate("MainWindow", "Locality"))
        self.cBlocality.addItems(self.Data.ReturnLocalityName(self.cBCity.currentText()))
        self.cBlocality.currentTextChanged.connect(self.UpdateRestaurantName)

        self.cBRestaurant.setToolTip(_translate("MainWindow", "Enter Restaurant Name !"))
        self.cBRestaurant.setCurrentText(_translate("MainWindow", "Restaurant Name"))
        self.cBRestaurant.setItemText(0, _translate("MainWindow", "Restaurant Name"))
        self.cBRestaurant.addItems(self.Data.ReturnRestaurantName(self.cBCity.currentText(),(self.cBlocality.currentText())))

        self.bSearch.clicked.connect(self.ShowResults)
        
        self.LTopRestaurants.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; color:#1b1b1b;\">Top </span><span style=\" font-size:20pt; color:#55aa00;\">Indian Restaurants</span></p></body></html>"))
        
        self.LRestaurantStar1.setText(_translate("MainWindow", str(self.Data.tempTopRestaurantDF['Aggregate rating'].iloc[0])))
        self.LRestaurantStar2.setText(_translate("MainWindow", str(self.Data.tempTopRestaurantDF['Aggregate rating'].iloc[1])))
        self.LRestaurantStar3.setText(_translate("MainWindow", str(self.Data.tempTopRestaurantDF['Aggregate rating'].iloc[2])))
        self.LRestaurantStar4.setText(_translate("MainWindow", str(self.Data.tempTopRestaurantDF['Aggregate rating'].iloc[3])))
        self.LRestaurantStar5.setText(_translate("MainWindow", str(self.Data.tempTopRestaurantDF['Aggregate rating'].iloc[4])))
        
        self.BRestaurant1.setText(_translate("MainWindow", self.Data.tempTopRestaurantDF['Restaurant Name'].iloc[0]))
        self.BRestaurant2.setText(_translate("MainWindow", self.Data.tempTopRestaurantDF['Restaurant Name'].iloc[1]))
        self.BRestaurant3.setText(_translate("MainWindow", self.Data.tempTopRestaurantDF['Restaurant Name'].iloc[2]))
        self.BRestaurant4.setText(_translate("MainWindow", self.Data.tempTopRestaurantDF['Restaurant Name'].iloc[3]))
        self.BRestaurant5.setText(_translate("MainWindow", self.Data.tempTopRestaurantDF['Restaurant Name'].iloc[4]))
        
        self.LRestaurantStar1.setToolTip(_translate("MainWindow", "Global Rating"))
        self.LRestaurantStar2.setToolTip(_translate("MainWindow", "Global Rating"))
        self.LRestaurantStar3.setToolTip(_translate("MainWindow", "Global Rating"))
        self.LRestaurantStar4.setToolTip(_translate("MainWindow", "Global Rating"))
        self.LRestaurantStar5.setToolTip(_translate("MainWindow", "Global Rating"))

        self.BRestaurant1.setToolTip(_translate("MainWindow", "Top #1"))
        self.BRestaurant2.setToolTip(_translate("MainWindow", "Top #2"))
        self.BRestaurant3.setToolTip(_translate("MainWindow", "Top #3"))
        self.BRestaurant4.setToolTip(_translate("MainWindow", "Top #4"))
        self.BRestaurant5.setToolTip(_translate("MainWindow", "Top #5"))

        self.BRestaurant1.clicked.connect(lambda : self.TopRestaurantNamesAction(0))
        self.BRestaurant2.clicked.connect(lambda : self.TopRestaurantNamesAction(1))
        self.BRestaurant3.clicked.connect(lambda : self.TopRestaurantNamesAction(2))
        self.BRestaurant4.clicked.connect(lambda : self.TopRestaurantNamesAction(3))
        self.BRestaurant5.clicked.connect(lambda : self.TopRestaurantNamesAction(4))

    #Prints Bottom frame of Front Page
    def TopRestaurantNamesAction(self,BNum):
        for i in range(5):
            if(BNum == i):
                self.Data.selectedCityName = self.Data.tempTopRestaurantDF['City'].iloc[i]
                self.Data.selectedLocalityName = self.Data.tempTopRestaurantDF['Locality'].iloc[i]
                self.Data.selectedRestaurantName = self.Data.tempTopRestaurantDF['Restaurant Name'].iloc[i]
        self.ClearScreen()

    #Dynamic Dependent Drop Down list (For locality names)
    def UpdateLocalityName(self):
        self.cBlocality.clear()
        self.cBlocality.addItems(self.Data.ReturnLocalityName(self.cBCity.currentText()))

    #Dynamic Dependent Drop Down list (For restaurant names)
    def UpdateRestaurantName(self):
        self.cBRestaurant.clear()
        self.cBRestaurant.addItems(self.Data.ReturnRestaurantName(self.cBCity.currentText(),self.cBlocality.currentText()))

    #Search Button implementation
    def ShowResults(self):
        self.Data.selectedRestaurantName = str(self.cBRestaurant.currentText())
        print("Search button Triggered...\nPrinting results...\n")
        self.CheckValues()

    #Verifying Values
    def CheckValues(self):
        print("In CheckValues()...")
        print("City : ",self.Data.selectedCityName)
        print("Locality : ",self.Data.selectedLocalityName)
        print("Restaurant Name : ",self.Data.selectedRestaurantName)

        if(self.Data.selectedCityName=='City'or self.Data.selectedCityName==''\
            or self.Data.selectedLocalityName == 'Locality' or self.Data.selectedLocalityName == ''\
            or self.Data.selectedRestaurantName == 'Restaurant Name' or  self.Data.selectedRestaurantName == ''):
            print("Error, unknownValues/invalidValues found")
            #dialog box
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Invalid values")
            msgbox.setText("Please select a valid combination!")
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.setDefaultButton(QMessageBox.Ok)
            msgbox.buttonClicked.connect(lambda : self.drawFrontPage)
            x = msgbox.exec_()
        elif(self.Data.selectedRestaurantName not in self.Data.ReturnRestaurantName(self.cBCity.currentText(),self.cBlocality.currentText())):
            print("Error, no Restaurant Found")
            #dialog box
            msgbox = QMessageBox()
            msgbox.setWindowTitle("No Restaurant Found")
            msgbox.setText("Error, No Restaurant Found : {}".format(self.Data.selectedRestaurantName))
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.setDefaultButton(QMessageBox.Ok)
            msgbox.buttonClicked.connect(lambda : self.drawFrontPage)
            x = msgbox.exec_()
        else:
            print("Safe To enter")
            self.ClearScreen()

    #Clearing and Initializing Result Window Qt Widgets
    def ClearScreen(self):
        print("Resetting All widgets")
        self.centralWidget2 = QtWidgets.QWidget(MainWindow)
        self.centralWidget2.setObjectName("centralWidget2")
        MainWindow.setCentralWidget(self.centralWidget2)

        self.centralWidget2.resize(1180, 700)
        self.centralWidget2.setMinimumSize(QtCore.QSize(1180, 700))
        self.centralWidget2.setMaximumSize(QtCore.QSize(1180, 700))
        self.centralWidget2.setStyleSheet("background-color: rgb(250, 250, 250);")
        self.widget = QtWidgets.QWidget(self.centralWidget2)
        self.widget.setGeometry(QtCore.QRect(50, 0, 1081, 711))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.widget.setFont(font)
        self.widget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget.setObjectName("widget")
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setGeometry(QtCore.QRect(40, 230, 1001, 381))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.tableWidget.setFont(font)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setAutoScroll(False)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        self.tableWidget.setItem(0, 0, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(39)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(70)
        self.BBack = QtWidgets.QPushButton(self.widget)
        self.BBack.setGeometry(QtCore.QRect(10, 30, 45, 45))
        self.BBack.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BBack.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.BBack.setAutoFillBackground(False)
        self.BBack.setStyleSheet("background-color: outset;\n"
                                "border-style:outset;")
        self.BBack.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(backButtonImageLink), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BBack.setIcon(icon)
        self.BBack.setIconSize(QtCore.QSize(40, 40))
        self.BBack.setObjectName("BBack")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(250, 20, 561, 101))
        self.label.setStyleSheet("background-color: outset;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 1081, 701))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(backGround2ImageLink))
        self.label_2.setObjectName("label_2")
        self.horizontalFrame = QtWidgets.QFrame(self.widget)
        self.horizontalFrame.setGeometry(QtCore.QRect(100, 160, 881, 41))
        self.horizontalFrame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.horizontalFrame.setStyleSheet("background-color: outset;")
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LCityName = QtWidgets.QLabel(self.horizontalFrame)
        self.LCityName.setStyleSheet("color: rgb(255, 170, 0);\n"
                                    "font: 75 10pt \"Microsoft YaHei UI\";\n"
                                    "background-color: transparent;")
        self.LCityName.setObjectName("LCityName")
        self.horizontalLayout.addWidget(self.LCityName)
        self.LCityNameEnter = QtWidgets.QLabel(self.horizontalFrame)
        self.LCityNameEnter.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "font: 9pt \"Microsoft YaHei UI\";\n"
                                        "background-color: outset;")
        self.LCityNameEnter.setObjectName("LCityNameEnter")
        self.horizontalLayout.addWidget(self.LCityNameEnter)
        self.LLocalityName = QtWidgets.QLabel(self.horizontalFrame)
        self.LLocalityName.setStyleSheet("color: rgb(255, 170, 0);\n"
                                        "font: 75 10pt \"Microsoft YaHei UI\";\n"
                                        "background-color: outset;")
        self.LLocalityName.setObjectName("LLocalityName")
        self.horizontalLayout.addWidget(self.LLocalityName)
        self.LLocaltyNameEnter = QtWidgets.QLabel(self.horizontalFrame)
        self.LLocaltyNameEnter.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            "font: 9pt \"Microsoft YaHei UI\";\n"
                                            "background-color: outset;")
        self.LLocaltyNameEnter.setObjectName("LLocaltyNameEnter")
        self.horizontalLayout.addWidget(self.LLocaltyNameEnter)
        self.LRestaurantName = QtWidgets.QLabel(self.horizontalFrame)
        self.LRestaurantName.setStyleSheet("color: rgb(255, 170, 0);\n"
                                        "font: 75 10pt \"Microsoft YaHei UI\";\n"
                                        "background-color: outset;")
        self.LRestaurantName.setObjectName("LRestaurantName")
        self.horizontalLayout.addWidget(self.LRestaurantName)
        self.LRestaurantNameEnter = QtWidgets.QLabel(self.horizontalFrame)
        self.LRestaurantNameEnter.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "font: 9pt \"Microsoft YaHei UI\";\n"
                                        "background-color: outset;")
        self.LRestaurantNameEnter.setObjectName("LRestaurantNameEnter")
        self.horizontalLayout.addWidget(self.LRestaurantNameEnter)
        self.label_2.raise_()
        self.tableWidget.raise_()
        self.BBack.raise_()
        self.label.raise_()
        self.horizontalFrame.raise_()

        self.retranslateNextUi(self.centralWidget2)
        QtCore.QMetaObject.connectSlotsByName(self.centralWidget2)

    #Implements Result Window Qt Widgets
    def retranslateNextUi(self, centralWidget2):
        _translate = QtCore.QCoreApplication.translate
        self.centralWidget2.setWindowTitle(_translate("centralWidget2", "Form"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("centralWidget2", "Sr. No."))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("centralWidget2", "Restaurant Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("centralWidget2", "Cuisines"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("centralWidget2", "Rating"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("centralWidget2", "Cosine Similarity Score"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()

        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.BBack.setToolTip(_translate("centralWidget2", "Back"))

        self.BBack.setShortcut(_translate("centralWidget2", "Backspace"))
      
        self.label.setText(_translate("centralWidget2", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:600; color:#ffffff;\">Restaurants </span><span style=\" font-size:24pt; font-weight:600; color:#55aa00;\">We Recommend</span></p><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ffffff;\">Based on </span><span style=\" font-size:16pt; font-weight:600; color:#55aa00;\">Your choice</span></p></body></html>"))
      
        self.LCityName.setText(_translate("centralWidget2", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">City Name :</span></p></body></html>"))
      
        self.LCityNameEnter.setText(_translate("centralWidget2", "<html><head/><body><p><span style=\" font-size:10pt;\">{}</span></p></body></html>".format(self.Data.selectedCityName)))
      
        self.LLocalityName.setText(_translate("centralWidget2", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Locality Name :</span></p></body></html>"))
      
        self.LLocaltyNameEnter.setText(_translate("centralWidget2", "<html><head/><body><p><span style=\" font-size:10pt;\">{}</span></p></body></html>".format(self.Data.selectedLocalityName)))
      
        self.LRestaurantName.setText(_translate("centralWidget2", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Restaurant Name :</span></p></body></html>"))
      
        self.LRestaurantNameEnter.setText(_translate("centralWidget2", "<html><head/><body><p><span style=\" font-size:10pt;\">{}</span></p></body></html>".format(self.Data.selectedRestaurantName)))
        
        self.BBack.clicked.connect(self.drawFrontPage)

        for index,row in self.Data.ReturnDF().iterrows():
            self.tableWidget.setItem(index,0,QtWidgets.QTableWidgetItem(str(index+1)))
            self.tableWidget.setItem(index,1,QtWidgets.QTableWidgetItem(row['Restaurant Name']))
            self.tableWidget.setItem(index,2,QtWidgets.QTableWidgetItem(row['Cuisines']))
            self.tableWidget.setItem(index,3,QtWidgets.QTableWidgetItem(str(row['Aggregate rating'])))
            self.tableWidget.setItem(index,4,QtWidgets.QTableWidgetItem(str(row['Cosine Similarity'])))
            """
            print(index,0,row['Restaurant Name'])
            print(index,1,row['Cuisines'])
            print(index,2,row['Aggregate rating'])
            print(index,3,row['Cosine Similarity'])
            """

        if(self.Data.ReturnDF().empty == True):
            print("Sorry, no recommendation")
            #dialog box
            msgbox = QMessageBox()
            msgbox.setWindowTitle("No Result !")
            msgbox.setText("Sorry, no recommendation available for {}, Right Now!".format(self.Data.selectedRestaurantName))
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setStandardButtons(QMessageBox.Retry|QMessageBox.Close)
            msgbox.setDefaultButton(QMessageBox.Retry)
            msgbox.buttonClicked.connect(self.nextUiPopup)
            x = msgbox.exec_()

    #Handles Pop Dialog for failure
    def nextUiPopup(self,i):
        print(i.text())
        if(i.text() == 'Retry'):
            self.drawFrontPage()
        else:
            sys.exit(0)


#main driver
if __name__ == "__main__":
    import sys#remove
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
