import json
import sys
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# import time
# import sys
# print(time.strftime("%Y-%m-%d", time.localtime())
#
# def visualizeData(self):
#     self.sub_win.show()
#
#
# def subWinFunc(self):
#     while True:
#         time.sleep(0.2)
#         if self.sub_data != '':
#             self.subWinSignal.emit(self.sub_data)
#
#         self.lookVisualDataButton.clicked.connect(self.visualizeData)
# 		self.sub_data = ''
# 		self.subWinSignal.connect(lambda log2: self.sub_win.getData(log2))
# 		self.subWinThread = threading.Thread(target=self.subWinFunc, daemon=True)
# 		self.subWinThread.start()

js ={"haha":11,"qwe":12}
temp = str(js)
print(temp+'\n')
print(eval(temp))