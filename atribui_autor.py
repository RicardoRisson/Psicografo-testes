import re
import csv

def processar_txt_poemas(caminho_txt, caminho_csv):
    # 1. Ler o ficheiro TXT tratando problemas de codificação (ANSI / UTF-8)
    try:
        with open(caminho_txt, "r", encoding="utf-8") as f:
            texto_completo = f.read()
    except UnicodeDecodeError:
        print("💡 Detectada codificação ANSI/Windows. Ajustando leitura...")
        with open(caminho_txt, "r", encoding="cp1252") as f:
            texto_completo = f.read()

    # 2. Lista de títulos exatos para o teste (adicione outros conforme desejar)
    # Escreva exatamente como aparecem no livro
    titulos_alvo = [
"NAPOLEÃO",
        "SONETO",
        "ILUSÃO",
        "DEIXA-ME!",
        "O VIZIR",
        "NÃO TE ESQUEÇAS DE MIM!",
        "SONETO",
        "ELEGIA",
        "O EXILADO",
        "AURORA",
        "AS SELVAS",
        "À LUCÍLA",
        "CHILDE-HAROLD",
        "O SABIÁ",
        "ESTÂNCIAS",
        "O MAR",
        "A TRISTEZA",
        "O ESTANDARTE AURIVERDE",
        "CANTO DO SERTANEJO",
        "AVE! MARIA!",
        "VOZ DO POETA",
        "SALMO I",
        "INVOCAÇÃO",
        "CANTO",
        "ARMAS",
        "I",
        "II",
        "III",
        "IV",
        "V",
        "VI",
        "VII",
        "VIII",
        "IX",
        "X",
        "CISMAS À NOITE",
        "SEXTILHAS",
        "CÂNTICO DO CALVÁRIO",
        "QUEIXAS DO POETA",
        "RESIGNAÇÃO",
        "PROTESTOS",
        "DESENGANO",
        "EM TODA A PARTE",
        "NO ERMO",
        "SETE DE SETEMBRO",
        "O ESCRAVO",
        "A CIDADE",
        "AO RIO DE JANEIRO",
        "A FLOR DO MARACUJÁ",
        "A ROÇA",
        "A CRIANÇA",
        "EXPIAÇÃO",
        "NOTURNO",
        "NARRAÇÃO",
        "EU AMO A NOITE",
        "A VOLTA",
        "A DESPEDIDA I",
        "A DESPEDIDA II"
        "CONFORTO",
        "VISÕES DA NOITE",
        "O CANTO DOS SABIÁS",
        "O RESPLENDOR DO TRONO",
        "EM VIAGEM",
        "A SOMBRA",
        "A LENDA DO AMAZONAS",
        "ESTÂNCIAS",
        "O ARREPENDIMENTO",
        "ENOJO",
        "O MESMO",
        "A UM MONUMENTO",
    ]

# 1. Cria a lista removendo as duplicatas
    titulos_unicos = list(set(titulos_alvo))
    
    # 2. Expressão regular corrigida usando 'titulos_unicos' e a variável 'p' correta
    padrao_busca = r"\n\s*(" + "|".join([r"\s+".join([re.escape(p) for p in t.split()]) for t in titulos_unicos]) + r")\s*\n"
    
    # Faz o corte preciso do texto com base nos títulos fornecidos
    partes = re.split(padrao_busca, texto_completo, flags=re.IGNORECASE)
    
    poemas_estruturados = []
    
    # O primeiro elemento (partes[0]) é o texto de introdução antes do primeiro poema, ignoramos.
    i = 1
    while i < len(partes) - 1:
        titulo = partes[i].strip()
        corpo = partes[i+1].strip()
        
        # Limpezas no corpo do poema caso vazem notas finais
        if "FIM" in corpo:
            corpo = corpo.split("FIM")[0].strip()
            
        poemas_estruturados.append([titulo.upper(), "Fagundes Varella", corpo])
        i += 2

    # 3. Guardar o resultado final no formato CSV esperado
    # O 'utf-8-sig' garante a acentuação perfeita para abrir direto no Excel
    with open(caminho_csv, mode='w', newline='', encoding='utf-8-sig') as f:
        escritor = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        # Cabeçalho do CSV
        escritor.writerow(['titulo', 'autor', 'texto'])
        # Dados dos poemas
        escritor.writerows(poemas_estruturados)

    print(f"\n✨ Sucesso! Foram extraídos {len(poemas_estruturados)} poemas com base nos títulos fornecidos.")
    print(f"Ficheiro guardado em: '{caminho_csv}'")

# --- Execução do Script ---
ficheiro_entrada = "EU.txt"

ficheiro_saida = "poemas_vagundes_varella.csv"

try:
    processar_txt_poemas(ficheiro_entrada, ficheiro_saida)
except Exception as e:
    print(f"Ocorreu um erro ao processar o TXT: {e}")