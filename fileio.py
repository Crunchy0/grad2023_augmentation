import os
from random import sample
from re import fullmatch
from librosa import load
from soundfile import write


def load_from_dir(dir_name, sr=22050, mask=".*", samples_needed=100000):
    dir_files = os.listdir(dir_name)
    dir_files = list(filter(lambda x: os.path.isfile(os.path.join(dir_name, x)), dir_files))
    dir_files = list(filter(lambda x: fullmatch(repr(mask)[1:-1], x), dir_files))
    samples_n = min(samples_needed, len(dir_files))
    fname_list = [os.path.join(dir_name, file_name) for file_name in sample(dir_files, samples_n)]
    return fname_list, [load(file, sr=sr) for file in fname_list]


def unload_audio(dir_name, fname_list, audio_list, note=""):
    if len(fname_list) != len(audio_list):
        raise RuntimeError("File names cannot be assigned to the resulting audio")

    if not os.path.exists(dir_name) or not os.path.isdir(dir_name):
        os.mkdir(dir_name, mode=0o777)

    sep = '.'
    new_fname_list = []
    for idx in range(len(audio_list)):
        samples, sr = audio_list[idx]
        dir_name_old, fname = os.path.split(fname_list[idx])

        fname_sep = fname.split(sep)
        fname_sep[0] = fname_sep[0] + "_" + note
        fname = sep.join(fname_sep)
        new_fname = os.path.join(dir_name, fname)
        new_fname_list.append(new_fname)

        write(new_fname, samples, sr)

    return new_fname_list, audio_list
