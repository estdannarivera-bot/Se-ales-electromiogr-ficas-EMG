import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks, hilbert
from scipy.ndimage import uniform_filter1d, median_filter
from scipy.fft import fft, fftfreq

# CONFIGURACIÓN
modo = "archivo"   # "captura" o "archivo"
fs = 2000          # solo captura
duracion = 10      # segundos

# OBTENER SEÑAL
if modo == "captura":
    import nidaqmx
    from nidaqmx.constants import AcquisitionType

    dispositivo = 'Dev2/ai0'
    total_muestras = int(fs * duracion)

    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(dispositivo)
        task.timing.cfg_samp_clk_timing(
            fs,
            sample_mode=AcquisitionType.FINITE,
            samps_per_chan=total_muestras
        )
        senal = task.read(number_of_samples_per_channel=total_muestras)

    senal = np.array(senal)
    t = np.arange(len(senal)) / fs

    # guardar archivo
    datos = np.column_stack((t, senal))
    np.savetxt("senal_guardada.txt", datos, delimiter=",",
               header="Tiempo,Amplitud", comments='')

else:
    data = np.loadtxt("senal_generador.txt", delimiter=None, skiprows=1)
    t = data[:,0]
    senal = data[:,1]

    fs = 1 / np.mean(np.diff(t))

# FILTRO PASABANDA
def filtro_pasabanda(signal, fs, lowcut=20, highcut=450):         # típicos para EMG
    nyq = 0.5 * fs                                                # frecuencia de Nyquist
    if highcut >= nyq:                                            # evitar aliasing
        highcut = nyq * 0.9                                       # dejar un margen

    b, a = butter(4, [lowcut/nyq, highcut/nyq], btype='band')     # filtro Butterworth de orden 4
    return filtfilt(b, a, signal)                                 # aplicar filtro sin fase

senal_filtrada = filtro_pasabanda(senal, fs)                      # filtrar señal para eliminar ruido y artefactos

senal_filtrada = median_filter(senal_filtrada, size=5)            # filtro mediana para eliminar picos aislados sin afectar la forma general de la señal

# ENVOLVENTE
envolvente = np.abs(hilbert(senal_filtrada))                        # calcular la envolvente usando la transformada de Hilbert
envolvente_suave = uniform_filter1d(envolvente, size=int(fs*0.2))   # suavizar la envolvente con un filtro de media móvil de 200ms para reducir fluctuaciones rápidas y resaltar tendencias generales

# DETECCIÓN DE CONTRACCIONES

# umbral dinámico basado en la media y desviación estándar de la envolvente 
# suavizada para adaptarse a diferentes niveles de señal y ruido
threshold = np.mean(envolvente_suave) + 0.8*np.std(envolvente_suave) 

peaks, _ = find_peaks(
    envolvente_suave,
    height=threshold,
    distance=int(fs*1),
    prominence=np.std(envolvente_suave)*0.5
)

print("Contracciones detectadas:", len(peaks))

# EXTRAER CONTRACCIONES
window = int(0.5 * fs)                                # ventana de 500ms
contracciones = []                                    # lista para almacenar segmentos de contracción

for p in peaks:                                         # extraer un segmento centrado en el pico con la ventana definida
    inicio = max(0, p - window)
    fin = min(len(senal_filtrada), p + window)
    contracciones.append(senal_filtrada[inicio:fin])    

# FRECUENCIA MEDIA Y MEDIANA
def calcular_frecuencias(segmento, fs):
    N = len(segmento)

    yf = np.abs(fft(segmento))[:N//2]
    xf = fftfreq(N, 1/fs)[:N//2]

    potencia = yf**2

    # frecuencia media
    f_media = np.sum(xf * potencia) / np.sum(potencia)

    # frecuencia mediana
    potencia_acum = np.cumsum(potencia)
    mitad = potencia_acum[-1] / 2
    f_mediana = xf[np.where(potencia_acum >= mitad)[0][0]]

    return f_media, f_mediana

freq_medias = []
freq_medianas = []

for c in contracciones:
    fm, fmd = calcular_frecuencias(c, fs)
    freq_medias.append(fm)
    freq_medianas.append(fmd)

# RESULTADOS
print("\nRESULTADOS")
print("-------------------------------------")
print("Contracción | Frecuencia Media | Frecuencia Mediana")

for i in range(len(freq_medias)):
    print(f"{i+1:^10} | {freq_medias[i]:^15.2f} | {freq_medianas[i]:^18.2f}")

# GRÁFICAS
plt.figure(figsize=(12,5))
plt.plot(t, senal_filtrada, label="Señal filtrada", linewidth=0.7)
plt.plot(t, envolvente_suave, label="Envolvente", linewidth=2)
plt.plot(peaks/fs, envolvente_suave[peaks], "ro", label="Contracciones")

plt.title("EMG - Detección de contracciones")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mV)")
plt.legend()
plt.grid()
plt.show()

# Evolución de frecuencias
plt.figure(figsize=(10,5))
plt.plot(freq_medias, '-o', label='Frecuencia Media')
plt.plot(freq_medianas, '-s', label='Frecuencia Mediana')

plt.title('Evolución de Frecuencias (Fatiga EMG)')
plt.xlabel('Contracción')
plt.ylabel('Frecuencia (Hz)')
plt.legend()
plt.grid()
plt.show()

# ANÁLISIS ESPECTRAL MEDIANTE FFT

picos_espectrales = []

n_contracciones = len(contracciones)
ncols = min(3, n_contracciones)
nrows = int(np.ceil(n_contracciones / ncols))

fig, axes = plt.subplots(nrows, ncols, figsize=(5*ncols, 4*nrows))
axes = np.array(axes).flatten()

for i, segmento in enumerate(contracciones):
    N = len(segmento)

    yf = np.abs(fft(segmento))[:N//2]
    xf = fftfreq(N, 1/fs)[:N//2]

    # NORMALIZACIÓN
    yf_norm = yf / np.max(yf)

    # evitar frecuencia 0 (log)
    xf_plot = xf[1:]            
    yf_plot = yf_norm[1:]

    # PICO ESPECTRAL
    pico_idx = np.argmax(yf_plot)
    pico_freq = xf_plot[pico_idx]
    picos_espectrales.append(pico_freq)

    # GRÁFICA SEMILOG
    axes[i].semilogx(xf_plot, yf_plot, linewidth=0.8)
    axes[i].axvline(pico_freq, linestyle='--', linewidth=1,
                    label=f'Pico: {pico_freq:.1f} Hz')

    axes[i].set_title(f'Contracción {i+1}')
    axes[i].set_xlabel('Frecuencia (Hz)')
    axes[i].set_ylabel('Magnitud normalizada')
    axes[i].set_xlim([10, 500])   
    axes[i].legend(fontsize=8)
    axes[i].grid(which='both')

# ocultar subplots sobrantes
for j in range(n_contracciones, len(axes)):
    axes[j].set_visible(False)

plt.suptitle('Espectro FFT', fontsize=13)
plt.tight_layout()
plt.show()

# Evolución del pico espectral
plt.figure(figsize=(10,5))
plt.plot(range(1, n_contracciones+1), picos_espectrales, '-^',
         label='Pico espectral')

plt.title('Desplazamiento del pico espectral (Fatiga EMG)')
plt.xlabel('Contracción')
plt.ylabel('Frecuencia del pico (Hz)')
plt.xticks(range(1, n_contracciones+1))
plt.legend()
plt.grid()
plt.show()

# Resumen
print("\nPARTE C – ANÁLISIS ESPECTRAL")
print("-------------------------------------")
print("Contracción | Pico espectral (Hz)")
for i, pico in enumerate(picos_espectrales):
    print(f"{i+1:^10} | {pico:^20.2f}")