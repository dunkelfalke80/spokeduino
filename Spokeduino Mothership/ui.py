# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'spokeduino_mothershipKYDGgl.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLayout,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

from customtablewidget import CustomTableWidget

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(1100, 793)
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
        self.spokeTab = QWidget()
        self.spokeTab.setObjectName(u"spokeTab")
        self.horizontalLayoutDatabaseTop = QHBoxLayout(self.spokeTab)
        self.horizontalLayoutDatabaseTop.setObjectName(u"horizontalLayoutDatabaseTop")
        self.horizontalLayoutDatabase = QHBoxLayout()
        self.horizontalLayoutDatabase.setObjectName(u"horizontalLayoutDatabase")
        self.verticalLayoutDatabaseLeft = QVBoxLayout()
        self.verticalLayoutDatabaseLeft.setObjectName(u"verticalLayoutDatabaseLeft")
        self.groupBoxListSpoke = QGroupBox(self.spokeTab)
        self.groupBoxListSpoke.setObjectName(u"groupBoxListSpoke")
        self.verticalLayoutFilterDatabase = QVBoxLayout(self.groupBoxListSpoke)
        self.verticalLayoutFilterDatabase.setObjectName(u"verticalLayoutFilterDatabase")
        self.horizontalLayoutFilterDatabase = QHBoxLayout()
        self.horizontalLayoutFilterDatabase.setObjectName(u"horizontalLayoutFilterDatabase")
        self.lineEditFilterSpokeName = QLineEdit(self.groupBoxListSpoke)
        self.lineEditFilterSpokeName.setObjectName(u"lineEditFilterSpokeName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEditFilterSpokeName.sizePolicy().hasHeightForWidth())
        self.lineEditFilterSpokeName.setSizePolicy(sizePolicy1)

        self.horizontalLayoutFilterDatabase.addWidget(self.lineEditFilterSpokeName)

        self.comboBoxFilterSpokeType = QComboBox(self.groupBoxListSpoke)
        self.comboBoxFilterSpokeType.setObjectName(u"comboBoxFilterSpokeType")
        sizePolicy1.setHeightForWidth(self.comboBoxFilterSpokeType.sizePolicy().hasHeightForWidth())
        self.comboBoxFilterSpokeType.setSizePolicy(sizePolicy1)

        self.horizontalLayoutFilterDatabase.addWidget(self.comboBoxFilterSpokeType)

        self.horizontalSpacerFilter = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutFilterDatabase.addItem(self.horizontalSpacerFilter)

        self.lineEditFilterSpokeGauge = QLineEdit(self.groupBoxListSpoke)
        self.lineEditFilterSpokeGauge.setObjectName(u"lineEditFilterSpokeGauge")
        sizePolicy1.setHeightForWidth(self.lineEditFilterSpokeGauge.sizePolicy().hasHeightForWidth())
        self.lineEditFilterSpokeGauge.setSizePolicy(sizePolicy1)

        self.horizontalLayoutFilterDatabase.addWidget(self.lineEditFilterSpokeGauge)

        self.horizontalLayoutFilterDatabase.setStretch(3, 1)

        self.verticalLayoutFilterDatabase.addLayout(self.horizontalLayoutFilterDatabase)

        self.tableWidgetSpokeSelection = QTableWidget(self.groupBoxListSpoke)
        self.tableWidgetSpokeSelection.setObjectName(u"tableWidgetSpokeSelection")
        sizePolicy1.setHeightForWidth(self.tableWidgetSpokeSelection.sizePolicy().hasHeightForWidth())
        self.tableWidgetSpokeSelection.setSizePolicy(sizePolicy1)

        self.verticalLayoutFilterDatabase.addWidget(self.tableWidgetSpokeSelection)

        self.verticalLayoutFilterDatabase.setStretch(1, 1)

        self.verticalLayoutDatabaseLeft.addWidget(self.groupBoxListSpoke)

        self.groupBoxListSpokeMeasurements = QGroupBox(self.spokeTab)
        self.groupBoxListSpokeMeasurements.setObjectName(u"groupBoxListSpokeMeasurements")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBoxListSpokeMeasurements)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayoutSpokeDefinitionsDatabase_4 = QHBoxLayout()
        self.horizontalLayoutSpokeDefinitionsDatabase_4.setObjectName(u"horizontalLayoutSpokeDefinitionsDatabase_4")
        self.tableWidgetSpokeMeasurements = QTableWidget(self.groupBoxListSpokeMeasurements)
        self.tableWidgetSpokeMeasurements.setObjectName(u"tableWidgetSpokeMeasurements")
        sizePolicy1.setHeightForWidth(self.tableWidgetSpokeMeasurements.sizePolicy().hasHeightForWidth())
        self.tableWidgetSpokeMeasurements.setSizePolicy(sizePolicy1)

        self.horizontalLayoutSpokeDefinitionsDatabase_4.addWidget(self.tableWidgetSpokeMeasurements)


        self.verticalLayout_4.addLayout(self.horizontalLayoutSpokeDefinitionsDatabase_4)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayoutSpokeDefinitionsDatabase_6 = QHBoxLayout()
        self.horizontalLayoutSpokeDefinitionsDatabase_6.setObjectName(u"horizontalLayoutSpokeDefinitionsDatabase_6")
        self.pushButtonUseLeft = QPushButton(self.groupBoxListSpokeMeasurements)
        self.pushButtonUseLeft.setObjectName(u"pushButtonUseLeft")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButtonUseLeft.sizePolicy().hasHeightForWidth())
        self.pushButtonUseLeft.setSizePolicy(sizePolicy2)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        self.pushButtonUseLeft.setIcon(icon)

        self.horizontalLayoutSpokeDefinitionsDatabase_6.addWidget(self.pushButtonUseLeft)

        self.pushButtonUseRight = QPushButton(self.groupBoxListSpokeMeasurements)
        self.pushButtonUseRight.setObjectName(u"pushButtonUseRight")
        sizePolicy2.setHeightForWidth(self.pushButtonUseRight.sizePolicy().hasHeightForWidth())
        self.pushButtonUseRight.setSizePolicy(sizePolicy2)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoNext))
        self.pushButtonUseRight.setIcon(icon1)

        self.horizontalLayoutSpokeDefinitionsDatabase_6.addWidget(self.pushButtonUseRight)

        self.horizontalSpacerTypeDatabase_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutSpokeDefinitionsDatabase_6.addItem(self.horizontalSpacerTypeDatabase_6)

        self.pushButtonNewMeasurement = QPushButton(self.groupBoxListSpokeMeasurements)
        self.pushButtonNewMeasurement.setObjectName(u"pushButtonNewMeasurement")
        sizePolicy2.setHeightForWidth(self.pushButtonNewMeasurement.sizePolicy().hasHeightForWidth())
        self.pushButtonNewMeasurement.setSizePolicy(sizePolicy2)
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.pushButtonNewMeasurement.setIcon(icon2)

        self.horizontalLayoutSpokeDefinitionsDatabase_6.addWidget(self.pushButtonNewMeasurement)

        self.pushButtonEditMeasurement = QPushButton(self.groupBoxListSpokeMeasurements)
        self.pushButtonEditMeasurement.setObjectName(u"pushButtonEditMeasurement")
        sizePolicy2.setHeightForWidth(self.pushButtonEditMeasurement.sizePolicy().hasHeightForWidth())
        self.pushButtonEditMeasurement.setSizePolicy(sizePolicy2)
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties))
        self.pushButtonEditMeasurement.setIcon(icon3)

        self.horizontalLayoutSpokeDefinitionsDatabase_6.addWidget(self.pushButtonEditMeasurement)

        self.pushButtonDeleteMeasurement = QPushButton(self.groupBoxListSpokeMeasurements)
        self.pushButtonDeleteMeasurement.setObjectName(u"pushButtonDeleteMeasurement")
        sizePolicy2.setHeightForWidth(self.pushButtonDeleteMeasurement.sizePolicy().hasHeightForWidth())
        self.pushButtonDeleteMeasurement.setSizePolicy(sizePolicy2)
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        self.pushButtonDeleteMeasurement.setIcon(icon4)

        self.horizontalLayoutSpokeDefinitionsDatabase_6.addWidget(self.pushButtonDeleteMeasurement)


        self.verticalLayout_6.addLayout(self.horizontalLayoutSpokeDefinitionsDatabase_6)


        self.verticalLayout_4.addLayout(self.verticalLayout_6)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)


        self.verticalLayoutDatabaseLeft.addWidget(self.groupBoxListSpokeMeasurements)

        self.verticalLayoutDatabaseLeft.setStretch(0, 3)

        self.horizontalLayoutDatabase.addLayout(self.verticalLayoutDatabaseLeft)

        self.groupBoxCreateSpoke = QGroupBox(self.spokeTab)
        self.groupBoxCreateSpoke.setObjectName(u"groupBoxCreateSpoke")
        self.verticalLayoutSpokeDatabase = QVBoxLayout(self.groupBoxCreateSpoke)
        self.verticalLayoutSpokeDatabase.setObjectName(u"verticalLayoutSpokeDatabase")
        self.groupBoxSpokeManufacturer = QGroupBox(self.groupBoxCreateSpoke)
        self.groupBoxSpokeManufacturer.setObjectName(u"groupBoxSpokeManufacturer")
        self.verticalLayoutManufacturerDatabase = QVBoxLayout(self.groupBoxSpokeManufacturer)
        self.verticalLayoutManufacturerDatabase.setObjectName(u"verticalLayoutManufacturerDatabase")
        self.comboBoxSpokeManufacturer = QComboBox(self.groupBoxSpokeManufacturer)
        self.comboBoxSpokeManufacturer.setObjectName(u"comboBoxSpokeManufacturer")
        sizePolicy1.setHeightForWidth(self.comboBoxSpokeManufacturer.sizePolicy().hasHeightForWidth())
        self.comboBoxSpokeManufacturer.setSizePolicy(sizePolicy1)

        self.verticalLayoutManufacturerDatabase.addWidget(self.comboBoxSpokeManufacturer)

        self.horizontalLayoutDatabaseLeft = QHBoxLayout()
        self.horizontalLayoutDatabaseLeft.setObjectName(u"horizontalLayoutDatabaseLeft")
        self.horizontalLayoutDatabaseLeft.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.groupBoxNewSpokeManufacturer = QGroupBox(self.groupBoxSpokeManufacturer)
        self.groupBoxNewSpokeManufacturer.setObjectName(u"groupBoxNewSpokeManufacturer")
        sizePolicy1.setHeightForWidth(self.groupBoxNewSpokeManufacturer.sizePolicy().hasHeightForWidth())
        self.groupBoxNewSpokeManufacturer.setSizePolicy(sizePolicy1)
        self.verticalLayoutNewManufacturerDatabase = QVBoxLayout(self.groupBoxNewSpokeManufacturer)
        self.verticalLayoutNewManufacturerDatabase.setObjectName(u"verticalLayoutNewManufacturerDatabase")
        self.lineEditNewSpokeManufacturer = QLineEdit(self.groupBoxNewSpokeManufacturer)
        self.lineEditNewSpokeManufacturer.setObjectName(u"lineEditNewSpokeManufacturer")
        sizePolicy1.setHeightForWidth(self.lineEditNewSpokeManufacturer.sizePolicy().hasHeightForWidth())
        self.lineEditNewSpokeManufacturer.setSizePolicy(sizePolicy1)

        self.verticalLayoutNewManufacturerDatabase.addWidget(self.lineEditNewSpokeManufacturer)


        self.horizontalLayoutDatabaseLeft.addWidget(self.groupBoxNewSpokeManufacturer)

        self.pushButtonSaveAsSpokeManufacturer = QPushButton(self.groupBoxSpokeManufacturer)
        self.pushButtonSaveAsSpokeManufacturer.setObjectName(u"pushButtonSaveAsSpokeManufacturer")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButtonSaveAsSpokeManufacturer.sizePolicy().hasHeightForWidth())
        self.pushButtonSaveAsSpokeManufacturer.setSizePolicy(sizePolicy3)
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSaveAs))
        self.pushButtonSaveAsSpokeManufacturer.setIcon(icon5)

        self.horizontalLayoutDatabaseLeft.addWidget(self.pushButtonSaveAsSpokeManufacturer)

        self.horizontalLayoutDatabaseLeft.setStretch(0, 3)
        self.horizontalLayoutDatabaseLeft.setStretch(1, 1)

        self.verticalLayoutManufacturerDatabase.addLayout(self.horizontalLayoutDatabaseLeft)


        self.verticalLayoutSpokeDatabase.addWidget(self.groupBoxSpokeManufacturer)

        self.verticalSpacerDatabaseTop = QSpacerItem(20, 28, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutSpokeDatabase.addItem(self.verticalSpacerDatabaseTop)

        self.groupBoxSpoke = QGroupBox(self.groupBoxCreateSpoke)
        self.groupBoxSpoke.setObjectName(u"groupBoxSpoke")
        self.verticalLayoutSelectSpokeDatabase = QVBoxLayout(self.groupBoxSpoke)
        self.verticalLayoutSelectSpokeDatabase.setObjectName(u"verticalLayoutSelectSpokeDatabase")
        self.groupBoxName = QGroupBox(self.groupBoxSpoke)
        self.groupBoxName.setObjectName(u"groupBoxName")
        self.groupBoxName.setEnabled(True)
        self.verticalLayoutEditNewSpokeName = QVBoxLayout(self.groupBoxName)
        self.verticalLayoutEditNewSpokeName.setObjectName(u"verticalLayoutEditNewSpokeName")
        self.lineEditSpokeName = QLineEdit(self.groupBoxName)
        self.lineEditSpokeName.setObjectName(u"lineEditName")
        sizePolicy1.setHeightForWidth(self.lineEditSpokeName.sizePolicy().hasHeightForWidth())
        self.lineEditSpokeName.setSizePolicy(sizePolicy1)

        self.verticalLayoutEditNewSpokeName.addWidget(self.lineEditSpokeName)


        self.verticalLayoutSelectSpokeDatabase.addWidget(self.groupBoxName)

        self.horizontalLayoutSpokeDefinitionsDatabase = QHBoxLayout()
        self.horizontalLayoutSpokeDefinitionsDatabase.setObjectName(u"horizontalLayoutSpokeDefinitionsDatabase")
        self.groupBoxSpokeType = QGroupBox(self.groupBoxSpoke)
        self.groupBoxSpokeType.setObjectName(u"groupBoxSpokeType")
        sizePolicy1.setHeightForWidth(self.groupBoxSpokeType.sizePolicy().hasHeightForWidth())
        self.groupBoxSpokeType.setSizePolicy(sizePolicy1)
        self.groupBoxSpokeType.setMinimumSize(QSize(150, 0))
        self.verticalLayoutTypeDatabase = QVBoxLayout(self.groupBoxSpokeType)
        self.verticalLayoutTypeDatabase.setObjectName(u"verticalLayoutTypeDatabase")
        self.comboBoxSpokeType = QComboBox(self.groupBoxSpokeType)
        self.comboBoxSpokeType.setObjectName(u"comboBoxSpokeType")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.comboBoxSpokeType.sizePolicy().hasHeightForWidth())
        self.comboBoxSpokeType.setSizePolicy(sizePolicy4)

        self.verticalLayoutTypeDatabase.addWidget(self.comboBoxSpokeType)


        self.horizontalLayoutSpokeDefinitionsDatabase.addWidget(self.groupBoxSpokeType)

        self.horizontalSpacerTypeDatabase = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutSpokeDefinitionsDatabase.addItem(self.horizontalSpacerTypeDatabase)

        self.groupBoxSpokeGauge = QGroupBox(self.groupBoxSpoke)
        self.groupBoxSpokeGauge.setObjectName(u"groupBoxSpokeGauge")
        sizePolicy1.setHeightForWidth(self.groupBoxSpokeGauge.sizePolicy().hasHeightForWidth())
        self.groupBoxSpokeGauge.setSizePolicy(sizePolicy1)
        self.verticalLayoutGaugeDatabase = QVBoxLayout(self.groupBoxSpokeGauge)
        self.verticalLayoutGaugeDatabase.setObjectName(u"verticalLayoutGaugeDatabase")
        self.lineEditSpokeGauge = QLineEdit(self.groupBoxSpokeGauge)
        self.lineEditSpokeGauge.setObjectName(u"lineEditSpokeGauge")
        sizePolicy1.setHeightForWidth(self.lineEditSpokeGauge.sizePolicy().hasHeightForWidth())
        self.lineEditSpokeGauge.setSizePolicy(sizePolicy1)

        self.verticalLayoutGaugeDatabase.addWidget(self.lineEditSpokeGauge)


        self.horizontalLayoutSpokeDefinitionsDatabase.addWidget(self.groupBoxSpokeGauge)

        self.groupBoxSpokeWeight = QGroupBox(self.groupBoxSpoke)
        self.groupBoxSpokeWeight.setObjectName(u"groupBoxSpokeWeight")
        sizePolicy1.setHeightForWidth(self.groupBoxSpokeWeight.sizePolicy().hasHeightForWidth())
        self.groupBoxSpokeWeight.setSizePolicy(sizePolicy1)
        self.verticalLayoutWeightDatabase = QVBoxLayout(self.groupBoxSpokeWeight)
        self.verticalLayoutWeightDatabase.setObjectName(u"verticalLayoutWeightDatabase")
        self.lineEditSpokeWeight = QLineEdit(self.groupBoxSpokeWeight)
        self.lineEditSpokeWeight.setObjectName(u"lineEditSpokeWeight")
        sizePolicy1.setHeightForWidth(self.lineEditSpokeWeight.sizePolicy().hasHeightForWidth())
        self.lineEditSpokeWeight.setSizePolicy(sizePolicy1)

        self.verticalLayoutWeightDatabase.addWidget(self.lineEditSpokeWeight)


        self.horizontalLayoutSpokeDefinitionsDatabase.addWidget(self.groupBoxSpokeWeight)


        self.verticalLayoutSelectSpokeDatabase.addLayout(self.horizontalLayoutSpokeDefinitionsDatabase)

        self.groupBoxSpokeDimension = QGroupBox(self.groupBoxSpoke)
        self.groupBoxSpokeDimension.setObjectName(u"groupBoxSpokeDimension")
        self.verticalLayoutDimension = QVBoxLayout(self.groupBoxSpokeDimension)
        self.verticalLayoutDimension.setObjectName(u"verticalLayoutDimension")
        self.lineEditSpokeDimension = QLineEdit(self.groupBoxSpokeDimension)
        self.lineEditSpokeDimension.setObjectName(u"lineEditSpokeDimension")
        sizePolicy1.setHeightForWidth(self.lineEditSpokeDimension.sizePolicy().hasHeightForWidth())
        self.lineEditSpokeDimension.setSizePolicy(sizePolicy1)

        self.verticalLayoutDimension.addWidget(self.lineEditSpokeDimension)


        self.verticalLayoutSelectSpokeDatabase.addWidget(self.groupBoxSpokeDimension)

        self.groupBoxSpokeComment = QGroupBox(self.groupBoxSpoke)
        self.groupBoxSpokeComment.setObjectName(u"groupBoxSpokeComment")
        self.verticalLayoutCommentDatabase = QVBoxLayout(self.groupBoxSpokeComment)
        self.verticalLayoutCommentDatabase.setObjectName(u"verticalLayoutCommentDatabase")
        self.lineEditSpokeComment = QLineEdit(self.groupBoxSpokeComment)
        self.lineEditSpokeComment.setObjectName(u"lineEditSpokeComment")
        sizePolicy1.setHeightForWidth(self.lineEditSpokeComment.sizePolicy().hasHeightForWidth())
        self.lineEditSpokeComment.setSizePolicy(sizePolicy1)

        self.verticalLayoutCommentDatabase.addWidget(self.lineEditSpokeComment)


        self.verticalLayoutSelectSpokeDatabase.addWidget(self.groupBoxSpokeComment)


        self.verticalLayoutSpokeDatabase.addWidget(self.groupBoxSpoke)

        self.verticalSpacerDatabaseBottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutSpokeDatabase.addItem(self.verticalSpacerDatabaseBottom)

        self.horizontalLayoutSpokeButtonsDatabase = QHBoxLayout()
        self.horizontalLayoutSpokeButtonsDatabase.setObjectName(u"horizontalLayoutSpokeButtonsDatabase")
        self.pushButtonSpokeUpdate = QPushButton(self.groupBoxCreateSpoke)
        self.pushButtonSpokeUpdate.setObjectName(u"pushButtonSpokeUpdate")
        sizePolicy2.setHeightForWidth(self.pushButtonSpokeUpdate.sizePolicy().hasHeightForWidth())
        self.pushButtonSpokeUpdate.setSizePolicy(sizePolicy2)
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.pushButtonSpokeUpdate.setIcon(icon6)

        self.horizontalLayoutSpokeButtonsDatabase.addWidget(self.pushButtonSpokeUpdate)

        self.pushButtonSpokeSaveAs = QPushButton(self.groupBoxCreateSpoke)
        self.pushButtonSpokeSaveAs.setObjectName(u"pushButtonSpokeSaveAs")
        sizePolicy2.setHeightForWidth(self.pushButtonSpokeSaveAs.sizePolicy().hasHeightForWidth())
        self.pushButtonSpokeSaveAs.setSizePolicy(sizePolicy2)
        self.pushButtonSpokeSaveAs.setIcon(icon5)

        self.horizontalLayoutSpokeButtonsDatabase.addWidget(self.pushButtonSpokeSaveAs)

        self.pushButtonSpokeClear = QPushButton(self.groupBoxCreateSpoke)
        self.pushButtonSpokeClear.setObjectName(u"pushButtonSpokeClear")
        sizePolicy2.setHeightForWidth(self.pushButtonSpokeClear.sizePolicy().hasHeightForWidth())
        self.pushButtonSpokeClear.setSizePolicy(sizePolicy2)
        icon7 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
        self.pushButtonSpokeClear.setIcon(icon7)

        self.horizontalLayoutSpokeButtonsDatabase.addWidget(self.pushButtonSpokeClear)

        self.pushButtonSpokeDelete = QPushButton(self.groupBoxCreateSpoke)
        self.pushButtonSpokeDelete.setObjectName(u"pushButtonSpokeDelete")
        sizePolicy2.setHeightForWidth(self.pushButtonSpokeDelete.sizePolicy().hasHeightForWidth())
        self.pushButtonSpokeDelete.setSizePolicy(sizePolicy2)
        icon8 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.pushButtonSpokeDelete.setIcon(icon8)

        self.horizontalLayoutSpokeButtonsDatabase.addWidget(self.pushButtonSpokeDelete)


        self.verticalLayoutSpokeDatabase.addLayout(self.horizontalLayoutSpokeButtonsDatabase)


        self.horizontalLayoutDatabase.addWidget(self.groupBoxCreateSpoke)

        self.horizontalLayoutDatabase.setStretch(0, 2)
        self.horizontalLayoutDatabase.setStretch(1, 1)

        self.horizontalLayoutDatabaseTop.addLayout(self.horizontalLayoutDatabase)

        self.tabWidget.addTab(self.spokeTab, "")
        self.measurementTab = QWidget()
        self.measurementTab.setObjectName(u"measurementTab")
        self.horizontalLayoutMeasurementTop = QHBoxLayout(self.measurementTab)
        self.horizontalLayoutMeasurementTop.setObjectName(u"horizontalLayoutMeasurementTop")
        self.horizontalLayoutMeasurement = QHBoxLayout()
        self.horizontalLayoutMeasurement.setObjectName(u"horizontalLayoutMeasurement")
        self.horizontalLayoutMeasurementsLeft = QHBoxLayout()
        self.horizontalLayoutMeasurementsLeft.setObjectName(u"horizontalLayoutMeasurementsLeft")
        self.groupBoxMeasurementLeft = QGroupBox(self.measurementTab)
        self.groupBoxMeasurementLeft.setObjectName(u"groupBoxMeasurementLeft")
        self.verticalLayoutManufacturer = QVBoxLayout(self.groupBoxMeasurementLeft)
        self.verticalLayoutManufacturer.setObjectName(u"verticalLayoutManufacturer")
        self.horizontalLayoutManufacturerLeft = QHBoxLayout()
        self.horizontalLayoutManufacturerLeft.setObjectName(u"horizontalLayoutManufacturerLeft")
        self.tableWidgetMeasurements = CustomTableWidget(self.groupBoxMeasurementLeft)
        self.tableWidgetMeasurements.setObjectName(u"tableWidgetMeasurements")

        self.horizontalLayoutManufacturerLeft.addWidget(self.tableWidgetMeasurements)

        self.horizontalLayoutManufacturerLeft.setStretch(0, 5)

        self.verticalLayoutManufacturer.addLayout(self.horizontalLayoutManufacturerLeft)

        self.groupBoxMeasurementComment = QGroupBox(self.groupBoxMeasurementLeft)
        self.groupBoxMeasurementComment.setObjectName(u"groupBoxMeasurementComment")
        self.verticalLayoutCommentMeasurement = QVBoxLayout(self.groupBoxMeasurementComment)
        self.verticalLayoutCommentMeasurement.setObjectName(u"verticalLayoutCommentMeasurement")
        self.lineEditMeasurementComment = QLineEdit(self.groupBoxMeasurementComment)
        self.lineEditMeasurementComment.setObjectName(u"lineEditMeasurementComment")

        self.verticalLayoutCommentMeasurement.addWidget(self.lineEditMeasurementComment)


        self.verticalLayoutManufacturer.addWidget(self.groupBoxMeasurementComment)

        self.horizontalLayoutMeasurementsButtons = QHBoxLayout()
        self.horizontalLayoutMeasurementsButtons.setObjectName(u"horizontalLayoutMeasurementsButtons")
        self.pushButtonPreviousMeasurement = QPushButton(self.groupBoxMeasurementLeft)
        self.pushButtonPreviousMeasurement.setObjectName(u"pushButtonPreviousMeasurement")
        self.pushButtonPreviousMeasurement.setIcon(icon)

        self.horizontalLayoutMeasurementsButtons.addWidget(self.pushButtonPreviousMeasurement)

        self.pushButtonNextMeasurement = QPushButton(self.groupBoxMeasurementLeft)
        self.pushButtonNextMeasurement.setObjectName(u"pushButtonNextMeasurement")
        self.pushButtonNextMeasurement.setIcon(icon1)

        self.horizontalLayoutMeasurementsButtons.addWidget(self.pushButtonNextMeasurement)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutMeasurementsButtons.addItem(self.horizontalSpacer_6)

        self.pushButtonSaveMeasurement = QPushButton(self.groupBoxMeasurementLeft)
        self.pushButtonSaveMeasurement.setObjectName(u"pushButtonSaveMeasurement")
        self.pushButtonSaveMeasurement.setIcon(icon6)

        self.horizontalLayoutMeasurementsButtons.addWidget(self.pushButtonSaveMeasurement)


        self.verticalLayoutManufacturer.addLayout(self.horizontalLayoutMeasurementsButtons)


        self.horizontalLayoutMeasurementsLeft.addWidget(self.groupBoxMeasurementLeft)


        self.horizontalLayoutMeasurement.addLayout(self.horizontalLayoutMeasurementsLeft)

        self.horizontalLayoutMeasurementRight = QHBoxLayout()
        self.horizontalLayoutMeasurementRight.setObjectName(u"horizontalLayoutMeasurementRight")
        self.groupBoxMeasurementRight = QGroupBox(self.measurementTab)
        self.groupBoxMeasurementRight.setObjectName(u"groupBoxMeasurementRight")
        self.verticalLayoutMeasurementRight = QVBoxLayout(self.groupBoxMeasurementRight)
        self.verticalLayoutMeasurementRight.setObjectName(u"verticalLayoutMeasurementRight")

        self.horizontalLayoutMeasurementRight.addWidget(self.groupBoxMeasurementRight)


        self.horizontalLayoutMeasurement.addLayout(self.horizontalLayoutMeasurementRight)

        self.horizontalLayoutMeasurement.setStretch(0, 1)
        self.horizontalLayoutMeasurement.setStretch(1, 2)

        self.horizontalLayoutMeasurementTop.addLayout(self.horizontalLayoutMeasurement)

        self.tabWidget.addTab(self.measurementTab, "")
        self.tensioningTab = QWidget()
        self.tensioningTab.setObjectName(u"tensioningTab")
        self.horizontalLayoutTensioningTabTop = QHBoxLayout(self.tensioningTab)
        self.horizontalLayoutTensioningTabTop.setObjectName(u"horizontalLayoutTensioningTabTop")
        self.horizontalLayoutTensioningTab = QHBoxLayout()
        self.horizontalLayoutTensioningTab.setObjectName(u"horizontalLayoutTensioningTab")
        self.groupBoxSideLeft = QGroupBox(self.tensioningTab)
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
        self.tableWidgetTensioningLeft = CustomTableWidget(self.groupBoxTensionValuesLeft)
        self.tableWidgetTensioningLeft.setObjectName(u"tableWidgetTensioningLeft")

        self.verticalLayoutSelectedTensionValuesLeft.addWidget(self.tableWidgetTensioningLeft)


        self.verticalLayoutSideLeft.addWidget(self.groupBoxTensionValuesLeft)

        self.verticalLayoutSideLeft.setStretch(1, 2)
        self.verticalLayoutSideLeft.setStretch(2, 10)

        self.horizontalLayoutTensioningTab.addWidget(self.groupBoxSideLeft)

        self.groupBoxSideRight = QGroupBox(self.tensioningTab)
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
        self.tableWidgetTensioningRight = CustomTableWidget(self.groupBoxTensionValuesRight)
        self.tableWidgetTensioningRight.setObjectName(u"tableWidgetTensioningRight")

        self.verticalLayoutSelectedTensionValuesRight.addWidget(self.tableWidgetTensioningRight)


        self.verticalLayoutSideRight.addWidget(self.groupBoxTensionValuesRight)

        self.verticalLayoutSideRight.setStretch(1, 2)
        self.verticalLayoutSideRight.setStretch(2, 10)

        self.horizontalLayoutTensioningTab.addWidget(self.groupBoxSideRight)

        self.groupBoxWheel = QGroupBox(self.tensioningTab)
        self.groupBoxWheel.setObjectName(u"groupBoxWheel")
        sizePolicy1.setHeightForWidth(self.groupBoxWheel.sizePolicy().hasHeightForWidth())
        self.groupBoxWheel.setSizePolicy(sizePolicy1)
        self.verticalLayoutMeasurement = QVBoxLayout(self.groupBoxWheel)
        self.verticalLayoutMeasurement.setObjectName(u"verticalLayoutMeasurement")
        self.verticalLayoutWheelDiagram = QVBoxLayout()
        self.verticalLayoutWheelDiagram.setSpacing(6)
        self.verticalLayoutWheelDiagram.setObjectName(u"verticalLayoutWheelDiagram")

        self.verticalLayoutMeasurement.addLayout(self.verticalLayoutWheelDiagram)

        self.gridLayoutTensionButtons = QGridLayout()
        self.gridLayoutTensionButtons.setObjectName(u"gridLayoutTensionButtons")
        self.gridLayoutTensionButtons.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.pushButtonStartTensioning = QPushButton(self.groupBoxWheel)
        self.pushButtonStartTensioning.setObjectName(u"pushButtonStartTensioning")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.pushButtonStartTensioning.sizePolicy().hasHeightForWidth())
        self.pushButtonStartTensioning.setSizePolicy(sizePolicy5)
        icon9 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp))
        self.pushButtonStartTensioning.setIcon(icon9)

        self.gridLayoutTensionButtons.addWidget(self.pushButtonStartTensioning, 0, 0, 1, 1)

        self.horizontalSpacerSpokeEditsLeft = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutTensionButtons.addItem(self.horizontalSpacerSpokeEditsLeft, 0, 4, 1, 1)

        self.pushButtonSwitchView = QPushButton(self.groupBoxWheel)
        self.pushButtonSwitchView.setObjectName(u"pushButtonSwitchView")
        sizePolicy5.setHeightForWidth(self.pushButtonSwitchView.sizePolicy().hasHeightForWidth())
        self.pushButtonSwitchView.setSizePolicy(sizePolicy5)
        icon10 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaylistRepeat))
        self.pushButtonSwitchView.setIcon(icon10)

        self.gridLayoutTensionButtons.addWidget(self.pushButtonSwitchView, 0, 5, 1, 1)

        self.pushButtonPreviousSpoke = QPushButton(self.groupBoxWheel)
        self.pushButtonPreviousSpoke.setObjectName(u"pushButtonPreviousSpoke")
        sizePolicy5.setHeightForWidth(self.pushButtonPreviousSpoke.sizePolicy().hasHeightForWidth())
        self.pushButtonPreviousSpoke.setSizePolicy(sizePolicy5)
        self.pushButtonPreviousSpoke.setIcon(icon)

        self.gridLayoutTensionButtons.addWidget(self.pushButtonPreviousSpoke, 0, 2, 1, 1)

        self.pushButtonNextSpoke = QPushButton(self.groupBoxWheel)
        self.pushButtonNextSpoke.setObjectName(u"pushButtonNextSpoke")
        sizePolicy5.setHeightForWidth(self.pushButtonNextSpoke.sizePolicy().hasHeightForWidth())
        self.pushButtonNextSpoke.setSizePolicy(sizePolicy5)
        self.pushButtonNextSpoke.setIcon(icon1)

        self.gridLayoutTensionButtons.addWidget(self.pushButtonNextSpoke, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutTensionButtons.addItem(self.horizontalSpacer, 0, 1, 1, 1)


        self.verticalLayoutMeasurement.addLayout(self.gridLayoutTensionButtons)

        self.verticalLayoutMeasurement.setStretch(0, 10)

        self.horizontalLayoutTensioningTab.addWidget(self.groupBoxWheel)

        self.horizontalLayoutTensioningTab.setStretch(0, 1)
        self.horizontalLayoutTensioningTab.setStretch(1, 1)
        self.horizontalLayoutTensioningTab.setStretch(2, 10)

        self.horizontalLayoutTensioningTabTop.addLayout(self.horizontalLayoutTensioningTab)

        self.tabWidget.addTab(self.tensioningTab, "")
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
        self.horizontalLayout_2 = QHBoxLayout(self.groupBoxSpokeduino)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBoxSpokeduinoPort = QComboBox(self.groupBoxSpokeduino)
        self.comboBoxSpokeduinoPort.setObjectName(u"comboBoxSpokeduinoPort")
        sizePolicy3.setHeightForWidth(self.comboBoxSpokeduinoPort.sizePolicy().hasHeightForWidth())
        self.comboBoxSpokeduinoPort.setSizePolicy(sizePolicy3)

        self.horizontalLayout_2.addWidget(self.comboBoxSpokeduinoPort)

        self.checkBoxSpokeduinoEnabled = QCheckBox(self.groupBoxSpokeduino)
        self.checkBoxSpokeduinoEnabled.setObjectName(u"checkBoxSpokeduinoEnabled")
        self.checkBoxSpokeduinoEnabled.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.checkBoxSpokeduinoEnabled.sizePolicy().hasHeightForWidth())
        self.checkBoxSpokeduinoEnabled.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.checkBoxSpokeduinoEnabled)


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
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.comboBoxTensiometer = QComboBox(self.groupBoxTensiometer)
        self.comboBoxTensiometer.setObjectName(u"comboBoxTensiometer")
        sizePolicy3.setHeightForWidth(self.comboBoxTensiometer.sizePolicy().hasHeightForWidth())
        self.comboBoxTensiometer.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.comboBoxTensiometer)

        self.pushButtonMultipleTensiometers = QPushButton(self.groupBoxTensiometer)
        self.pushButtonMultipleTensiometers.setObjectName(u"pushButtonMultipleTensiometers")
        sizePolicy2.setHeightForWidth(self.pushButtonMultipleTensiometers.sizePolicy().hasHeightForWidth())
        self.pushButtonMultipleTensiometers.setSizePolicy(sizePolicy2)
        icon11 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditSelectAll))
        self.pushButtonMultipleTensiometers.setIcon(icon11)

        self.horizontalLayout_3.addWidget(self.pushButtonMultipleTensiometers)


        self.verticalLayoutTensiometer.addLayout(self.horizontalLayout_3)

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
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.lineEditNewTensiometer.sizePolicy().hasHeightForWidth())
        self.lineEditNewTensiometer.setSizePolicy(sizePolicy6)

        self.verticalLayoutNewTensiometer.addWidget(self.lineEditNewTensiometer)


        self.horizontalLayoutNewTensiometer.addWidget(self.groupBoxtNewTensiometer)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutNewTensiometer.addItem(self.horizontalSpacer_5)

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
        self.verticalLayoutSetupLeft.setStretch(4, 1)

        self.horizontalLayoutSetupLeft.addLayout(self.verticalLayoutSetupLeft)

        self.groupBoxMeasurementSetup = QGroupBox(self.setupTab)
        self.groupBoxMeasurementSetup.setObjectName(u"groupBoxMeasurementSetup")
        sizePolicy1.setHeightForWidth(self.groupBoxMeasurementSetup.sizePolicy().hasHeightForWidth())
        self.groupBoxMeasurementSetup.setSizePolicy(sizePolicy1)
        self.verticalLayoutMeasurementSetup = QVBoxLayout(self.groupBoxMeasurementSetup)
        self.verticalLayoutMeasurementSetup.setObjectName(u"verticalLayoutMeasurementSetup")
        self.groupBoxSpokeMeasurementType = QGroupBox(self.groupBoxMeasurementSetup)
        self.groupBoxSpokeMeasurementType.setObjectName(u"groupBoxSpokeMeasurementType")
        self.verticalLayoutMeasurementType = QVBoxLayout(self.groupBoxSpokeMeasurementType)
        self.verticalLayoutMeasurementType.setObjectName(u"verticalLayoutMeasurementType")
        self.radioButtonMeasurementDefault = QRadioButton(self.groupBoxSpokeMeasurementType)
        self.radioButtonMeasurementDefault.setObjectName(u"radioButtonMeasurementDefault")
        self.radioButtonMeasurementDefault.setChecked(True)

        self.verticalLayoutMeasurementType.addWidget(self.radioButtonMeasurementDefault)

        self.radioButtonMeasurementCustom = QRadioButton(self.groupBoxSpokeMeasurementType)
        self.radioButtonMeasurementCustom.setObjectName(u"radioButtonMeasurementCustom")

        self.verticalLayoutMeasurementType.addWidget(self.radioButtonMeasurementCustom)


        self.verticalLayoutMeasurementSetup.addWidget(self.groupBoxSpokeMeasurementType)

        self.groupBoxMeasurementDirection = QGroupBox(self.groupBoxMeasurementSetup)
        self.groupBoxMeasurementDirection.setObjectName(u"groupBoxMeasurementDirection")
        self.verticalLayoutMeasurementDirectionDown = QVBoxLayout(self.groupBoxMeasurementDirection)
        self.verticalLayoutMeasurementDirectionDown.setObjectName(u"verticalLayoutMeasurementDirectionDown")
        self.radioButtonMeasurementDown = QRadioButton(self.groupBoxMeasurementDirection)
        self.radioButtonMeasurementDown.setObjectName(u"radioButtonMeasurementDown")
        self.radioButtonMeasurementDown.setChecked(True)

        self.verticalLayoutMeasurementDirectionDown.addWidget(self.radioButtonMeasurementDown)

        self.radioButtonMeasurementUp = QRadioButton(self.groupBoxMeasurementDirection)
        self.radioButtonMeasurementUp.setObjectName(u"radioButtonMeasurementUp")

        self.verticalLayoutMeasurementDirectionDown.addWidget(self.radioButtonMeasurementUp)


        self.verticalLayoutMeasurementSetup.addWidget(self.groupBoxMeasurementDirection)

        self.groupBoxFitType = QGroupBox(self.groupBoxMeasurementSetup)
        self.groupBoxFitType.setObjectName(u"groupBoxFitType")
        self.verticalLayoutMeasurementDirectionDown_2 = QVBoxLayout(self.groupBoxFitType)
        self.verticalLayoutMeasurementDirectionDown_2.setObjectName(u"verticalLayoutMeasurementDirectionDown_2")
        self.radioButtonFitLinear = QRadioButton(self.groupBoxFitType)
        self.radioButtonFitLinear.setObjectName(u"radioButtonFitLinear")
        self.radioButtonFitLinear.setChecked(True)

        self.verticalLayoutMeasurementDirectionDown_2.addWidget(self.radioButtonFitLinear)

        self.radioButtonFitQuadratic = QRadioButton(self.groupBoxFitType)
        self.radioButtonFitQuadratic.setObjectName(u"radioButtonFitQuadratic")
        self.radioButtonFitQuadratic.setChecked(False)

        self.verticalLayoutMeasurementDirectionDown_2.addWidget(self.radioButtonFitQuadratic)

        self.radioButtonFitCubic = QRadioButton(self.groupBoxFitType)
        self.radioButtonFitCubic.setObjectName(u"radioButtonFitCubic")
        self.radioButtonFitCubic.setChecked(False)

        self.verticalLayoutMeasurementDirectionDown_2.addWidget(self.radioButtonFitCubic)

        self.radioButtonFitQuartic = QRadioButton(self.groupBoxFitType)
        self.radioButtonFitQuartic.setObjectName(u"radioButtonFitQuartic")
        self.radioButtonFitQuartic.setChecked(False)

        self.verticalLayoutMeasurementDirectionDown_2.addWidget(self.radioButtonFitQuartic)

        self.radioButtonFitSpline = QRadioButton(self.groupBoxFitType)
        self.radioButtonFitSpline.setObjectName(u"radioButtonFitSpline")
        self.radioButtonFitSpline.setChecked(False)

        self.verticalLayoutMeasurementDirectionDown_2.addWidget(self.radioButtonFitSpline)

        self.radioButtonFitExponential = QRadioButton(self.groupBoxFitType)
        self.radioButtonFitExponential.setObjectName(u"radioButtonFitExponential")
        self.radioButtonFitExponential.setChecked(False)

        self.verticalLayoutMeasurementDirectionDown_2.addWidget(self.radioButtonFitExponential)

        self.radioButtonFitLogarithmic = QRadioButton(self.groupBoxFitType)
        self.radioButtonFitLogarithmic.setObjectName(u"radioButtonFitLogarithmic")
        self.radioButtonFitLogarithmic.setChecked(False)

        self.verticalLayoutMeasurementDirectionDown_2.addWidget(self.radioButtonFitLogarithmic)

        self.radioButtonFitPowerLaw = QRadioButton(self.groupBoxFitType)
        self.radioButtonFitPowerLaw.setObjectName(u"radioButtonFitPowerLaw")
        self.radioButtonFitPowerLaw.setChecked(False)

        self.verticalLayoutMeasurementDirectionDown_2.addWidget(self.radioButtonFitPowerLaw)


        self.verticalLayoutMeasurementSetup.addWidget(self.groupBoxFitType)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutMeasurementSetup.addItem(self.verticalSpacer)


        self.horizontalLayoutSetupLeft.addWidget(self.groupBoxMeasurementSetup)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutSetupLeft.addItem(self.horizontalSpacer_2)

        self.verticalLayoutDirectionsConverter = QVBoxLayout()
        self.verticalLayoutDirectionsConverter.setObjectName(u"verticalLayoutDirectionsConverter")
        self.groupBoxDirectionsSetup = QGroupBox(self.setupTab)
        self.groupBoxDirectionsSetup.setObjectName(u"groupBoxDirectionsSetup")
        sizePolicy1.setHeightForWidth(self.groupBoxDirectionsSetup.sizePolicy().hasHeightForWidth())
        self.groupBoxDirectionsSetup.setSizePolicy(sizePolicy1)
        self.verticalLayoutMeasurementDirection = QVBoxLayout(self.groupBoxDirectionsSetup)
        self.verticalLayoutMeasurementDirection.setObjectName(u"verticalLayoutMeasurementDirection")
        self.groupBoxWheelRotationDirection = QGroupBox(self.groupBoxDirectionsSetup)
        self.groupBoxWheelRotationDirection.setObjectName(u"groupBoxWheelRotationDirection")
        self.verticalLayoutRotationDirectionClockwise = QVBoxLayout(self.groupBoxWheelRotationDirection)
        self.verticalLayoutRotationDirectionClockwise.setObjectName(u"verticalLayoutRotationDirectionClockwise")
        self.radioButtonRotationClockwise = QRadioButton(self.groupBoxWheelRotationDirection)
        self.radioButtonRotationClockwise.setObjectName(u"radioButtonRotationClockwise")
        self.radioButtonRotationClockwise.setChecked(True)

        self.verticalLayoutRotationDirectionClockwise.addWidget(self.radioButtonRotationClockwise)

        self.radioButtonRotationCounterclockwise = QRadioButton(self.groupBoxWheelRotationDirection)
        self.radioButtonRotationCounterclockwise.setObjectName(u"radioButtonRotationCounterclockwise")

        self.verticalLayoutRotationDirectionClockwise.addWidget(self.radioButtonRotationCounterclockwise)


        self.verticalLayoutMeasurementDirection.addWidget(self.groupBoxWheelRotationDirection)

        self.groupBoxWheelMeasurementType = QGroupBox(self.groupBoxDirectionsSetup)
        self.groupBoxWheelMeasurementType.setObjectName(u"groupBoxWheelMeasurementType")
        self.verticalLayoutMeasurementTypeLeftRight = QVBoxLayout(self.groupBoxWheelMeasurementType)
        self.verticalLayoutMeasurementTypeLeftRight.setObjectName(u"verticalLayoutMeasurementTypeLeftRight")
        self.radioButtonLeftRight = QRadioButton(self.groupBoxWheelMeasurementType)
        self.radioButtonLeftRight.setObjectName(u"radioButtonLeftRight")
        self.radioButtonLeftRight.setChecked(False)

        self.verticalLayoutMeasurementTypeLeftRight.addWidget(self.radioButtonLeftRight)

        self.radioButtonSideBySide = QRadioButton(self.groupBoxWheelMeasurementType)
        self.radioButtonSideBySide.setObjectName(u"radioButtonSideBySide")
        self.radioButtonSideBySide.setChecked(True)

        self.verticalLayoutMeasurementTypeLeftRight.addWidget(self.radioButtonSideBySide)

        self.radioButtonRightLeft = QRadioButton(self.groupBoxWheelMeasurementType)
        self.radioButtonRightLeft.setObjectName(u"radioButtonRightLeft")
        self.radioButtonRightLeft.setEnabled(True)
        self.radioButtonRightLeft.setChecked(False)

        self.verticalLayoutMeasurementTypeLeftRight.addWidget(self.radioButtonRightLeft)


        self.verticalLayoutMeasurementDirection.addWidget(self.groupBoxWheelMeasurementType)


        self.verticalLayoutDirectionsConverter.addWidget(self.groupBoxDirectionsSetup)

        self.verticalSpacerUnit = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutDirectionsConverter.addItem(self.verticalSpacerUnit)


        self.horizontalLayoutSetupLeft.addLayout(self.verticalLayoutDirectionsConverter)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutSetupLeft.addItem(self.horizontalSpacer_3)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutSetupLeft.addItem(self.horizontalSpacer_4)

        self.groupBoxUnits = QGroupBox(self.setupTab)
        self.groupBoxUnits.setObjectName(u"groupBoxUnits")
        self.verticalLayoutUnits = QVBoxLayout(self.groupBoxUnits)
        self.verticalLayoutUnits.setObjectName(u"verticalLayoutUnits")
        self.groupBoxUnitSetup = QGroupBox(self.groupBoxUnits)
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


        self.verticalLayoutUnits.addWidget(self.groupBoxUnitSetup)

        self.groupBoxUnitConverter = QGroupBox(self.groupBoxUnits)
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
        self.lineEditConverterNewton = QLineEdit(self.groupBoxTensionConverterNewton)
        self.lineEditConverterNewton.setObjectName(u"lineEditConverterNewton")
        sizePolicy1.setHeightForWidth(self.lineEditConverterNewton.sizePolicy().hasHeightForWidth())
        self.lineEditConverterNewton.setSizePolicy(sizePolicy1)

        self.verticalLayoutConverterNewton.addWidget(self.lineEditConverterNewton)


        self.verticalLayoutUnitCoverter.addWidget(self.groupBoxTensionConverterNewton)

        self.groupBoxTensionConverterKgF = QGroupBox(self.groupBoxUnitConverter)
        self.groupBoxTensionConverterKgF.setObjectName(u"groupBoxTensionConverterKgF")
        sizePolicy1.setHeightForWidth(self.groupBoxTensionConverterKgF.sizePolicy().hasHeightForWidth())
        self.groupBoxTensionConverterKgF.setSizePolicy(sizePolicy1)
        self.groupBoxTensionConverterKgF.setMinimumSize(QSize(0, 0))
        self.verticalLayoutConverterKgF = QVBoxLayout(self.groupBoxTensionConverterKgF)
        self.verticalLayoutConverterKgF.setObjectName(u"verticalLayoutConverterKgF")
        self.lineEditConverterKgF = QLineEdit(self.groupBoxTensionConverterKgF)
        self.lineEditConverterKgF.setObjectName(u"lineEditConverterKgF")
        sizePolicy1.setHeightForWidth(self.lineEditConverterKgF.sizePolicy().hasHeightForWidth())
        self.lineEditConverterKgF.setSizePolicy(sizePolicy1)

        self.verticalLayoutConverterKgF.addWidget(self.lineEditConverterKgF)


        self.verticalLayoutUnitCoverter.addWidget(self.groupBoxTensionConverterKgF)

        self.groupBoxTensionConverterLbF = QGroupBox(self.groupBoxUnitConverter)
        self.groupBoxTensionConverterLbF.setObjectName(u"groupBoxTensionConverterLbF")
        sizePolicy1.setHeightForWidth(self.groupBoxTensionConverterLbF.sizePolicy().hasHeightForWidth())
        self.groupBoxTensionConverterLbF.setSizePolicy(sizePolicy1)
        self.groupBoxTensionConverterLbF.setMinimumSize(QSize(0, 0))
        self.verticalLayoutLbFConverter = QVBoxLayout(self.groupBoxTensionConverterLbF)
        self.verticalLayoutLbFConverter.setObjectName(u"verticalLayoutLbFConverter")
        self.lineEditConverterLbF = QLineEdit(self.groupBoxTensionConverterLbF)
        self.lineEditConverterLbF.setObjectName(u"lineEditConverterLbF")
        sizePolicy1.setHeightForWidth(self.lineEditConverterLbF.sizePolicy().hasHeightForWidth())
        self.lineEditConverterLbF.setSizePolicy(sizePolicy1)

        self.verticalLayoutLbFConverter.addWidget(self.lineEditConverterLbF)


        self.verticalLayoutUnitCoverter.addWidget(self.groupBoxTensionConverterLbF)


        self.verticalLayoutUnits.addWidget(self.groupBoxUnitConverter)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutUnits.addItem(self.verticalSpacer_2)


        self.horizontalLayoutSetupLeft.addWidget(self.groupBoxUnits)

        self.horizontalSpacerReserved = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutSetupLeft.addItem(self.horizontalSpacerReserved)


        self.horizontalLayoutSetup.addLayout(self.horizontalLayoutSetupLeft)

        self.tabWidget.addTab(self.setupTab, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1100, 33))
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
        self.groupBoxListSpoke.setTitle(QCoreApplication.translate("mainWindow", u"Spokes", None))
        self.groupBoxListSpokeMeasurements.setTitle(QCoreApplication.translate("mainWindow", u"Measurements", None))
        self.pushButtonUseLeft.setText(QCoreApplication.translate("mainWindow", u"Use on the left", None))
        self.pushButtonUseRight.setText(QCoreApplication.translate("mainWindow", u"Use on the right", None))
        self.pushButtonNewMeasurement.setText(QCoreApplication.translate("mainWindow", u"Add", None))
        self.pushButtonEditMeasurement.setText(QCoreApplication.translate("mainWindow", u"Edit", None))
        self.pushButtonDeleteMeasurement.setText(QCoreApplication.translate("mainWindow", u"Remove", None))
        self.groupBoxCreateSpoke.setTitle(QCoreApplication.translate("mainWindow", u"Select or create a spoke", None))
        self.groupBoxSpokeManufacturer.setTitle(QCoreApplication.translate("mainWindow", u"Manufacturer", None))
        self.groupBoxNewSpokeManufacturer.setTitle(QCoreApplication.translate("mainWindow", u"New manufacturer", None))
        self.pushButtonSaveAsSpokeManufacturer.setText(QCoreApplication.translate("mainWindow", u"Save as new", None))
        self.groupBoxSpoke.setTitle(QCoreApplication.translate("mainWindow", u"Spoke", None))
        self.groupBoxName.setTitle(QCoreApplication.translate("mainWindow", u"Name", None))
        self.groupBoxSpokeType.setTitle(QCoreApplication.translate("mainWindow", u"Type", None))
        self.groupBoxSpokeGauge.setTitle(QCoreApplication.translate("mainWindow", u"Gauge", None))
        self.groupBoxSpokeWeight.setTitle(QCoreApplication.translate("mainWindow", u"Weight", None))
        self.groupBoxSpokeDimension.setTitle(QCoreApplication.translate("mainWindow", u"Dimension", None))
        self.groupBoxSpokeComment.setTitle(QCoreApplication.translate("mainWindow", u"Comment", None))
        self.pushButtonSpokeUpdate.setText(QCoreApplication.translate("mainWindow", u"Update", None))
        self.pushButtonSpokeSaveAs.setText(QCoreApplication.translate("mainWindow", u"Save as new", None))
        self.pushButtonSpokeClear.setText(QCoreApplication.translate("mainWindow", u"Clear", None))
        self.pushButtonSpokeDelete.setText(QCoreApplication.translate("mainWindow", u"Delete", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.spokeTab), QCoreApplication.translate("mainWindow", u"Spokes", None))
        self.groupBoxMeasurementLeft.setTitle(QCoreApplication.translate("mainWindow", u"Measurement", None))
        self.groupBoxMeasurementComment.setTitle(QCoreApplication.translate("mainWindow", u"Comment", None))
        self.pushButtonPreviousMeasurement.setText(QCoreApplication.translate("mainWindow", u"Previous", None))
        self.pushButtonNextMeasurement.setText(QCoreApplication.translate("mainWindow", u"Next", None))
        self.pushButtonSaveMeasurement.setText(QCoreApplication.translate("mainWindow", u"Save", None))
        self.groupBoxMeasurementRight.setTitle(QCoreApplication.translate("mainWindow", u"Trendline chart", None))
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
        self.pushButtonStartTensioning.setText(QCoreApplication.translate("mainWindow", u"Start", None))
        self.pushButtonSwitchView.setText(QCoreApplication.translate("mainWindow", u"Switch view", None))
        self.pushButtonPreviousSpoke.setText(QCoreApplication.translate("mainWindow", u"Previous spoke", None))
        self.pushButtonNextSpoke.setText(QCoreApplication.translate("mainWindow", u"Next spoke", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tensioningTab), QCoreApplication.translate("mainWindow", u"Tension a wheel", None))
        self.groupBoxLanguage.setTitle(QCoreApplication.translate("mainWindow", u"Language", None))
        self.groupBoxSpokeduino.setTitle(QCoreApplication.translate("mainWindow", u"Spokeduino port", None))
        self.checkBoxSpokeduinoEnabled.setText(QCoreApplication.translate("mainWindow", u"Use Spokeduino", None))
        self.groupBoxTensiometer.setTitle(QCoreApplication.translate("mainWindow", u"Tensiometer", None))
        self.pushButtonMultipleTensiometers.setText("")
        self.groupBoxtNewTensiometer.setTitle(QCoreApplication.translate("mainWindow", u"New tensiometer", None))
        self.pushButtonNewTensiometer.setText(QCoreApplication.translate("mainWindow", u"Create", None))
        self.groupBoxMeasurementSetup.setTitle(QCoreApplication.translate("mainWindow", u"Spoke measuring", None))
        self.groupBoxSpokeMeasurementType.setTitle(QCoreApplication.translate("mainWindow", u"Measurement type", None))
        self.radioButtonMeasurementDefault.setText(QCoreApplication.translate("mainWindow", u"Default values", None))
        self.radioButtonMeasurementCustom.setText(QCoreApplication.translate("mainWindow", u"Custom values", None))
        self.groupBoxMeasurementDirection.setTitle(QCoreApplication.translate("mainWindow", u"Spoke measurement direction", None))
        self.radioButtonMeasurementDown.setText(QCoreApplication.translate("mainWindow", u"From high to low", None))
        self.radioButtonMeasurementUp.setText(QCoreApplication.translate("mainWindow", u"From low to high", None))
        self.groupBoxFitType.setTitle(QCoreApplication.translate("mainWindow", u"Fit type", None))
        self.radioButtonFitLinear.setText(QCoreApplication.translate("mainWindow", u"Linear", None))
        self.radioButtonFitQuadratic.setText(QCoreApplication.translate("mainWindow", u"Quadratic", None))
        self.radioButtonFitCubic.setText(QCoreApplication.translate("mainWindow", u"Cubic", None))
        self.radioButtonFitQuartic.setText(QCoreApplication.translate("mainWindow", u"Quartic", None))
        self.radioButtonFitSpline.setText(QCoreApplication.translate("mainWindow", u"Spline", None))
        self.radioButtonFitExponential.setText(QCoreApplication.translate("mainWindow", u"Exponential", None))
        self.radioButtonFitLogarithmic.setText(QCoreApplication.translate("mainWindow", u"Logarithmic", None))
        self.radioButtonFitPowerLaw.setText(QCoreApplication.translate("mainWindow", u"Power law", None))
        self.groupBoxDirectionsSetup.setTitle(QCoreApplication.translate("mainWindow", u"Wheel tensioning", None))
        self.groupBoxWheelRotationDirection.setTitle(QCoreApplication.translate("mainWindow", u"Wheel rotation direction", None))
        self.radioButtonRotationClockwise.setText(QCoreApplication.translate("mainWindow", u"Clockwise", None))
        self.radioButtonRotationCounterclockwise.setText(QCoreApplication.translate("mainWindow", u"Counterclockwise", None))
        self.groupBoxWheelMeasurementType.setTitle(QCoreApplication.translate("mainWindow", u"Wheel measurement direction", None))
        self.radioButtonLeftRight.setText(QCoreApplication.translate("mainWindow", u"Left-Right", None))
        self.radioButtonSideBySide.setText(QCoreApplication.translate("mainWindow", u"Side by side", None))
        self.radioButtonRightLeft.setText(QCoreApplication.translate("mainWindow", u"Right-Left", None))
        self.groupBoxUnits.setTitle(QCoreApplication.translate("mainWindow", u"Units", None))
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

