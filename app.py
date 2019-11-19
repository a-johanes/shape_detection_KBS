from cvProcessor import CVProcessor
import logging
import json
from gui import GUI
import wx

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(name)s: %(message)s')

if __name__ == '__main__':
    print('Shape detection KBS')

    config = {}

    with open('config.json') as config_file:
        config = json.load(config_file)

    with open(config['shape_file']) as shape_file:
        config['shape'] = json.load(shape_file)

    print(config)

    app = wx.App()
    frm = GUI(None, config)

    frm.Show()

    app.MainLoop()