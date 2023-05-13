import numpy as np
from soundset import SoundSet
from audiomentations import \
    AddBackgroundNoise, \
    AddShortNoises, \
    PitchShift, \
    RoomSimulator, \
    LowPassFilter, \
    Compose

tf_list = []


def generate_tf_list():
    # Background noises transforms
    noise_color_list = [
        "brown",
    ]
    ss_noise = SoundSet("./bg_noises", "./bg_noises")
    ss_noise.transform_and_save("source", noise_color_list, sr=16000)

    bg_noise_brown = AddBackgroundNoise(
        sounds_path=ss_noise.get_path("source", "brown"),
        min_snr_in_db=1.0,
        max_snr_in_db=5.0,
        p=1.0
    )


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
        min_mic_azimuth=-np.pi / 3,
        max_mic_azimuth=np.pi / 3,
        min_mic_elevation=-np.pi / 6,
        max_mic_elevation=np.pi / 6,
        min_absorption_value=0.025,
        max_absorption_value=0.1,
        leave_length_unchanged=False,
        max_order=6,
        p=1.0
    )

    # Short sounds transform
    types_l = ["scramble", "impact"]
    ss_sn = SoundSet("./noises/original", "./noises")
    ss_sn.transform_and_save("reverbed", types_l, 44100, reverb)

    scramble_ns = AddShortNoises(
        sounds_path=ss_sn.get_path("reverbed", "scramble"),
        min_snr_in_db=-5.0,
        max_snr_in_db=10.0,
        min_time_between_sounds=5.0,
        max_time_between_sounds=8.0,
        p=1.0
    )

    impact_ns = AddShortNoises(
        sounds_path=ss_sn.get_path("reverbed", "impact"),
        p=1.0
    )

    pshift = PitchShift(
        min_semitones=-3.0,
        max_semitones=0.0,
        p=1.0
    )

    lowpass = LowPassFilter(
        min_cutoff_freq=4000.0,
        max_cutoff_freq=6000.0,
        p=1.0
    )

    tf_list.append(
        Compose(
            [
                scramble_ns,
                pshift
            ],
            p=1.0
        )
    )

    tf_list.append(
        Compose(
            [
                impact_ns,
                bg_noise_brown,
                lowpass
            ],
            p=1.0
        )
    )


def get_tf_list():
    generate_tf_list()
    return tf_list
