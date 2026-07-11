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
"POEMA - D",
"POEMA - LUZ MEDITERRÂNE",
"POEMA - LUZ MEDITERRÂNE - C",
"POEMA - LUZ MEDITERRÂNE - M",
"POEMA - HISTÓRIEUM LM",
"POEMA - HISTÓRIEUM LM - IIIC",
"POEMA - FELICID DE",
"POEMA - FELICID DE - I",
"POEMA - FELICID DE - C",
"POEMA - FELICID DE - IM",
"POEMA - FELICID DE - VIV",
"POEMA - FELICID DE - D",
"POEMA - FELICID DE - DI",
"POEMA - POEM SIN C B DOS",
"POEMA - POEM SIN C B DOS - D",

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
            
        poemas_estruturados.append([titulo.upper(), "Raul de Leoni", corpo])
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
ficheiro_saida = "poemas_raul_de_leoni.csv"

try:
    processar_txt_poemas(ficheiro_entrada, ficheiro_saida)
except Exception as e:
    print(f"Ocorreu um erro ao processar o TXT: {e}")