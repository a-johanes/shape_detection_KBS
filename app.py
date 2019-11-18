from cvProcessor import CVProcessor
import logging
import json

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s: %(message)s')

if __name__ == '__main__':
    print('Shape detection KBS')

    config = {}

    with open('config.json') as config_file:
        config = json.load(config_file)

    print(config)

    shape_list = CVProcessor.processImage('segitiga.png', config)
    for shape in shape_list:
        print(shape)