import logging
import re
import numpy as np
from typing import List, Dict, Set, Tuple
from cvProcessor import ShapeData
from itertools import combinations
from clips import Environment, Symbol
from dataclasses import dataclass


@dataclass
class CLIPSResult():
    hit_rule: Set[str]
    fact_out: Set[str]


class CLIPS():
    def __init__(self, config: Dict) -> None:
        self.config = config
        self.is_shape_init = False
        self.static_env = Environment()
        self.env = []
        self.shape_fact = ''
        self.run_result = []
        logging.getLogger('clips/load').info('Loading clips file {}'.format(config['kbs_file']))
        self.static_env.load(config['kbs_file'])

    def setShape(self, shape_list: List[ShapeData]) -> None:
        self.is_shape_init = False
        self.shape_list = shape_list
        self.env = [Environment() for _ in range(len(shape_list))]
        for idx, shape in enumerate(shape_list):
            logging.getLogger('clips/load').debug('Init new shape')
            self.env[idx].load(self.config['kbs_file'])
            self.env[idx].reset()
            self.initShapeFact(shape, self.env[idx])
        self.is_shape_init = True
        self.shape_fact = self.genFacts()

    def processParallel(self, shape: ShapeData) -> Set[Tuple[int, int]]:
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

    def initShapeFact(self, shape: ShapeData, env: Environment) -> None:
        logger = logging.getLogger('clips/fact-assert')
        env.assert_string('(objek (sisi {}))'.format(len(shape.side)))

        for side in shape.side:
            side_fact = '(sisi (from {}) (to {}) (length {}))'.format(*side)
            logger.debug('Asserting {}'.format(side_fact))
            env.assert_string(side_fact)

        for point in shape.degree:
            degree_fact = '(sudut (id {}) (degree {}))'.format(*point)
            logger.debug('Asserting {}'.format(degree_fact))
            env.assert_string(degree_fact)

        parallel_set = self.processParallel(shape)

        parallel_count = len(parallel_set)
        parallel_fact = '(paralel (jumlah {}))'.format(parallel_count)

        logger.debug('Asserting {}'.format(parallel_fact))
        env.assert_string(parallel_fact)

    def factNormalizer(self, fact: str) -> str:
        return re.sub('^(f-\d+\s+)', '', fact)

    def filterFact(self, fact: str, key: str) -> str:
        match = re.match('^\({} "([a-z- ]+)"\)$'.format(key), fact)
        if match is not None:
            return match.groups()[0]
        else:
            return None

    def getRules(self) -> str:
        text_output = []
        for rule in self.static_env.rules():
            text_output.append(str(rule))

        return '\n'.join(text_output)

    def run(self) -> List[CLIPSResult]:
        logger = logging.getLogger('clips/run')
        logger.info('Running clips for all shape')
        self.run_result = []
        for env in self.env:
            logger.debug('Checking env')
            env.run()
            temp_rule_hit = set()
            temp_fact_out = set()
            for fact in env.facts():
                fact_string = self.factNormalizer(str(fact))
                logger.debug('Checking fact {}'.format(fact_string))

                rule_hit_match = self.filterFact(fact_string, 'hit-rule')
                if rule_hit_match is not None:
                    temp_rule_hit.add(rule_hit_match)

                bentuk_match = self.filterFact(fact_string, 'bentuk')
                if bentuk_match is not None:
                    logger.debug('Found bentuk {}'.format(bentuk_match))
                    temp_fact_out.add(bentuk_match)

                atribut_match = self.filterFact(fact_string, 'atribut')
                if atribut_match is not None:
                    logger.debug('Found atribut {}'.format(atribut_match))
                    temp_fact_out.add(atribut_match)

            self.run_result.append(CLIPSResult(temp_rule_hit, temp_fact_out))
            logger.debug('Hit rules: {}'.format(temp_rule_hit))

        return self.run_result

    def reset(self) -> None:
        for env in self.env:
            env.reset()

    def genFacts(self) -> str:
        text_output = []
        for idx, env in enumerate(self.env):
            text_output.append('')
            text_output.append('Shape {}'.format(idx))
            text_output.append('')

            for fact in env.facts():
                fact_string = self.factNormalizer(str(fact))
                text_output.append(fact_string)

        return '\n'.join(text_output)

    def getFacts(self) -> str:
        return self.shape_fact

    def isShapeLoaded(self) -> bool:
        return self.is_shape_init
