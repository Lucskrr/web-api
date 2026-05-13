"""
Script para verificar se todas as correções de segurança foram aplicadas
"""

import os
import sys

# Setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

print("="*70)
print("VERIFICADOR DE SEGURANÇA - API DE JOGOS")
print("="*70)

checks = []

# Check 1: Serializer tem validações
print("\n[1/5] Verificando validações no Serializer...")
try:
    with open(os.path.join(BASE_DIR, 'jogos', 'serializers.py')) as f:
        content = f.read()
    
    has_nota_validation = 'min_value=0' in content and 'max_value=10' in content
    has_nome_validation = 'def validate_nome' in content
    has_tipo_validation = 'def validate_tipo' in content
    has_review_validation = 'def validate_review' in content
    
    if all([has_nota_validation, has_nome_validation, has_tipo_validation, has_review_validation]):
        print("✅ PASS: Serializer tem todas as validações")
        checks.append(True)
    else:
        print(f"❌ FAIL: Faltam validações no Serializer")
        if not has_nota_validation:
            print("   - Falta validação de nota (min_value=0, max_value=10)")
        if not has_nome_validation:
            print("   - Falta validate_nome")
        if not has_tipo_validation:
            print("   - Falta validate_tipo")
        if not has_review_validation:
            print("   - Falta validate_review")
        checks.append(False)
except Exception as e:
    print(f"❌ ERROR: {e}")
    checks.append(False)

# Check 2: Modelo tem limite de tamanho para review
print("\n[2/5] Verificando limite de tamanho no Modelo...")
try:
    with open(os.path.join(BASE_DIR, 'jogos', 'models.py')) as f:
        content = f.read()
    
    has_review_limit = 'max_length=5000' in content and 'review' in content
    
    if has_review_limit:
        print("✅ PASS: Modelo tem max_length=5000 para review")
        checks.append(True)
    else:
        print("❌ FAIL: Modelo não tem limite de tamanho para review")
        checks.append(False)
except Exception as e:
    print(f"❌ ERROR: {e}")
    checks.append(False)

# Check 3: JogosListCreateView tem autenticação
print("\n[3/5] Verificando autenticação em JogosListCreateView...")
try:
    with open(os.path.join(BASE_DIR, 'jogos', 'views.py')) as f:
        content = f.read()
    
    # Encontrar a classe JogosListCreateView
    import re
    pattern = r'class JogosListCreateView\(APIView\):.*?(?=class|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        class_content = match.group(0)
        has_auth = 'authentication_classes' in class_content and 'permission_classes' in class_content
        has_token = 'TokenAuthentication' in class_content
        has_perm = 'IsAuthenticated' in class_content
        
        if has_auth and has_token and has_perm:
            print("✅ PASS: JogosListCreateView tem autenticação")
            checks.append(True)
        else:
            print("❌ FAIL: JogosListCreateView sem autenticação completa")
            if not has_auth:
                print("   - Faltam authentication_classes/permission_classes")
            if not has_token:
                print("   - Falta TokenAuthentication")
            if not has_perm:
                print("   - Falta IsAuthenticated")
            checks.append(False)
    else:
        print("❌ FAIL: Não encontrou classe JogosListCreateView")
        checks.append(False)
except Exception as e:
    print(f"❌ ERROR: {e}")
    checks.append(False)

# Check 4: JogoDetailView tem autenticação
print("\n[4/5] Verificando autenticação em JogoDetailView...")
try:
    with open(os.path.join(BASE_DIR, 'jogos', 'views.py')) as f:
        content = f.read()
    
    pattern = r'class JogoDetailView\(APIView\):.*?(?=class|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        class_content = match.group(0)
        has_auth = 'authentication_classes' in class_content and 'permission_classes' in class_content
        
        if has_auth:
            print("✅ PASS: JogoDetailView tem autenticação")
            checks.append(True)
        else:
            print("❌ FAIL: JogoDetailView sem autenticação")
            checks.append(False)
    else:
        print("❌ FAIL: Não encontrou classe JogoDetailView")
        checks.append(False)
except Exception as e:
    print(f"❌ ERROR: {e}")
    checks.append(False)

# Check 5: Scripts de teste existem
print("\n[5/5] Verificando se scripts de teste foram criados...")
try:
    test_simple = os.path.exists(os.path.join(BASE_DIR, 'scripts', 'api_test_simple.py'))
    test_stress = os.path.exists(os.path.join(BASE_DIR, 'scripts', 'api_stress_test.py'))
    
    if test_simple and test_stress:
        print("✅ PASS: Ambos os scripts de teste existem")
        checks.append(True)
    else:
        print("❌ FAIL: Scripts de teste não encontrados")
        if not test_simple:
            print("   - Falta api_test_simple.py")
        if not test_stress:
            print("   - Falta api_stress_test.py")
        checks.append(False)
except Exception as e:
    print(f"❌ ERROR: {e}")
    checks.append(False)

# Resumo
print("\n" + "="*70)
print("RESUMO")
print("="*70)

passed = sum(checks)
total = len(checks)
percentage = (passed / total * 100) if total > 0 else 0

print(f"\n✅ Passou: {passed}/{total}")
print(f"📈 Taxa:   {percentage:.0f}%")

if passed == total:
    print("\n🎉 TODAS AS VERIFICAÇÕES PASSARAM!")
    print("\n⏭️  Próximo passo: Execute os testes")
    print("   python scripts/api_test_simple.py")
    sys.exit(0)
else:
    print("\n❌ Algumas verificações falharam")
    print("   Verifique os erros acima")
    sys.exit(1)
