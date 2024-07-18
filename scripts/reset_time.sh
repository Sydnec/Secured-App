#!/bin/bash

# Fonction pour désynchroniser l'heure du système sous Windows
reset_time_windows() {
    echo "Désynchronisation de l'heure du système sous Windows"
    w32tm /config /manualpeerlist:"time.windows.com" /syncfromflags:manual /reliable:YES /update
    net stop w32time
    net start w32time
    w32tm /resync
}

# Fonction pour désynchroniser l'heure du système sous macOS
reset_time_macos() {
    echo "Désynchronisation de l'heure du système sous macOS"
    sudo systemsetup -setnetworktimeserver time.apple.com
    sudo sntp -sS time.apple.com
}

# Fonction pour désynchroniser l'heure du système sous Linux
reset_time_linux() {
    echo "Désynchronisation de l'heure du système sous Linux"
    sudo timedatectl set-ntp false
    sudo ntpdate time.nist.gov
}

# Détecter le système d'exploitation
case "$(uname -s)" in
    CYGWIN*|MINGW32*|MSYS*|MINGW*)
        reset_time_windows
        ;;
    Darwin)
        reset_time_macos
        ;;
    Linux)
        reset_time_linux
        ;;
    *)
        echo "Système d'exploitation non supporté"
        ;;
esac

echo "Désynchronisation de l'heure du système terminée."
