#!/bin/bash
# Pre-commit hook para verificar arquivos grandes (>30MB)
# Salve como .git/hooks/pre-commit e dê permissão de execução

MAX_SIZE=31457280  # 30MB em bytes

echo "🔍 Verificando arquivos grandes (>30MB)..."

# Verificar arquivos staged
large_files=()
while IFS= read -r -d '' file; do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        if [ "$size" -gt "$MAX_SIZE" ]; then
            size_mb=$((size / 1024 / 1024))
            large_files+=("$file ($size_mb MB)")
        fi
    fi
done < <(git diff --cached --name-only -z)

if [ ${#large_files[@]} -gt 0 ]; then
    echo "❌ ERRO: Arquivos muito grandes detectados (>30MB):"
    printf '   • %s\n' "${large_files[@]}"
    echo ""
    echo "💡 Soluções:"
    echo "   1. Adicione ao .gitignore:"
    echo "      echo 'nome_do_arquivo.ext' >> .gitignore"
    echo ""
    echo "   2. Configure Git LFS:"
    echo "      git lfs track '*.extensao'"
    echo "      git add .gitattributes"
    echo ""
    echo "   3. Remova do staging:"
    echo "      git reset HEAD nome_do_arquivo.ext"
    echo ""
    exit 1
fi

echo "✅ Nenhum arquivo grande detectado"
exit 0
