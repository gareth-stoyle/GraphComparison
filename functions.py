### miscellaneous functions ###
from flask import request
import time
import threading

def get_adj_list(form):
    adj_list = {}
    for i in range(int(len(form)/3)):
        edge_list = request.form.getlist('edge{}'.format(i+1))
        weight_list = request.form.getlist('weight{}'.format(i+1))
        vertex = request.form['vertex{}'.format(i+1)]
        # Zip the edges and weights together as tuples
        result = list(zip(weight_list, edge_list))
        # Filter out empty tuples
        cleaned_result = [(int(weight), edge) for weight, edge in result if weight]
        adj_list[vertex] = cleaned_result
    return adj_list

def compare_graphs(graph, source, target):
    t = time.time()
    start = time.time()
    for _ in range(1000000):
        x = graph.dijkstra(source, target)
    dijkstra_time = time.time() - start

    start = time.time()
    for _ in range(1000000):
        x = graph.bellman_ford(source, target)
    bellman_time = time.time() - start
    
    return (dijkstra_time, bellman_time)