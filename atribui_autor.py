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
        "ANTÍFONA",
        "SIDERAÇÕES",
        "LÉSBIA",
        "MÚMIA",
        "EM SONHOS...",
        "LUBRICIDADE",
        "MONJA",
        "CRISTO DE BRONZE",
        "CLAMANDO...",
        "BRAÇOS",
        "REGINA COELI",
        "SONHO BRANCO",
        "CANÇÃO DA FORMOSURA",
        "TORRE DE OURO",
        "CARNAL E MÍSTICO",
        "A DOR",
        "ENCARNAÇÃO",
        "SONHADOR",
        "NOIVA DA AGONIA",
        "LUA",
        "SATÃ",
        "BELEZA MORTA",
        "AFRA",
        "PRIMEIRA COMUNHÃO",
        "JUDIA",
        "VELHAS TRISTEZAS",
        "VISÃO DA MORTE",
        "DEUSA SERENA",
        "TULIPA REAL",
        "APARIÇÃO",
        "VESPERAL",
        "DANÇA DO VENTRE",
        "FOEDERIS ARCA",
        "TUBERCULOSA",
        "FLOR DO MAR",
        "DILACERAÇÕES",
        "REGENERADA",
        "SENTIMENTOS CARNAIS",
        "CRISTAIS",
        "SINFONIAS DO OCASO",
        "REBELADO",
        "MUSICA MISTERIOSA...",
        "POST MORTEM",
        "ALDA",
        "ACROBATA DA DOR",
        "ANGELUS...",
        "LEMBRANÇAS APAGADAS",
        "SUPREMO DESEJO",
        "SONATAS",
        "MAJESTADE CAÍDA",
        "INCENSOS",
        "LUZ DOLOROSA...",
        "TORTURA ETERNA",
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
            
        poemas_estruturados.append([titulo.upper(), "Cruz e Souza", corpo])
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

ficheiro_saida = "poemas_cruz_e_souza.csv"

try:
    processar_txt_poemas(ficheiro_entrada, ficheiro_saida)
except Exception as e:
    print(f"Ocorreu um erro ao processar o TXT: {e}")