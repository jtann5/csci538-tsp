from graph import EuclideanTSPGraph
import os

# directory to place dataset, basic name of tsp instances, number of nodes per instance, number of instances to generate, force generation
def generate_dataset(dir, base_name, nodes, num, force=False):
    os.makedirs(dir, exist_ok=True)
    temp = EuclideanTSPGraph()

    for i in range(num):
        name = base_name + str(i+1)
        filepath = dir + "/" + name + ".tsp"

        if not force and os.path.exists(filepath):
            print(f"File {filepath} already exists. Skipping generation.")
            continue

        temp.name = name
        temp.generate_random(nodes)
        temp.save_to_file(filepath)


if __name__ == "__main__":
    generate_dataset("tsp5", "tsp5-", 5, 20)
