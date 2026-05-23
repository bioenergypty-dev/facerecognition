#!/usr/bin/env python3
"""
Script para generar certificados SSL autofirmados para HTTPS local
Ejecuta este script UNA SOLA VEZ antes de correr la aplicación
"""

import os
import sys
from pathlib import Path

def generar_certificados():
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID, ExtensionOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from datetime import datetime, timedelta
        import socket
    except ImportError:
        print("❌ Error: Se necesita 'cryptography'. Instalando...")
        os.system(f'"{sys.executable}" -m pip install cryptography')
        return generar_certificados()

    # Crear directorio de certificados
    cert_dir = Path("certs")
    cert_dir.mkdir(exist_ok=True)
    
    cert_file = cert_dir / "cert.pem"
    key_file = cert_dir / "key.pem"
    
    # Verificar si ya existen
    if cert_file.exists() and key_file.exists():
        print("✅ Los certificados ya existen en ./certs/")
        print(f"   📁 {cert_file}")
        print(f"   🔑 {key_file}")
        return True
    
    print("🔐 Generando certificados SSL autofirmados...")
    
    # Generar clave privada
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Obtener hostname e IP
    hostname = socket.gethostname()
    try:
        ip_local = socket.gethostbyname(hostname)
    except:
        ip_local = "127.0.0.1"
    
    # Crear certificado autofirmado
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Local"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Local"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"FaceRecognition"),
        x509.NameAttribute(NameOID.COMMON_NAME, hostname),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(hostname),
            x509.DNSName("localhost"),
            x509.DNSName("*.local"),
            x509.IPAddress(ip_local),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # Guardar certificado
    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    # Guardar clave privada
    with open(key_file, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    print("✅ Certificados generados exitosamente!")
    print(f"   📁 Certificado: {cert_file}")
    print(f"   🔑 Clave: {key_file}")
    print(f"   ℹ️  Válido por: 365 días")
    print(f"   🖥️  Hostname: {hostname}")
    print(f"   📍 IP Local: {ip_local}")
    print()
    print("⚠️  ADVERTENCIA: Este es un certificado autofirmado.")
    print("   El navegador mostrará una advertencia de seguridad.")
    print("   Esto es NORMAL y SEGURO en redes locales.")
    print()
    return True

if __name__ == "__main__":
    try:
        generar_certificados()
        print("🎉 ¡Listo! Ahora puedes ejecutar: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
