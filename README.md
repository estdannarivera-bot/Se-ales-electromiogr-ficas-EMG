
# Laboratorio 4  
## Señales electromiográficas EMG  

**Programa:** Ingeniería Biomédica  
**Asignatura:** Procesamiento Digital de Señales  
**Universidad:** Universidad Militar Nueva Granada  
**Estudiantes:** Danna Rivera, Duvan Paez

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

![Deteccion de contracciones]()

 
