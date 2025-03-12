# SystemMonitor - Tableau de Bord PC en Temps Réel

**SystemMonitor** est une application de surveillance en temps réel des performances d'un ordinateur sous Windows et Linux. Il affiche des informations clés sur l'utilisation du CPU, de la RAM, du disque, du réseau, ainsi que la température et l'utilisation du GPU. L'interface graphique est basée sur **PyQt5** et **PyQtGraph**, offrant des graphiques dynamiques pour suivre l'évolution des ressources système.

## 📌 Fonctionnalités

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

- 🚀 **Optimisé pour Windows et Linux**  
  - Utilisation de **WMI** pour récupérer les données sous Windows.  
  - Compatibilité avec **psutil** et **OpenHardwareMonitor**.  

## 🛠 Installation

### 1️⃣ Prérequis

Assurez-vous d'avoir **Python 3.8+** installé ainsi que les dépendances suivantes :

```sh
pip install psutil pyqt5 pyqtgraph requests wmi
```

### 2️⃣ Cloner le projet

```sh
git clone https://github.com/neosoda/SystemMonitor.git
cd SystemMonitor
```

### 3️⃣ Lancer l'application

Sous **Windows** :
```sh
python system_monitor.py
```

Sous **Linux** :
```sh
python3 system_monitor.py
```

## 🔧 Configuration OpenHardwareMonitor

L'application utilise **[OpenHardwareMonitor](https://openhardwaremonitor.org/)** pour récupérer la température CPU/GPU sous Windows. Assurez-vous que **OpenHardwareMonitor.exe** est dans le même dossier que le script ou modifiez le chemin dans `get_openhardwaremonitor_path()`.

## 📸 Aperçu

![Capture d'écran 2025-03-12 184830](https://github.com/user-attachments/assets/d43e145a-52b3-4253-9dc6-3dcc53bf13e7)

![Capture d'écran 2025-03-12 184819](https://github.com/user-attachments/assets/c0e38269-0f13-48ba-b6a9-5d66d17f7323)


## 🚀 Améliorations Futures

- ✅ Ajout d'un mode **sombre** et de nouveaux thèmes.  
- ✅ Support amélioré pour **Linux** et **MacOS**.  
- ✅ Export des données en **CSV** ou **JSON**.  
- ✅ Intégration d'une alerte en cas de surchauffe ou d'utilisation excessive.  

## 👨‍💻 Auteur

Développé par **(https://github.com/neosoda)** 🛠.

## 📜 Licence

Ce projet est sous licence **MIT** – vous pouvez l'utiliser librement.
