# Audio Experiment — Option C: Environmental Sound Analysis

## Selected option and question

**Option C:** Analyse one lecturer-supplied clock-tick recording. **Research question:** How does a 512-sample STFT window differ from a 2048-sample window for the timing and frequency structure of mechanical ticks when the audio and hop are kept fixed?

The executed `analysis.ipynb` includes the original and excerpt audio players, figures, a quantitative region/attack description, and written interpretations. This is one individual experiment; no classifier or denoising experiments are included.

## Audio filename and attribution

- Original supplied filename: **`3-142593-A-38.wav`** (5.00 seconds, mono, 44,100 Hz).
- Class in the lecturer's dataset manifest: **`clock_tick`**.
- Original source: *Ticking.aif* by **timgormly**, [Freesound sound 142593](https://freesound.org/people/timgormly/sounds/142593/), **CC0**.
- Course dataset: [ESC-50](https://github.com/karolpiczak/ESC-50) classroom subset; ESC-50 is distributed under **CC BY-NC 3.0**. The original attribution file is preserved in `attribution/ESC50_LICENSE.txt`, and the course manifest in `attribution/course_manifest.csv`.
- Only this one original WAV from the supplied package is included in `audio/`, so the experiment can be rerun. No complete dataset is uploaded. If the course has additional redistribution restrictions, remove the WAV from a public repository but retain filename, hash, attribution, and original local data.

## Settings

| Setting | Value |
| --- | --- |
| Target sample rate | 16,000 Hz |
| Channels | Original mono (no stereo downmix required) |
| Original / analysis rate | 44,100 Hz → 16,000 Hz (polyphase resampling) |
| Spectrogram window | Hann |
| Short window | 512 samples = 32 ms |
| Long window | 2,048 samples = 128 ms |
| Hop for both | 160 samples = 10 ms |
| FFT size | Equal to its respective window length |
| Magnitude display | dB on a shared colour scale |

## How to run

1. Install Python 3.10–3.12, then run `python -m pip install -r requirements.txt`.
2. Open this folder in VS Code / JupyterLab, or run `jupyter notebook`.
3. Open `analysis.ipynb`, select Python 3 and run **all cells** top to bottom. The expected input WAV is already in `audio/`.
4. Use the two in-notebook audio players to listen to the full recording and to the selected time interval. Compare the generated figures with the already-saved copies.
5. Save the executed notebook and commit/push the repository to GitHub. Submit that **GitHub repository URL** in Moodle, making sure the lecturer can view it.

The notebook is self-contained and uses NumPy, SciPy, Matplotlib and IPython rather than the large classifier/neural-audio packages from the full lecture notebook. Its STFT trade-off procedure follows the spectral analysis demonstrated in **Block 2** of the provided `Audio_Course_Student.ipynb`.

## Generated results

Running the notebook saves:

- `results/01_waveform_and_spectrum.png`
- `results/02_spectrograms_512_vs_2048.png`
- `results/03_selected_time_frequency_region.png`
- `results/comparison.csv`
- `results/recording_metadata.json`

The metadata JSON records the exact filename, original WAV hash, duration, chosen time-frequency region, and RMS-envelope attack measurements. The WAV fingerprint helps verify that both STFT settings were applied to the same source.

## Conclusion and limitation

**Observed clock-tick structure:** Approximately **22** prominent RMS-envelope attacks across 5 seconds, with a median attack spacing of **0.23 s**. The maximum-energy 0.40-second interval is **2.10–2.50 s**. Its local FFT peak is about **3022.5 Hz**, and the highlighted frequency region is **2822.5–3222.5 Hz**. This band highlights one prominent component, not all broadband tick energy.

**Preferred setting:** **512 samples**, because the 32-ms window shows tick timing more sharply than the 128-ms alternative. The 2048-sample window provides finer frequency spacing (7.8125 Hz vs. 31.25 Hz) but visibly smears brief attacks in time. Both use an unchanged 10-ms hop and common intensity scale.

**Limitation:** This is one five-second recording, with no independently verified timing annotations. Tick count depends on the peak detector's thresholds. Resampling eliminates information above 8 kHz, and the observed spectrogram alone cannot establish a sound's physical source or generalise to all recording conditions.

## Coursework integrity

The notebook and documentation were prepared with AI assistance, using the exact lecturer-supplied WAV rather than substituted audio. Numeric findings come from executing the analysis on that file. The in-notebook audio players support independent listening verification.
