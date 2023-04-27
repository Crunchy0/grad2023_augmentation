import os
from re import fullmatch
from numpy.random import randint
from librosa import load
from soundfile import write as sf_write


def load_from_dir(dir_name, mask=r".*", samples_needed=100000):
    try:
        dir_files = os.listdir(dir_name)
    except FileNotFoundError:
        return None
    dir_files = list(filter(lambda x: os.path.isfile(os.path.join(dir_name, x)), dir_files))
    dir_files = list(filter(lambda x: fullmatch(mask, x), dir_files))

    fname_list = []
    while samples_needed > 0:
        if not len(dir_files) > 0:
            break
        file_name = dir_files.pop(randint(0, len(dir_files)))
        file_name = os.path.join(dir_name, file_name)
        fname_list.append(file_name)
        samples_needed -= 1
    return fname_list, [load(file) for file in fname_list]


def unload_audio(dir_name, fname_list, audio_list, note="mod"):
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

        sf_write(new_fname, samples, sr)

    return new_fname_list, audio_list
