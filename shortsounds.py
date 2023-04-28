import os
import fileio


def apply_transform(source_list, transform):
    if not callable(transform):
        return source_list

    modified_list = []
    for samples, sr in source_list:
        modified_list.append((transform(samples, sr), sr))
    return modified_list


def dir_present(dir_name):
    return os.path.exists(dir_name) and os.path.isdir(dir_name)


def dir_filter(dir_name):
    if not os.path.exists(dir_name):
        raise FileNotFoundError(
            "File {name} does not exist".format(name=dir_name)
        )
    if not os.path.isdir(dir_name):
        raise NotADirectoryError(
            "File {name} is not a directory".format(name=dir_name)
        )


class ShortSounds:
    def __init__(self, src_dir, dst_dir):
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.soundset_d = dict()
        dir_filter(src_dir)
        dir_filter(dst_dir)

    def transform_and_save(self, kword, types_l, transform=None):
        s_type_src_paths = []
        for s_type in types_l:
            s_type_src = os.path.join(self.src_dir, s_type)
            if not dir_present(s_type_src):
                print("Skipping sound type \"{t}\", no directory".format(t=s_type))
                continue
            s_type_src_paths.append(s_type_src)

        if not len(s_type_src_paths) > 0:
            return False

        kw_dir_path = os.path.join(self.dst_dir, kword)
        if kword not in os.listdir(self.dst_dir):
            os.mkdir(kw_dir_path, 0o777)
        dir_filter(kw_dir_path)

        soundset_d = dict()
        for src_path in s_type_src_paths:
            s_type = os.path.split(src_path)[1]
            dst_path = os.path.join(kw_dir_path, s_type)
            if s_type not in os.listdir(kw_dir_path):
                os.mkdir(dst_path, 0o777)
            dir_filter(dst_path)

            fname_l, audio_l = fileio.load_from_dir(src_path)
            mod_audio_l = apply_transform(audio_l, transform)
            fileio.unload_audio(dst_path, fname_l, mod_audio_l, kword)
            soundset_d[s_type] = dst_path

        self.soundset_d[kword] = soundset_d
        return True

    def get_path(self, kword, s_type):
        return self.soundset_d[kword][s_type]
