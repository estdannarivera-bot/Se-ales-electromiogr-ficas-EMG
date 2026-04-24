
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
 

  

### Detección de contracciones — Señal emulada

![Deteccion de contracciones]()

 
