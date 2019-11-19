import logging
import re
import numpy as np
from typing import List
from cvProcessor import ShapeData
from itertools import combinations
from clips import Environment, Symbol


class CLIPS():
    def __init__(self, config):
        self.config = config
        self.is_shape_init = False
        self.env = Environment()
        with open(config['kbs_file']) as kbs_file:
            logging.getLogger('clips/load').info('Loading clips file {}'.format(config['kbs_file']))
            # self.env.build(kbs_file.read())
            self.env.load(config['kbs_file'])

    def setShape(self, shape_list):
        self.env.reset()
        self.is_shape_init = False
        self.shape_list = shape_list
        self.initShapeFact(self.shape_list)
        self.is_shape_init = True

    def processParallel(self, shape: ShapeData):
        logger = logging.getLogger('clips/parallel')

        logger.info('Processing shape with {} sides for parallel'.format(len(shape.side)))
        logger.debug('Slope epsilon: {}'.format(self.config['slope_eps']))

        side_combin = combinations(shape.side, 2)

        parallel_set = set()

        for side_pair in side_combin:
            if (np.isinf(side_pair[0][3]) and np.isinf(side_pair[1][3])):
                parallel_set.add((side_pair[0][0], side_pair[1][0]))
            if (np.abs(side_pair[0][3] - side_pair[1][3]) < self.config['slope_eps']):
                parallel_set.add((side_pair[0][0], side_pair[1][0]))

        logger.debug('Parallel result set {}'.format(parallel_set))
        return parallel_set

    def initShapeFact(self, shape_list: List[ShapeData]):
        logger = logging.getLogger('clips/fact-assert')
        for shape in shape_list[:1]:
            self.env.assert_string('(objek (sisi {}))'.format(len(shape.side)))

            for side in shape.side:
                side_fact = '(sisi (from {}) (to {}) (length {}))'.format(*side)
                logger.debug('Asserting {}'.format(side_fact))
                self.env.assert_string(side_fact)

            for point in shape.degree:
                degree_fact = '(sudut (id {}) (degree {}))'.format(*point)
                logger.debug('Asserting {}'.format(degree_fact))
                self.env.assert_string(degree_fact)

            parallel_set = self.processParallel(shape)

            parallel_count = len(parallel_set)
            parallel_fact = '(paralel (jumlah {}))'.format(parallel_count)

            logger.debug('Asserting {}'.format(parallel_fact))
            self.env.assert_string(parallel_fact)

    def getRules(self):
        text_output = []
        for rule in self.env.rules():
            text_output.append(str(rule))

        return '\n'.join(text_output)

    def getFacts(self):
        text_output = []
        for fact in self.env.facts():
            fact_string = str(fact)
            fact_string = re.sub('^(f-\d+\s+)', '', fact_string)
            text_output.append(fact_string)

        return '\n'.join(text_output)

    def isShapeLoaded(self):
        return self.is_shape_init
