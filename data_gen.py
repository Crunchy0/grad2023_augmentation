from soundset import SoundSet
import transforms.fan
import transforms.gearbox
import transforms.pump
import transforms.slider
import transforms.valve
import transforms.ToyCar
import transforms.ToyTrain

tr_l_fan = transforms.fan.get_tf_list()
tr_l_gearbox = transforms.gearbox.get_tf_list()
tr_l_pump = transforms.pump.get_tf_list()
tr_l_slider = transforms.slider.get_tf_list()
tr_l_valve = transforms.valve.get_tf_list()
tr_l_ToyCar = transforms.ToyCar.get_tf_list()
tr_l_ToyTrain = transforms.ToyTrain.get_tf_list()

dataset = SoundSet("./datasets/source", "./datasets")
for i in range(len(tr_l_fan)):
    dataset.transform_and_save(
        "augmented",
        ["fan"],
        sr=16000,
        transform=tr_l_fan[i],
        note="tr{i}".format(i=i),
        samples_n=1
    )

for i in range(len(tr_l_gearbox)):
    dataset.transform_and_save(
        "augmented",
        ["gearbox"],
        sr=16000,
        transform=tr_l_gearbox[i],
        note="tr{i}".format(i=i),
        samples_n=1
    )

for i in range(len(tr_l_pump)):
    dataset.transform_and_save(
        "augmented",
        ["pump"],
        sr=16000,
        transform=tr_l_pump[i],
        note="tr{i}".format(i=i),
        samples_n=1
    )

for i in range(len(tr_l_slider)):
    dataset.transform_and_save(
        "augmented",
        ["slider"],
        sr=16000,
        transform=tr_l_slider[i],
        note="tr{i}".format(i=i),
        samples_n=1
    )

for i in range(len(tr_l_valve)):
    dataset.transform_and_save(
        "augmented",
        ["valve"],
        sr=16000,
        transform=tr_l_valve[i],
        note="tr{i}".format(i=i),
        samples_n=1
    )

for i in range(len(tr_l_ToyCar)):
    dataset.transform_and_save(
        "augmented",
        ["ToyCar"],
        sr=16000,
        transform=tr_l_ToyCar[i],
        note="tr{i}".format(i=i),
        samples_n=1
    )

for i in range(len(tr_l_ToyTrain)):
    dataset.transform_and_save(
        "augmented",
        ["ToyTrain"],
        sr=16000,
        transform=tr_l_ToyTrain[i],
        note="tr{i}".format(i=i),
        samples_n=1
    )

