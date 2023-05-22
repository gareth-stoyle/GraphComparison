import sys
import os
import pytest
# Get the parent directory of the current file (tests directory)
# Add the preceeding dir to the Python path
sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}/../')
from graph import *


adj_list = {
    'France': [(200, 'Italy'), (400, 'Ireland')],
    'Italy': [(200, 'France'), (400, 'England')],
    'Ireland': [(400, 'France'), (100, 'England')],
    'England': []
}
graph = Graph(adj_list)

def test_add_vertex():
    assert graph.add_vertex('Z') == True

def test_add_edge():
    assert graph.add_edge('Z', 'Ireland', 100) == True

def test_dijkstra():
    assert graph.dijkstra('France', 'England') == [500, ['France', 'Ireland', 'England']]

def test_bellman_ford():
    assert graph.bellman_ford('France', 'England') == [500, ['France', 'Ireland', 'England']]
