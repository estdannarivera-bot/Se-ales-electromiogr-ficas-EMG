
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

## Requisitos e instalación
 
**Python 3.8+** con las siguientes librerías:
 
```bash
pip install numpy matplotlib scipy
```
 
**Ejecución:**
 
```bash
python emg_fatiga.py
```
 
> Asegúrese de que los archivos `senal_cap_gen.txt` y `senal_cap.txt` estén en el mismo
> directorio que el script, o ajuste la ruta en la variable `ARCHIVOS` al inicio del código.
 
---
 
## Parte A — Señal emulada (generador)
### Descripción
 
Se configuró el generador de señales biológicas en modo EMG, simulando aproximadamente
cinco contracciones musculares voluntarias. La señal fue adquirida, almacenada y procesada
para calcular la frecuencia media y mediana de cada contracción.

### Procesamiento en Python
 
| Paso | Descripción |
|------|-------------|
| Filtro pasa-banda | Butterworth orden 4, 20–450 Hz |
| Filtro de mediana | Ventana de 5 muestras (supresión de artefactos) |
| Envolvente | Transformada de Hilbert + suavizado uniforme (150 ms) |
| Detección de picos | `find_peaks` con distancia mínima de **1.5 s** y umbral en percentil 85 |
| Segmentación | Ventanas de ±600 ms centradas en cada pico |
| Análisis espectral | FFT con ventana de Hanning, banda 20–450 Hz |
 
> **Nota sobre el parámetro de distancia:** Se utiliza `min_dist_s = 1.5 s` (en lugar de
> 0.8 s) porque el generador produce pulsos muy regulares y simétricos. Una distancia menor
> provocaba doble detección en los flancos de subida/bajada de cada contracción, resultando
> en ~10 picos en lugar de 5 y frecuencias medianas con oscilación artificial entre ~50 Hz y
> ~80 Hz. 
