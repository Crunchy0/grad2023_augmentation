import os
from fileio import load_from_dir, unload_audio
from transform import apply_transform


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


class SoundSet:
    def __init__(self, src_dir, dst_dir):
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.soundset_d = dict()
        dir_filter(src_dir)
        dir_filter(dst_dir)

    def transform_and_save(
            self,
            kword: str,
            types_l: list,
            sr=22050,
            transform=None,
            fname_mask: str = ".*",
            note: str = "",
            samples_n: int = 100000
    ):
        kword_dir_match_idx = None
        s_type_src_paths = []
        for s_type in types_l:
            s_type_src = os.path.join(self.src_dir, s_type)
            if s_type_src in s_type_src_paths:
                continue
            if not dir_present(s_type_src):
                print("Skipping sound type \"{t}\", no directory".format(t=s_type))
                continue
            if s_type == kword:
                kword_dir_match_idx = len(s_type_src_paths)
            s_type_src_paths.append(s_type_src)

        if not len(s_type_src_paths) > 0:
            print("No directory from types_l exists in {d}".format(d=self.src_dir))
            return False

        kw_dir_path = os.path.join(self.dst_dir, kword)
        if callable(transform):
            if self.src_dir == self.dst_dir and kword_dir_match_idx:
                print("Keyword matches the name of this directory: {s}".format(
                    s=s_type_src_paths[kword_dir_match_idx]
                ))
                return False
            if kword not in os.listdir(self.dst_dir):
                os.mkdir(kw_dir_path, 0o777)
            dir_filter(kw_dir_path)

        soundset_d = dict()
        if kword in self.soundset_d.keys():
            soundset_d = self.soundset_d[kword]
        for src_path in s_type_src_paths:
            s_type = os.path.split(src_path)[1]
            if not callable(transform):
                if not (s_type in soundset_d.keys()):
                    soundset_d[s_type] = src_path
                continue
            dst_path = os.path.join(kw_dir_path, s_type)
            if s_type not in os.listdir(kw_dir_path):
                os.mkdir(dst_path, 0o777)
            dir_filter(dst_path)

            fname_l, audio_l = load_from_dir(src_path, sr, fname_mask, samples_n)
            mod_audio_l = apply_transform(audio_l, transform)
            unload_audio(dst_path, fname_l, mod_audio_l, kword if note == "" else note)
            soundset_d[s_type] = dst_path

        self.soundset_d[kword] = soundset_d
        return True

    def get_path(self, kword, s_type):
        return self.soundset_d[kword][s_type]

    def list_paths(self, kword, types_l):
        return list(zip(types_l, (self.get_path(kword, s_type) for s_type in types_l)))

    def delete(self, kword, s_type=None):
        if s_type is None:
            del self.soundset_d[kword]
            return
        del self.soundset_d[kword][s_type]
