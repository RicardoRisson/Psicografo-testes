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

    # 2. Lista de títulos exatos para o teste

    #-=~=~LEMBRAR DE ESCREVER ALGO ANTES DO PRIMEIRO TITULO SENAO BUGA E NAO PEGA=~=~-


    titulos_alvo = [
"POEMA - V",
"POEMA - NIRVANA",
"POEMA - NIRVANA - D",
"POEMA - PSICHÉ",
"POEMA - PSICHÉ - V",
"POEMA - IMAGEM DA DOR",
"POEMA - VANA",
"POEMA - HARMONIAS DE UMA NOITE DE VERÃO",
"POEMA - HARMONIAS DE UMA NOITE DE VERÃO - C",
"POEMA - A SELIA DO LEÃO",
"POEMA - MEDITAÇÕES - I",
"POEMA - MEDITAÇÕES - D",
"POEMA - LUBRICUS ANGUIS",
"POEMA - LUBRICUS ANGUIS - D",
"POEMA - DESILUDIDO",
"POEMA - NUA E CRUA",
"POEMA - NUA E CRUA - D",
"POEMA - NUA E CRUA - C",
"POEMA - AMÉM!",
"POEMA - FETICHISMO",
"POEMA - DEUS IMPASSÍVEL",
"POEMA - VAE VICTIS!",
"POEMA - DIÁLOGOS - I",
"POEMA - GREEN SPOT",
"POEMA - GREEN SPOT - D",
"POEMA - PÉLAGO INVISÍVEL",
"POEMA - HINO A CÓLERA",
"POEMA - BÁLSAMO NOS PRANTOS",
"POEMA - BÁLSAMO NOS PRANTOS - C",
"POEMA - PAPÉIS-VELHOS",
"POEMA - UM FRAGMENTO - I",
"POEMA - UM FRAGMENTO - V",
"POEMA - A SOMBRA DA MORTE",
"POEMA - VERBO LIBERTADOR",
"POEMA - SOBRE A MORTE DE JOSÉ BONIFÁCIO",
"POEMA - ONDAS... - I",
"POEMA - ONDAS... - V",
"POEMA - AMOR CRIADOR",
"POEMA - AMOR CRIADOR - C",
"POEMA - PAZ ENTRE OS HOMENS",
"POEMA - CAUCHEMAR",
"POEMA - MAZZEPA",
"POEMA - BANZO",
"POEMA - BANZO - V",
"POEMA - BANZO - D",
"POEMA - HORÓSCOPO",
"POEMA - ÚLTIMO PORTO",
"POEMA - ÚLTIMO PORTO - D",
"POEMA - CÍTERA",
"POEMA - ODE PARNASIANA",
"POEMA - ODE PARNASIANA - D",
"POEMA - BEIJOS DO CÉU",
"POEMA - MISSA DA RESSURREIÇÃO",
"POEMA - MISSA DA RESSURREIÇÃO - D",
"POEMA - MISSA DA RESSURREIÇÃO - M",
"POEMA - A UMA CANTORA",
"POEMA - A UMA CANTORA - C",
"POEMA - NUVEM BRANCA",
"POEMA - NUVEM BRANCA - D",
"POEMA - IXION",
"POEMA - CONCHITA",
"POEMA - JÉSSICA",
"POEMA - ZULMIRA",
"POEMA - ANIMA CHLORIDIS",
"POEMA - SONHO TURCO",
"POEMA - SONHO TURCO - V",
"POEMA - SONHO TURCO - M",
"POEMA - NO ANIVERSÁRIO DE UM POETA",
"POEMA - NO ANIVERSÁRIO DE UM POETA - C",
"POEMA - SOZINHA",
"POEMA - PRIMEIRAS VIGÍLIAS",
"POEMA - PRIMEIRAS VIGÍLIAS - D",
"POEMA - A FLOR AZUL",
"POEMA - VÉSPER",
"POEMA - VÉSPER - D",
"POEMA - POEMA DA NOITE",
"POEMA - TRISTEZA DE MOMO",
"POEMA - EVITERNO AMOR",
"POEMA - DOLORES",
"POEMA - FILOMELA",
"POEMA - MOFA E DESPEITO",
"POEMA - EMISSÁRIO DOS DEUSES",
"POEMA - O VELHO E A TABELIÃO",
"POEMA - A ESTÁTUA DE JÚPITER",
"POEMA - A ESTÁTUA DE JÚPITER - L",
"POEMA - VICTOR HUGO",
"POEMA - EPOPÉIA DO LEÃO",
"POEMA - EPOPÉIA DO LEÃO - V",
"POEMA - EPOPÉIA DO LEÃO - C",
"POEMA - EPOPÉIA DO LEÃO - VI",
"POEMA - BIOGRAFIA"
    ]

    # Cria a lista removendo as duplicatas mantendo a ordem para o relatório visual
    titulos_unicos = []
    for t in titulos_alvo:
        t_limpo = t.strip()
        if t_limpo and t_limpo not in titulos_unicos:
            titulos_unicos.append(t_limpo)
    
    # Expressão regular corrigida usando 'titulos_unicos'
    padrao_busca = r"\n\s*(" + "|".join([r"\s+".join([re.escape(p) for p in t.split()]) for t in titulos_unicos]) + r")\s*\n"
    
    # Faz o corte preciso do texto com base nos títulos fornecidos
    partes = re.split(padrao_busca, texto_completo, flags=re.IGNORECASE)
    
    poemas_estruturados = []
    titulos_encontrados_normalizados = set()
    
    # Extração dos poemas do resultado do split
    i = 1
    while i < len(partes) - 1:
        titulo = partes[i].strip()
        corpo = partes[i+1].strip()
        
        if "FIM" in corpo:
            corpo = corpo.split("FIM")[0].strip()
            
        poemas_estruturados.append([titulo.upper(), "Raimundo Correia", corpo])
        titulos_encontrados_normalizados.add(titulo.lower())
        i += 2

    # --- Relatório de Verificação no Terminal ---
    print("\n📊 --- RELATÓRIO DE TÍTULOS ---")
    for t in titulos_unicos:
        if t.lower() in titulos_encontrados_normalizados:
            print(f"[✓] {t}")
        else:
            print(f"[X] {t}")
    print("--------------------------------\n")

    # 3. Guardar o resultado final no formato CSV esperado
    with open(caminho_csv, mode='w', newline='', encoding='utf-8-sig') as f:
        escritor = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        escritor.writerow(['titulo', 'autor', 'texto'])
        escritor.writerows(poemas_estruturados)

    print(f"✨ Sucesso! Foram extraídos {len(poemas_estruturados)} poemas com base nos títulos fornecidos.")
    print(f"Ficheiro guardado em: '{caminho_csv}'")

# --- Execução do Script ---
ficheiro_entrada = "EU.txt"
ficheiro_saida = "aleluias_raimundo_correia.csv"

try:
    processar_txt_poemas(ficheiro_entrada, ficheiro_saida)
except Exception as e:
    print(f"Ocorreu um erro ao processar o TXT: {e}")