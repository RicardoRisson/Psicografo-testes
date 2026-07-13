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
"APARIÇÃO NAS ÁGUAS - I",
"APARIÇÃO NAS ÁGUAS - II",
"APARIÇÃO NAS ÁGUAS - III",
"APARIÇÃO NAS ÁGUAS - IV",
"APARIÇÃO NAS ÁGUAS - V",
"APARIÇÃO NAS ÁGUAS - VI",
"VAPOROSA - I",
"III - O ÍDOLO - A MANHÃES DE CAMPOS",
"IV - TRINDADES - AO DR FERREIRA DE ARAÚJO",
"V - CALMA NO MAR - IMITAÇÃO DE MIÇKIEWICZ",
"VI - TENEBROSA",
"VII - O COLAR",
"VIII - À SOMBRA DAS ÁRVORES",
"IX - QUADRO ANTIGO - A TEÓFILO DIAS",
"X - O PRIMEIRO BEIJO",
"XI - VISÃO DAS RUÍNAS - A L. NICOLI.",
"XII - INTERIOR - A TOMÁS ALVES FILHO",
"XIII - ONDULAÇÕES",
"XIV - TRIUNFO SATÂNICO - A PEDRO PAULO DO AMARAL.",
"XV - NA ALAMEDA - A MARIANO DE OLIVEIRA",
"XVI - TOILETTE LÍRICO - A BELISÁRIO DE SOUZA",
"S1",
"S2",
"XX - MÍSTICA - A JOAQUIM MALDONADO - I",
"XX - MÍSTICA - A JOAQUIM MALDONADO - II",
"XX - MÍSTICA - A JOAQUIM MALDONADO - III",
"XXI - AO SOL POENTE - A ARTUR AZEVEDO",
"XXII",
"XXIII",
"XXIV - TORTURAS DO IDEAL - A JOSÉ DO PATROCÍNIO - I",
"XXIV - TORTURAS DO IDEAL - A JOSÉ DO PATROCÍNIO - II",
"XXIV - TORTURAS DO IDEAL - A JOSÉ DO PATROCÍNIO - III",
"XXIV - TORTURAS DO IDEAL - A JOSÉ DO PATROCÍNIO - IV",
"XXIV - TORTURAS DO IDEAL - A JOSÉ DO PATROCÍNIO - V",
"VI - Vozes no ar",
"VII",
"VIII",
"IX",
"X - I",
"X - II",
"X - III",
"X - IV",
"X - V",
"X - XI",
"X - XII",
"X - XIII",
"XXV - A FONTOURA XAVIER",
"XXVI - O MÊS DE OUTUBRO - A ARTUR AZEVEDO",
"XXVII - LUZ NOVA - A A. BARREIROS - I",
"XXVII - LUZ NOVA - A A. BARREIROS - II",
"XXVII - LUZ NOVA - A A. BARREIROS - III",
"XXVII - LUZ NOVA - A A. BARREIROS - IV",
"XXVII - LUZ NOVA - A A. BARREIROS - V",
"XXVII - LUZ NOVA - A A. BARREIROS - VI",
"XXVII - LUZ NOVA - A A. BARREIROS - VII",
"XXVII - LUZ NOVA - A A. BARREIROS - VIII",
"XXVII - LUZ NOVA - A A. BARREIROS - IX",
"XXVII - LUZ NOVA - A A. BARREIROS - X",
"XXVII - LUZ NOVA - A A. BARREIROS - XI",
"XXVII - LUZ NOVA - A A. BARREIROS - XII",
"XXVII - LUZ NOVA - A A. BARREIROS - XIII"
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
            
        poemas_estruturados.append([titulo.upper(), "Alberto de Oliveira", corpo])
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
ficheiro_saida = "poemas_alberto_de_oliveira.csv"

try:
    processar_txt_poemas(ficheiro_entrada, ficheiro_saida)
except Exception as e:
    print(f"Ocorreu um erro ao processar o TXT: {e}")