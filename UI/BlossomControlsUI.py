#!/usr/bin/python

from PyQt6.QtWidgets import (QWidget, QSlider, QHBoxLayout,
                             QLabel, QApplication, QGridLayout, QStylePainter, QStyleOptionSlider, QStyle, QVBoxLayout, QPushButton, QListWidget, QLineEdit)
from PyQt6.QtCore import (Qt, pyqtSignal)
from PyQt6.QtGui import QPainter
import sys
import json
import math

# from blossompy import Blossom
# bl = Blossom(sequence_dir='../blossompy/src/sequences')


# overriding slider class
# https://stackoverflow.com/questions/68179408/i-need-to-put-several-marks-on-a-qslider
# ^^^ is likely an earlier version than PyQt6

class TickOverride(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticks = set()
        self.setTickPosition(self.TickPosition.TicksAbove)

    def addTick(self, value=None):
        if isinstance(value, bool) or value is None:
            value = self.value()
        if not value in self.ticks and self.minimum() <= value <= self.maximum():
            self.ticks.add(value)
            self.update()

    def removeTick(self, value=None):
        if isinstance(value, bool) or value is None:
            value = self.value()
        if value in self.ticks:
            self.ticks.discard(value)
            self.update()

    def paintEvent(self, event):
        qp = QStylePainter(self)
        opt = QStyleOptionSlider()
        style = self.style()
        self.initStyleOption(opt)

        # draw the groove only
        opt.subControls = style.SubControl.SC_SliderGroove
        qp.drawComplexControl(style.ComplexControl.CC_Slider, opt)

        sliderMin = self.minimum()
        sliderMax = self.maximum()
        sliderLength = style.pixelMetric(style.PixelMetric.PM_SliderLength, opt, self)
        span = style.pixelMetric(style.PixelMetric.PM_SliderSpaceAvailable, opt, self)

        # if the tick option is set and ticks actually exist, draw them
        if self.ticks and self.tickPosition():
            qp.save()
            # second (integer) input controls ticker height relative to slider
            qp.translate(opt.rect.x() + sliderLength / 2, 7)
            grooveRect = style.subControlRect(
                style.ComplexControl.CC_Slider, opt, style.SubControl.SC_SliderGroove)
            grooveTop = grooveRect.top() - 1
            grooveBottom = grooveRect.bottom() + 1
            ticks = self.tickPosition()
            bottom = self.height()
            for value in sorted(self.ticks):
                x = style.sliderPositionFromValue(
                    sliderMin, sliderMax, value, span)
                if ticks and self.TickPosition.TicksAbove:
                    qp.drawLine(x, 10, x, grooveTop)
                if ticks and self.TickPosition.TicksBelow:
                    qp.drawLine(x, grooveBottom, x, bottom)
            qp.restore()

        opt.subControls = style.SubControl.SC_SliderHandle
        opt.activeSubControls = style.SubControl.SC_SliderHandle
        if self.isSliderDown():
            opt.state |= style.StateFlag.State_Sunken
        qp.drawComplexControl(style.ComplexControl.CC_Slider, opt)



class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # bl.connect()  # safe init and connects to blossom and puts blossom in reset position
        # bl.load_sequences()

        grid = QGridLayout()

        # breaks slider color for some reason
        # self.setStyleSheet('background-color:purple')
        
        
        global maxMillis
        maxMillis = 5000
        
        # max millis entry
        self.maxMillisEntry = QLineEdit()
        self.maxMillisEntry.setMaximumWidth(60)

        # max millis button
        self.maxMillisButton = QPushButton("Enter", self)
        self.maxMillisButton.setMaximumWidth(60)
        self.maxMillisButton.clicked.connect(self.maxMillisButtonClicked)
        
        # new sequences
        self.slider = TickOverride(Qt.Orientation.Horizontal, self)
        self.slider.setRange(0, maxMillis)
        self.slider.setPageStep(1)
        self.slider.setSingleStep(1000)
        self.slider.valueChanged.connect(self.updateSlider)
        self.slider.setTickPosition(TickOverride.TickPosition.TicksAbove)

        # add tick button
        self.addTickButton = QPushButton("Add Tick", self)
        self.addTickButton.clicked.connect(self.addTickClicked)

        # delete tick button
        self.deleteTickButton = QPushButton("Delete Tick", self)
        self.deleteTickButton.clicked.connect(self.deleteTickClicked)

        # tower 1
        self.tower1 = QSlider(Qt.Orientation.Horizontal, self)
        self.tower1.setRange(0, 180)
        self.tower1.setPageStep(5)
        self.tower1.setSingleStep(5)
        self.tower1.valueChanged.connect(self.updateTower1)

        # tower 2
        self.tower2 = QSlider(Qt.Orientation.Horizontal, self)
        self.tower2.setRange(0, 180)
        self.tower2.setPageStep(5)
        self.tower2.setSingleStep(5)
        self.tower2.valueChanged.connect(self.updateTower2)

        # tower 3
        self.tower3 = QSlider(Qt.Orientation.Horizontal, self)
        self.tower3.setRange(0, 180)
        self.tower3.setPageStep(5)
        self.tower3.setSingleStep(5)
        self.tower3.valueChanged.connect(self.updateTower3)

        # base
        self.base = QSlider(Qt.Orientation.Horizontal, self)
        self.base.setRange(0, 180)
        self.base.setPageStep(5)
        self.base.setSingleStep(5)
        self.base.valueChanged.connect(self.updateBase)

        # ears
        self.ears = QSlider(Qt.Orientation.Horizontal, self)
        self.ears.setRange(0, 180)
        self.ears.setPageStep(5)
        self.ears.setSingleStep(5)
        self.ears.valueChanged.connect(self.updateEars)

        # list
        self.list = QListWidget()

        # sequence name entry box
        self.sequenceName = QLineEdit()
        self.sequenceName.setMaximumWidth(180)

        # save button
        self.saveButton = QPushButton("Save", self)
        self.saveButton.setMaximumWidth(60)
        self.saveButton.clicked.connect(self.saveSequence)



        ######### Labels ##########

        # max millis
        self.maxMillisLabel = QLabel('Max Millis:', self)
        self.maxMillisLabel.setAlignment(Qt.AlignmentFlag.AlignLeft |
                               Qt.AlignmentFlag.AlignVCenter)
        self.maxMillisLabel.setMinimumWidth(80)

        # new sequence bar label
        self.sliderLabel = QLabel('Sequence Timeline:', self)
        self.sliderLabel.setAlignment(Qt.AlignmentFlag.AlignLeft |
                               Qt.AlignmentFlag.AlignVCenter)
        self.sliderLabel.setMinimumWidth(80)

        self.sliderValue = QLabel('0', self)
        self.sliderValue.setAlignment(Qt.AlignmentFlag.AlignCenter |
                               Qt.AlignmentFlag.AlignVCenter)
        self.sliderValue.setMinimumWidth(40)

        # tower 1 label/value
        self.tower1label = QLabel('Tower 1:', self)
        self.tower1label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                               Qt.AlignmentFlag.AlignVCenter)
        self.tower1label.setMinimumWidth(80)

        self.tower1value = QLabel('0', self)
        self.tower1value.setAlignment(Qt.AlignmentFlag.AlignCenter |
                               Qt.AlignmentFlag.AlignVCenter)
        self.tower1value.setMinimumWidth(40)

        # tower 2 label/value
        self.tower2label = QLabel('Tower 2:', self)
        self.tower2label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                               Qt.AlignmentFlag.AlignVCenter)
        self.tower2label.setMinimumWidth(80)
        
        self.tower2value = QLabel('0', self)
        self.tower2value.setAlignment(Qt.AlignmentFlag.AlignCenter |
                              Qt.AlignmentFlag.AlignVCenter)
        self.tower2value.setMinimumWidth(40)

        # tower 3 label/value
        self.tower3label = QLabel('Tower 3:', self)
        self.tower3label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                               Qt.AlignmentFlag.AlignVCenter)
        self.tower3label.setMinimumWidth(80)
        
        self.tower3value = QLabel('0', self)
        self.tower3value.setAlignment(Qt.AlignmentFlag.AlignCenter |
                              Qt.AlignmentFlag.AlignVCenter)
        self.tower3value.setMinimumWidth(40)

        # base label/value
        self.baseLabel = QLabel('Base:', self)
        self.baseLabel.setAlignment(Qt.AlignmentFlag.AlignLeft |
                               Qt.AlignmentFlag.AlignVCenter)
        self.baseLabel.setMinimumWidth(80)
        
        self.baseValue = QLabel('0', self)
        self.baseValue.setAlignment(Qt.AlignmentFlag.AlignCenter |
                              Qt.AlignmentFlag.AlignVCenter)
        self.baseValue.setMinimumWidth(40)

        # ears label/value
        self.earsLabel = QLabel('Ears:', self)
        self.earsLabel.setAlignment(Qt.AlignmentFlag.AlignLeft |
                              Qt.AlignmentFlag.AlignVCenter)
        self.earsLabel.setMinimumWidth(80)

        self.earsValue = QLabel('0', self)
        self.earsValue.setAlignment(Qt.AlignmentFlag.AlignCenter |
                              Qt.AlignmentFlag.AlignVCenter)
        self.earsValue.setMinimumWidth(40)

        # save sequence label
        self.saveSequenceLabel = QLabel('Name/Save Sequence:', self)
        self.saveSequenceLabel.setAlignment(Qt.AlignmentFlag.AlignLeft |
                              Qt.AlignmentFlag.AlignVCenter)
        self.saveSequenceLabel.setMinimumWidth(80)

        # adding items to grid display
        grid.addWidget(self.maxMillisLabel, 0, 0)

        grid.addWidget(self.maxMillisEntry, 1, 0)
        grid.addWidget(self.maxMillisButton, 2, 0)

        grid.addWidget(self.sliderLabel, 3, 0)

        grid.addWidget(self.slider, 4, 0)
        grid.addWidget(self.sliderValue, 4, 1)

        grid.addWidget(self.addTickButton, 4, 2)
        grid.addWidget(self.deleteTickButton, 5, 2)

        grid.addWidget(self.tower1label, 5, 0)
        grid.addWidget(self.tower1, 6, 0)
        grid.addWidget(self.tower1value, 6, 1)

        grid.addWidget(self.tower2label, 7, 0)
        grid.addWidget(self.tower2, 8, 0)
        grid.addWidget(self.tower2value, 8, 1)

        grid.addWidget(self.tower3label, 9, 0)
        grid.addWidget(self.tower3, 10, 0)
        grid.addWidget(self.tower3value, 10, 1)

        grid.addWidget(self.baseLabel, 11, 0)
        grid.addWidget(self.base, 12, 0)
        grid.addWidget(self.baseValue, 12, 1)

        grid.addWidget(self.earsLabel, 13, 0)
        grid.addWidget(self.ears, 14, 0)
        grid.addWidget(self.earsValue, 14, 1)

        grid.addWidget(self.saveSequenceLabel, 15, 0)
        grid.addWidget(self.sequenceName, 16, 0)
        grid.addWidget(self.saveButton, 17, 0)

        grid.addWidget(self.list, 18, 0)

        self.setLayout(grid)

        self.setGeometry(350, 100, 600, 600)
        self.setWindowTitle('Blossom Controls')
        self.show()
    

    #init new list of frames/tower position tracker variables
    global frames_list
    frames_list =  []
    global tower1currentValue
    tower1currentValue = 0
    global tower2currentValue
    tower2currentValue = 0
    global tower3currentValue
    tower3currentValue = 0
    global baseCurrentValue
    baseCurrentValue = 0
    global earsCurrentValue
    earsCurrentValue = 0
    
    global sliderCurrentValue
    sliderCurrentValue = 0
    
    def updateSlider(self, value):
        global sliderCurrentValue
        sliderCurrentValue = 0
        sliderCurrentValue = value
        self.sliderValue.setText(str(value))

    def maxMillisButtonClicked(self, value):
        global maxMillis
        maxMillis = int(self.maxMillisEntry.text())
        self.slider.setRange(0, maxMillis)
   
    def addTickClicked(self, value):
        self.slider.addTick(value)
        self.list.insertItem(value, str(sliderCurrentValue) + ' millis: \n  tower_1 = ' + str(tower1currentValue) + ', \n  tower_2 = ' + str(tower2currentValue) + ', \n  tower_3 = ' + str(tower3currentValue) + ', \n  base = ' + str(baseCurrentValue) + ', \n  ears = ' + str(earsCurrentValue))
        
        frames_list.append ({
            'positions' : [
                {
                    'dof': 'tower_1',
                    'pos': math.radians(tower1currentValue)
                },
                {
                    'dof': 'tower_2',
                    'pos': math.radians(tower2currentValue)
                },
                {
                    'dof': 'tower_3',
                    'pos': math.radians(tower3currentValue)
                },
                {
                    'dof': 'base',
                    'pos': math.radians(baseCurrentValue)
                },
                {
                    'dof': 'ears',
                    'pos': math.radians(earsCurrentValue)
                }
            ],
            'millis': sliderCurrentValue
        })

        frames_list.sort(key=lambda x: x['millis'])
        

    def deleteTickClicked(self, value):
        self.slider.removeTick(value)
        items_list = self.list.findItems(str(sliderCurrentValue), Qt.MatchFlag.MatchStartsWith)
        
        for item in items_list:
            r = self.list.row(item)
            self.list.takeItem(r)

        global frames_list
        for idx, obj in enumerate(frames_list):
            if obj['millis'] == sliderCurrentValue:
                frames_list.pop(idx)


    def updateTower1(self, value):
        global tower1currentValue
        tower1currentValue = 0
        tower1currentValue = value
        self.tower1value.setText(str(value))
        # bl.motor_goto('tower_1', value, 0.1)

    def updateTower2(self, value):
        global tower2currentValue
        tower2currentValue = 0
        tower2currentValue = value
        self.tower2value.setText(str(value))
        # bl.motor_goto('tower_2', value, 0.1)

    def updateTower3(self, value):
        global tower3currentValue
        tower3currentValue = 0
        tower3currentValue = value
        self.tower3value.setText(str(value))
        # bl.motor_goto('tower_3', value, 0.1)

    def updateBase(self, value):
        global baseCurrentValue
        baseCurrentValue = 0
        baseCurrentValue = value
        self.baseValue.setText(str(value))

    def updateEars(self, value):
        global earsCurrentValue
        earsCurrentValue = 0
        earsCurrentValue = value
        self.earsValue.setText(str(value))
        # bl.motor_goto('tower_4', value, 0.1) 
        # name of ears motor??? ^^


    def saveSequence(self, value):
        seqName = self.sequenceName.text()
        global frames_list
        first_iteration_flag = 1
        temp_list = []
        idx = 0

        while idx != len(frames_list):
            if first_iteration_flag == 1 and frames_list[idx]['millis'] != 0:
                millis1 = 0.0
                millis2 = frames_list[idx]['millis']

                frame1_m1 = 0
                frame1_m2 = 0
                frame1_m3 = 0
                frame1_base = 0
                frame1_ears = 0

                frame2_m1 = frames_list[idx]['positions'][0]['pos']
                frame2_m2 = frames_list[idx]['positions'][1]['pos']
                frame2_m3 = frames_list[idx]['positions'][2]['pos']
                frame2_base = frames_list[idx]['positions'][3]['pos']
                frame2_ears = frames_list[idx]['positions'][4]['pos']
                
                idx-=1
                first_iteration_flag = 0

            elif frames_list[idx] == frames_list[-1]:                    
                millis1 = frames_list[idx]['millis']/1
                millis2 = 0

                frame1_m1 = frames_list[idx]['positions'][0]['pos']
                frame1_m2 = frames_list[idx]['positions'][1]['pos']
                frame1_m3 = frames_list[idx]['positions'][2]['pos']
                frame1_base = frames_list[idx]['positions'][3]['pos']
                frame1_ears = frames_list[idx]['positions'][4]['pos']

                frame2_m1 = 0
                frame2_m2 = 0
                frame2_m3 = 0
                frame2_base = 0
                frame2_ears = 0

            else:
                millis1 = frames_list[idx]['millis']/1
                millis2 = frames_list[idx+1]['millis']

                frame1_m1 = frames_list[idx]['positions'][0]['pos']
                frame1_m2 = frames_list[idx]['positions'][1]['pos']
                frame1_m3 = frames_list[idx]['positions'][2]['pos']
                frame1_base = frames_list[idx]['positions'][3]['pos']
                frame1_ears = frames_list[idx]['positions'][4]['pos']

                frame2_m1 = frames_list[idx+1]['positions'][0]['pos']
                frame2_m2 = frames_list[idx+1]['positions'][1]['pos']
                frame2_m3 = frames_list[idx+1]['positions'][2]['pos']
                frame2_base = frames_list[idx+1]['positions'][3]['pos']
                frame2_ears = frames_list[idx+1]['positions'][4]['pos']


            millis_diff = millis2-millis1
            m1_increment = (frame2_m1-frame1_m1)/(millis_diff)
            m2_increment = (frame2_m2-frame1_m2)/(millis_diff)
            m3_increment = (frame2_m3-frame1_m3)/(millis_diff)
            base_increment = (frame2_base-frame1_base)/(millis_diff/10)
            ears_increment = (frame2_ears-frame1_ears)/(millis_diff)

            new_m1 = frame1_m1
            new_m2 = frame1_m2
            new_m3 = frame1_m3
            new_base = frame1_base
            new_ears = frame1_ears
            new_millis = millis1/1

            # framed between 1 and 2
            millis_diff = int(abs(millis_diff)/10)
            for x in range(1, millis_diff+1):
                new_m1 += m1_increment
                new_m2 += m2_increment
                new_m3 += m3_increment
                new_base += base_increment
                new_ears += ears_increment
                new_millis += 10

                if new_millis > maxMillis:
                    break
                
                temp_list.append ({
                    'positions' : [
                        {
                            'dof': 'tower_1',
                            'pos': new_m1
                        },
                        {
                            'dof': 'tower_2',
                            'pos': new_m2
                        },
                        {
                            'dof': 'tower_3',
                            'pos': new_m3
                        },
                        {
                            'dof': 'base',
                            'pos': new_base
                        },
                        {
                            'dof': 'ears',
                            'pos': new_ears
                        }   
                    ],
                    'millis': new_millis
                })
            
            idx+=1

        frames_list.extend(temp_list)
        frames_list.sort(key=lambda x: x['millis'])


        with open(seqName + '_sequence.json','w') as seq_file:
            json.dump({'animation': seqName, 'frame_list': frames_list}, seq_file, indent=2)

        frames_list = []
        

def main():

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()