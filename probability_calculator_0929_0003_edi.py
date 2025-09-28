# 代码生成时间: 2025-09-29 00:03:30
from math import factorial
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest
import numpy as np

# Probability Distribution Calculator class
class ProbabilityDistributionCalculator:
    def __init__(self, data):
        """
        Initializes the Probability Distribution Calculator with data.
        :param data: A list of numbers representing the distribution data.
        """
        self.data = data
        self.mean = np.mean(data)
        self.std_dev = np.std(data)
        self.variance = np.var(data)

    def probability_density(self, x):
        "