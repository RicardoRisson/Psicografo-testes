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
        "Antonio - I",
"Antonio - II",
"Menino e Moço - I",
"Menino e Moço - II",
"Os Cavalleiros - I",
"Os Cavalleiros - II",
"Purinha - I",
"Purinha - II",
"Elegia - I",
"Elegia - II",
"Os Sinos - I",
"Os Sinos - II",
"Terças-Feiras - I",
"Terças-Feiras - II",
"Carta a Manoel - I",
"Carta a Manoel - II",
"Para As Raparigas de Coimbra - I",
"Para As Raparigas de Coimbra - II",
"Luzitania no Bairro-Latino - I",
"Luzitania no Bairro-Latino - II",
"Os Figos Pretos - I",
"Os Figos Pretos - II",
"Febre Vermelha - I",
"Febre Vermelha - II",
"Poentes de França - I",
"Poentes de França - II",
"Pobre Tysica - I",
"Pobre Tysica - II",
"A Poezia do Outomno - I",
"A Poezia do Outomno - II",
"Enterro de Ophelia - I",
"Enterro de Ophelia - II",
"Ballada do Caixão - I",
"Ballada do Caixão - II",
"Á Toa - I",
"Á Toa - II",
"A Vida - I",
"A Vida - II",
"O Somno de João - I",
"O Somno de João - II",
"Ao Canto do Lume - I",
"Ao Canto do Lume - II",
"A Sombra - I",
"A Sombra - II",
"O Meu Cachimbo - I",
"O Meu Cachimbo - II",
"Ca (ro) Da (ta) Ver (mibus) - I",
"Ca (ro) Da (ta) Ver (mibus) - II",
"Quando Chegar a Hora - I",
"Quando Chegar a Hora - II",
"Certa Velhinha - I",
"Certa Velhinha - II",
"Males de Anto - I",
"Males de Anto - II",
"Ah Deixem-me Dormir! - I",
"Ah Deixem-me Dormir! - II",
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
            
        poemas_estruturados.append([titulo.upper(), "Antônio Nobre", corpo])
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
ficheiro_saida = "poemas_antônio_nobre.csv"

try:
    processar_txt_poemas(ficheiro_entrada, ficheiro_saida)
except Exception as e:
    print(f"Ocorreu um erro ao processar o TXT: {e}")