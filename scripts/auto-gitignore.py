#!/usr/bin/env python3
"""
Script para automaticamente adicionar arquivos grandes ao .gitignore
"""
import os
import sys
from pathlib import Path

def find_large_files(directory='.', max_size_mb=30):
    """Encontra arquivos maiores que max_size_mb"""
    max_size_bytes = max_size_mb * 1024 * 1024
    large_files = []
    
    for root, dirs, files in os.walk(directory):
        # Pular diretórios do git e outros
        dirs[:] = [d for d in dirs if not d.startswith('.git')]
        
        for file in files:
            file_path = Path(root) / file
            try:
                if file_path.stat().st_size > max_size_bytes:
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    large_files.append((str(file_path), size_mb))
            except (OSError, FileNotFoundError):
                continue
    
    return sorted(large_files, key=lambda x: x[1], reverse=True)

def read_gitignore():
    """Lê o arquivo .gitignore atual"""
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            return set(line.strip() for line in f if line.strip() and not line.startswith('#'))
    return set()

def update_gitignore(new_patterns):
    """Atualiza o .gitignore com novos padrões"""
    gitignore_path = Path('.gitignore')
    
    # Ler conteúdo atual
    existing_content = ""
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            existing_content = f.read()
    
    # Adicionar novos padrões
    with open(gitignore_path, 'a') as f:
        if existing_content and not existing_content.endswith('\n'):
            f.write('\n')
        f.write('\n# Arquivos grandes detectados automaticamente\n')
        for pattern in sorted(new_patterns):
            f.write(f'{pattern}\n')

def main():
    max_size = 30  # MB
    if len(sys.argv) > 1:
        max_size = int(sys.argv[1])
    
    print(f"🔍 Procurando arquivos maiores que {max_size}MB...")
    
    large_files = find_large_files(max_size_mb=max_size)
    existing_ignores = read_gitignore()
    
    if not large_files:
        print(f"✅ Nenhum arquivo maior que {max_size}MB encontrado!")
        return
    
    print(f"❗ Encontrados {len(large_files)} arquivos grandes:")
    
    new_patterns = []
    total_size = 0
    
    for file_path, size_mb in large_files:
        total_size += size_mb
        print(f"📁 {file_path:50} {size_mb:8.1f}MB", end="")
        
        if file_path not in existing_ignores:
            new_patterns.append(file_path)
            print(" → NOVO")
        else:
            print(" → já no .gitignore")
    
    print(f"\n📊 Total: {total_size:.1f}MB em {len(large_files)} arquivos")
    
    if new_patterns:
        print(f"\n🔧 Adicionando {len(new_patterns)} novos padrões ao .gitignore...")
        update_gitignore(new_patterns)
        print("✅ .gitignore atualizado!")
        
        print("\n💡 Próximos passos:")
        print("   git add .gitignore")
        print("   git commit -m 'Update .gitignore with large files'")
    else:
        print("\n✅ Todos os arquivos grandes já estão no .gitignore!")

if __name__ == "__main__":
    main()
