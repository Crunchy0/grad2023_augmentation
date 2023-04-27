import fileio
from audiomentations import \
    AddGaussianNoise,\
    AddShortNoises,\
    AddBackgroundNoise,\
    Compose


def apply_transforms(source_list, transforms_queue=None):
    if (type(transforms_queue) is not list) or (len(transforms_queue) == 0):
        return source_list

    modified_list = []
    for samples, sr in source_list:
        new_samples = samples
        for transform in transforms_queue:
            if not callable(transform):
                continue
            new_samples = transform(new_samples, sr)
        modified_list.append((new_samples, sr))
    return modified_list


# Paths
source_dir = "./samples"
dest_dir = "./test"

file_mask = r".*"

# Audiomentations transforms
transformBG = AddBackgroundNoise(
    sounds_path="background",
    p=1.0,
    min_snr_in_db=-3.0,
    max_snr_in_db=3.0
)

transformSN = AddShortNoises(
    sounds_path="noises",
    min_time_between_sounds=0.5,
    max_time_between_sounds=1.0,
    min_snr_in_db=0.0,
    max_snr_in_db=5.0,
    noise_rms="absolute",
    p=1.0
)

transformGN = AddGaussianNoise(
    min_amplitude=0.003,
    max_amplitude=0.015,
    p=1.0
)

tf_list = [transformBG, transformSN, transformGN]

fname_l, audio_l = fileio.load_from_dir(source_dir, file_mask, 200)
mod_audio_l = apply_transforms(audio_l, [Compose(tf_list, p=1.0, shuffle=False)])
new_fname_l, new_audio_l = fileio.unload_audio(dest_dir, fname_l, mod_audio_l)
