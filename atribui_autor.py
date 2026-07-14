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
"INTRODUÇÃO",
"O VIÚVO - Parte I",
"O VIÚVO - Parte II",
"O VIÚVO - Parte III",
"O VIÚVO - Parte IV",
"O VIÚVO - Parte V",
"O VIÚVO - Parte VI",
"Capítulo I - Parte I",
"Capítulo I - Parte II",
"Capítulo I - Parte III",
"Capítulo I - Parte IV",
"Capítulo I - Parte V",
"Capítulo II - Parte I",
"Capítulo II - Parte II",
"Capítulo II - Parte III",
"Capítulo II - Parte IV",
"Capítulo III",
"QUESTÃO DE HONRA - Parte I",
"QUESTÃO DE HONRA - Parte II",
"QUESTÃO DE HONRA - Parte III",
"QUESTÃO DE HONRA - Parte IV",
"QUESTÃO DE HONRA - Parte V",
"QUESTÃO DE HONRA - Parte VI",
"Capítulo I - Parte I",
"Capítulo I - Parte II",
"Capítulo I - Parte III",
"Capítulo I - Parte IV",
"Capítulo II - Parte I",
"Capítulo II - Parte II",
"Capítulo II - Parte III",
"Capítulo I - Parte I",
"Capítulo I - Parte II",
"Capítulo I - Parte III",
"Capítulo I - Parte IV",
"Capítulo I - Parte V",
"PLEBISCITO - Parte I",
"PLEBISCITO - Parte II",
"PLEBISCITO - Parte III",
"PLEBISCITO - Parte IV",
"A PRAIA DE SANTA LUZIA - Parte I",
"A PRAIA DE SANTA LUZIA - Parte II",
"A PRAIA DE SANTA LUZIA - Parte III",
"A PRAIA DE SANTA LUZIA - Parte IV",
"A PRAIA DE SANTA LUZIA - Parte V",
"A PRAIA DE SANTA LUZIA - Parte VI",
"BLACK - Parte I",
"BLACK - Parte II",
"BLACK - Parte III",
"BLACK - Parte IV",
"A FILHA DO PATRÃO",
"Capítulo I - Parte I",
"Capítulo I - Parte II",
"Capítulo I - Parte III",
"Capítulo II",
"Capítulo III - Parte I",
"Capítulo III - Parte II",
"Capítulo III - Parte III",
"Capítulo IV",
"ARDIL - Parte I",
"ARDIL - Parte II",
"ARDIL - Parte III",
"ARDIL - Parte IV",
"ARDIL - Parte V",
"ÚTIL INDA BRINCANDO - Parte I",
"ÚTIL INDA BRINCANDO - Parte II",
"ÚTIL INDA BRINCANDO - Parte III",
"ÚTIL INDA BRINCANDO - Parte IV",
"ÚTIL INDA BRINCANDO - Parte V",
"Capítulo II - Parte I",
"Capítulo II - Parte II",
"Capítulo II - Parte III",
"Capítulo II - Parte IV",
"Capítulo II - Parte V",
"Capítulo III",
"UMA NOITE EM PETRÓPOLIS - Parte I",
"UMA NOITE EM PETRÓPOLIS - Parte II",
"UMA NOITE EM PETRÓPOLIS - Parte III",
"UMA NOITE EM PETRÓPOLIS - Parte IV",
"UMA NOITE EM PETRÓPOLIS - Parte V",
"UMA NOITE EM PETRÓPOLIS - Parte VI",
"UMA NOITE EM PETRÓPOLIS - Parte VII",
"UMA NOITE EM PETRÓPOLIS - Parte VIII",
"UMA EMBAIXADA - Parte I",
"UMA EMBAIXADA - Parte II",
"UMA EMBAIXADA - Parte III",
"UMA EMBAIXADA - Parte IV",
"UMA EMBAIXADA - Parte V",
"UMA EMBAIXADA - Parte VI",
"UMA EMBAIXADA - Parte VII",
"VINGANÇA - Parte I",
"VINGANÇA - Parte II",
"VINGANÇA - Parte III",
"VINGANÇA - Parte IV",
"VINGANÇA - Parte V",
"VINGANÇA - Parte VI",
"VINGANÇA - Parte VII",
"VINGANÇA - Parte VIII",
"VINGANÇA - Parte IX",
"COMO EU ME DIVERTI",
"ATO ÚNICO - Parte I",
"ATO ÚNICO - Parte II",
"ATO ÚNICO - Parte III",
"ATO ÚNICO - Parte IV",
"ATO ÚNICO - Parte V",
"ATO ÚNICO - Parte VI",
"A “DONA BRANCA” - Parte I",
"A “DONA BRANCA” - Parte II",
"A “DONA BRANCA” - Parte III",
"A “DONA BRANCA” - Parte IV",
"A “DONA BRANCA” - Parte V",
"A “DONA BRANCA” - Parte VI",
"O VELHO LIMA - Parte I",
"O VELHO LIMA - Parte II",
"O VELHO LIMA - Parte III",
"O VELHO LIMA - Parte IV",
"A “RÉCLAME’",
"Capítulo I - Parte I",
"Capítulo I - Parte II",
"Capítulo I - Parte III",
"Capítulo II - Parte I",
"Capítulo II - Parte II",
"Capítulo II - Parte III",
"Capítulo III",
"O CONTRABANDO",
"Capítulo I - Parte I",
"Capítulo I - Parte II",
"Capítulo I - Parte III",
"Capítulo II - Parte I",
"Capítulo II - Parte II",
"Capítulo III - Parte I",
"Capítulo III - Parte II",
"Capítulo III - Parte III",
"Capítulo III - Parte IV",
"Capítulo III - Parte V",
"Capítulo III - Parte VI",
"Capítulo III - Parte VII",
"Capítulo III - Parte VIII",
"Capítulo IV",
"Capítulo V - Parte I",
"Capítulo V - Parte II",
"Capítulo VI - Parte I",
"Capítulo VI - Parte II",
"Capítulo VI - Parte III",
"Capítulo I",
"Capítulo II - Parte I",
"Capítulo II - Parte II",
"Capítulo III",
"Capítulo IV - Parte I",
"Capítulo IV - Parte II",
"Capítulo V",
"Capítulo I - Parte I",
"Capítulo I - Parte II",
"Capítulo II - Parte I",
"Capítulo II - Parte II",
"Capítulo II - Parte III",
"Capítulo II - Parte IV",
"Capítulo III"    ]

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
            
        poemas_estruturados.append([titulo.upper(), "Artur Azevedo", corpo])
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
ficheiro_saida = "poemas_artur_azevedo.csv"

try:
    processar_txt_poemas(ficheiro_entrada, ficheiro_saida)
except Exception as e:
    print(f"Ocorreu um erro ao processar o TXT: {e}")