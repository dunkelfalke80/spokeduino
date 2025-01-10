# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'spokeduino_mothershipvSkQkQ.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLayout,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QTableView,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(1171, 768)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainWindow.sizePolicy().hasHeightForWidth())
        mainWindow.setSizePolicy(sizePolicy)
        mainWindow.setMinimumSize(QSize(1024, 768))
        self.actionAbout = QAction(mainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionMeasure_a_new_spoke = QAction(mainWindow)
        self.actionMeasure_a_new_spoke.setObjectName(u"actionMeasure_a_new_spoke")
        self.actionBuild_a_wheel = QAction(mainWindow)
        self.actionBuild_a_wheel.setObjectName(u"actionBuild_a_wheel")
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.databaseTab = QWidget()
        self.databaseTab.setObjectName(u"databaseTab")
        self.horizontalLayoutDatabaseTop = QHBoxLayout(self.databaseTab)
        self.horizontalLayoutDatabaseTop.setObjectName(u"horizontalLayoutDatabaseTop")
        self.horizontalLayoutDatabase = QHBoxLayout()
        self.horizontalLayoutDatabase.setObjectName(u"horizontalLayoutDatabase")
        self.verticalLayoutDatabaseLeft = QVBoxLayout()
        self.verticalLayoutDatabaseLeft.setObjectName(u"verticalLayoutDatabaseLeft")
        self.groupBoxListSpokesDatabase = QGroupBox(self.databaseTab)
        self.groupBoxListSpokesDatabase.setObjectName(u"groupBoxListSpokesDatabase")
        self.verticalLayoutFilterDatabase = QVBoxLayout(self.groupBoxListSpokesDatabase)
        self.verticalLayoutFilterDatabase.setObjectName(u"verticalLayoutFilterDatabase")
        self.horizontalLayoutFilterDatabase = QHBoxLayout()
        self.horizontalLayoutFilterDatabase.setObjectName(u"horizontalLayoutFilterDatabase")
        self.lineEditFilterName = QLineEdit(self.groupBoxListSpokesDatabase)
        self.lineEditFilterName.setObjectName(u"lineEditFilterName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEditFilterName.sizePolicy().hasHeightForWidth())
        self.lineEditFilterName.setSizePolicy(sizePolicy1)

        self.horizontalLayoutFilterDatabase.addWidget(self.lineEditFilterName)

        self.horizontalSpacerFilter = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutFilterDatabase.addItem(self.horizontalSpacerFilter)

        self.lineEditFilterGauge = QLineEdit(self.groupBoxListSpokesDatabase)
        self.lineEditFilterGauge.setObjectName(u"lineEditFilterGauge")
        sizePolicy1.setHeightForWidth(self.lineEditFilterGauge.sizePolicy().hasHeightForWidth())
        self.lineEditFilterGauge.setSizePolicy(sizePolicy1)

        self.horizontalLayoutFilterDatabase.addWidget(self.lineEditFilterGauge)

        self.comboBoxFilterType = QComboBox(self.groupBoxListSpokesDatabase)
        self.comboBoxFilterType.setObjectName(u"comboBoxFilterType")
        sizePolicy1.setHeightForWidth(self.comboBoxFilterType.sizePolicy().hasHeightForWidth())
        self.comboBoxFilterType.setSizePolicy(sizePolicy1)

        self.horizontalLayoutFilterDatabase.addWidget(self.comboBoxFilterType)

        self.horizontalLayoutFilterDatabase.setStretch(0, 10)
        self.horizontalLayoutFilterDatabase.setStretch(2, 1)
        self.horizontalLayoutFilterDatabase.setStretch(3, 5)

        self.verticalLayoutFilterDatabase.addLayout(self.horizontalLayoutFilterDatabase)

        self.tableViewSpokesDatabase = QTableView(self.groupBoxListSpokesDatabase)
        self.tableViewSpokesDatabase.setObjectName(u"tableViewSpokesDatabase")
        sizePolicy1.setHeightForWidth(self.tableViewSpokesDatabase.sizePolicy().hasHeightForWidth())
        self.tableViewSpokesDatabase.setSizePolicy(sizePolicy1)

        self.verticalLayoutFilterDatabase.addWidget(self.tableViewSpokesDatabase)

        self.verticalLayoutFilterDatabase.setStretch(1, 1)

        self.verticalLayoutDatabaseLeft.addWidget(self.groupBoxListSpokesDatabase)

        self.groupBoxListMeasurementsDatabase = QGroupBox(self.databaseTab)
        self.groupBoxListMeasurementsDatabase.setObjectName(u"groupBoxListMeasurementsDatabase")
        self.verticalLayoutMeasurementsDatabase = QVBoxLayout(self.groupBoxListMeasurementsDatabase)
        self.verticalLayoutMeasurementsDatabase.setObjectName(u"verticalLayoutMeasurementsDatabase")
        self.verticalLayoutMeasurements = QVBoxLayout()
        self.verticalLayoutMeasurements.setObjectName(u"verticalLayoutMeasurements")
        self.tableViewMeasurements = QTableView(self.groupBoxListMeasurementsDatabase)
        self.tableViewMeasurements.setObjectName(u"tableViewMeasurements")
        sizePolicy1.setHeightForWidth(self.tableViewMeasurements.sizePolicy().hasHeightForWidth())
        self.tableViewMeasurements.setSizePolicy(sizePolicy1)

        self.verticalLayoutMeasurements.addWidget(self.tableViewMeasurements)


        self.verticalLayoutMeasurementsDatabase.addLayout(self.verticalLayoutMeasurements)

        self.horizontalLayoutMeasurementsButtonsDatabase = QHBoxLayout()
        self.horizontalLayoutMeasurementsButtonsDatabase.setObjectName(u"horizontalLayoutMeasurementsButtonsDatabase")
        self.pushButtonUseMeasurementLeft = QPushButton(self.groupBoxListMeasurementsDatabase)
        self.pushButtonUseMeasurementLeft.setObjectName(u"pushButtonUseMeasurementLeft")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButtonUseMeasurementLeft.sizePolicy().hasHeightForWidth())
        self.pushButtonUseMeasurementLeft.setSizePolicy(sizePolicy2)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        self.pushButtonUseMeasurementLeft.setIcon(icon)

        self.horizontalLayoutMeasurementsButtonsDatabase.addWidget(self.pushButtonUseMeasurementLeft)

        self.pushButtonUseMeasurementRight = QPushButton(self.groupBoxListMeasurementsDatabase)
        self.pushButtonUseMeasurementRight.setObjectName(u"pushButtonUseMeasurementRight")
        sizePolicy2.setHeightForWidth(self.pushButtonUseMeasurementRight.sizePolicy().hasHeightForWidth())
        self.pushButtonUseMeasurementRight.setSizePolicy(sizePolicy2)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoNext))
        self.pushButtonUseMeasurementRight.setIcon(icon1)

        self.horizontalLayoutMeasurementsButtonsDatabase.addWidget(self.pushButtonUseMeasurementRight)

        self.horizontalSpacerMeasurementsBottom = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutMeasurementsButtonsDatabase.addItem(self.horizontalSpacerMeasurementsBottom)

        self.pushButtonAddMeasurement = QPushButton(self.groupBoxListMeasurementsDatabase)
        self.pushButtonAddMeasurement.setObjectName(u"pushButtonAddMeasurement")
        sizePolicy2.setHeightForWidth(self.pushButtonAddMeasurement.sizePolicy().hasHeightForWidth())
        self.pushButtonAddMeasurement.setSizePolicy(sizePolicy2)
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.pushButtonAddMeasurement.setIcon(icon2)

        self.horizontalLayoutMeasurementsButtonsDatabase.addWidget(self.pushButtonAddMeasurement)

        self.pushButtonDeleteMeasurement = QPushButton(self.groupBoxListMeasurementsDatabase)
        self.pushButtonDeleteMeasurement.setObjectName(u"pushButtonDeleteMeasurement")
        sizePolicy2.setHeightForWidth(self.pushButtonDeleteMeasurement.sizePolicy().hasHeightForWidth())
        self.pushButtonDeleteMeasurement.setSizePolicy(sizePolicy2)
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        self.pushButtonDeleteMeasurement.setIcon(icon3)

        self.horizontalLayoutMeasurementsButtonsDatabase.addWidget(self.pushButtonDeleteMeasurement)

        self.pushButtonDeleteSpoke = QPushButton(self.groupBoxListMeasurementsDatabase)
        self.pushButtonDeleteSpoke.setObjectName(u"pushButtonDeleteSpoke")
        sizePolicy2.setHeightForWidth(self.pushButtonDeleteSpoke.sizePolicy().hasHeightForWidth())
        self.pushButtonDeleteSpoke.setSizePolicy(sizePolicy2)
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.pushButtonDeleteSpoke.setIcon(icon4)

        self.horizontalLayoutMeasurementsButtonsDatabase.addWidget(self.pushButtonDeleteSpoke)


        self.verticalLayoutMeasurementsDatabase.addLayout(self.horizontalLayoutMeasurementsButtonsDatabase)

        self.verticalLayoutMeasurementsDatabase.setStretch(0, 1)

        self.verticalLayoutDatabaseLeft.addWidget(self.groupBoxListMeasurementsDatabase)

        self.verticalLayoutDatabaseLeft.setStretch(0, 3)
        self.verticalLayoutDatabaseLeft.setStretch(1, 2)

        self.horizontalLayoutDatabase.addLayout(self.verticalLayoutDatabaseLeft)

        self.horizontalSpacerDatabaseCenter = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutDatabase.addItem(self.horizontalSpacerDatabaseCenter)

        self.groupBoxSpokeDatabase = QGroupBox(self.databaseTab)
        self.groupBoxSpokeDatabase.setObjectName(u"groupBoxSpokeDatabase")
        self.verticalLayoutSpokeDatabase = QVBoxLayout(self.groupBoxSpokeDatabase)
        self.verticalLayoutSpokeDatabase.setObjectName(u"verticalLayoutSpokeDatabase")
        self.groupBoxManufacturer = QGroupBox(self.groupBoxSpokeDatabase)
        self.groupBoxManufacturer.setObjectName(u"groupBoxManufacturer")
        self.verticalLayoutManufacturerDatabase = QVBoxLayout(self.groupBoxManufacturer)
        self.verticalLayoutManufacturerDatabase.setObjectName(u"verticalLayoutManufacturerDatabase")
        self.comboBoxManufacturer = QComboBox(self.groupBoxManufacturer)
        self.comboBoxManufacturer.setObjectName(u"comboBoxManufacturer")
        sizePolicy1.setHeightForWidth(self.comboBoxManufacturer.sizePolicy().hasHeightForWidth())
        self.comboBoxManufacturer.setSizePolicy(sizePolicy1)

        self.verticalLayoutManufacturerDatabase.addWidget(self.comboBoxManufacturer)

        self.horizontalLayoutDatabaseLeft = QHBoxLayout()
        self.horizontalLayoutDatabaseLeft.setObjectName(u"horizontalLayoutDatabaseLeft")
        self.horizontalLayoutDatabaseLeft.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.groupBoxNewManufacturer = QGroupBox(self.groupBoxManufacturer)
        self.groupBoxNewManufacturer.setObjectName(u"groupBoxNewManufacturer")
        sizePolicy1.setHeightForWidth(self.groupBoxNewManufacturer.sizePolicy().hasHeightForWidth())
        self.groupBoxNewManufacturer.setSizePolicy(sizePolicy1)
        self.verticalLayoutNewManufacturerDatabase = QVBoxLayout(self.groupBoxNewManufacturer)
        self.verticalLayoutNewManufacturerDatabase.setObjectName(u"verticalLayoutNewManufacturerDatabase")
        self.lineEditNewManufacturer = QLineEdit(self.groupBoxNewManufacturer)
        self.lineEditNewManufacturer.setObjectName(u"lineEditNewManufacturer")
        sizePolicy1.setHeightForWidth(self.lineEditNewManufacturer.sizePolicy().hasHeightForWidth())
        self.lineEditNewManufacturer.setSizePolicy(sizePolicy1)

        self.verticalLayoutNewManufacturerDatabase.addWidget(self.lineEditNewManufacturer)


        self.horizontalLayoutDatabaseLeft.addWidget(self.groupBoxNewManufacturer)

        self.horizontalSpacerManufacturer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutDatabaseLeft.addItem(self.horizontalSpacerManufacturer)

        self.pushButtonNewManufacturer = QPushButton(self.groupBoxManufacturer)
        self.pushButtonNewManufacturer.setObjectName(u"pushButtonNewManufacturer")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButtonNewManufacturer.sizePolicy().hasHeightForWidth())
        self.pushButtonNewManufacturer.setSizePolicy(sizePolicy3)
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
        self.pushButtonNewManufacturer.setIcon(icon5)

        self.horizontalLayoutDatabaseLeft.addWidget(self.pushButtonNewManufacturer)

        self.horizontalLayoutDatabaseLeft.setStretch(0, 3)
        self.horizontalLayoutDatabaseLeft.setStretch(2, 1)

        self.verticalLayoutManufacturerDatabase.addLayout(self.horizontalLayoutDatabaseLeft)


        self.verticalLayoutSpokeDatabase.addWidget(self.groupBoxManufacturer)

        self.verticalSpacerDatabaseTop = QSpacerItem(20, 28, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutSpokeDatabase.addItem(self.verticalSpacerDatabaseTop)

        self.groupBoxSpoke = QGroupBox(self.groupBoxSpokeDatabase)
        self.groupBoxSpoke.setObjectName(u"groupBoxSpoke")
        self.verticalLayoutSelectSpokeDatabase = QVBoxLayout(self.groupBoxSpoke)
        self.verticalLayoutSelectSpokeDatabase.setObjectName(u"verticalLayoutSelectSpokeDatabase")
        self.comboBoxSpoke = QComboBox(self.groupBoxSpoke)
        self.comboBoxSpoke.setObjectName(u"comboBoxSpoke")
        sizePolicy1.setHeightForWidth(self.comboBoxSpoke.sizePolicy().hasHeightForWidth())
        self.comboBoxSpoke.setSizePolicy(sizePolicy1)

        self.verticalLayoutSelectSpokeDatabase.addWidget(self.comboBoxSpoke)


        self.verticalLayoutSpokeDatabase.addWidget(self.groupBoxSpoke)

        self.groupBoxName = QGroupBox(self.groupBoxSpokeDatabase)
        self.groupBoxName.setObjectName(u"groupBoxName")
        self.groupBoxName.setEnabled(True)
        self.verticalLayoutEditNewSpokeName = QVBoxLayout(self.groupBoxName)
        self.verticalLayoutEditNewSpokeName.setObjectName(u"verticalLayoutEditNewSpokeName")
        self.lineEditName = QLineEdit(self.groupBoxName)
        self.lineEditName.setObjectName(u"lineEditName")
        sizePolicy1.setHeightForWidth(self.lineEditName.sizePolicy().hasHeightForWidth())
        self.lineEditName.setSizePolicy(sizePolicy1)

        self.verticalLayoutEditNewSpokeName.addWidget(self.lineEditName)


        self.verticalLayoutSpokeDatabase.addWidget(self.groupBoxName)

        self.horizontalLayoutSpokeDefinitionsDatabase = QHBoxLayout()
        self.horizontalLayoutSpokeDefinitionsDatabase.setObjectName(u"horizontalLayoutSpokeDefinitionsDatabase")
        self.groupBoxType = QGroupBox(self.groupBoxSpokeDatabase)
        self.groupBoxType.setObjectName(u"groupBoxType")
        sizePolicy1.setHeightForWidth(self.groupBoxType.sizePolicy().hasHeightForWidth())
        self.groupBoxType.setSizePolicy(sizePolicy1)
        self.groupBoxType.setMinimumSize(QSize(150, 0))
        self.verticalLayoutTypeDatabase = QVBoxLayout(self.groupBoxType)
        self.verticalLayoutTypeDatabase.setObjectName(u"verticalLayoutTypeDatabase")
        self.comboBoxType = QComboBox(self.groupBoxType)
        self.comboBoxType.setObjectName(u"comboBoxType")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.comboBoxType.sizePolicy().hasHeightForWidth())
        self.comboBoxType.setSizePolicy(sizePolicy4)

        self.verticalLayoutTypeDatabase.addWidget(self.comboBoxType)


        self.horizontalLayoutSpokeDefinitionsDatabase.addWidget(self.groupBoxType)

        self.horizontalSpacerTypeDatabase = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutSpokeDefinitionsDatabase.addItem(self.horizontalSpacerTypeDatabase)

        self.groupBoxGauge = QGroupBox(self.groupBoxSpokeDatabase)
        self.groupBoxGauge.setObjectName(u"groupBoxGauge")
        sizePolicy1.setHeightForWidth(self.groupBoxGauge.sizePolicy().hasHeightForWidth())
        self.groupBoxGauge.setSizePolicy(sizePolicy1)
        self.verticalLayoutGaugeDatabase = QVBoxLayout(self.groupBoxGauge)
        self.verticalLayoutGaugeDatabase.setObjectName(u"verticalLayoutGaugeDatabase")
        self.lineEditGauge = QLineEdit(self.groupBoxGauge)
        self.lineEditGauge.setObjectName(u"lineEditGauge")
        sizePolicy1.setHeightForWidth(self.lineEditGauge.sizePolicy().hasHeightForWidth())
        self.lineEditGauge.setSizePolicy(sizePolicy1)

        self.verticalLayoutGaugeDatabase.addWidget(self.lineEditGauge)


        self.horizontalLayoutSpokeDefinitionsDatabase.addWidget(self.groupBoxGauge)

        self.groupBoxWeight = QGroupBox(self.groupBoxSpokeDatabase)
        self.groupBoxWeight.setObjectName(u"groupBoxWeight")
        sizePolicy1.setHeightForWidth(self.groupBoxWeight.sizePolicy().hasHeightForWidth())
        self.groupBoxWeight.setSizePolicy(sizePolicy1)
        self.verticalLayoutWeightDatabase = QVBoxLayout(self.groupBoxWeight)
        self.verticalLayoutWeightDatabase.setObjectName(u"verticalLayoutWeightDatabase")
        self.lineEditWeight = QLineEdit(self.groupBoxWeight)
        self.lineEditWeight.setObjectName(u"lineEditWeight")
        sizePolicy1.setHeightForWidth(self.lineEditWeight.sizePolicy().hasHeightForWidth())
        self.lineEditWeight.setSizePolicy(sizePolicy1)

        self.verticalLayoutWeightDatabase.addWidget(self.lineEditWeight)


        self.horizontalLayoutSpokeDefinitionsDatabase.addWidget(self.groupBoxWeight)


        self.verticalLayoutSpokeDatabase.addLayout(self.horizontalLayoutSpokeDefinitionsDatabase)

        self.groupBoxDimension = QGroupBox(self.groupBoxSpokeDatabase)
        self.groupBoxDimension.setObjectName(u"groupBoxDimension")
        self.verticalLayoutDimension = QVBoxLayout(self.groupBoxDimension)
        self.verticalLayoutDimension.setObjectName(u"verticalLayoutDimension")
        self.lineEditDimension = QLineEdit(self.groupBoxDimension)
        self.lineEditDimension.setObjectName(u"lineEditDimension")
        sizePolicy1.setHeightForWidth(self.lineEditDimension.sizePolicy().hasHeightForWidth())
        self.lineEditDimension.setSizePolicy(sizePolicy1)

        self.verticalLayoutDimension.addWidget(self.lineEditDimension)


        self.verticalLayoutSpokeDatabase.addWidget(self.groupBoxDimension)

        self.groupBoxSpokeComment = QGroupBox(self.groupBoxSpokeDatabase)
        self.groupBoxSpokeComment.setObjectName(u"groupBoxSpokeComment")
        self.verticalLayoutCommentDatabase = QVBoxLayout(self.groupBoxSpokeComment)
        self.verticalLayoutCommentDatabase.setObjectName(u"verticalLayoutCommentDatabase")
        self.lineEditSpokeComment = QLineEdit(self.groupBoxSpokeComment)
        self.lineEditSpokeComment.setObjectName(u"lineEditSpokeComment")
        sizePolicy1.setHeightForWidth(self.lineEditSpokeComment.sizePolicy().hasHeightForWidth())
        self.lineEditSpokeComment.setSizePolicy(sizePolicy1)

        self.verticalLayoutCommentDatabase.addWidget(self.lineEditSpokeComment)


        self.verticalLayoutSpokeDatabase.addWidget(self.groupBoxSpokeComment)

        self.verticalSpacerDatabaseBottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutSpokeDatabase.addItem(self.verticalSpacerDatabaseBottom)

        self.horizontalLayoutSpokeButtonsDatabase = QHBoxLayout()
        self.horizontalLayoutSpokeButtonsDatabase.setObjectName(u"horizontalLayoutSpokeButtonsDatabase")
        self.pushButtonCreateSpoke = QPushButton(self.groupBoxSpokeDatabase)
        self.pushButtonCreateSpoke.setObjectName(u"pushButtonCreateSpoke")
        sizePolicy2.setHeightForWidth(self.pushButtonCreateSpoke.sizePolicy().hasHeightForWidth())
        self.pushButtonCreateSpoke.setSizePolicy(sizePolicy2)
        self.pushButtonCreateSpoke.setIcon(icon2)

        self.horizontalLayoutSpokeButtonsDatabase.addWidget(self.pushButtonCreateSpoke)

        self.horizontalSpacerSpokeDatabaseLeft = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutSpokeButtonsDatabase.addItem(self.horizontalSpacerSpokeDatabaseLeft)

        self.pushButtonEditSpoke = QPushButton(self.groupBoxSpokeDatabase)
        self.pushButtonEditSpoke.setObjectName(u"pushButtonEditSpoke")
        sizePolicy2.setHeightForWidth(self.pushButtonEditSpoke.sizePolicy().hasHeightForWidth())
        self.pushButtonEditSpoke.setSizePolicy(sizePolicy2)
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSaveAs))
        self.pushButtonEditSpoke.setIcon(icon6)

        self.horizontalLayoutSpokeButtonsDatabase.addWidget(self.pushButtonEditSpoke)

        self.horizontalSpacerSpokeDatabaseRight = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutSpokeButtonsDatabase.addItem(self.horizontalSpacerSpokeDatabaseRight)

        self.pushButtonClearSpoke = QPushButton(self.groupBoxSpokeDatabase)
        self.pushButtonClearSpoke.setObjectName(u"pushButtonClearSpoke")
        sizePolicy2.setHeightForWidth(self.pushButtonClearSpoke.sizePolicy().hasHeightForWidth())
        self.pushButtonClearSpoke.setSizePolicy(sizePolicy2)
        icon7 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditUndo))
        self.pushButtonClearSpoke.setIcon(icon7)

        self.horizontalLayoutSpokeButtonsDatabase.addWidget(self.pushButtonClearSpoke)


        self.verticalLayoutSpokeDatabase.addLayout(self.horizontalLayoutSpokeButtonsDatabase)


        self.horizontalLayoutDatabase.addWidget(self.groupBoxSpokeDatabase)

        self.horizontalLayoutDatabase.setStretch(0, 2)
        self.horizontalLayoutDatabase.setStretch(2, 1)

        self.horizontalLayoutDatabaseTop.addLayout(self.horizontalLayoutDatabase)

        self.tabWidget.addTab(self.databaseTab, "")
        self.measurementTab = QWidget()
        self.measurementTab.setObjectName(u"measurementTab")
        self.horizontalLayoutMeasurementTop = QHBoxLayout(self.measurementTab)
        self.horizontalLayoutMeasurementTop.setObjectName(u"horizontalLayoutMeasurementTop")
        self.horizontalLayoutMeasurement = QHBoxLayout()
        self.horizontalLayoutMeasurement.setObjectName(u"horizontalLayoutMeasurement")
        self.horizontalLayoutMeasurementsLeft = QHBoxLayout()
        self.horizontalLayoutMeasurementsLeft.setObjectName(u"horizontalLayoutMeasurementsLeft")
        self.groupBoxMeasurement = QGroupBox(self.measurementTab)
        self.groupBoxMeasurement.setObjectName(u"groupBoxMeasurement")
        self.verticalLayoutManufacturer = QVBoxLayout(self.groupBoxMeasurement)
        self.verticalLayoutManufacturer.setObjectName(u"verticalLayoutManufacturer")
        self.horizontalLayoutManufacturerLeft = QHBoxLayout()
        self.horizontalLayoutManufacturerLeft.setObjectName(u"horizontalLayoutManufacturerLeft")
        self.tableWidgetMeasurements = QTableWidget(self.groupBoxMeasurement)
        self.tableWidgetMeasurements.setObjectName(u"tableWidgetMeasurements")

        self.horizontalLayoutManufacturerLeft.addWidget(self.tableWidgetMeasurements)

        self.horizontalLayoutManufacturerLeft.setStretch(0, 5)

        self.verticalLayoutManufacturer.addLayout(self.horizontalLayoutManufacturerLeft)

        self.groupBoxFormula = QGroupBox(self.groupBoxMeasurement)
        self.groupBoxFormula.setObjectName(u"groupBoxFormula")
        self.horizontalLayoutFormula = QHBoxLayout(self.groupBoxFormula)
        self.horizontalLayoutFormula.setObjectName(u"horizontalLayoutFormula")
        self.lineEditFormula = QLineEdit(self.groupBoxFormula)
        self.lineEditFormula.setObjectName(u"lineEditFormula")

        self.horizontalLayoutFormula.addWidget(self.lineEditFormula)

        self.horizontalSpacerMeasurementCenterLeft = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutFormula.addItem(self.horizontalSpacerMeasurementCenterLeft)

        self.pushButtonCalculateFormula = QPushButton(self.groupBoxFormula)
        self.pushButtonCalculateFormula.setObjectName(u"pushButtonCalculateFormula")
        icon8 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SyncSynchronizing))
        self.pushButtonCalculateFormula.setIcon(icon8)

        self.horizontalLayoutFormula.addWidget(self.pushButtonCalculateFormula)

        self.horizontalLayoutFormula.setStretch(0, 1)

        self.verticalLayoutManufacturer.addWidget(self.groupBoxFormula)

        self.groupBoxMeasurementComment = QGroupBox(self.groupBoxMeasurement)
        self.groupBoxMeasurementComment.setObjectName(u"groupBoxMeasurementComment")
        self.verticalLayoutCommentMeasurement = QVBoxLayout(self.groupBoxMeasurementComment)
        self.verticalLayoutCommentMeasurement.setObjectName(u"verticalLayoutCommentMeasurement")
        self.lineEditMeasurementComment = QLineEdit(self.groupBoxMeasurementComment)
        self.lineEditMeasurementComment.setObjectName(u"lineEditMeasurementComment")

        self.verticalLayoutCommentMeasurement.addWidget(self.lineEditMeasurementComment)


        self.verticalLayoutManufacturer.addWidget(self.groupBoxMeasurementComment)

        self.horizontalLayoutMeasurementsButtons = QHBoxLayout()
        self.horizontalLayoutMeasurementsButtons.setObjectName(u"horizontalLayoutMeasurementsButtons")
        self.pushButtonPreviousMeasurement = QPushButton(self.groupBoxMeasurement)
        self.pushButtonPreviousMeasurement.setObjectName(u"pushButtonPreviousMeasurement")
        self.pushButtonPreviousMeasurement.setIcon(icon)

        self.horizontalLayoutMeasurementsButtons.addWidget(self.pushButtonPreviousMeasurement)

        self.pushButtonNextMeasurement = QPushButton(self.groupBoxMeasurement)
        self.pushButtonNextMeasurement.setObjectName(u"pushButtonNextMeasurement")
        self.pushButtonNextMeasurement.setIcon(icon1)

        self.horizontalLayoutMeasurementsButtons.addWidget(self.pushButtonNextMeasurement)

        self.horizontalSpacerMeasurementBottomLeft = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutMeasurementsButtons.addItem(self.horizontalSpacerMeasurementBottomLeft)

        self.pushButtonSaveMeasurement = QPushButton(self.groupBoxMeasurement)
        self.pushButtonSaveMeasurement.setObjectName(u"pushButtonSaveMeasurement")
        icon9 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.pushButtonSaveMeasurement.setIcon(icon9)

        self.horizontalLayoutMeasurementsButtons.addWidget(self.pushButtonSaveMeasurement)


        self.verticalLayoutManufacturer.addLayout(self.horizontalLayoutMeasurementsButtons)


        self.horizontalLayoutMeasurementsLeft.addWidget(self.groupBoxMeasurement)


        self.horizontalLayoutMeasurement.addLayout(self.horizontalLayoutMeasurementsLeft)

        self.horizontalSpacerMeasurementCenter = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutMeasurement.addItem(self.horizontalSpacerMeasurementCenter)

        self.groupBoxSpokeMeasurement = QGroupBox(self.measurementTab)
        self.groupBoxSpokeMeasurement.setObjectName(u"groupBoxSpokeMeasurement")
        self.verticalLayoutSpokeMeasurement = QVBoxLayout(self.groupBoxSpokeMeasurement)
        self.verticalLayoutSpokeMeasurement.setObjectName(u"verticalLayoutSpokeMeasurement")
        self.groupBoxManufacturer2 = QGroupBox(self.groupBoxSpokeMeasurement)
        self.groupBoxManufacturer2.setObjectName(u"groupBoxManufacturer2")
        self.verticalLayoutManufacturerMeasurement = QVBoxLayout(self.groupBoxManufacturer2)
        self.verticalLayoutManufacturerMeasurement.setObjectName(u"verticalLayoutManufacturerMeasurement")
        self.comboBoxManufacturer2 = QComboBox(self.groupBoxManufacturer2)
        self.comboBoxManufacturer2.setObjectName(u"comboBoxManufacturer2")
        sizePolicy1.setHeightForWidth(self.comboBoxManufacturer2.sizePolicy().hasHeightForWidth())
        self.comboBoxManufacturer2.setSizePolicy(sizePolicy1)

        self.verticalLayoutManufacturerMeasurement.addWidget(self.comboBoxManufacturer2)

        self.horizontalLayoutManufacturer = QHBoxLayout()
        self.horizontalLayoutManufacturer.setObjectName(u"horizontalLayoutManufacturer")
        self.groupBoxNewManufacturer2 = QGroupBox(self.groupBoxManufacturer2)
        self.groupBoxNewManufacturer2.setObjectName(u"groupBoxNewManufacturer2")
        sizePolicy1.setHeightForWidth(self.groupBoxNewManufacturer2.sizePolicy().hasHeightForWidth())
        self.groupBoxNewManufacturer2.setSizePolicy(sizePolicy1)
        self.verticalLayoutNewManufacturerMeasurement = QVBoxLayout(self.groupBoxNewManufacturer2)
        self.verticalLayoutNewManufacturerMeasurement.setObjectName(u"verticalLayoutNewManufacturerMeasurement")
        self.lineEditNewManufacturer2 = QLineEdit(self.groupBoxNewManufacturer2)
        self.lineEditNewManufacturer2.setObjectName(u"lineEditNewManufacturer2")
        sizePolicy1.setHeightForWidth(self.lineEditNewManufacturer2.sizePolicy().hasHeightForWidth())
        self.lineEditNewManufacturer2.setSizePolicy(sizePolicy1)

        self.verticalLayoutNewManufacturerMeasurement.addWidget(self.lineEditNewManufacturer2)


        self.horizontalLayoutManufacturer.addWidget(self.groupBoxNewManufacturer2)

        self.horizontalSpacerManufacturer2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutManufacturer.addItem(self.horizontalSpacerManufacturer2)

        self.pushButtonNewManufacturer2 = QPushButton(self.groupBoxManufacturer2)
        self.pushButtonNewManufacturer2.setObjectName(u"pushButtonNewManufacturer2")
        sizePolicy3.setHeightForWidth(self.pushButtonNewManufacturer2.sizePolicy().hasHeightForWidth())
        self.pushButtonNewManufacturer2.setSizePolicy(sizePolicy3)
        self.pushButtonNewManufacturer2.setIcon(icon5)

        self.horizontalLayoutManufacturer.addWidget(self.pushButtonNewManufacturer2)

        self.horizontalLayoutManufacturer.setStretch(0, 3)
        self.horizontalLayoutManufacturer.setStretch(2, 1)

        self.verticalLayoutManufacturerMeasurement.addLayout(self.horizontalLayoutManufacturer)


        self.verticalLayoutSpokeMeasurement.addWidget(self.groupBoxManufacturer2)

        self.verticalSpacerMeasurementTop = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutSpokeMeasurement.addItem(self.verticalSpacerMeasurementTop)

        self.groupBoxSpoke2 = QGroupBox(self.groupBoxSpokeMeasurement)
        self.groupBoxSpoke2.setObjectName(u"groupBoxSpoke2")
        self.verticalLayoutSelectSpokeMeasurement = QVBoxLayout(self.groupBoxSpoke2)
        self.verticalLayoutSelectSpokeMeasurement.setObjectName(u"verticalLayoutSelectSpokeMeasurement")
        self.comboBoxSpoke2 = QComboBox(self.groupBoxSpoke2)
        self.comboBoxSpoke2.setObjectName(u"comboBoxSpoke2")
        sizePolicy1.setHeightForWidth(self.comboBoxSpoke2.sizePolicy().hasHeightForWidth())
        self.comboBoxSpoke2.setSizePolicy(sizePolicy1)

        self.verticalLayoutSelectSpokeMeasurement.addWidget(self.comboBoxSpoke2)


        self.verticalLayoutSpokeMeasurement.addWidget(self.groupBoxSpoke2)

        self.groupBoxName2 = QGroupBox(self.groupBoxSpokeMeasurement)
        self.groupBoxName2.setObjectName(u"groupBoxName2")
        self.verticalLayoutSpokeNameMeasurement = QVBoxLayout(self.groupBoxName2)
        self.verticalLayoutSpokeNameMeasurement.setObjectName(u"verticalLayoutSpokeNameMeasurement")
        self.lineEditName2 = QLineEdit(self.groupBoxName2)
        self.lineEditName2.setObjectName(u"lineEditName2")
        sizePolicy1.setHeightForWidth(self.lineEditName2.sizePolicy().hasHeightForWidth())
        self.lineEditName2.setSizePolicy(sizePolicy1)

        self.verticalLayoutSpokeNameMeasurement.addWidget(self.lineEditName2)


        self.verticalLayoutSpokeMeasurement.addWidget(self.groupBoxName2)

        self.horizontalLayoutSpokeDefinitionsMeasurement = QHBoxLayout()
        self.horizontalLayoutSpokeDefinitionsMeasurement.setObjectName(u"horizontalLayoutSpokeDefinitionsMeasurement")
        self.groupBoxType2 = QGroupBox(self.groupBoxSpokeMeasurement)
        self.groupBoxType2.setObjectName(u"groupBoxType2")
        self.verticalLayoutTypeMeasurement = QVBoxLayout(self.groupBoxType2)
        self.verticalLayoutTypeMeasurement.setObjectName(u"verticalLayoutTypeMeasurement")
        self.comboBoxType2 = QComboBox(self.groupBoxType2)
        self.comboBoxType2.setObjectName(u"comboBoxType2")
        sizePolicy4.setHeightForWidth(self.comboBoxType2.sizePolicy().hasHeightForWidth())
        self.comboBoxType2.setSizePolicy(sizePolicy4)
        self.comboBoxType2.setMinimumSize(QSize(150, 0))

        self.verticalLayoutTypeMeasurement.addWidget(self.comboBoxType2)


        self.horizontalLayoutSpokeDefinitionsMeasurement.addWidget(self.groupBoxType2)

        self.horizontalSpacerSpokeMeasurement = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutSpokeDefinitionsMeasurement.addItem(self.horizontalSpacerSpokeMeasurement)

        self.groupBoxGauge2 = QGroupBox(self.groupBoxSpokeMeasurement)
        self.groupBoxGauge2.setObjectName(u"groupBoxGauge2")
        self.verticalLayoutGaugeMeasurement = QVBoxLayout(self.groupBoxGauge2)
        self.verticalLayoutGaugeMeasurement.setObjectName(u"verticalLayoutGaugeMeasurement")
        self.lineEditGauge2 = QLineEdit(self.groupBoxGauge2)
        self.lineEditGauge2.setObjectName(u"lineEditGauge2")
        sizePolicy1.setHeightForWidth(self.lineEditGauge2.sizePolicy().hasHeightForWidth())
        self.lineEditGauge2.setSizePolicy(sizePolicy1)

        self.verticalLayoutGaugeMeasurement.addWidget(self.lineEditGauge2)


        self.horizontalLayoutSpokeDefinitionsMeasurement.addWidget(self.groupBoxGauge2)

        self.groupBoxWeight2 = QGroupBox(self.groupBoxSpokeMeasurement)
        self.groupBoxWeight2.setObjectName(u"groupBoxWeight2")
        self.verticalLayoutWeightMeasurement = QVBoxLayout(self.groupBoxWeight2)
        self.verticalLayoutWeightMeasurement.setObjectName(u"verticalLayoutWeightMeasurement")
        self.lineEditWeight2 = QLineEdit(self.groupBoxWeight2)
        self.lineEditWeight2.setObjectName(u"lineEditWeight2")
        sizePolicy1.setHeightForWidth(self.lineEditWeight2.sizePolicy().hasHeightForWidth())
        self.lineEditWeight2.setSizePolicy(sizePolicy1)

        self.verticalLayoutWeightMeasurement.addWidget(self.lineEditWeight2)


        self.horizontalLayoutSpokeDefinitionsMeasurement.addWidget(self.groupBoxWeight2)

        self.horizontalLayoutSpokeDefinitionsMeasurement.setStretch(0, 10)
        self.horizontalLayoutSpokeDefinitionsMeasurement.setStretch(1, 1)
        self.horizontalLayoutSpokeDefinitionsMeasurement.setStretch(2, 1)
        self.horizontalLayoutSpokeDefinitionsMeasurement.setStretch(3, 1)

        self.verticalLayoutSpokeMeasurement.addLayout(self.horizontalLayoutSpokeDefinitionsMeasurement)

        self.groupBoxDimension2 = QGroupBox(self.groupBoxSpokeMeasurement)
        self.groupBoxDimension2.setObjectName(u"groupBoxDimension2")
        self.verticalLayoutSpokeDimensionMeasurement = QVBoxLayout(self.groupBoxDimension2)
        self.verticalLayoutSpokeDimensionMeasurement.setObjectName(u"verticalLayoutSpokeDimensionMeasurement")
        self.lineEditDimension2 = QLineEdit(self.groupBoxDimension2)
        self.lineEditDimension2.setObjectName(u"lineEditDimension2")
        sizePolicy1.setHeightForWidth(self.lineEditDimension2.sizePolicy().hasHeightForWidth())
        self.lineEditDimension2.setSizePolicy(sizePolicy1)

        self.verticalLayoutSpokeDimensionMeasurement.addWidget(self.lineEditDimension2)


        self.verticalLayoutSpokeMeasurement.addWidget(self.groupBoxDimension2)

        self.groupBoxSpokeComment2 = QGroupBox(self.groupBoxSpokeMeasurement)
        self.groupBoxSpokeComment2.setObjectName(u"groupBoxSpokeComment2")
        self.verticalLayoutSpokeCommentMeasurement = QVBoxLayout(self.groupBoxSpokeComment2)
        self.verticalLayoutSpokeCommentMeasurement.setObjectName(u"verticalLayoutSpokeCommentMeasurement")
        self.lineEditSpokeComment2 = QLineEdit(self.groupBoxSpokeComment2)
        self.lineEditSpokeComment2.setObjectName(u"lineEditSpokeComment2")
        sizePolicy1.setHeightForWidth(self.lineEditSpokeComment2.sizePolicy().hasHeightForWidth())
        self.lineEditSpokeComment2.setSizePolicy(sizePolicy1)

        self.verticalLayoutSpokeCommentMeasurement.addWidget(self.lineEditSpokeComment2)


        self.verticalLayoutSpokeMeasurement.addWidget(self.groupBoxSpokeComment2)

        self.verticalSpacerMeasurementBottom = QSpacerItem(20, 28, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutSpokeMeasurement.addItem(self.verticalSpacerMeasurementBottom)

        self.horizontalLayoutSpokeButtonsMeasurement = QHBoxLayout()
        self.horizontalLayoutSpokeButtonsMeasurement.setObjectName(u"horizontalLayoutSpokeButtonsMeasurement")
        self.pushButtonCreateSpoke2 = QPushButton(self.groupBoxSpokeMeasurement)
        self.pushButtonCreateSpoke2.setObjectName(u"pushButtonCreateSpoke2")
        sizePolicy2.setHeightForWidth(self.pushButtonCreateSpoke2.sizePolicy().hasHeightForWidth())
        self.pushButtonCreateSpoke2.setSizePolicy(sizePolicy2)
        self.pushButtonCreateSpoke2.setIcon(icon2)

        self.horizontalLayoutSpokeButtonsMeasurement.addWidget(self.pushButtonCreateSpoke2)

        self.horizontalSpacerMeasurementRight = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutSpokeButtonsMeasurement.addItem(self.horizontalSpacerMeasurementRight)

        self.pushButtonMeasureSpoke = QPushButton(self.groupBoxSpokeMeasurement)
        self.pushButtonMeasureSpoke.setObjectName(u"pushButtonMeasureSpoke")
        sizePolicy2.setHeightForWidth(self.pushButtonMeasureSpoke.sizePolicy().hasHeightForWidth())
        self.pushButtonMeasureSpoke.setSizePolicy(sizePolicy2)
        icon10 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties))
        self.pushButtonMeasureSpoke.setIcon(icon10)

        self.horizontalLayoutSpokeButtonsMeasurement.addWidget(self.pushButtonMeasureSpoke)


        self.verticalLayoutSpokeMeasurement.addLayout(self.horizontalLayoutSpokeButtonsMeasurement)


        self.horizontalLayoutMeasurement.addWidget(self.groupBoxSpokeMeasurement)

        self.horizontalLayoutMeasurement.setStretch(0, 2)
        self.horizontalLayoutMeasurement.setStretch(2, 1)

        self.horizontalLayoutMeasurementTop.addLayout(self.horizontalLayoutMeasurement)

        self.tabWidget.addTab(self.measurementTab, "")
        self.tensionTab = QWidget()
        self.tensionTab.setObjectName(u"tensionTab")
        self.horizontalLayoutTensionTabTop = QHBoxLayout(self.tensionTab)
        self.horizontalLayoutTensionTabTop.setObjectName(u"horizontalLayoutTensionTabTop")
        self.horizontalLayoutTensionTab = QHBoxLayout()
        self.horizontalLayoutTensionTab.setObjectName(u"horizontalLayoutTensionTab")
        self.groupBoxSideLeft = QGroupBox(self.tensionTab)
        self.groupBoxSideLeft.setObjectName(u"groupBoxSideLeft")
        sizePolicy1.setHeightForWidth(self.groupBoxSideLeft.sizePolicy().hasHeightForWidth())
        self.groupBoxSideLeft.setSizePolicy(sizePolicy1)
        self.verticalLayoutSideLeft = QVBoxLayout(self.groupBoxSideLeft)
        self.verticalLayoutSideLeft.setSpacing(1)
        self.verticalLayoutSideLeft.setObjectName(u"verticalLayoutSideLeft")
        self.verticalLayoutSideLeft.setContentsMargins(2, 1, 2, 1)
        self.horizontalLayoutAmountTensionLeft = QHBoxLayout()
        self.horizontalLayoutAmountTensionLeft.setObjectName(u"horizontalLayoutAmountTensionLeft")
        self.horizontalLayoutAmountTensionLeft.setContentsMargins(-1, 0, -1, -1)
        self.groupBoxSpokeAmountLeft = QGroupBox(self.groupBoxSideLeft)
        self.groupBoxSpokeAmountLeft.setObjectName(u"groupBoxSpokeAmountLeft")
        sizePolicy1.setHeightForWidth(self.groupBoxSpokeAmountLeft.sizePolicy().hasHeightForWidth())
        self.groupBoxSpokeAmountLeft.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.groupBoxSpokeAmountLeft)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEditSpokeAmountLeft = QLineEdit(self.groupBoxSpokeAmountLeft)
        self.lineEditSpokeAmountLeft.setObjectName(u"lineEditSpokeAmountLeft")
        sizePolicy2.setHeightForWidth(self.lineEditSpokeAmountLeft.sizePolicy().hasHeightForWidth())
        self.lineEditSpokeAmountLeft.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.lineEditSpokeAmountLeft)


        self.horizontalLayoutAmountTensionLeft.addWidget(self.groupBoxSpokeAmountLeft)

        self.horizontalSpacerAmountTensionLeft = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutAmountTensionLeft.addItem(self.horizontalSpacerAmountTensionLeft)

        self.GroupBoxTargetTensionLeft = QGroupBox(self.groupBoxSideLeft)
        self.GroupBoxTargetTensionLeft.setObjectName(u"GroupBoxTargetTensionLeft")
        sizePolicy2.setHeightForWidth(self.GroupBoxTargetTensionLeft.sizePolicy().hasHeightForWidth())
        self.GroupBoxTargetTensionLeft.setSizePolicy(sizePolicy2)
        self.horizontalLayoutNewtonKgfLeft = QHBoxLayout(self.GroupBoxTargetTensionLeft)
        self.horizontalLayoutNewtonKgfLeft.setObjectName(u"horizontalLayoutNewtonKgfLeft")
        self.lineEditTargetTensionLeft = QLineEdit(self.GroupBoxTargetTensionLeft)
        self.lineEditTargetTensionLeft.setObjectName(u"lineEditTargetTensionLeft")
        sizePolicy2.setHeightForWidth(self.lineEditTargetTensionLeft.sizePolicy().hasHeightForWidth())
        self.lineEditTargetTensionLeft.setSizePolicy(sizePolicy2)

        self.horizontalLayoutNewtonKgfLeft.addWidget(self.lineEditTargetTensionLeft)


        self.horizontalLayoutAmountTensionLeft.addWidget(self.GroupBoxTargetTensionLeft)


        self.verticalLayoutSideLeft.addLayout(self.horizontalLayoutAmountTensionLeft)

        self.groupBoxSelectedSpokeLeft = QGroupBox(self.groupBoxSideLeft)
        self.groupBoxSelectedSpokeLeft.setObjectName(u"groupBoxSelectedSpokeLeft")
        self.verticalLayoutSelectedSpokeLeft = QVBoxLayout(self.groupBoxSelectedSpokeLeft)
        self.verticalLayoutSelectedSpokeLeft.setSpacing(6)
        self.verticalLayoutSelectedSpokeLeft.setObjectName(u"verticalLayoutSelectedSpokeLeft")
        self.plainTextEditSelectedSpokeLeft = QPlainTextEdit(self.groupBoxSelectedSpokeLeft)
        self.plainTextEditSelectedSpokeLeft.setObjectName(u"plainTextEditSelectedSpokeLeft")
        self.plainTextEditSelectedSpokeLeft.setReadOnly(True)

        self.verticalLayoutSelectedSpokeLeft.addWidget(self.plainTextEditSelectedSpokeLeft)


        self.verticalLayoutSideLeft.addWidget(self.groupBoxSelectedSpokeLeft)

        self.groupBoxTensionValuesLeft = QGroupBox(self.groupBoxSideLeft)
        self.groupBoxTensionValuesLeft.setObjectName(u"groupBoxTensionValuesLeft")
        self.verticalLayoutSelectedTensionValuesLeft = QVBoxLayout(self.groupBoxTensionValuesLeft)
        self.verticalLayoutSelectedTensionValuesLeft.setSpacing(6)
        self.verticalLayoutSelectedTensionValuesLeft.setObjectName(u"verticalLayoutSelectedTensionValuesLeft")
        self.tableViewTensionsLeft = QTableView(self.groupBoxTensionValuesLeft)
        self.tableViewTensionsLeft.setObjectName(u"tableViewTensionsLeft")

        self.verticalLayoutSelectedTensionValuesLeft.addWidget(self.tableViewTensionsLeft)


        self.verticalLayoutSideLeft.addWidget(self.groupBoxTensionValuesLeft)

        self.verticalLayoutSideLeft.setStretch(1, 2)
        self.verticalLayoutSideLeft.setStretch(2, 10)

        self.horizontalLayoutTensionTab.addWidget(self.groupBoxSideLeft)

        self.groupBoxSideRight = QGroupBox(self.tensionTab)
        self.groupBoxSideRight.setObjectName(u"groupBoxSideRight")
        sizePolicy1.setHeightForWidth(self.groupBoxSideRight.sizePolicy().hasHeightForWidth())
        self.groupBoxSideRight.setSizePolicy(sizePolicy1)
        self.verticalLayoutSideRight = QVBoxLayout(self.groupBoxSideRight)
        self.verticalLayoutSideRight.setSpacing(1)
        self.verticalLayoutSideRight.setObjectName(u"verticalLayoutSideRight")
        self.verticalLayoutSideRight.setContentsMargins(2, 1, 2, 1)
        self.horizontalLayoutAmountTensionRight = QHBoxLayout()
        self.horizontalLayoutAmountTensionRight.setObjectName(u"horizontalLayoutAmountTensionRight")
        self.horizontalLayoutAmountTensionRight.setContentsMargins(-1, 0, -1, -1)
        self.groupBoxSpokeAmountRight = QGroupBox(self.groupBoxSideRight)
        self.groupBoxSpokeAmountRight.setObjectName(u"groupBoxSpokeAmountRight")
        self.verticalLayoutSpokeAmountRight = QVBoxLayout(self.groupBoxSpokeAmountRight)
        self.verticalLayoutSpokeAmountRight.setSpacing(6)
        self.verticalLayoutSpokeAmountRight.setObjectName(u"verticalLayoutSpokeAmountRight")
        self.lineEditSpokeAmountRight = QLineEdit(self.groupBoxSpokeAmountRight)
        self.lineEditSpokeAmountRight.setObjectName(u"lineEditSpokeAmountRight")

        self.verticalLayoutSpokeAmountRight.addWidget(self.lineEditSpokeAmountRight)


        self.horizontalLayoutAmountTensionRight.addWidget(self.groupBoxSpokeAmountRight)

        self.horizontalSpacerAmountTensionRight = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutAmountTensionRight.addItem(self.horizontalSpacerAmountTensionRight)

        self.GroupBoxTargetTensionRight = QGroupBox(self.groupBoxSideRight)
        self.GroupBoxTargetTensionRight.setObjectName(u"GroupBoxTargetTensionRight")
        sizePolicy2.setHeightForWidth(self.GroupBoxTargetTensionRight.sizePolicy().hasHeightForWidth())
        self.GroupBoxTargetTensionRight.setSizePolicy(sizePolicy2)
        self.horizontalLayoutNewtonKgfRight = QHBoxLayout(self.GroupBoxTargetTensionRight)
        self.horizontalLayoutNewtonKgfRight.setObjectName(u"horizontalLayoutNewtonKgfRight")
        self.lineEditTargetTensionRight = QLineEdit(self.GroupBoxTargetTensionRight)
        self.lineEditTargetTensionRight.setObjectName(u"lineEditTargetTensionRight")
        sizePolicy2.setHeightForWidth(self.lineEditTargetTensionRight.sizePolicy().hasHeightForWidth())
        self.lineEditTargetTensionRight.setSizePolicy(sizePolicy2)

        self.horizontalLayoutNewtonKgfRight.addWidget(self.lineEditTargetTensionRight)


        self.horizontalLayoutAmountTensionRight.addWidget(self.GroupBoxTargetTensionRight)


        self.verticalLayoutSideRight.addLayout(self.horizontalLayoutAmountTensionRight)

        self.groupBoxSelectedSpokeRight = QGroupBox(self.groupBoxSideRight)
        self.groupBoxSelectedSpokeRight.setObjectName(u"groupBoxSelectedSpokeRight")
        self.verticalLayoutSelectedSpokeRight = QVBoxLayout(self.groupBoxSelectedSpokeRight)
        self.verticalLayoutSelectedSpokeRight.setSpacing(6)
        self.verticalLayoutSelectedSpokeRight.setObjectName(u"verticalLayoutSelectedSpokeRight")
        self.plainTextEditSelectedSpokeRight = QPlainTextEdit(self.groupBoxSelectedSpokeRight)
        self.plainTextEditSelectedSpokeRight.setObjectName(u"plainTextEditSelectedSpokeRight")
        self.plainTextEditSelectedSpokeRight.setReadOnly(True)

        self.verticalLayoutSelectedSpokeRight.addWidget(self.plainTextEditSelectedSpokeRight)


        self.verticalLayoutSideRight.addWidget(self.groupBoxSelectedSpokeRight)

        self.groupBoxTensionValuesRight = QGroupBox(self.groupBoxSideRight)
        self.groupBoxTensionValuesRight.setObjectName(u"groupBoxTensionValuesRight")
        self.verticalLayoutSelectedTensionValuesRight = QVBoxLayout(self.groupBoxTensionValuesRight)
        self.verticalLayoutSelectedTensionValuesRight.setSpacing(6)
        self.verticalLayoutSelectedTensionValuesRight.setObjectName(u"verticalLayoutSelectedTensionValuesRight")
        self.tableViewTensionsRight = QTableView(self.groupBoxTensionValuesRight)
        self.tableViewTensionsRight.setObjectName(u"tableViewTensionsRight")

        self.verticalLayoutSelectedTensionValuesRight.addWidget(self.tableViewTensionsRight)


        self.verticalLayoutSideRight.addWidget(self.groupBoxTensionValuesRight)

        self.verticalLayoutSideRight.setStretch(1, 2)
        self.verticalLayoutSideRight.setStretch(2, 10)

        self.horizontalLayoutTensionTab.addWidget(self.groupBoxSideRight)

        self.groupBoxWheel = QGroupBox(self.tensionTab)
        self.groupBoxWheel.setObjectName(u"groupBoxWheel")
        sizePolicy1.setHeightForWidth(self.groupBoxWheel.sizePolicy().hasHeightForWidth())
        self.groupBoxWheel.setSizePolicy(sizePolicy1)
        self.verticalLayoutMeasurement = QVBoxLayout(self.groupBoxWheel)
        self.verticalLayoutMeasurement.setObjectName(u"verticalLayoutMeasurement")
        self.verticalLayoutWheelDiagram = QVBoxLayout()
        self.verticalLayoutWheelDiagram.setSpacing(6)
        self.verticalLayoutWheelDiagram.setObjectName(u"verticalLayoutWheelDiagram")
        self.graphicsViewDiagram = QGraphicsView(self.groupBoxWheel)
        self.graphicsViewDiagram.setObjectName(u"graphicsViewDiagram")

        self.verticalLayoutWheelDiagram.addWidget(self.graphicsViewDiagram)


        self.verticalLayoutMeasurement.addLayout(self.verticalLayoutWheelDiagram)

        self.gridLayoutTensionButtons = QGridLayout()
        self.gridLayoutTensionButtons.setObjectName(u"gridLayoutTensionButtons")
        self.gridLayoutTensionButtons.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalSpacerSpokeEditsLeft = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutTensionButtons.addItem(self.horizontalSpacerSpokeEditsLeft, 0, 3, 1, 1)

        self.pushButtonPreviousSpoke = QPushButton(self.groupBoxWheel)
        self.pushButtonPreviousSpoke.setObjectName(u"pushButtonPreviousSpoke")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.pushButtonPreviousSpoke.sizePolicy().hasHeightForWidth())
        self.pushButtonPreviousSpoke.setSizePolicy(sizePolicy5)
        self.pushButtonPreviousSpoke.setIcon(icon)

        self.gridLayoutTensionButtons.addWidget(self.pushButtonPreviousSpoke, 0, 1, 1, 1)

        self.pushButtonNextSpoke = QPushButton(self.groupBoxWheel)
        self.pushButtonNextSpoke.setObjectName(u"pushButtonNextSpoke")
        sizePolicy5.setHeightForWidth(self.pushButtonNextSpoke.sizePolicy().hasHeightForWidth())
        self.pushButtonNextSpoke.setSizePolicy(sizePolicy5)
        self.pushButtonNextSpoke.setIcon(icon1)

        self.gridLayoutTensionButtons.addWidget(self.pushButtonNextSpoke, 0, 2, 1, 1)

        self.pushButtonSwitchView = QPushButton(self.groupBoxWheel)
        self.pushButtonSwitchView.setObjectName(u"pushButtonSwitchView")
        sizePolicy5.setHeightForWidth(self.pushButtonSwitchView.sizePolicy().hasHeightForWidth())
        self.pushButtonSwitchView.setSizePolicy(sizePolicy5)
        icon11 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaylistRepeat))
        self.pushButtonSwitchView.setIcon(icon11)

        self.gridLayoutTensionButtons.addWidget(self.pushButtonSwitchView, 0, 4, 1, 1)


        self.verticalLayoutMeasurement.addLayout(self.gridLayoutTensionButtons)

        self.verticalLayoutMeasurement.setStretch(0, 10)

        self.horizontalLayoutTensionTab.addWidget(self.groupBoxWheel)

        self.horizontalLayoutTensionTab.setStretch(0, 1)
        self.horizontalLayoutTensionTab.setStretch(1, 1)
        self.horizontalLayoutTensionTab.setStretch(2, 10)

        self.horizontalLayoutTensionTabTop.addLayout(self.horizontalLayoutTensionTab)

        self.tabWidget.addTab(self.tensionTab, "")
        self.setupTab = QWidget()
        self.setupTab.setObjectName(u"setupTab")
        self.horizontalLayoutSetup = QHBoxLayout(self.setupTab)
        self.horizontalLayoutSetup.setObjectName(u"horizontalLayoutSetup")
        self.horizontalLayoutSetupLeft = QHBoxLayout()
        self.horizontalLayoutSetupLeft.setObjectName(u"horizontalLayoutSetupLeft")
        self.verticalLayoutSetupLeft = QVBoxLayout()
        self.verticalLayoutSetupLeft.setObjectName(u"verticalLayoutSetupLeft")
        self.groupBoxLanguage = QGroupBox(self.setupTab)
        self.groupBoxLanguage.setObjectName(u"groupBoxLanguage")
        sizePolicy3.setHeightForWidth(self.groupBoxLanguage.sizePolicy().hasHeightForWidth())
        self.groupBoxLanguage.setSizePolicy(sizePolicy3)
        self.groupBoxLanguage.setMinimumSize(QSize(250, 0))
        self.verticalLayoutSetupLaguage = QVBoxLayout(self.groupBoxLanguage)
        self.verticalLayoutSetupLaguage.setObjectName(u"verticalLayoutSetupLaguage")
        self.comboBoxSelectLanguage = QComboBox(self.groupBoxLanguage)
        self.comboBoxSelectLanguage.setObjectName(u"comboBoxSelectLanguage")
        sizePolicy3.setHeightForWidth(self.comboBoxSelectLanguage.sizePolicy().hasHeightForWidth())
        self.comboBoxSelectLanguage.setSizePolicy(sizePolicy3)

        self.verticalLayoutSetupLaguage.addWidget(self.comboBoxSelectLanguage)


        self.verticalLayoutSetupLeft.addWidget(self.groupBoxLanguage)

        self.groupBoxSpokeduino = QGroupBox(self.setupTab)
        self.groupBoxSpokeduino.setObjectName(u"groupBoxSpokeduino")
        sizePolicy3.setHeightForWidth(self.groupBoxSpokeduino.sizePolicy().hasHeightForWidth())
        self.groupBoxSpokeduino.setSizePolicy(sizePolicy3)
        self.groupBoxSpokeduino.setMinimumSize(QSize(250, 0))
        self.verticalLayoutSelectPort = QVBoxLayout(self.groupBoxSpokeduino)
        self.verticalLayoutSelectPort.setObjectName(u"verticalLayoutSelectPort")
        self.comboBoxSpokeduinoPort = QComboBox(self.groupBoxSpokeduino)
        self.comboBoxSpokeduinoPort.setObjectName(u"comboBoxSpokeduinoPort")
        sizePolicy3.setHeightForWidth(self.comboBoxSpokeduinoPort.sizePolicy().hasHeightForWidth())
        self.comboBoxSpokeduinoPort.setSizePolicy(sizePolicy3)

        self.verticalLayoutSelectPort.addWidget(self.comboBoxSpokeduinoPort)


        self.verticalLayoutSetupLeft.addWidget(self.groupBoxSpokeduino)

        self.verticalSpacerLanguageTensiometer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutSetupLeft.addItem(self.verticalSpacerLanguageTensiometer)

        self.groupBoxTensiometer = QGroupBox(self.setupTab)
        self.groupBoxTensiometer.setObjectName(u"groupBoxTensiometer")
        sizePolicy3.setHeightForWidth(self.groupBoxTensiometer.sizePolicy().hasHeightForWidth())
        self.groupBoxTensiometer.setSizePolicy(sizePolicy3)
        self.groupBoxTensiometer.setMinimumSize(QSize(250, 0))
        self.verticalLayoutTensiometer = QVBoxLayout(self.groupBoxTensiometer)
        self.verticalLayoutTensiometer.setObjectName(u"verticalLayoutTensiometer")
        self.comboBoxTensiometer = QComboBox(self.groupBoxTensiometer)
        self.comboBoxTensiometer.setObjectName(u"comboBoxTensiometer")
        sizePolicy3.setHeightForWidth(self.comboBoxTensiometer.sizePolicy().hasHeightForWidth())
        self.comboBoxTensiometer.setSizePolicy(sizePolicy3)

        self.verticalLayoutTensiometer.addWidget(self.comboBoxTensiometer)

        self.horizontalLayoutNewTensiometer = QHBoxLayout()
        self.horizontalLayoutNewTensiometer.setObjectName(u"horizontalLayoutNewTensiometer")
        self.groupBoxtNewTensiometer = QGroupBox(self.groupBoxTensiometer)
        self.groupBoxtNewTensiometer.setObjectName(u"groupBoxtNewTensiometer")
        sizePolicy3.setHeightForWidth(self.groupBoxtNewTensiometer.sizePolicy().hasHeightForWidth())
        self.groupBoxtNewTensiometer.setSizePolicy(sizePolicy3)
        self.groupBoxtNewTensiometer.setMinimumSize(QSize(250, 0))
        self.verticalLayoutNewTensiometer = QVBoxLayout(self.groupBoxtNewTensiometer)
        self.verticalLayoutNewTensiometer.setObjectName(u"verticalLayoutNewTensiometer")
        self.lineEditNewTensiometer = QLineEdit(self.groupBoxtNewTensiometer)
        self.lineEditNewTensiometer.setObjectName(u"lineEditNewTensiometer")
        sizePolicy3.setHeightForWidth(self.lineEditNewTensiometer.sizePolicy().hasHeightForWidth())
        self.lineEditNewTensiometer.setSizePolicy(sizePolicy3)

        self.verticalLayoutNewTensiometer.addWidget(self.lineEditNewTensiometer)


        self.horizontalLayoutNewTensiometer.addWidget(self.groupBoxtNewTensiometer)

        self.pushButtonNewTensiometer = QPushButton(self.groupBoxTensiometer)
        self.pushButtonNewTensiometer.setObjectName(u"pushButtonNewTensiometer")
        sizePolicy2.setHeightForWidth(self.pushButtonNewTensiometer.sizePolicy().hasHeightForWidth())
        self.pushButtonNewTensiometer.setSizePolicy(sizePolicy2)
        self.pushButtonNewTensiometer.setIcon(icon2)

        self.horizontalLayoutNewTensiometer.addWidget(self.pushButtonNewTensiometer)


        self.verticalLayoutTensiometer.addLayout(self.horizontalLayoutNewTensiometer)


        self.verticalLayoutSetupLeft.addWidget(self.groupBoxTensiometer)

        self.verticalSpacerSetupLeftReserved = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutSetupLeft.addItem(self.verticalSpacerSetupLeftReserved)

        self.verticalLayoutSetupLeft.setStretch(0, 1)
        self.verticalLayoutSetupLeft.setStretch(1, 1)
        self.verticalLayoutSetupLeft.setStretch(3, 1)
        self.verticalLayoutSetupLeft.setStretch(4, 1)

        self.horizontalLayoutSetupLeft.addLayout(self.verticalLayoutSetupLeft)

        self.verticalLayoutDirectionsConverter = QVBoxLayout()
        self.verticalLayoutDirectionsConverter.setObjectName(u"verticalLayoutDirectionsConverter")
        self.groupBoxDirectionsSetup = QGroupBox(self.setupTab)
        self.groupBoxDirectionsSetup.setObjectName(u"groupBoxDirectionsSetup")
        sizePolicy1.setHeightForWidth(self.groupBoxDirectionsSetup.sizePolicy().hasHeightForWidth())
        self.groupBoxDirectionsSetup.setSizePolicy(sizePolicy1)
        self.verticalLayoutMeasurementDirection = QVBoxLayout(self.groupBoxDirectionsSetup)
        self.verticalLayoutMeasurementDirection.setObjectName(u"verticalLayoutMeasurementDirection")
        self.groupBoxSpokeMeasurementDirection = QGroupBox(self.groupBoxDirectionsSetup)
        self.groupBoxSpokeMeasurementDirection.setObjectName(u"groupBoxSpokeMeasurementDirection")
        self.verticalLayoutMeasurementDirectionDown = QVBoxLayout(self.groupBoxSpokeMeasurementDirection)
        self.verticalLayoutMeasurementDirectionDown.setObjectName(u"verticalLayoutMeasurementDirectionDown")
        self.radioButtonSpokeMeasurementDirectionDown = QRadioButton(self.groupBoxSpokeMeasurementDirection)
        self.radioButtonSpokeMeasurementDirectionDown.setObjectName(u"radioButtonSpokeMeasurementDirectionDown")
        self.radioButtonSpokeMeasurementDirectionDown.setChecked(True)

        self.verticalLayoutMeasurementDirectionDown.addWidget(self.radioButtonSpokeMeasurementDirectionDown)

        self.radioButtonSpokeMeasurementDirectionUp = QRadioButton(self.groupBoxSpokeMeasurementDirection)
        self.radioButtonSpokeMeasurementDirectionUp.setObjectName(u"radioButtonSpokeMeasurementDirectionUp")

        self.verticalLayoutMeasurementDirectionDown.addWidget(self.radioButtonSpokeMeasurementDirectionUp)


        self.verticalLayoutMeasurementDirection.addWidget(self.groupBoxSpokeMeasurementDirection)

        self.groupBoxWheelRotationDirection = QGroupBox(self.groupBoxDirectionsSetup)
        self.groupBoxWheelRotationDirection.setObjectName(u"groupBoxWheelRotationDirection")
        self.verticalLayoutRotationDirectionClockwise = QVBoxLayout(self.groupBoxWheelRotationDirection)
        self.verticalLayoutRotationDirectionClockwise.setObjectName(u"verticalLayoutRotationDirectionClockwise")
        self.radioButtonWheelRotationDirectionClockwise = QRadioButton(self.groupBoxWheelRotationDirection)
        self.radioButtonWheelRotationDirectionClockwise.setObjectName(u"radioButtonWheelRotationDirectionClockwise")
        self.radioButtonWheelRotationDirectionClockwise.setChecked(True)

        self.verticalLayoutRotationDirectionClockwise.addWidget(self.radioButtonWheelRotationDirectionClockwise)

        self.radioButtonWheelRotationDirectionAnticlockwise = QRadioButton(self.groupBoxWheelRotationDirection)
        self.radioButtonWheelRotationDirectionAnticlockwise.setObjectName(u"radioButtonWheelRotationDirectionAnticlockwise")

        self.verticalLayoutRotationDirectionClockwise.addWidget(self.radioButtonWheelRotationDirectionAnticlockwise)


        self.verticalLayoutMeasurementDirection.addWidget(self.groupBoxWheelRotationDirection)

        self.groupBoxWheelMeasurementType = QGroupBox(self.groupBoxDirectionsSetup)
        self.groupBoxWheelMeasurementType.setObjectName(u"groupBoxWheelMeasurementType")
        self.verticalLayoutMeasurementTypeLeftRight = QVBoxLayout(self.groupBoxWheelMeasurementType)
        self.verticalLayoutMeasurementTypeLeftRight.setObjectName(u"verticalLayoutMeasurementTypeLeftRight")
        self.radioButtonWheelMeasurementTypeLeftRight = QRadioButton(self.groupBoxWheelMeasurementType)
        self.radioButtonWheelMeasurementTypeLeftRight.setObjectName(u"radioButtonWheelMeasurementTypeLeftRight")
        self.radioButtonWheelMeasurementTypeLeftRight.setChecked(False)

        self.verticalLayoutMeasurementTypeLeftRight.addWidget(self.radioButtonWheelMeasurementTypeLeftRight)

        self.radioButtonWheelMeasurementTypeSideBySide = QRadioButton(self.groupBoxWheelMeasurementType)
        self.radioButtonWheelMeasurementTypeSideBySide.setObjectName(u"radioButtonWheelMeasurementTypeSideBySide")
        self.radioButtonWheelMeasurementTypeSideBySide.setChecked(True)

        self.verticalLayoutMeasurementTypeLeftRight.addWidget(self.radioButtonWheelMeasurementTypeSideBySide)

        self.radioButtonWheelMeasurementTypRightLeft = QRadioButton(self.groupBoxWheelMeasurementType)
        self.radioButtonWheelMeasurementTypRightLeft.setObjectName(u"radioButtonWheelMeasurementTypRightLeft")
        self.radioButtonWheelMeasurementTypRightLeft.setEnabled(True)
        self.radioButtonWheelMeasurementTypRightLeft.setChecked(False)

        self.verticalLayoutMeasurementTypeLeftRight.addWidget(self.radioButtonWheelMeasurementTypRightLeft)


        self.verticalLayoutMeasurementDirection.addWidget(self.groupBoxWheelMeasurementType)


        self.verticalLayoutDirectionsConverter.addWidget(self.groupBoxDirectionsSetup)

        self.verticalSpacerUnit = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutDirectionsConverter.addItem(self.verticalSpacerUnit)

        self.groupBoxUnitSetup = QGroupBox(self.setupTab)
        self.groupBoxUnitSetup.setObjectName(u"groupBoxUnitSetup")
        sizePolicy3.setHeightForWidth(self.groupBoxUnitSetup.sizePolicy().hasHeightForWidth())
        self.groupBoxUnitSetup.setSizePolicy(sizePolicy3)
        self.groupBoxUnitSetup.setMinimumSize(QSize(250, 0))
        self.verticalLayoutButtonNewton = QVBoxLayout(self.groupBoxUnitSetup)
        self.verticalLayoutButtonNewton.setObjectName(u"verticalLayoutButtonNewton")
        self.radioButtonNewton = QRadioButton(self.groupBoxUnitSetup)
        self.radioButtonNewton.setObjectName(u"radioButtonNewton")
        sizePolicy3.setHeightForWidth(self.radioButtonNewton.sizePolicy().hasHeightForWidth())
        self.radioButtonNewton.setSizePolicy(sizePolicy3)
        self.radioButtonNewton.setChecked(True)

        self.verticalLayoutButtonNewton.addWidget(self.radioButtonNewton)

        self.radioButtonKgF = QRadioButton(self.groupBoxUnitSetup)
        self.radioButtonKgF.setObjectName(u"radioButtonKgF")
        sizePolicy3.setHeightForWidth(self.radioButtonKgF.sizePolicy().hasHeightForWidth())
        self.radioButtonKgF.setSizePolicy(sizePolicy3)

        self.verticalLayoutButtonNewton.addWidget(self.radioButtonKgF)

        self.radioButtonLbF = QRadioButton(self.groupBoxUnitSetup)
        self.radioButtonLbF.setObjectName(u"radioButtonLbF")
        sizePolicy5.setHeightForWidth(self.radioButtonLbF.sizePolicy().hasHeightForWidth())
        self.radioButtonLbF.setSizePolicy(sizePolicy5)

        self.verticalLayoutButtonNewton.addWidget(self.radioButtonLbF)


        self.verticalLayoutDirectionsConverter.addWidget(self.groupBoxUnitSetup)

        self.verticalSpacerDirectionsConverter = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutDirectionsConverter.addItem(self.verticalSpacerDirectionsConverter)

        self.groupBoxUnitConverter = QGroupBox(self.setupTab)
        self.groupBoxUnitConverter.setObjectName(u"groupBoxUnitConverter")
        self.verticalLayoutUnitCoverter = QVBoxLayout(self.groupBoxUnitConverter)
        self.verticalLayoutUnitCoverter.setObjectName(u"verticalLayoutUnitCoverter")
        self.groupBoxTensionConverterNewton = QGroupBox(self.groupBoxUnitConverter)
        self.groupBoxTensionConverterNewton.setObjectName(u"groupBoxTensionConverterNewton")
        sizePolicy1.setHeightForWidth(self.groupBoxTensionConverterNewton.sizePolicy().hasHeightForWidth())
        self.groupBoxTensionConverterNewton.setSizePolicy(sizePolicy1)
        self.groupBoxTensionConverterNewton.setMinimumSize(QSize(0, 0))
        self.verticalLayoutConverterNewton = QVBoxLayout(self.groupBoxTensionConverterNewton)
        self.verticalLayoutConverterNewton.setObjectName(u"verticalLayoutConverterNewton")
        self.lineEditTensionConverterNewton = QLineEdit(self.groupBoxTensionConverterNewton)
        self.lineEditTensionConverterNewton.setObjectName(u"lineEditTensionConverterNewton")
        sizePolicy1.setHeightForWidth(self.lineEditTensionConverterNewton.sizePolicy().hasHeightForWidth())
        self.lineEditTensionConverterNewton.setSizePolicy(sizePolicy1)

        self.verticalLayoutConverterNewton.addWidget(self.lineEditTensionConverterNewton)


        self.verticalLayoutUnitCoverter.addWidget(self.groupBoxTensionConverterNewton)

        self.groupBoxTensionConverterKgF = QGroupBox(self.groupBoxUnitConverter)
        self.groupBoxTensionConverterKgF.setObjectName(u"groupBoxTensionConverterKgF")
        sizePolicy1.setHeightForWidth(self.groupBoxTensionConverterKgF.sizePolicy().hasHeightForWidth())
        self.groupBoxTensionConverterKgF.setSizePolicy(sizePolicy1)
        self.groupBoxTensionConverterKgF.setMinimumSize(QSize(0, 0))
        self.verticalLayoutConverterKgF = QVBoxLayout(self.groupBoxTensionConverterKgF)
        self.verticalLayoutConverterKgF.setObjectName(u"verticalLayoutConverterKgF")
        self.lineEditTensionConverterKgF = QLineEdit(self.groupBoxTensionConverterKgF)
        self.lineEditTensionConverterKgF.setObjectName(u"lineEditTensionConverterKgF")
        sizePolicy1.setHeightForWidth(self.lineEditTensionConverterKgF.sizePolicy().hasHeightForWidth())
        self.lineEditTensionConverterKgF.setSizePolicy(sizePolicy1)

        self.verticalLayoutConverterKgF.addWidget(self.lineEditTensionConverterKgF)


        self.verticalLayoutUnitCoverter.addWidget(self.groupBoxTensionConverterKgF)

        self.groupBoxTensionConverterLbF = QGroupBox(self.groupBoxUnitConverter)
        self.groupBoxTensionConverterLbF.setObjectName(u"groupBoxTensionConverterLbF")
        sizePolicy1.setHeightForWidth(self.groupBoxTensionConverterLbF.sizePolicy().hasHeightForWidth())
        self.groupBoxTensionConverterLbF.setSizePolicy(sizePolicy1)
        self.groupBoxTensionConverterLbF.setMinimumSize(QSize(0, 0))
        self.verticalLayoutLbFConverter = QVBoxLayout(self.groupBoxTensionConverterLbF)
        self.verticalLayoutLbFConverter.setObjectName(u"verticalLayoutLbFConverter")
        self.lineEditTensionConverterLbF = QLineEdit(self.groupBoxTensionConverterLbF)
        self.lineEditTensionConverterLbF.setObjectName(u"lineEditTensionConverterLbF")
        sizePolicy1.setHeightForWidth(self.lineEditTensionConverterLbF.sizePolicy().hasHeightForWidth())
        self.lineEditTensionConverterLbF.setSizePolicy(sizePolicy1)

        self.verticalLayoutLbFConverter.addWidget(self.lineEditTensionConverterLbF)


        self.verticalLayoutUnitCoverter.addWidget(self.groupBoxTensionConverterLbF)


        self.verticalLayoutDirectionsConverter.addWidget(self.groupBoxUnitConverter)

        self.verticalSpacerDirectionsConverterReserved = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutDirectionsConverter.addItem(self.verticalSpacerDirectionsConverterReserved)


        self.horizontalLayoutSetupLeft.addLayout(self.verticalLayoutDirectionsConverter)

        self.horizontalSpacerReserved = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutSetupLeft.addItem(self.horizontalSpacerReserved)


        self.horizontalLayoutSetup.addLayout(self.horizontalLayoutSetupLeft)

        self.tabWidget.addTab(self.setupTab, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1171, 22))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mainWindow)
        self.statusbar.setObjectName(u"statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.actionMeasure_a_new_spoke)
        self.menuHelp.addAction(self.actionBuild_a_wheel)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(mainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QCoreApplication.translate("mainWindow", u"Spokeduino Mothership", None))
        self.actionAbout.setText(QCoreApplication.translate("mainWindow", u"About", None))
        self.actionMeasure_a_new_spoke.setText(QCoreApplication.translate("mainWindow", u"Measure a new spoke", None))
        self.actionBuild_a_wheel.setText(QCoreApplication.translate("mainWindow", u"Build a wheel", None))
        self.groupBoxListSpokesDatabase.setTitle(QCoreApplication.translate("mainWindow", u"Spokes", None))
        self.groupBoxListMeasurementsDatabase.setTitle(QCoreApplication.translate("mainWindow", u"Measurements", None))
        self.pushButtonUseMeasurementLeft.setText(QCoreApplication.translate("mainWindow", u"Use on the left", None))
        self.pushButtonUseMeasurementRight.setText(QCoreApplication.translate("mainWindow", u"Use on the right", None))
        self.pushButtonAddMeasurement.setText(QCoreApplication.translate("mainWindow", u"Add measurement", None))
        self.pushButtonDeleteMeasurement.setText(QCoreApplication.translate("mainWindow", u"Delete measurement", None))
        self.pushButtonDeleteSpoke.setText(QCoreApplication.translate("mainWindow", u"Delete spoke", None))
        self.groupBoxSpokeDatabase.setTitle(QCoreApplication.translate("mainWindow", u"Select or create a spoke", None))
        self.groupBoxManufacturer.setTitle(QCoreApplication.translate("mainWindow", u"Manufacturer", None))
        self.groupBoxNewManufacturer.setTitle(QCoreApplication.translate("mainWindow", u"New manufacturer", None))
        self.pushButtonNewManufacturer.setText(QCoreApplication.translate("mainWindow", u"Create", None))
        self.groupBoxSpoke.setTitle(QCoreApplication.translate("mainWindow", u"Spoke", None))
        self.groupBoxName.setTitle(QCoreApplication.translate("mainWindow", u"Name", None))
        self.groupBoxType.setTitle(QCoreApplication.translate("mainWindow", u"Type", None))
        self.groupBoxGauge.setTitle(QCoreApplication.translate("mainWindow", u"Gauge", None))
        self.groupBoxWeight.setTitle(QCoreApplication.translate("mainWindow", u"Weight", None))
        self.groupBoxDimension.setTitle(QCoreApplication.translate("mainWindow", u"Dimension", None))
        self.groupBoxSpokeComment.setTitle(QCoreApplication.translate("mainWindow", u"Comment", None))
        self.pushButtonCreateSpoke.setText(QCoreApplication.translate("mainWindow", u"Create", None))
        self.pushButtonEditSpoke.setText(QCoreApplication.translate("mainWindow", u"Edit", None))
        self.pushButtonClearSpoke.setText(QCoreApplication.translate("mainWindow", u"Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.databaseTab), QCoreApplication.translate("mainWindow", u"Browse the spoke database", None))
        self.groupBoxMeasurement.setTitle(QCoreApplication.translate("mainWindow", u"Measurement", None))
        self.groupBoxFormula.setTitle(QCoreApplication.translate("mainWindow", u"Formula", None))
        self.pushButtonCalculateFormula.setText(QCoreApplication.translate("mainWindow", u"Calculate", None))
        self.groupBoxMeasurementComment.setTitle(QCoreApplication.translate("mainWindow", u"Comment", None))
        self.pushButtonPreviousMeasurement.setText(QCoreApplication.translate("mainWindow", u"Previous", None))
        self.pushButtonNextMeasurement.setText(QCoreApplication.translate("mainWindow", u"Next", None))
        self.pushButtonSaveMeasurement.setText(QCoreApplication.translate("mainWindow", u"Save", None))
        self.groupBoxSpokeMeasurement.setTitle(QCoreApplication.translate("mainWindow", u"Select or create a spoke", None))
        self.groupBoxManufacturer2.setTitle(QCoreApplication.translate("mainWindow", u"Manufacturer", None))
        self.groupBoxNewManufacturer2.setTitle(QCoreApplication.translate("mainWindow", u"New manufacturer", None))
        self.pushButtonNewManufacturer2.setText(QCoreApplication.translate("mainWindow", u"Create", None))
        self.groupBoxSpoke2.setTitle(QCoreApplication.translate("mainWindow", u"Spoke", None))
        self.groupBoxName2.setTitle(QCoreApplication.translate("mainWindow", u"Name", None))
        self.groupBoxType2.setTitle(QCoreApplication.translate("mainWindow", u"Type", None))
        self.groupBoxGauge2.setTitle(QCoreApplication.translate("mainWindow", u"Gauge", None))
        self.groupBoxWeight2.setTitle(QCoreApplication.translate("mainWindow", u"Weight", None))
        self.groupBoxDimension2.setTitle(QCoreApplication.translate("mainWindow", u"Dimension", None))
        self.groupBoxSpokeComment2.setTitle(QCoreApplication.translate("mainWindow", u"Comment", None))
        self.pushButtonCreateSpoke2.setText(QCoreApplication.translate("mainWindow", u"Create", None))
        self.pushButtonMeasureSpoke.setText(QCoreApplication.translate("mainWindow", u"Measure", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.measurementTab), QCoreApplication.translate("mainWindow", u"Measure a new spoke", None))
        self.groupBoxSideLeft.setTitle(QCoreApplication.translate("mainWindow", u"Left side", None))
        self.groupBoxSpokeAmountLeft.setTitle(QCoreApplication.translate("mainWindow", u"Spoke amount", None))
        self.GroupBoxTargetTensionLeft.setTitle(QCoreApplication.translate("mainWindow", u"Target tension", None))
        self.groupBoxSelectedSpokeLeft.setTitle(QCoreApplication.translate("mainWindow", u"Selected spoke", None))
        self.groupBoxTensionValuesLeft.setTitle(QCoreApplication.translate("mainWindow", u"Tension values", None))
        self.groupBoxSideRight.setTitle(QCoreApplication.translate("mainWindow", u"Right side", None))
        self.groupBoxSpokeAmountRight.setTitle(QCoreApplication.translate("mainWindow", u"Spoke amount", None))
        self.GroupBoxTargetTensionRight.setTitle(QCoreApplication.translate("mainWindow", u"Target tension", None))
        self.groupBoxSelectedSpokeRight.setTitle(QCoreApplication.translate("mainWindow", u"Selected spoke", None))
        self.groupBoxTensionValuesRight.setTitle(QCoreApplication.translate("mainWindow", u"Tension values", None))
        self.groupBoxWheel.setTitle(QCoreApplication.translate("mainWindow", u"Tension and dishing diagram", None))
        self.pushButtonPreviousSpoke.setText(QCoreApplication.translate("mainWindow", u"Previous spoke", None))
        self.pushButtonNextSpoke.setText(QCoreApplication.translate("mainWindow", u"Next spoke", None))
        self.pushButtonSwitchView.setText(QCoreApplication.translate("mainWindow", u"Switch view", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tensionTab), QCoreApplication.translate("mainWindow", u"Tension a wheel", None))
        self.groupBoxLanguage.setTitle(QCoreApplication.translate("mainWindow", u"Language", None))
        self.groupBoxSpokeduino.setTitle(QCoreApplication.translate("mainWindow", u"Spokeduino port", None))
        self.groupBoxTensiometer.setTitle(QCoreApplication.translate("mainWindow", u"Tensiometer", None))
        self.groupBoxtNewTensiometer.setTitle(QCoreApplication.translate("mainWindow", u"New tensiometer", None))
        self.pushButtonNewTensiometer.setText(QCoreApplication.translate("mainWindow", u"Create", None))
        self.groupBoxDirectionsSetup.setTitle(QCoreApplication.translate("mainWindow", u"Directions", None))
        self.groupBoxSpokeMeasurementDirection.setTitle(QCoreApplication.translate("mainWindow", u"Spoke measurement direction", None))
        self.radioButtonSpokeMeasurementDirectionDown.setText(QCoreApplication.translate("mainWindow", u"From high to low", None))
        self.radioButtonSpokeMeasurementDirectionUp.setText(QCoreApplication.translate("mainWindow", u"From low to high", None))
        self.groupBoxWheelRotationDirection.setTitle(QCoreApplication.translate("mainWindow", u"Wheel rotation direction", None))
        self.radioButtonWheelRotationDirectionClockwise.setText(QCoreApplication.translate("mainWindow", u"Clockwise", None))
        self.radioButtonWheelRotationDirectionAnticlockwise.setText(QCoreApplication.translate("mainWindow", u"Anticlockwise", None))
        self.groupBoxWheelMeasurementType.setTitle(QCoreApplication.translate("mainWindow", u"Wheel measurement direction", None))
        self.radioButtonWheelMeasurementTypeLeftRight.setText(QCoreApplication.translate("mainWindow", u"Left-Right", None))
        self.radioButtonWheelMeasurementTypeSideBySide.setText(QCoreApplication.translate("mainWindow", u"Side by side", None))
        self.radioButtonWheelMeasurementTypRightLeft.setText(QCoreApplication.translate("mainWindow", u"Right-Left", None))
        self.groupBoxUnitSetup.setTitle(QCoreApplication.translate("mainWindow", u"Unit", None))
        self.radioButtonNewton.setText(QCoreApplication.translate("mainWindow", u"Newton", None))
        self.radioButtonKgF.setText(QCoreApplication.translate("mainWindow", u"kgF", None))
        self.radioButtonLbF.setText(QCoreApplication.translate("mainWindow", u"lbF", None))
        self.groupBoxUnitConverter.setTitle(QCoreApplication.translate("mainWindow", u"Unit converter", None))
        self.groupBoxTensionConverterNewton.setTitle(QCoreApplication.translate("mainWindow", u"Newton", None))
        self.groupBoxTensionConverterKgF.setTitle(QCoreApplication.translate("mainWindow", u"kgF", None))
        self.groupBoxTensionConverterLbF.setTitle(QCoreApplication.translate("mainWindow", u"lbF", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.setupTab), QCoreApplication.translate("mainWindow", u"Setup", None))
        self.menuHelp.setTitle(QCoreApplication.translate("mainWindow", u"Help", None))
    # retranslateUi

