
# Laboratorio 4  
## Señales electromiográficas EMG  

**Programa:** Ingeniería Biomédica  
**Asignatura:** Procesamiento Digital de Señales  
**Universidad:** Universidad Militar Nueva Granada  
**Estudiantes:** Danna Rivera, Duvan Paez

---

![algoritmoEMG](algoritmoEMG.png)

---
## Introducción
 
La electromiografía (EMG) es fundamental porque permite registrar la actividad eléctrica de los músculos en tiempo real, lo que facilita analizar su activación, intensidad y estado funcional. En esta práctica, su uso permitió detectar contracciones y estudiar la señal tanto en el dominio del tiempo como de la frecuencia, evidenciando comportamientos como la fatiga muscular mediante cambios en las frecuencias características. En la ingeniería biomédica, la EMG es clave para aplicaciones como el desarrollo de prótesis controladas por señales musculares, sistemas de rehabilitación, diagnóstico de trastornos neuromusculares y el diseño de interfaces humano-máquina, lo que la convierte en una herramienta esencial para entender e interactuar con el sistema neuromuscular.
 
---

 
## Parte A — Señal emulada (generador)
### Descripción

En esta parte se trabaja con el archivo `senal_generador.txt`, que contiene la señal generada por el simulador de señales biológicas configurado en modo EMG, emulando aproximadamente cinco contracciones musculares voluntarias. La señal fue adquirida, almacenada y procesada para calcular la frecuencia media y mediana de cada contracción.
 
Para ejecutar esta parte, asegúrate de que el archivo `senal_generador.txt` esté en la misma carpeta que el script y que la variable `modo` esté configurada como:
 
```python
modo = "archivo"
```
 
Y que la línea de carga apunte al archivo correcto:
 
```python
data = np.loadtxt("senal_generador.txt", delimiter=None, skiprows=1)
```
### Procesamiento en Python
 
1. **Carga la señal** desde el archivo `.txt` y recalcula la frecuencia de muestreo `fs` a partir de los tiempos registrados.
2. **Aplica un filtro pasa banda Butterworth** (20–450 Hz, orden 4) para eliminar ruido de baja frecuencia (artefactos de movimiento) y de alta frecuencia (ruido eléctrico). Se complementa con un filtro de mediana para suprimir picos aislados.
3. **Calcula la envolvente** de la señal usando la transformada de Hilbert, seguida de un suavizado con filtro de media móvil (ventana de 200 ms).
4. **Detecta las contracciones** mediante un umbral dinámico basado en la media y desviación estándar de la envolvente, utilizando `find_peaks` con restricciones de distancia mínima y prominencia.
5. **Calcula la frecuencia media y mediana** espectral para cada contracción segmentada, aplicando FFT sobre ventanas de ±500 ms centradas en cada pico detectado.
6. **Grafica** la señal filtrada con su envolvente, los picos de contracción detectados, y la evolución de frecuencia media y mediana a lo largo de las contracciones.
```python
# Fragmento clave – cálculo de frecuencia media y mediana
def calcular_frecuencias(segmento, fs):
    N = len(segmento)
    yf = np.abs(fft(segmento))[:N//2]
    xf = fftfreq(N, 1/fs)[:N//2]
    potencia = yf**2
    f_media = np.sum(xf * potencia) / np.sum(potencia)
    potencia_acum = np.cumsum(potencia)
    f_mediana = xf[np.where(potencia_acum >= potencia_acum[-1]/2)[0][0]]
    return f_media, f_mediana
```


### Detección de contracciones — Señal emulada

![Deteccion de contracciones](EMG-GENERADORSENALES.png)

### Evolución de frecuencias 

![Evolución de frecuencias](EFRECUENCIASGENERADOR.png)

### Tabla de parámetros extraídos 

| Contracción | Frecuencia Media |Frecuencia Mediana |
|---|---|---|
|1|99.34|58.01|
|2|99.82|57.01|
|3|96.94 |56.01|
|4|98.01 |56.01|
|5|97.75 |56.01|

## Parte B – Captura de la señal de paciente
### Descripción

En esta parte se trabaja con el archivo `senal_guardada.txt`, que contiene la señal EMG real registrada desde electrodos de superficie colocados sobre el grupo muscular del voluntario (antebrazo), quien realizó contracciones repetidas hasta 5 contracciones. 
Para ejecutar esta parte, modifica la línea de carga en el script:
 
```python
data = np.loadtxt("senal_captura.txt", delimiter=None, skiprows=1)
```
 
El resto de la variable `modo` se mantiene en `"archivo"`.

 ### Procesamiento en Python
 
 El flujo de procesamiento es idéntico al de la Parte A, pero aplicado sobre una señal real con mayor variabilidad y ruido. Los pasos clave son:
 
1. **Carga de la señal real** desde `senal_guardada.txt` con recálculo automático de `fs`.
2. **Filtrado pasa banda (20–450 Hz)** + filtro de mediana para acondicionar la señal y reducir artefactos de movimiento, ruido de red eléctrica y picos espurios.
3. **Cálculo de la envolvente** con transformada de Hilbert y suavizado de 200 ms, que permite visualizar la activación muscular de forma continua.
4. **Detección automática de contracciones** con umbral adaptativo. En señales reales, el número de contracciones varía según el nivel de esfuerzo del voluntario.
5. **Segmentación y cálculo de frecuencia media y mediana** por contracción.
6. **Análisis de tendencia:** se espera observar una **disminución progresiva** de ambas frecuencias a medida que el músculo se aproxima a la fatiga, fenómeno asociado a la acumulación de metabolitos y al reclutamiento de fibras lentas.


```python
# Umbral dinámico adaptado a la señal real
threshold = np.mean(envolvente_suave) + 0.8 * np.std(envolvente_suave)
 
peaks, _ = find_peaks(
    envolvente_suave,
    height=threshold,
    distance=int(fs * 1),          # mínimo 1 segundo entre contracciones
    prominence=np.std(envolvente_suave) * 0.5
)
```

### Detección de contracciones — Señal paciente

![Deteccion de contracciones](EMG-PACIENTE.png)

### Evolución de frecuencias 

![Evolución de frecuencias](FRECUENCIASPACIENTE.png)

### Tabla de parámetros extraídos 

| Contracción | Frecuencia Media |Frecuencia Mediana |
|---|---|---|
|1| 110.06 |87.03|
|2| 97.31 |77.03|
|3| 87.50 |71.02|
|4| 108.46 |84.03|
|5| 115.54 |103.04|

## Parte C - Análisis espectral mediante FFT

Para analizar el comportamiento en frecuencia de la señal EMG, se aplicó la Transformada Rápida de Fourier (FFT) a cada una de las contracciones detectadas.

El cálculo del espectro se realizó de la siguiente manera:

```python
yf = np.abs(fft(segmento))[:N//2]
xf = fftfreq(N, 1/fs)[:N//2]
```

Para facilitar la comparación entre contracciones, la magnitud fue normalizada y representada en escala semilogarítmica:

```python
yf = yf / np.max(yf)
plt.semilogx(xf[1:], yf[1:])
```
### Señal del generador

**Espectro de amplitud (FFT)**

![FFT_generador](FFT_generador.png)


![FFT_Pico](FFT_Pico.png)


