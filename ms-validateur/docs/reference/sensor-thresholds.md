# Seuils capteurs

Les seuils sont definis dans `src/config/sensor_thresholds.py`.

| Capteur | Seuil modere | Seuil critique | Unite |
|---|---:|---:|---|
| `co2` | 800 | 1000 | ppm |
| `temperature` | 35 | 40 | C |
| `noise` | 70 | 85 | dB |
| `humidity` | 60 | 75 | % |
| `pressure` | 1000 | 1200 | hPa |

Le seuil retourne dans la reponse correspond au prochain seuil d'alerte :

- niveau `normal` : seuil modere ;
- niveau `moderate` : seuil critique ;
- niveau `critical` : seuil critique ;
- niveau `unknow` : `null`.
