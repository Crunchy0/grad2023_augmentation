import os
from re import fullmatch

mtype_l=[
    "fan",
    "gearbox",
    "pump",
    "slider",
    "valve",
    "ToyCar",
    "ToyTrain"
]

res_dir = "../dcase2021_task2_baseline_ae/result"
results = os.listdir(res_dir)
res_count_l = []
for mtype in mtype_l:
    anomalies_count = 0
    overall_count = 0
    mtype_res_l = list(filter(lambda r: fullmatch(repr("decision_result_" + mtype + ".*")[1:-1], r), results))
    for res in mtype_res_l:
        full_path = os.path.join(res_dir, res)
        file = open(full_path, 'r')
        lines = file.readlines()
        for line in lines:
            if line.split(",")[1][0] == "1":
                anomalies_count += 1
        overall_count += len(lines)
        file.close()
    percent = (anomalies_count/overall_count) * 100
    res_count_l.append(mtype + " : " + str(anomalies_count) + "/" + str(overall_count) + " | " + str(percent) + "%\n")

res_count_f = open("./results.txt", 'w')
res_count_f.writelines(res_count_l)
res_count_f.close()
