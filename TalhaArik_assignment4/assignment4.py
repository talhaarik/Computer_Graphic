# CENG 487 Assignment by Talha Arık
# 270201060
# 01/2022

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import sys

def center_point(p1, p2):
    return [(p1[i]+p2[i])/2 for i in range(3)]

def sum_point(p1, p2):
    return [p1[i]+p2[i] for i in range(3)]

def div_point(p, d):
    return [p[i]/d for i in range(3)]

def mul_point(p, m):
    return [p[i]*m for i in range(3)]

def get_face_points(input_points, input_faces):
    face_points = []
    for curr_face in input_faces:
        face_points.append(np.mean(input_points[curr_face], axis=0))
    return face_points

def get_edges_faces(input_points, input_faces):
    edges = []
    for facenum, face in enumerate(input_faces):
        num_points = len(face)
        for pointindex in range(num_points):
            pointnum_1, pointnum_2 = face[pointindex], face[(pointindex + 1) % num_points]
            if pointnum_1 > pointnum_2:
                pointnum_1, pointnum_2 = pointnum_2, pointnum_1
            edges.append([pointnum_1, pointnum_2, facenum])

    edges = sorted(edges)

    merged_edges = []
    for i in range(len(edges) - 1):
        e1, e2 = edges[i], edges[i + 1]
        if e1[0] == e2[0] and e1[1] == e2[1]:
            merged_edges.append([e1[0], e1[1], e1[2], e2[2]])
            i += 1
        else:
            merged_edges.append([e1[0], e1[1], e1[2], None])
    else:
        merged_edges.append([edges[-1][0], edges[-1][1], edges[-1][2], None])

    edges_centers = []
    for me in merged_edges:
        p1 = input_points[me[0]]
        p2 = input_points[me[1]]
        cp = center_point(p1, p2)
        edges_centers.append(me + [cp])

    return edges_centers

def get_edge_points(input_points, edges_faces, face_points):
    edge_points = []
    for edge in edges_faces:
        cp = edge[4]
        fp1 = face_points[edge[2]]
        fp2 = face_points[edge[3]] if edge[3] is not None else fp1
        cfp = center_point(fp1, fp2)
        edge_point = center_point(cp, cfp)
        edge_points.append(edge_point)
    return edge_points

def get_avg_face_points(input_points, input_faces, face_points):
    avg_face_points = [[0.0, 0.0, 0.0] for _ in range(len(input_points))]
    point_counts = [0 for _ in range(len(input_points))]
    for facenum, face in enumerate(input_faces):
        fp = face_points[facenum]
        for pointnum in face:
            avg_face_points[pointnum] = [sum(x) for x in zip(avg_face_points[pointnum], fp)]
            point_counts[pointnum] += 1
    avg_face_points = [[point[0]/point_counts[i], point[1]/point_counts[i], point[2]/point_counts[i]] for i,point in enumerate(avg_face_points)]
    return avg_face_points


def get_avg_mid_edges_and_points_faces(input_points, edges_faces, input_faces):
    num_points = len(input_points)

    temp_points = [[0.0, 0.0, 0.0] for _ in range(num_points)]
    points_faces = [0 for _ in range(num_points)]

    for edge in edges_faces:
        cp = edge[4]
        for pointnum in [edge[0], edge[1]]:
            temp_points[pointnum] = [sum(x) for x in zip(temp_points[pointnum], cp)]
            points_faces[pointnum] += 1

    avg_mid_edges = [list(map(lambda x: x / points_faces[i], temp_points[i])) for i in range(num_points)]
    return avg_mid_edges, points_faces


def get_new_points(input_points, avg_face_points, avg_mid_edges):
    new_points = []
    n = len(input_points)
    m1 = [ (n - 3.0) / n for _ in range(n)]
    m2 = [ 1.0 / n for _ in range(n)]
    m3 = [ 2.0 / n for _ in range(n)]

    for pointnum in range(n):
        old_coords = input_points[pointnum]
        p1 = [a * b for a,b in zip(old_coords,m1[pointnum])]
        afp = avg_face_points[pointnum]
        p2 = [a * b for a,b in zip(afp,m2[pointnum])]
        ame = avg_mid_edges[pointnum]
        p3 = [a * b for a,b in zip(ame,m3[pointnum])]
        p4 = [sum(x) for x in zip(p1, p2)]
        new_coords = [sum(x) for x in zip(p4, p3)]
        new_points.append(new_coords)
    return new_points


def cmc_subdiv(input_points, input_faces):
    face_points = get_face_points(input_points, input_faces)
    edges_faces = get_edges_faces(input_points, input_faces)
    edge_points = get_edge_points(input_points, edges_faces, face_points)
    avg_face_points = get_avg_face_points(input_points, input_faces, face_points)
    avg_mid_edges = get_avg_mid_edges_and_points_faces(input_points, edges_faces)
    new_points = get_new_points(input_points, avg_face_points, avg_mid_edges)
    new_points += face_points + edge_points

    # create a dictionary to map old point indices to new point indices
    point_map = {i: i for i in range(len(input_points))}
    for i in range(len(input_points), len(new_points)):
        point_map[i] = i

    # create a dictionary to map edge indices to new edge point indices
    edge_map = {(a, b): i + len(input_points) for i, (a, b, _, _, _) in enumerate(edges_faces)}

    new_faces = []
    for face in input_faces:
        n = len(face)
        if n == 3:
            a, b, c = face
            new_faces.append((a, edge_map[(a, b)], edge_map[(c, a)], point_map[c + len(input_points)]))
            new_faces.append((b, edge_map[(b, c)], edge_map[(a, b)], point_map[a + len(input_points)]))
            new_faces.append((c, edge_map[(c, a)], edge_map[(b, c)], point_map[b + len(input_points)]))
        elif n == 4:
            a, b, c, d = face
            new_faces.append((a, edge_map[(a, b)], point_map[face.index(a) + len(input_points)], edge_map[(d, a)]))
            new_faces.append((b, edge_map[(b, c)], point_map[face.index(a) + len(input_points)], edge_map[(a, b)]))
            new_faces.append((c, edge_map[(c, d)], point_map[face.index(a) + len(input_points)], edge_map[(b, c)]))
            new_faces.append((d, edge_map[(d, a)], point_map[face.index(a) + len(input_points)], edge_map[(c, d)]))
    return new_points, new_faces


def graph_output(output_points, output_faces):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for facenum in range(len(output_faces)):
        curr_face = output_faces[facenum]
        xcurr = []
        ycurr = []
        zcurr = []
        for pointnum in range(len(curr_face)):
            xcurr.append(output_points[curr_face[pointnum]][0])
            ycurr.append(output_points[curr_face[pointnum]][1])
            zcurr.append(output_points[curr_face[pointnum]][2])
        xcurr.append(output_points[curr_face[0]][0])
        ycurr.append(output_points[curr_face[0]][1])
        zcurr.append(output_points[curr_face[0]][2])
        ax.plot(xcurr, ycurr, zcurr, color='b')
    plt.show()

# cube
input_points = [
    [-1.0, 1.0, 1.0],
    [-1.0, -1.0, 1.0],
    [1.0, -1.0, 1.0],
    [1.0, 1.0, 1.0],
    [1.0, -1.0, -1.0],
    [1.0, 1.0, -1.0],
    [-1.0, -1.0, -1.0],
    [-1.0, 1.0, -1.0]
]

input_faces = [
    [0, 1, 2, 3],
    [3, 2, 4, 5],
    [5, 4, 6, 7],
    [7, 0, 3, 5],
    [7, 6, 1, 0],
    [6, 1, 2, 4],
]

iterations = 4
output_points, output_faces = input_points, input_faces

for i in range(iterations):
    output_points, output_faces = cmc_subdiv(output_points, output_faces)

graph_output(output_points, output_faces)


