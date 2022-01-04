import json

def save_clustering(file, ks, y_pred, std, mean):
    f = open(str(file)+".json", "a")
    clustering = {}
    clustering['number_of_clusters'] = len(ks.cluster_centers_)
    clustering['centroids'] = {}
    for i in range(len(ks.cluster_centers_)):
        clustering['centroids'][str(i)] = ks.cluster_centers_[i].ravel().tolist()
    clustering['clusters'] = y_pred.tolist()
    clustering['standard_deviation'] = std.tolist()
    clustering['mean'] = mean.tolist()
    f.write(json.dumps(clustering))
    f.close()

def load_file_to_json(file):
    f = open(str(file)+".json", "r")
    content = f.read()
    f.close()
    return json.loads(content)

def save_file_json(file, content):
    f = open(file+'.json', "a")
    f.write(json.dumps(content))
    f.close()