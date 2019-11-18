import logging
import numpy as np
from typing import List
from cvProcessor import ShapeData
from itertools import combinations
from clips import Environment, Symbol


class CLIPS():
    def __init__(self, config, shape_list):
        self.shape_list = shape_list
        self.config = config
        self.initShapeFact(self.shape_list)
        self.env = Environment()
        with open(config['kbs_file']) as kbs_file:
            logging.getLogger('clips/load').info('Loading clips file {}'.format(config['kbs_file']))
            # self.env.build(kbs_file.read())
            self.env.load(config['kbs_file'])

    def processParallel(self, shape: ShapeData):
        logger = logging.getLogger('clips/parallel')

        logger.info('Processing shape with {} sides for parallel'.format(len(shape.side)))
        logger.debug('Slope epsilon: {}'.format(self.config['slope_eps']))

        side_combin = combinations(shape.side, 2)

        parallel_set = set()

        for side_pair in side_combin:
            print(side_pair)
            if (np.isinf(side_pair[0][3]) and np.isinf(side_pair[1][3])):
                parallel_set.add((side_pair[0][0], side_pair[1][0]))
            if (np.abs(side_pair[0][3] - side_pair[1][3]) < self.config['slope_eps']):
                parallel_set.add((side_pair[0][0], side_pair[1][0]))

        logger.debug('Parallel result set {}'.format(parallel_set))
        return parallel_set

    def initShapeFact(self, shape_list: List[ShapeData]):
        for shape in shape_list:
            for point in shape.degree:
                # self.env.assert()
                pass
            self.processParallel(shape)

    def getRules(self):
        print(self.env.find_template('objek'))
        self.env.run()
        for rule in self.env.rules():
            print(type(rule))
            print(rule)
        print('b')
        return self.env.rules()
