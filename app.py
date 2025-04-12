import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDialog, QCalendarWidget, QFormLayout, QLineEdit, QGridLayout, QFrame
from PySide6.QtCore import QDate, Qt, QDateTime, QPointF
import sys
from src.json_func import OTDStorage
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtGui import QPainter, QFont, QRegularExpressionValidator
from src.sdtime import SDTime

jsonFileName = "ot.json"
otdStorage = OTDStorage(jsonFileName)
sdt = SDTime()

version_flag = False

class OTCalculator(QDialog):
    """
    A dialog to calculate the OT time based on the start and end times and of course known work hour.
    """
    def __init__(self):

        def actualWorkHours():
            """
            Calculate the actual work hours based on the input times.
            """
            # Ensure the full time is entered in the format HH:MM before passing to diffTime
            for edit in [backTimeEdit, riceTimeEdit, lunchEndEdit, workEndEdit]:
                if len(edit.text()) == 2:
                    edit.setText(edit.text() + ":")

            backTime = backTimeEdit.text() if len(backTimeEdit.text()) == 5 else ""
            riceTime = riceTimeEdit.text() if len(riceTimeEdit.text()) == 5 else ""
            lunchEnd = lunchEndEdit.text() if len(lunchEndEdit.text()) == 5 else ""
            workEnd = workEndEdit.text() if len(workEndEdit.text()) == 5 else ""

            if not all([backTime, riceTime, lunchEnd, workEnd]):
                return

            actualLunchLength = sdt.diffTime(riceTime, lunchEnd)
            totalActualLength = sdt.diffTime(backTime, workEnd)
            actualWorkLength = totalActualLength - actualLunchLength

            # Update the labels with the calculated values
            actualWorkLengthLabel.setText(f"{actualWorkLength} 分鐘")
            actualLunchLengthLabel.setText(f"{actualLunchLength} 分鐘")
            totalActualLengthLabel.setText(f"{totalActualLength} 分鐘")

            ot = totalActualLength - sdt.diffTime(otdStorage.workhour_start, otdStorage.workhour_end)

            otLengthLabel.setText(f"{ot} 分鐘" if isinstance(ot, int) else "--- 分鐘")



        super().__init__()
        self.setWindowTitle("OT 時長計算")
        self.setMinimumSize(300, 200)

        gridLaytout = QGridLayout()
        titleLabel = QLabel("<b>OT 時長計算</b>")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setStyleSheet("font-size: 18px; font-weight: bold;")
        gridLaytout.addWidget(titleLabel, 0, 0, 1, 2)

        # Add two smaller QLabel widgets
        idealTimeLabel = QLabel("理想打卡時間")
        idealTimeLabel.setStyleSheet("font-size: 14px; font-weight: bold;")
        actualTimeLabel = QLabel("實際打卡時間")
        actualTimeLabel.setStyleSheet("font-size: 14px; font-weight: bold;")
        idealTimeLabel.setAlignment(Qt.AlignCenter)
        actualTimeLabel.setAlignment(Qt.AlignCenter)
        gridLaytout.addWidget(idealTimeLabel, 1, 0)
        gridLaytout.addWidget(actualTimeLabel, 1, 1)

        # Left frame with QFormLayout
        leftFrame = QFrame()
        leftFrame.setFrameShape(QFrame.Box)
        leftFrame.setLineWidth(2)
        leftLayout = QFormLayout()
        leftFrame.setLayout(leftLayout)
        leftLayout.addRow(QLabel("返工時間:"), QLineEdit(otdStorage.workhour_start, readOnly=True))
        leftLayout.addRow(QLabel("放飯時間:"), QLineEdit(otdStorage.workhour_lunch_start, readOnly=True))
        leftLayout.addRow(QLabel("完飯時間:"), QLineEdit(otdStorage.workhour_lunch_end, readOnly=True))
        leftLayout.addRow(QLabel("放工時間:"), QLineEdit(otdStorage.workhour_end, readOnly=True))
        gridLaytout.addWidget(leftFrame, 2, 0)

        regExpr = QRegularExpressionValidator(r"^(?:[01]\d|2[0-3]):[0-5]\d$")

        # Right frame with QFormLayout
        rightFrame = QFrame()
        rightFrame.setFrameShape(QFrame.Box)
        rightFrame.setLineWidth(2)
        rightLayout = QFormLayout()
        rightFrame.setLayout(rightLayout)
        backTimeEdit =  QLineEdit()
        backTimeEdit.setPlaceholderText("00:00-23:59")
        backTimeEdit.setValidator(regExpr)
        rightLayout.addRow(QLabel("返工時間:"), backTimeEdit)
        riceTimeEdit = QLineEdit()
        riceTimeEdit.setPlaceholderText("00:00-23:59")
        riceTimeEdit.setValidator(regExpr)
        rightLayout.addRow(QLabel("放飯時間:"), riceTimeEdit)
        lunchEndEdit = QLineEdit()
        lunchEndEdit.setPlaceholderText("00:00-23:59")
        lunchEndEdit.setValidator(regExpr)
        rightLayout.addRow(QLabel("完飯時間:"), lunchEndEdit)
        workEndEdit = QLineEdit()
        workEndEdit.setPlaceholderText("00:00-23:59")
        workEndEdit.setValidator(regExpr)
        rightLayout.addRow(QLabel("放工時間:"), workEndEdit)
        gridLaytout.addWidget(rightFrame, 2, 1)

        buttomFrame = QFrame()
        buttomFrame.setFrameShape(QFrame.Box)
        buttomFrame.setLineWidth(2)
        buttomLayout = QGridLayout()
        buttomFrame.setLayout(buttomLayout)

        # Finding details for normal work hours
        buttomLayout.addWidget(QLabel("<b>正常工時:</b>"), 0, 0, 1, 1)
        buttomLayout.addWidget(QLabel("<b>正常午餐時間:</b>"), 1, 0, 1, 1)
        buttomLayout.addWidget(QLabel("<b>總在校時間:</b>"), 2, 0, 1, 1)

        normalWorkLengthLabel = QLabel(f"{sdt.diffTime(otdStorage.workhour_start, otdStorage.workhour_end) - 60} 分鐘")
        normalLunchLengthLabel = QLabel(f"{sdt.diffTime(otdStorage.workhour_lunch_start, otdStorage.workhour_lunch_end)} 分鐘")
        totalTimeLengthLabel = QLabel(f"{sdt.diffTime(otdStorage.workhour_start, otdStorage.workhour_end)} 分鐘")
        normalWorkLengthLabel.setAlignment(Qt.AlignLeft)
        normalLunchLengthLabel.setAlignment(Qt.AlignLeft)
        totalTimeLengthLabel.setAlignment(Qt.AlignLeft)

        buttomLayout.addWidget(normalWorkLengthLabel, 0, 1, 1, 1)
        buttomLayout.addWidget(normalLunchLengthLabel, 1, 1, 1, 1)
        buttomLayout.addWidget(totalTimeLengthLabel, 2, 1, 1, 1)

        buttomLayout.addWidget(QLabel("<b>實際工時:</b>"), 0, 2, 1, 1)
        buttomLayout.addWidget(QLabel("<b>實際午餐時間:</b>"), 1, 2, 1, 1)
        buttomLayout.addWidget(QLabel("<b>實際總在校時間:</b>"), 2, 2, 1, 1)

        actualWorkLengthLabel = QLabel("--- 分鐘")
        actualLunchLengthLabel = QLabel("--- 分鐘")
        totalActualLengthLabel = QLabel("--- 分鐘")

        actualWorkLengthLabel.setAlignment(Qt.AlignLeft)
        actualLunchLengthLabel.setAlignment(Qt.AlignLeft)
        totalActualLengthLabel.setAlignment(Qt.AlignLeft)

        buttomLayout.addWidget(actualWorkLengthLabel, 0, 3, 1, 1)
        buttomLayout.addWidget(actualLunchLengthLabel, 1, 3, 1, 1)
        buttomLayout.addWidget(totalActualLengthLabel, 2, 3, 1, 1)

        # Finding details for actual work hours
        backTimeEdit.textEdited.connect(actualWorkHours)
        riceTimeEdit.textEdited.connect(actualWorkHours)
        lunchEndEdit.textEdited.connect(actualWorkHours)
        workEndEdit.textEdited.connect(actualWorkHours)

        buttomLayout.addWidget(QLabel("<b>OT 時長:</b>"), 3, 1, 1, 1)
        otLengthLabel = QLabel("--- 分鐘")
        otLengthLabel.setAlignment(Qt.AlignLeft)
        buttomLayout.addWidget(otLengthLabel, 3, 2, 1, 1)

        gridLaytout.addWidget(buttomFrame, 3, 0, 1, 2)

        self.setLayout(gridLaytout)

class OTRecordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OT 記錄")
        self.setMinimumSize(200, 300)
        vlayout = QVBoxLayout()
        vlayout.addWidget(QLabel("請在下面的表格中填寫OT的詳細信息"))

        # The form layout in the middle of the dialog
        formL = QFormLayout()
        formL.addRow(QLabel("<b>請各位同事記錄OT!</b>"), QLabel("OT Reminder"))
        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setMinimumDate(QDate.currentDate().addDays(-7)) # Set the minimum date to 7 days ago
        formL.addRow(QLabel("OT日期:"), calendar)
        length = QLineEdit()
        formL.addRow(QLabel("OT時長 (in mins):"), length)
        reason = QLineEdit()
        formL.addRow(QLabel("OT原因 (Optional):"), reason)
        by = QLineEdit()
        formL.addRow(QLabel("邊個叫你OT (Optional):"), by)
        vlayout.addLayout(formL)

        button = QPushButton("新增OT記錄")
        vlayout.addWidget(button)
        button.clicked.connect(lambda: self.saveOT(calendar.selectedDate(), length.text(), reason.text(), by.text()))
        # Add a close button to the dialog
        close_button = QPushButton("關閉")
        close_button.clicked.connect(self.accept)  # Close the dialog
        vlayout.addWidget(close_button, alignment=Qt.AlignCenter)

        self.setLayout(vlayout)   # Confirm the layout of the dialog
        self.show()

        self.calculator = OTCalculator()
        self.calculator.setParent(None)  # Detach the calculator dialog from the record dialog
        self.calculator.move(self.x()+ self.width(), self.y())  # Move the calculator dialog to a new position
        self.calculator.show()  # Show the calculator dialog in a new window

    def close(self):
        self.calculator.close()  # Close the calculator dialog when the record dialog is closed
        return super().close()

    def reject(self):
        self.calculator.reject()
        return super().reject()

    def accept(self):
        self.calculator.accept()  # Close the calculator dialog when the record dialog is closed
        return super().accept()

    def saveOT(self, date: QDate, length: int, reason: str, by: str):
        """
        Save the OT details to the JSON file.
        """
        # Convert the date to a string
        date_str = date.toString("yyyy-MM-dd")
        # Convert the length to a number
        try:
            otdStorage.newEntry(date_str, int(length), reason, by)
        except ValueError:
            error_dialog = QDialog(self)
            error_dialog.setWindowTitle("輸入錯誤")
            error_layout = QVBoxLayout()
            error_layout.addWidget(QLabel("OT時長必須是一個有效的數字！請重新輸入。"))
            close_button = QPushButton("關閉")
            close_button.clicked.connect(error_dialog.close)
            error_layout.addWidget(close_button)
            error_dialog.setLayout(error_layout)
            error_dialog.exec()
            return
        
        # Show a message box to confirm the entry
        recorded_dialog = QDialog(self)
        recorded_dialog.setWindowTitle("OT記錄成功")
        recorded_layout = QVBoxLayout()

        # Add confirmation message
        confirmation_message = QLabel(f"<b>OT記錄成功！</b><br>"
                          f"OT日期: {date_str}<br>"
                          f"OT時長: {length} 分鐘")
        if reason:
            confirmation_message.setText(confirmation_message.text() + f"<br>OT原因: {reason}")
        if by:
            confirmation_message.setText(confirmation_message.text() + f"<br>邊個叫: {by}")
        confirmation_message.setAlignment(Qt.AlignCenter)
        recorded_layout.addWidget(confirmation_message)

        # Add close button
        close_button = QPushButton("關閉")
        close_button.clicked.connect(recorded_dialog.close)  # Close the dialog
        recorded_layout.addWidget(close_button, alignment=Qt.AlignCenter)

        recorded_dialog.setLayout(recorded_layout)
        recorded_dialog.exec()

class OTGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(400, 220)  # Set minimum size for the windo
        self.setWindowTitle("OT 記錄器")

        # Create a layout and add widgets to it
        layout = QVBoxLayout()

        #Only appear if version_flag is False
        if not version_flag:
            layout.addWidget(QLabel("請各位不要忘記自己貢獻比學校嘅時間!"))
            layout.addWidget(QLabel("一寸光陰一寸金，"))
            layout.addWidget(QLabel("寸金難買寸光陰!"))
            layout.addWidget(QLabel("請各位同事珍惜時間……"))
        else:
            self.setWindowTitle("OT 記錄器(地下專用版本)")
        
        button = QPushButton("按我記錄OT")
        button2 = QPushButton("按我查看OT記錄(Graph)")
        button3 =  QPushButton("按我查看OT記錄(統計)")
        layout.addWidget(button)
        layout.addWidget(button2)
        layout.addWidget(button3)
        # Set the layout to a central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connnect button
        button.clicked.connect(OTRecordDialog) 
        button2.clicked.connect(self.showOTGraph)
        button3.clicked.connect(self.showOTStats)

    
    def showOTGraph(self):
        """
        Display a time-based graph showing the amount of OT recorded.
        """

        # Retrieve data from storage
        data = otdStorage.entries  # Assuming this returns a list of dicts with 'date' and 'length'
        minDate = QDateTime().fromString(otdStorage.firstDate(), "yyyy-MM-dd")
        maxDate = QDateTime().fromString(otdStorage.lastDate(), "yyyy-MM-dd")

        # Prepare data for the graph
        series = QLineSeries()
        for entry in data:
            series.append(QPointF(QDateTime.fromString(entry['date'], "yyyy-MM-dd").toMSecsSinceEpoch(), entry['amount']))
        series.setPointLabelsVisible(True)  # Show point labels
        series.setPointLabelsFormat("@yPoint mins")  # Format for point labels
        series.setPointLabelsFont(QFont("Arial", 10))
        series.setPointLabelsColor("#4b006e")
        series.setPointLabelsClipping(False)  # Ensure labels are fully visible
        #series.setPointLabelsPosition(QLineSeries.LabelsAbove)  # Position labels above the points

        # Create the chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("OT 時間記錄")
        chart.setAnimationOptions(QChart.AllAnimations)

        axisX = QDateTimeAxis()
        axisX.setTitleText("日期")
        axisX.setFormat("yyyy-MM-dd")  # Set the date format
        axisX.setTickCount(minDate.daysTo(maxDate) + 3)
        axisX.setLabelsAngle(-90)  # Rotate the labels for better readability
        axisX.setRange(minDate.addDays(-1), maxDate.addDays(1))  # Set the range of the x-axis
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText("OT 時長 (分鐘)")
        axisY.setLabelFormat("%d")
        axisY.setTickCount(len(data) + 1)
        axisY.setRange(0, 0 if len(data) == 0 else max(entry['amount'] for entry in data) + 10)  # Add some padding
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        # Create a chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumSize(960, 640)  # Set minimum size for the chart view

        # Display the chart in a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("OT 記錄圖表")
        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        close_button = QPushButton("關閉")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        dialog.setLayout(layout)
        dialog.exec()
    
    def showDetailedStats(self, turnOff=False):
        """
        This function add a new panel between the bottom'est button and the monthly stats panel,
        after that resize the window to fit the new panel.

        The state of the show detailed stats button will be changed to "隱藏更詳細的統計"
        and this function will be called again to hide the detailed stats panel.
        """
        if turnOff:
            # Hide the detailed stats panel
            self.detailedStatsFrame.hide()
            self.detailedStatsButton.setText("顯示更詳細的統計")
            return
        else:
            # Show the detailed stats panel
            self.detailedStatsFrame.show()
            self.detailedStatsButton.setText("隱藏更詳細的統計")
            self.resize(self.width(), self.height() + 200)  # Resize the window to fit the new panel, actual size will be determined later

    def showOTStats(self):
        """
        Display a dialog with OT statistics.
        """
            
        def div(x, y):
            return x / y if y != 0 else 0

        # Retrieve data from storage
        data = otdStorage.entries
        dialog = QDialog(self)
        dialog.setWindowTitle("OT 記錄統計")
        dialog.setMinimumSize(400,300)

        # Grid layout with 4 rows and 2 columns
        grid_layout = QGridLayout()

        # The topic label at the top
        topicLabel = QLabel("<b>OT 記錄統計</b>")
        topicLabel.setAlignment(Qt.AlignCenter)
        topicLabel.setStyleSheet("font-size: 18px; font-weight: bold;")
        grid_layout.addWidget(topicLabel, 0, 0, 1, 2)

        # The first frame that span row 1 and column 1 and 2
        totalStatsFrame = QFrame()
        totalStatsFrame.setFrameShape(QFrame.Box)
        totalStatsFrame.setLineWidth(2)
        totalStatsLayout = QVBoxLayout()
        totalStatsFrame.setLayout(totalStatsLayout)
        totalStatsLabel = QLabel("<b>總計</b>")
        totalStatsLabel.setAlignment(Qt.AlignCenter)
        totalStatsLabel.setStyleSheet("font-size: 14px; font-weight: bold;")
        totalStatsLayout.addWidget(totalStatsLabel)
        totalStatsLayout.addWidget(QLabel(f"OT 總時長: {otdStorage.totalLength} 分鐘"))
        totalStatsLayout.addWidget(QLabel(f"OT 總次數: {otdStorage.total} 次"))
        totalStatsLayout.addWidget(QLabel(f"平均每次 OT 時長: {div(otdStorage.totalLength, otdStorage.total):.2f} 分鐘"))
        totalStatsLayout.addWidget(QLabel(f"OT 中位數: {otdStorage.median()} 分鐘"))
        totalStatsLayout.addWidget(QLabel(f"OT 標準差: {otdStorage.standardDeviation():.2f} 分鐘"))
        grid_layout.addWidget(totalStatsFrame, 1, 0, 1, 2)


        # The second frame that spans row 2 and column 1
        thisWeekFrame = QFrame()
        thisWeekFrame.setFrameShape(QFrame.Box)
        thisWeekFrame.setLineWidth(2)
        thisWeekLayout = QVBoxLayout()
        thisWeekFrame.setLayout(thisWeekLayout)
        thisWeekLabel = QLabel("<b>本周</b>")
        thisWeekLabel.setAlignment(Qt.AlignCenter)
        thisWeekLabel.setStyleSheet("font-size: 14px; font-weight: bold;")
        thisWeekLayout.addWidget(thisWeekLabel)
        thisWeekTotalLength = otdStorage.rangedTotalLength(sdt.thisWeekStart(), sdt.thisWeekEnd())
        thisWeekTotal = otdStorage.rangedTotal(sdt.thisWeekStart(), sdt.thisWeekEnd())
        thisWeekLayout.addWidget(QLabel(f"OT 總時長: {thisWeekTotalLength} 分鐘"))
        thisWeekLayout.addWidget(QLabel(f"OT 總次數: {thisWeekTotal} 次"))
        thisWeekLayout.addWidget(QLabel(f"平均每次 OT 時長: {div(thisWeekTotalLength, thisWeekTotal):.2f} 分鐘"))
        grid_layout.addWidget(thisWeekFrame, 2, 0)

        # The third frame that spans row 2 and column 2
        lastWeekFrame = QFrame()
        lastWeekFrame.setFrameShape(QFrame.Box)
        lastWeekFrame.setLineWidth(2)
        lastWeekLayout = QVBoxLayout()
        lastWeekFrame.setLayout(lastWeekLayout)
        lastWeekLabel = QLabel("<b>上周</b>")
        lastWeekLabel.setAlignment(Qt.AlignCenter)
        lastWeekLabel.setStyleSheet("font-size: 14px; font-weight: bold;")
        lastWeekLayout.addWidget(lastWeekLabel)
        lastWeekTotalLength = otdStorage.rangedTotalLength(sdt.lastWeekStart(), sdt.lastWeekEnd())
        lastWeekTotal = otdStorage.rangedTotal(sdt.lastWeekStart(), sdt.lastWeekEnd())
        lastWeekLayout.addWidget(QLabel(f"OT 總時長: {lastWeekTotalLength} 分鐘"))
        lastWeekLayout.addWidget(QLabel(f"OT 總次數: {lastWeekTotal} 次"))
        lastWeekLayout.addWidget(QLabel(f"平均每次 OT 時長: {div(lastWeekTotalLength, lastWeekTotal):.2f} 分鐘"))
        grid_layout.addWidget(lastWeekFrame, 2, 1)

        # The fourth frame that spans row 3 and column 1
        thisMonthFrame = QFrame()
        thisMonthFrame.setFrameShape(QFrame.Box)
        thisMonthFrame.setLineWidth(2)
        thisMonthLayout = QVBoxLayout()
        thisMonthFrame.setLayout(thisMonthLayout)
        thisMonthLabel = QLabel("<b>本月</b>")
        thisMonthLabel.setAlignment(Qt.AlignCenter)
        thisMonthLabel.setStyleSheet("font-size: 14px; font-weight: bold;")
        thisMonthLayout.addWidget(thisMonthLabel)
        thisMonthTotalLength = otdStorage.rangedTotalLength(sdt.thisMonthStart(), sdt.thisMonthEnd())
        thisMonthTotal = otdStorage.rangedTotal(sdt.thisMonthStart(), sdt.thisMonthEnd())
        thisMonthLayout.addWidget(QLabel(f"OT 總時長: {thisMonthTotalLength} 分鐘"))
        thisMonthLayout.addWidget(QLabel(f"OT 總次數: {thisMonthTotal} 次"))
        thisMonthLayout.addWidget(QLabel(f"平均每次 OT 時長: {div(thisMonthTotalLength, thisMonthTotal):.2f} 分鐘"))
        grid_layout.addWidget(thisMonthFrame, 3, 0)

        # The fifth frame that spans row 3 and column 2
        lastMonthFrame = QFrame()
        lastMonthFrame.setFrameShape(QFrame.Box)
        lastMonthFrame.setLineWidth(2)
        lastMonthLayout = QVBoxLayout()
        lastMonthFrame.setLayout(lastMonthLayout)
        lastMonthLabel = QLabel("<b>上月</b>")
        lastMonthLabel.setAlignment(Qt.AlignCenter)
        lastMonthLabel.setStyleSheet("font-size: 14px; font-weight: bold;")
        lastMonthLayout.addWidget(lastMonthLabel)
        lastMonthTotalLength = otdStorage.rangedTotalLength(sdt.lastMonthStart(), sdt.lastMonthEnd())
        lastMonthTotal = otdStorage.rangedTotal(sdt.lastMonthStart(), sdt.lastMonthEnd())
        lastMonthLayout.addWidget(QLabel(f"OT 總時長: {lastMonthTotalLength} 分鐘"))
        lastMonthLayout.addWidget(QLabel(f"OT 總次數: {lastMonthTotal} 次"))
        lastMonthLayout.addWidget(QLabel(f"平均每次 OT 時長: {div(lastMonthTotalLength, lastMonthTotal):.2f} 分鐘"))
        grid_layout.addWidget(lastMonthFrame, 3, 1)

        # Detailed frame, initially hidden
        self.detailedStatsFrame = QFrame()
        self.detailedStatsFrame.setFrameShape(QFrame.Box)
        self.detailedStatsFrame.setLineWidth(2)
        

        # Add a button at the bottom that asks if the user want to show a more detailed statistics
        button = QPushButton("顯示更詳細的統計")
        button.clicked.connect(self.showDetailedStats)
        grid_layout.addWidget(button, 4, 0, 1, 2)   # span 2 columns

        dialog.setLayout(grid_layout)
        dialog.exec()



if __name__ == "__main__":
    otdStorage.loadJson()  # Load the JSON file
    
    name = os.path.basename(sys.argv[0])  # Get the name of the file
    if name == "OT 記錄器(地下專用版本).exe":
        version_flag = True

    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft JhengHei UI", 11))
    ot_gui = OTGUI()
    ot_gui.show()
    sys.exit(app.exec())
    
