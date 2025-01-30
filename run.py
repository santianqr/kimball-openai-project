import os
import subprocess
import sys

def run_command(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)

def main():
    # Instalar los requisitos
    print("📦 Instalando los requisitos...")
    run_command("pip install -r requirements.txt")

    # Formatear el código con black
    print("🖌 Formateando el código con black...")
    run_command("black .")

    # Ejecutar linter con flake8
    print("🔍 Ejecutando linter con flake8...")
    run_command("flake8 .")

    # Ejecutar pruebas con pytest
    print("🧪 Ejecutando pruebas con pytest...")
    run_command("pytest")

    # Ejecutar el script principal
    print("🚀 Ejecutando el script principal...")
    run_command("python main.py")

if __name__ == "__main__":
    main()