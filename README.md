<div align="center">

# SystemMonitor

**Un tableau de bord de surveillance PC, en temps réel.**

CPU · Mémoire · Disques · Réseau · Capteurs matériels

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/Interface-PyQt5-41CD52)
![Plateforme](https://img.shields.io/badge/Plateforme-Windows-0078D4?logo=windows&logoColor=white)
[![Licence](https://img.shields.io/badge/Licence-MIT-64748b)](LICENSE)

[Fonctionnalités](#fonctionnalités) · [Installation](#installation) · [Captures](#captures-décran) · [Limites connues](#limites-connues)

</div>

---

SystemMonitor affiche l'utilisation du processeur, de la mémoire, du disque et du réseau dans une interface **PyQt5 / PyQtGraph**. Les températures et la charge GPU peuvent être récupérées via **OpenHardwareMonitor**, lorsque les capteurs sont disponibles.

## Fonctionnalités

- 🖥 **Surveillance CPU, RAM, Disque et Réseau**  
  - Affichage en temps réel de l'utilisation CPU, RAM et disque.  
  - Mesure des vitesses d'envoi et de réception réseau (Ko/s).  
  - Indicateurs colorés pour alerter en cas d'utilisation excessive.  

- 🌡 **Température et Utilisation du CPU & GPU**  
  - Récupération de la température du processeur et du GPU via **OpenHardwareMonitor**.  
  - Affichage de l'utilisation en pourcentage du GPU.  

- 📶 **Informations Réseau**  
  - Affichage de l'IP locale et de l'IP publique de l'ordinateur.  

- 📊 **Interface Graphique Interactive avec Graphiques Dynamiques**  
  - Suivi visuel en temps réel des performances du système.  
  - Graphiques interactifs pour CPU, RAM, disque, réseau et GPU.  
  - Bouton permettant d'afficher ou masquer les graphiques.  

- 🎨 **Thème Personnalisable**  
  - Interface moderne avec un thème "Azure".  

- **Collecte des données système** : utilisation de `psutil` ; accès aux capteurs Windows via WMI et OpenHardwareMonitor.

## Installation

### Prérequis

Sous **Windows**, installez Python 3.8+ puis les dépendances suivantes :

```sh
pip install psutil pyqt5 pyqtgraph requests wmi
```

### Cloner le dépôt

```sh
git clone https://github.com/neosoda/SystemMonitor.git
cd SystemMonitor
```

### Démarrer

Sous **Windows** :
```sh
python dashboard.py
```

L'exécution native sous Linux n'est **pas garantie** dans l'état actuel du code (import WMI et appels à des API Windows).

## Capteurs et OpenHardwareMonitor

L'application utilise **[OpenHardwareMonitor](https://openhardwaremonitor.org/)** pour récupérer la température CPU/GPU sous Windows. Assurez-vous que **OpenHardwareMonitor.exe** est dans le même dossier que le script ou modifiez le chemin dans `get_openhardwaremonitor_path()`.

## Captures d'écran

![Capture d'écran 2025-03-12 184830](https://github.com/user-attachments/assets/d43e145a-52b3-4253-9dc6-3dcc53bf13e7)

![Capture d'écran 2025-03-12 184819](https://github.com/user-attachments/assets/c0e38269-0f13-48ba-b6a9-5d66d17f7323)


## Limites connues

- Le démarrage d'OpenHardwareMonitor et la collecte WMI utilisent actuellement des API propres à Windows.
- Les températures CPU/GPU dépendent des capteurs disponibles ; une valeur `N/A` ne signifie pas nécessairement une panne.
- Le chemin d'OpenHardwareMonitor peut nécessiter une adaptation, notamment pour un exécutable packagé.

## Auteur

Développé par [neosoda](https://github.com/neosoda).

## Licence

Ce projet est sous licence **MIT** – vous pouvez l'utiliser librement.
