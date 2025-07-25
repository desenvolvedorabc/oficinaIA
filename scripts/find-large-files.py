#!/usr/bin/env python3
"""
Script para encontrar arquivos grandes no repositório
"""
import os
import sys
from pathlib import Path

def find_large_files(directory='.', max_size_mb=30):
    """Encontra arquivos maiores que max_size_mb"""
    max_size_bytes = max_size_mb * 1024 * 1024
    large_files = []
    
    for root, dirs, files in os.walk(directory):
        # Pular diretórios do git
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            file_path = Path(root) / file
            try:
                if file_path.stat().st_size > max_size_bytes:
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    large_files.append((str(file_path), size_mb))
            except (OSError, FileNotFoundError):
                continue
    
    return sorted(large_files, key=lambda x: x[1], reverse=True)

def main():
    max_size = 30  # MB
    if len(sys.argv) > 1:
        max_size = int(sys.argv[1])
    
    print(f"🔍 Procurando arquivos maiores que {max_size}MB...")
    print("="*60)
    
    large_files = find_large_files(max_size_mb=max_size)
    
    if not large_files:
        print(f"✅ Nenhum arquivo maior que {max_size}MB encontrado!")
        return
    
    print(f"❗ Encontrados {len(large_files)} arquivos grandes:")
    print()
    
    total_size = 0
    for file_path, size_mb in large_files:
        print(f"📁 {file_path:50} {size_mb:8.1f}MB")
        total_size += size_mb
    
    print("="*60)
    print(f"📊 Total: {total_size:.1f}MB em {len(large_files)} arquivos")
    print()
    print("💡 Para adicionar ao .gitignore:")
    for file_path, _ in large_files:
        if not any(pattern in file_path for pattern in ['.git/', '__pycache__/']):
            print(f"echo '{file_path}' >> .gitignore")

if __name__ == "__main__":
    main()
