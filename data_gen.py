import numpy as np
from soundset import SoundSet
from transform import apply_transform
import noise
import fileio
from audiomentations import \
    AddBackgroundNoise, \
    AddGaussianNoise, \
    AddShortNoises, \
    PitchShift, \
    RoomSimulator, \
    LowPassFilter, \
    HighPassFilter, \
    BandPassFilter, \
    Compose

# Transforms definition

reverb = RoomSimulator(
    min_size_x=2.0,
    max_size_x=4.0,
    min_size_y=2.0,
    max_size_y=4.0,
    min_size_z=2.0,
    max_size_z=3.0,
    min_source_x=1.0,
    max_source_x=3.0,
    min_source_y=1.0,
    max_source_y=3.0,
    min_source_z=0.5,
    max_source_z=2.5,
    min_mic_distance=0.2,
    max_mic_distance=3.0,
    min_mic_azimuth=-np.pi/3,
    max_mic_azimuth=np.pi/3,
    min_mic_elevation=-np.pi/6,
    max_mic_elevation=np.pi/6,
    min_absorption_value=0.025,
    max_absorption_value=0.1,
    leave_length_unchanged=False,
    #use_ray_tracing=False,
    max_order=6,
    p=1.0
)

# Noise generation
noise_dur = 10.0
noise_sr = 22050

noise_color_list = [
    "white",
    "blue",
    "purple",
    "brown",
    "pink"
]

noise_fname_l, noise_l = noise.generate_set(
    noise_dur,
    noise_sr,
    amp_l=[0.1, 0.2, 0.3, 0.4],
    col_l=noise_color_list
)
fileio.unload_audio("./bg_noises", noise_fname_l, noise_l)

bg_noise = AddBackgroundNoise(
    sounds_path="./bg_noises",
    min_snr_in_db=1.0,
    max_snr_in_db=15.0,
    p=1.0
)

gauss_noise = AddGaussianNoise(
    min_amplitude=0.005,
    max_amplitude=0.03,
    p=1.0
)

# Short sounds transform
ss = SoundSet("./noises", "./noises_test")
ss_dict = ss.transform_and_save("fan", ["clatter", "impact"], reverb)

sh_noises = Compose(
    [AddShortNoises(ss.get_path("fan", "impact"), p=1.0),
     AddShortNoises(ss.get_path("fan", "clatter"), p=1.0)],
    p=1.0
)

pshift = PitchShift(
    min_semitones=-4.0,
    max_semitones=2.0,
    p=1.0
)

lowpass = LowPassFilter(
    min_cutoff_freq=1000.0,
    max_cutoff_freq=4000.0,
    p=1.0
)

highpass = HighPassFilter(
    min_cutoff_freq=400.0,
    max_cutoff_freq=2500.0,
    p=1.0
)

bandpass = BandPassFilter(
    min_center_freq=400.0,
    max_center_freq=4000.0,
    min_bandwidth_fraction=0.1,
    max_bandwidth_fraction=1.5,
    p=1
)

composed_transform = Compose(
    [
        pshift,
        sh_noises,
        bg_noise
    ]
)

file_mask = r".*"
# Paths
source_dir = "../dev_data/fan/train"
dest_dir = "./test/fan_test"


fname_l, audio_l = fileio.load_from_dir(source_dir, file_mask, 100)
mod_audio_l = apply_transform(audio_l, composed_transform)
new_fname_l, new_audio_l = fileio.unload_audio(dest_dir, fname_l, mod_audio_l, "mod")
