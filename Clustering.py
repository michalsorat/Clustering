from random import randint
import math
import matplotlib.pyplot as plt
import time
import copy

def generate_points(nr_of_points):
    map = []
    for i in range (20):
        point = []
        x = randint(-5000, 5000)
        y = randint(-5000, 5000)
        point.append(x)
        point.append(y)
        map.append(point)
    for i in range (nr_of_points):
        point = []
        x_offset = randint(-100, 100)
        y_offset = randint(-100, 100)
        point = map[randint(0,19)].copy()
        point[0] = point[0] + x_offset
        point[1] = point[1] + y_offset
        map.append(point)
    return map

def euclidean_dist(A,B):
    return math.sqrt(abs(A[0] - B[0])**2 + (abs(A[1] - B[1])**2))

def clustering(map, centers, k):
    clusters = [[] for i  in range(k)]

    average_dist = [0] * k
    x_total = [0] * k
    y_total = [0] * k
    for i in range(len(map)-1):
        smallest_dist = 1000000
        temp = 0
        for m in range(k):
            dist = euclidean_dist(map[i], centers[m])
            if (smallest_dist > dist):
                smallest_dist = dist
                temp = m
        x_total[temp] += map[i][0]
        y_total[temp] += map[i][1]
        average_dist[temp] += smallest_dist
        clusters[temp].append(map[i])

    for j in range(k):
        if (len(clusters[j]) != 0):
            average_dist[j] //= len(clusters[j])
    return clusters, average_dist, x_total, y_total

def display(clusters):
    dict_of_colors = {0: "orange", 1: "navy", 2: "black", 3: "blue",
                      4: "brown", 5: "chartreuse", 6: "crimson", 7: "darkgreen",
                      8: "fuchsia", 9: "gold", 10: "green", 11: "grey", 12: "magenta",
                      13: "azure", 14: "aqua", 15: "plum", 16: "navy", 17: "sienna",
                      18: "teal", 19: "violet"}
    for j, cluster in enumerate(clusters):
        for i in range(len(cluster)):
            plt.plot(cluster[i][0], cluster[i][1], ".", color = dict_of_colors[j])
        print(".", end = "")
    print()
    plt.show()

def generate_init_centers(map, k):
    centers = []
    for j in range(k):
        tmp = map[randint(0, len(map)-1)].copy()
        while(tmp in centers):
            tmp = map[randint(0, len(map)-1)].copy()
        centers.append(tmp)
    return centers

def is_end(centers, new_centers, average_dist, k):
    not_changed = 0
    not_far = 0
    iter = 0
    while(iter < k):
            if (centers[iter] == new_centers[iter]):
                not_changed += 1
            if (average_dist[iter] < 500):
                not_far += 1
            iter += 1
    if (not_changed == len(centers) or not_far == len(average_dist)):
        return True
    else:
        return False

def calc_centroids(clusters, k, x_total, y_total):
    new_centers = []
    for i in range(k):
        center = []
        if (len(clusters[i]) != 0):
            x = x_total[i] // len(clusters[i])
            y = y_total[i] // len(clusters[i])
            center.append(x)
            center.append(y)
        else:
            x = 10000
            y = 10000
            center.append(x)
            center.append(y)
        new_centers.append(center)
    return new_centers

def k_means(map, type):
    k = int(input("Enter K: "))
    start_time = time.time()
    centers = generate_init_centers(map, k).copy()
    clusters, average_dist, x_total, y_total = clustering(map, centers, k)
    iter_count = 0
    while(1):
        new_centers = calc_centroids(clusters, k, x_total, y_total)
        iter_count += 1
        if (type == "medoid"):
            medoids = [0] * k
            for i in range(k):
                smallest_dist = 1000000
                for point in clusters[i]:
                    dist = euclidean_dist(point, new_centers[i])
                    if (smallest_dist > dist):
                        smallest_dist = dist
                        medoids[i] = point
            new_centers = medoids.copy()

        if (is_end(centers, new_centers, average_dist, k)):
            break
        else:
            centers = new_centers.copy()
        clusters, average_dist, x_total, y_total = clustering(map, centers, k)

    print(f"Number of iterations done: {iter_count}")   
    #for dist in average_dist:
    #    print(f"{average_dist.index(dist)} : {dist}")
    average = 0
    for dist in average_dist:
        average += dist
    average //= len(average_dist)
    print(f"Average distance from centers is: {average}")
    print("--- %s seconds ---" % (time.time() - start_time))
    display(clusters)

def aglomerative_clustering(map):
    k = int(input("Enter K: "))
    init_k = len(map)
    #sizes = [[0 for x in range(len(map))] for y in range(len(map))] 
    centers = map.copy()
    clusters = [[] for i  in range(len(map))]
    for i, cluster in enumerate(clusters):
        cluster.append(map[i])

    #for i, center in enumerate(centers):
    #    for j, ctr in enumerate(centers):
    #        if (ctr != center):
    #            dist = euclidean_dist(ctr, center)
    #            sizes[i][j] = round(dist, 0)
    while(init_k != k):
        smallest_dist = 1000000
        for i, center in enumerate(centers):
            for j, ctr in enumerate(centers):
                if (ctr != center):
                    dist = euclidean_dist(ctr, center)
                    if (smallest_dist > dist):
                        center1 = ctr
                        center2 = center
                        smallest_dist = dist
        new_center = []
        x = (center1[0] + center2[0]) // 2
        y = (center1[1] + center2[1]) // 2
        new_center.append(x)
        new_center.append(y)
        #spoji dva klastre
        for point in clusters[centers.index(center2)]:
            clusters[centers.index(center1)].append(point)
        #spoji 2 centra
        centers[centers.index(center1)] = new_center.copy()
        #zmaze jeden z klastrov
        clusters.pop(centers.index(center2))
        #zmaze jeden z centier
        centers.pop(centers.index(center2))
        init_k -= 1
        print(".", end= "")
    display(clusters)

            

def main():
    map = []
    nr_of_points = int(input("Enter number of points on the map: "))
    map = generate_points(nr_of_points)
    while (1):
        x = int(input("K-means centroid (1)\nK-means medoid (2)\nAglomeratívne zhlukovanie centroid (3)\nEnd (4)\n\n"))
        if (x == 1):
            k_means(map, "centroid")
        elif (x == 2):
            k_means(map, "medoid")
        elif (x == 3):
            aglomerative_clustering(map)
        elif (x == 4):
            break
        else: break


if __name__ == "__main__":
    main()
