def find_link_neighbors(link_id, xmlRoot):
    neighbors = []
    node1 = -1
    node2 = -1
    for link in xmlRoot.findall("./links/link"):
        if link_id == link.get('id'):
            node1 = link.get('from')
            node2 = link.get('to')
            break
    for link in xmlRoot.findall("./links/link"):
        if node1 == link.get('from') or node1 == link.get('to'):
            if not link.get('id') in neighbors:
                neighbors.append(link.get('id'))
    for link in xmlRoot.findall("./links/link"):
        if node2 == link.get('to') or node2 == link.get('from'):
            if not link.get('id') in neighbors:
                neighbors.append(link.get('id'))
    return neighbors

def get_links_indexs(neighbors, labels, labels_indexs):
    neighbor_indexs = []
    for neighbor in neighbors:
        for label in labels:
            if str(neighbor)+'-' in label:
                neighbor_indexs.append(labels_indexs[label])
                break
    return neighbor_indexs

def get_links_labels_indexs(neighbors, labels, labels_indexs):
    neighbor_labels = []
    neighbor_indexs = []
    for neighbor in neighbors:
        for label in labels:
            if str(neighbor)+'-' in label:
                neighbor_indexs.append(labels_indexs[label])
                neighbor_labels.append(neighbor)
                break
    return neighbors, neighbor_indexs

def add_trips(series_first_indexs, links_centroid, time_series_labels_first):
    trips_second_scenario = []
    trips_second_scenario_2 = []
    for i in series_first_indexs:
        links_centroid.append(time_series_labels_first[i])
        for j in vehicles_links_series_first[i]:
            a = j.split("_")
            if not j in trips_second_scenario_2:
                trips_second_scenario_2.append(j)
            if not a[0] in trips_second_scenario:
                trips_second_scenario.append(a[0])
    return trips_second_scenario, trips_second_scenario_2, links_centroid

def add_trips_labels(series_first_labels, links_centroid, time_series_labels_first):
    trips_second_scenario = []
    trips_second_scenario_2 = []
    for i in series_first_labels:
        if i in links_centroid:
            for k in links_centroid[i]:
                for j in k:
                    a = j.split("_")
                    if not j in trips_second_scenario_2:
                        trips_second_scenario_2.append(j)
                    if not a[0] in trips_second_scenario:
                        trips_second_scenario.append(a[0])
    return trips_second_scenario, trips_second_scenario_2, links_centroid

def get_links_ids_from_label(labels):
    links_ids = []
    for label in labels:
        link_id = label.split('-')[0]
        if not link_id in links_ids:
            links_ids.append(label.split('-')[0])
    return links_ids

def add_to_list(a, b):
    for e in b:
        if not e in a:
            a.append(e)
    return a

def add_trips_from_level(centroids_first_indexs, xmlRoot, time_series_labels_first, time_series_labels_first_dict, level):
    trips_second_scenario = []
    trips_second_scenario_2 = []
    links_centroid = []
    trips_second_scenario, trips_second_scenario_2, links_centroid = add_trips(centroids_first_indexs, links_centroid, time_series_labels_first)
    i = 0
    aux_search = get_links_ids_from_label(links_centroid)
    useds = []
    while len(aux_search) > 0:
        print("Level:", i)
        aux_search_2 = []
        print("Aux search: ", len(aux_search))
        while len(aux_search) > 0:
            link = aux_search.pop()
            if not link in useds:
                neighbor_labels, neighbor_indexs =  get_links_labels_indexs(find_link_neighbors(link, xmlRoot), time_series_labels_first, time_series_labels_first_dict)
                a, b, links_centroid = add_trips(neighbor_indexs, links_centroid, time_series_labels_first)
                trips_second_scenario = add_to_list(trips_second_scenario, a)
                trips_second_scenario_2 = add_to_list(trips_second_scenario_2, b)
                aux_search_2.extend(neighbor_labels)
                useds.append(link)
        aux_search = aux_search_2
        i = i + 1
    print(len(useds), len(xmlRoot.findall("./links/link")), len(useds) == len(xmlRoot.findall("./links/link")))
    return trips_second_scenario, trips_second_scenario_2

def add_trips_from_level_2(centroids_first_indexs, xmlRoot, time_series_labels_first, vehicles_links_series_first_dict, time_series_labels_first_dict, percentage, tripsAmount):
    trips_second_scenario = []
    trips_second_scenario_2 = []
    links_centroid = []
    trips_second_scenario, trips_second_scenario_2, links_centroid = add_trips(centroids_first_indexs, links_centroid, time_series_labels_first)
    i = 0
    aux_search = get_links_ids_from_label(links_centroid)
    useds = []
    while ((len(trips_second_scenario) / tripsAmount) * 100) < percentage:
        print("Size:", len(trips_second_scenario))
        print("Percentage:", ((len(trips_second_scenario) / tripsAmount) * 100), "%")
        aux_search_2 = []
        while len(aux_search) > 0:
            print("entrou")
            link = aux_search.pop()
            if not link in useds:
                neighbor_labels, neighbor_indexs =  get_links_labels_indexs(find_link_neighbors(link, xmlRoot), time_series_labels_first, time_series_labels_first_dict)
                print(neighbor_labels, neighbor_indexs)
                #print("neighbor_indexs", link, len(neighbor_indexs), neighbor_indexs)
                a, b, links_centroid = add_trips_labels(neighbor_indexs, vehicles_links_series_first_dict, time_series_labels_first)
                print(a)
                trips_second_scenario = add_to_list(trips_second_scenario, a)
                trips_second_scenario_2 = add_to_list(trips_second_scenario_2, b)
                aux_search_2.extend(neighbor_labels)
                useds.append(link)
        aux_search = aux_search_2
        i = i + 1
    print(len(useds), len(xmlRoot.findall("./links/link")), len(useds) == len(xmlRoot.findall("./links/link")))
    return trips_second_scenario, trips_second_scenario_2

