import cv2
import os
import logging
import json
import numpy as np
from typing import Dict
from matplotlib import pyplot
from dataclasses import dataclass
from typing import List, Tuple


@dataclass()
class ShapeData():
    vertex: List[Tuple[int, int, int]]  # id, x, y
    degree: List[Tuple[int, int]]  # id, deg
    side: List[Tuple[int, int, int, float]]  # id_from, id_to, length, gradien


class CVProcessor():
    @staticmethod
    def processImage(filename: str, config: Dict) -> List[ShapeData]:
        logger = logging.getLogger('opencv')

        if not os.path.isfile(filename):
            logger.error('{} is not a file'.format(filename))
            raise Exception('{} is not a file'.format(filename))

        img_mat = cv2.imread(filename)

        if img_mat is None:
            logger.error('{} is not an image file'.format(filename))
            raise Exception('{} is not an image file'.format(filename))

        logger.info('Loaded image with h:{} w:{} c:{}'.format(*img_mat.shape))
        logger.debug(
            'Thresholding image with min: {} and max: {}'.format(
                config['threshold']['min'], config['threshold']['max']
            )
        )

        gray_mat = cv2.cvtColor(img_mat, cv2.COLOR_BGR2GRAY)
        _, threshold_mat = cv2.threshold(
            gray_mat, config['threshold']['min'], config['threshold']['max'], cv2.THRESH_BINARY
        )

        cv2.imshow('gray', gray_mat)
        cv2.waitKey(0)

        cv2.imshow('thres', threshold_mat)
        cv2.waitKey(0)

        contours, _ = cv2.findContours(threshold_mat, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        logger.info('Detected {} shapes'.format(len(contours)))

        cv2.drawContours(img_mat, contours, -1, (0, 255, 0), -1)

        cv2.imshow('contours', img_mat)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        shape_list = []

        logger.debug('Approx poly with eps: {}'.format(config['approx_eps']))

        contours = [
            cv2.approxPolyDP(cnt, config['approx_eps'] * cv2.arcLength(cnt, True), True)
            for cnt in contours
        ]

        logger.debug('Allowing shape with <= {} contours'.format(config['max_contour']))

        for cnt in filter(lambda x: len(x) <= config['max_contour'], contours):
            logger.info('Processing shape with {} element'.format(len(cnt)))
            vertex_np = [np.array([point[0][0], point[0][1]]) for point in cnt]
            vertex = [(idx, point[0], point[1]) for idx, point in enumerate(vertex_np)]
            print(vertex)

            degree = []
            side = []
            for i in range(len(vertex)):
                prev_index = (len(vertex) - 1) if (i - 1 < 0) else (i - 1)
                next_index = 0 if (i + 1 == len(vertex)) else i + 1

                test_point = vertex_np[i]
                prev_point = vertex_np[prev_index]
                next_point = vertex_np[next_index]

                veca = prev_point - test_point
                vecb = next_point - test_point

                cosine_angle = np.dot(veca, vecb) / (np.linalg.norm(veca) * np.linalg.norm(vecb))
                angle = np.degrees(np.arccos(cosine_angle))
                degree.append((i, round(angle, config['degree_approx'])))

                vecside = test_point - next_point
                length = np.linalg.norm(vecside)

                slope = vecside[1] / vecside[0]

                side.append((i, next_index, round(length, config['length_approx']), slope))

            shape_list.append(ShapeData(vertex, degree, side))

        logger.info('{} shape pass len check'.format(len(shape_list)))

        return shape_list
