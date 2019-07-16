import pandas as pd
import os
from cvrpGraph import cvrpGraph
from GraphAdjList import Graph


def readInstanceList(path):
    files = os.listdir(path)
    return files


def createGraph(files):

    g = cvrpGraph()
    for f in files:
        data = pd.read_csv('cvrp/'+f, sep="\n", header=None)
        i = 0
        for d in data[0]:
            line = d.split(':')
            if line[0] == "NAME":
                print((line[1]))
                g.setName(line[1].strip())
            if line[0] == "CAPACITY":
                print(int(line[1]))
                g.setCapacity(line[1].strip())
            if line[0] == "COMMENT":
                print((line[1]))
                g.setComment(line[1])
            if line[0] == "TYPE":
                if "CVRP" != line[1]:
                    print(
                        "Your input data are not suitable for this algo, please input a TSP format")
            if line[0] == "DIMENSION":
                dimension = int(line[1])
                print(dimension)
            if line[0] == "EDGE_WEIGHT_TYPE":
                w_type = (line[1]).strip()

            if line[0] == "EDGE_WEIGHT_FORMAT":
                w_format = (line[1]).strip()

            if line[0] == "NODE_COORD_TYPE":
                n_c_type = (line[1]).strip()

            if line[0] == "NODE_COORD_SECTION":
                if w_type == "EUC_2D":
                    print(w_type)
                    parse_euc2d(g, data, i+1)
                if w_type == "GEO":
                    print(w_type)
                    # arse_geo(g, tspfile)
            if line[0] == "EDGE_WEIGHT_SECTION":
                if w_type == "EXPLICIT":
                    print("cacca")
                    #parse_w_matrix(g, w_format, data)
            if line[0] == "EOF:":
                break
            i += 1


def parse_euc2d(graph, data, index):

    dimension = graph.getDimension()
    temp_vertex = [dimension] * dimension

    while len(data[0][index+1].split()) < 2:

        toSplit = data[0][index].split()
        index += 1

    #     words = deque(line.split())
    #     vertex_name = words.popleft()
    #     if vertex_name == str(i):
    #         x = float(words.popleft())
    #         y = float(words.popleft())
    #         temp_vertex[int(vertex_name)-1] = [x, y]
    #         i += 1
    #     else:
    #         break
    # # creating vertex
    # for i in range(dimension):
    #     p = temp_vertex[i]
    #     for j in range(dimension):
    #         if i != j:
    #             q = temp_vertex[j]
    #             dist = sqrt(((p[0] - q[0])**2) + (p[1] - q[1])**2)
    #             graph.add_edge(i, j, dist)


def parse_w_matrix(graph, format, data):

    print("debug")
    dimension = graph.getDimension()
    matrix_temp = []

    for d in data[0]:
        line = d.split()
        keyword = line[1]
        if keyword == "DEMAND_SECTION" or \
           keyword == "DISPLAY_DATA_SECTION":
            break
        row = [float(el) for el in line.split()]
        matrix_temp += row
    # matrix_temp = np.array(matrix_temp)
    # matrix = np.zeros((dimension, dimension))
    # if format == "FULL_MATRIX":
    #     matrix = matrix_temp.reshape((dimension, dimension))

    # elif format == "LOWER_DIAG_ROW":
    #     indices = np.tril_indices(dimension)
    #     matrix[indices] = matrix_temp

    # elif format == "UPPER_ROW":
    #     indices = np.triu_indices(dimension, 1)
    #     matrix[indices] = matrix_temp

    # for i in range(dimension):
    #     for j in range(dimension):
    #         graph.add_edge(i, j, float(matrix[i][j]))


def parse_geo(graph, tspfile):

    dimension = graph.get_dimension()
    # temp_vertex = [None] * dimension
    # i = 1
    # for line in tspfile:
    #     words = deque(line.split())
    #     vertex_name = words.popleft()
    #     if vertex_name == str(i):
    #         x = float(words.popleft())
    #         y = float(words.popleft())
    #         temp_vertex[int(vertex_name)-1] = [x, y]
    #         i += 1
    #     else:
    #         break
    # # creating vertex
    # for i in range(dimension):
    #     p = temp_vertex[i]
    #     deg = int(p[0])
    #     min = p[0] - deg
    #     latitude_p = pi * (deg + 0.5 * min / 0.3) / 180.0
    #     deg = int(p[1])
    #     min = p[1] - deg
    #     longitude_p = pi * (deg + 0.5 * min / 0.3) / 180.0
    #     for j in range(dimension):
    #         q = temp_vertex[j]
    #         deg = int(q[0])
    #         min = q[0] - deg
    #         latitude_q = pi * (deg + 0.5 * min / 0.3) / 180.0
    #         deg = int(q[1])
    #         min = q[1] - deg
    #         longitude_q = pi * (deg + 0.5 * min / 0.3) / 180.0

    #         RRR = 6378.388
    #         q1 = cos(longitude_p - longitude_q)
    #         q2 = cos(latitude_p - latitude_q)
    #         q3 = cos(latitude_p + latitude_q)
    #         dij = int(RRR * acos(0.5 * ((0.1 + q1) * q2 - (1.0 - q1) * q3)) +
    #                   1.0)
    #         graph.add_edge(i, j, dij)
