import numpy as np

import fileio

noise_color = {
    'white': lambda f: 1,
    'blue': lambda f: np.sqrt(f),
    'purple': lambda f: f,
    'brown': lambda f: 1/np.where(f == 0, float('inf'), f),
    'pink': lambda f: 1/np.where(f == 0, float('inf'), np.sqrt(f))
}


def col_psd(color='white'):
    if color in noise_color.keys():
        return noise_color[color]
    raise KeyError("No noise matching color \"{c}\"".format(c=color))


def generate(n_samples, psd=col_psd(), amplitude=0.5, normalize=True):
    white_noise_signal = np.random.randn(n_samples)
    white_noise_spectrum = np.fft.rfft(white_noise_signal)

    psd_filter = psd(np.fft.rfftfreq(n_samples))
    #if normalize:
    #    psd_filter /= np.sqrt(np.mean(psd_filter ** 2))

    filtered_spectrum = white_noise_spectrum * psd_filter
    filtered_signal = np.fft.irfft(filtered_spectrum)

    if normalize:
        filtered_signal -= np.mean(filtered_signal)
        filtered_signal /= np.std(filtered_signal)

    return amplitude * filtered_signal


def supplement_fname(prefix, amp):
    return prefix + "_noise_amp_" + "_".join(str(amp).split('.')) + ".wav"


def generate_set(dir_name, duration, sample_rate, amp_l=None, col_l=None, psd_l=None):
    psd_list = None
    fname_prefix_l = None
    if type(col_l) is list and len(col_l) > 0:
        psd_list = [col_psd(col) for col in col_l]
        fname_prefix_l = [col for col in col_l]
    elif type(psd_l) is list and len(psd_l) > 0:
        psd_list = [psd for psd in psd_l]
        fname_prefix_l = ["psd[" + str(idx) + "]" for idx in range(len(psd_l))]
    if psd_list is None:
        print("Unable to generate nosie PSD list")
        return None

    if amp_l is None:
        amp_l = [0.5]

    for idx in range(len(psd_list)):
        noise_l = []
        fname_l = []
        for amp in amp_l:
            noise = generate(int(duration * sample_rate), psd_list[idx], amp)
            fname_l.append(supplement_fname(fname_prefix_l[idx], amp))
            noise_l.append((noise, sample_rate))
        fileio.unload_audio(dir_name + "/" + fname_prefix_l[idx], fname_l, noise_l)
