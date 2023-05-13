import noise

# Noise generation
noise_dur = 10.0
noise_sr = 16000

noise_color_list = [
    "white",
    "blue",
    "purple",
    "brown",
    "pink"
]

noise.generate_set(
    "./bg_noises",
    noise_dur,
    noise_sr,
    amp_l=[0.1, 0.2, 0.3, 0.4],
    col_l=noise_color_list
)
