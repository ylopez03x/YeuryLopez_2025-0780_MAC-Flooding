# YeuryLopez_2025-0780_MAC-Flooding
Laboratorio de Seguridad de Redes - Script de ataque MAC Flooding usando Python3 y Scapy.
# MAC Flooding Attack
**Autor:** Yeury Lopez de Leon  
**Matrícula:** 2025-0780  
**Materia:** Seguridad de Redes  
**Fecha:** 31/05/2026  

---

## Objetivo del Laboratorio
Demostrar el ataque MAC Flooding en un entorno de laboratorio 
controlado usando EVE-NG, evidenciando cómo un atacante puede 
saturar la tabla CAM de un switch Cisco para convertirlo en un 
HUB y capturar tráfico que no le pertenece.

---

## Objetivo del Script
Inundar la tabla CAM (Content Addressable Memory) del switch SW1 
con miles de direcciones MAC falsas hasta agotarla, forzando al 
switch a realizar flooding de todos los paquetes hacia todos los 
puertos.

### Parámetros usados
| Parámetro | Valor | Descripción |
|---|---|---|
| INTERFAZ | eth0 | Interfaz de Kali hacia SW1 |
| PAQUETES | 10000 | Cantidad de MACs falsas a generar |
| Red objetivo | 172.25.78.0/24 | Red del laboratorio |

### Requisitos para utilizar la herramienta
- Kali Linux con Python 3
- Librería Scapy instalada (`pip install scapy`)
- Permisos root (`sudo`)
- Conectividad capa 2 con el switch objetivo

---

## Documentación del funcionamiento del Script

El script funciona en los siguientes pasos:

**1. Generación de MACs aleatorias**  
La función `random_mac()` genera direcciones MAC completamente 
aleatorias de 6 bytes para cada paquete enviado.

**2. Generación de IPs aleatorias**  
La función `random_ip()` genera IPs dentro del rango 
172.25.78.1-254 para simular hosts ficticios.

**3. Construcción del paquete**  
Cada paquete es construido con Scapy usando capas Ethernet y ARP 
con MACs e IPs falsas tanto en origen como en destino.

**4. Envío masivo**  
Se envían 10,000 paquetes por la interfaz eth0 sin esperar 
respuesta (`sendp` con verbose=False).

**5. Progreso**  
El script muestra el progreso cada 100 paquetes enviados.

---

## Documentación de la Red

### Topología
> 📸 **[INSERTAR CAPTURA DE PANTALLA DE LA TOPOLOGÍA EN EVE-NG]**  
> Usar la captura del canvas completo con nombre y matrícula visibles

### Direccionamiento IP
| Dispositivo | Interfaz | Dirección IP | Máscara | Rol |
|---|---|---|---|---|
| R1 | fa0/0 | 172.25.78.1 | /24 | Gateway + DHCP Server |
| SW1 | VLAN1 | 172.25.78.2 | /24 | Switch Core - Root Bridge |
| SW2 | VLAN1 | 172.25.78.3 | /24 | Switch Acceso |
| Kali | eth0 | 172.25.78.10 | /24 | Atacante |
| PC1 | eth0 | 172.25.78.20 | /24 | Víctima 1 (estática) |
| PC2 | eth0 | 172.25.78.21 | /24 | Víctima 2 (DHCP) |

### Conexiones
| Dispositivo A | Interfaz | Dispositivo B | Interfaz |
|---|---|---|---|
| R1 | fa0/0 | SW1 | e0/0 |
| SW1 | e0/1 | Kali | eth0 |
| SW1 | e0/2 | PC1 | eth0 |
| SW1 | e0/3 | SW2 | e0/0 |
| SW2 | e0/1 | PC2 | eth0 |

### Herramientas utilizadas
- EVE-NG Community Edition
- Cisco vIOS-L2 v15.2 (SW1, SW2)
- Cisco vIOS v15.6 (R1)
- Kali Linux 2024
- Python 3 + Scapy

---

## Capturas de Pantalla

### Topología del laboratorio
> 📸 **[INSERTAR CAPTURA DE LA TOPOLOGÍA]**

### Antes del ataque - Tabla CAM de SW1
> 📸 **[INSERTAR CAPTURA DE: show mac address-table count en SW1]**

### Ejecución del script
> 📸 **[INSERTAR CAPTURA DEL SCRIPT CORRIENDO EN KALI]**

### Durante el ataque - Tabla CAM llena
> 📸 **[INSERTAR CAPTURA DE: show mac address-table count en SW1 con tabla llena]**

### Tráfico capturado en Kali
> 📸 **[INSERTAR CAPTURA DE: tcpdump -i eth0 mostrando tráfico ajeno]**

---

## Contramedidas

### Port Security en SW1
Configurar Port Security limita la cantidad de MACs permitidas 
por puerto, bloqueando el ataque:

```cisco
interface ethernet 0/1
 switchport mode access
 switchport port-security
 switchport port-security maximum 5
 switchport port-security violation restrict
 switchport port-security aging time 2
```

### Verificación de la contramedida
> 📸 **[INSERTAR CAPTURA DE: show port-security interface ethernet 0/1]**

### Resultado
Con Port Security activo, el switch bloquea automáticamente 
cualquier intento de registrar más de 5 MACs por puerto, 
registrando las violaciones sin afectar el tráfico legítimo.

> 📸 **[INSERTAR CAPTURA DEL SCRIPT CORRIENDO CON CONTRAMEDIDA ACTIVA]**