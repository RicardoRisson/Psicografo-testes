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
        "Beatrice",
        "Pepa - I",
        "Pepa - II",
        "Pepa - III",
        "Pepa - IV",
        "Pepa - V",
        "Pepa - VI",
        "Pepa - VII",
        "Pepa - VIII",
        "Pepa - IX",
        "Pepa - X",
        "Pepa - XI",
        "Pepa - XII",
        "Pepa - XIII",
        "Pepa - XIV",
        "Pepa - XV",
        "Pepa - XVI",
        "Idílio Sonhado - I",
        "Idílio Sonhado - II",
        "Idílio Sonhado - III",
        "Idílio Sonhado - IV",
        "Maria - I",
        "Maria - II",
        "Maria - III",
        "Maria - IV",
        "Maria - V",
        "Maria - VI",
        "Maria - VII",
        "Maria - VIII",
        "Maria - IX",
        "Maria - X",
        "Maria - XI",
        "Maria - XII",
        "Maria - XIII",
        "Maria - XIV",
        "A GUITARRA - I",
        "A GUITARRA - II",
        "A GUITARRA - III",
        "A GUITARRA - IV",
        "A GUITARRA - V",
        "A GUITARRA - VI",
        "AO LUAR - I",
        "AO LUAR - II",
        "LIMOEIRO VERDE - I",
        "LIMOEIRO VERDE - II",
        "AMOR ALEGRE",
        "Poesias Diversas - I",
        "Poesias Diversas - II",
        "Poesias Diversas - III",
        "Poesias Diversas - IV",
        "Poesias Diversas - V",
        "Poesias Diversas - VI",
        "Poesias Diversas - VII",
        "Poesias Diversas - VIII",
        "Poesias Diversas - IX",
        "Poesias Diversas - X",
        "Poesias Diversas - RESPOSTA",
        "Poesias Diversas - XI",
        "Poesias Diversas - XII",
        "Poesias Diversas - XIII",
        "Poesias Diversas - XIV",
        "Poesias Diversas - XV",
        "Poesias Diversas - XVI",
        "Poesias Diversas - XVII",
        "SAUDADES PAGÃS - I",
        "SAUDADES PAGÃS - II",
        "SAUDADES PAGÃS - III",
        "SAUDADES PAGÃS - IV",
        "SAUDADES PAGÃS - V",
        "SAUDADES PAGÃS - VI",
        "SAUDADES PAGÃS - VII",
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
            
        poemas_estruturados.append([titulo.upper(), "Antero de Quental", corpo])
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
ficheiro_saida = "poemas_antero_de_quental.csv"

try:
    processar_txt_poemas(ficheiro_entrada, ficheiro_saida)
except Exception as e:
    print(f"Ocorreu um erro ao processar o TXT: {e}")