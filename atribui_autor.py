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
        "PROFISSÃO DE FÉ",
        "A MORTE DE TAPYR",
        "A MORTE DE TAPYR - II",
        "A MORTE DE TAPYR - III",
        "A MORTE DE TAPYR - IV",
        "A MORTE DE TAPYR - V",
        "A GONÇALVES DIAS",
        "GUERREIRA",
        "A GONÇALVES DIAS",
        "GUERREIRA",
        "A UM GRANDE HOMEM",
        "A SESTA DE NERO",
        "O INCÊNDIO DE ROMA",
        "O SONHO DE MARCO ANTÔNIO - I",
        "O SONHO DE MARCO ANTÔNIO - II",
        "O SONHO DE MARCO ANTÔNIO - III",
        "VIA LÁCTEA - I",
        "VIA LÁCTEA - II",
        "VIA LÁCTEA - III",
        "VIA LÁCTEA - IV",
        "VIA LÁCTEA - V",
        "VIA LÁCTEA - VI",
        "VIA LÁCTEA - VII",
        "VIA LÁCTEA - VIII",
        "VIA LÁCTEA - IX",
        "VIA LÁCTEA - X",
        "VIA LÁCTEA - XI",
        "VIA LÁCTEA - XII",
        "VIA LÁCTEA - XIII",
        "VIA LÁCTEA - XIV",
        "VIA LÁCTEA - XV",
        "VIA LÁCTEA - XVI",
        "VIA LÁCTEA - XVII",
        "VIA LÁCTEA - XVIII",
        "VIA LÁCTEA - XIX",
        "VIA LÁCTEA - XX",
        "VIA LÁCTEA - XXI",
        "VIA LÁCTEA - XXII",
        "VIA LÁCTEA - XXIII",
        "VIA LÁCTEA - XXIV",
        "VIA LÁCTEA - XXV",
        "VIA LÁCTEA - XXVI",
        "VIA LÁCTEA - XXVII",
        "VIA LÁCTEA - XXVIII",
        "VIA LÁCTEA - XXIX",
        "O coração que sofre, separado",
        "SARÇAS DE FOGO NA THEBAIDA",
        "E nestas noites sossegadas",
        "NUMA CONCHA",
        "SUPPLICA",
        "CANÇÃO",
        "RIO ABAIXO",
        "PARÁFRASE DE BAUDELAIRE",
        "RIOS E PÂNTANOS",
        "DE VOLTA DO BAILE",
        "SAHARA",
        "BEIJO ETERNO",
        "POMBA E CHACAL",
        "MEDALHA ANTIGA",
        "NO CÁRCERE",
        "OLHANDO A CORRENTE",
        "NEL MEZZO DEL CAMIN..."
        "SOLITUDO",
        "A CANÇÃO DE ROMEU",
        "A TENTAÇÃO DE XENÓKRATES",
        "A TENTAÇÃO DE XENÓKRATES - II",
        "A TENTAÇÃO DE XENÓKRATES - III",
        "A TENTAÇÃO DE XENÓKRATES - IV",
        "A AVENIDA DAS LÁGRIMAS (A um Poeta morto)",
        "INANIA VERBA",
        "MIDSUMMER NIGHT’S DREAM",
        "MATER",
        "INCONTENTADO",
        "SONHO",
        "PRIMAVERA",
        "DORMINDO",
        "NOCTURNO",
        "VIRGENS MORTAS",
        "O CAVALLEIRO POBRE",
        "IDA",
        "NOITE DE INVERNO",
        "VANITAS",
        "TERCETOSI",
        "II",
        "IN EXTREMIS",
        "A ALVORADA DO AMOR",
        "VITA NUOVA",
        "MANHÃ DE VERÃO",
        "DENTRO DA NOITE",
        "CAMPO SANTO",
        "DESTERRO",
        "ROMEU E JULIETA",
        "VINHA DE NABOT",
        "SACRILÉGIO",
        "ESTÂNCIAS - I",
        "ESTÂNCIAS - II",
        "ESTÂNCIAS - III",
        "ESTÂNCIAS - IV",
        "PECADOR",
        "REI DESTHRONADO",
        "SONETO",
        "A UM VIOLINISTA",
        "A UM VIOLINISTA - II",
        "EM UMA TARDE DE OUTONO",
        "BALADAS ROMÂNTICAS",
        "BALADAS ROMÂNTICAS II — Azul",
        "III — Verde",
        "IV — Negra",
        "VELHA PÁGINA",
        "I — O Castelo",
        "II — As fadas da lagoa",
        "III — O Remorso",
        "IV — O Castigo",
        "TÉDIO",
        "REQUIESCAT",
        "SURDINA",
        "ÚLTIMA PÁGINA",
        "AS VIAGENSI — Primeira migração",
        "II — Os Fenícios",
        "III — Israel",
        "IV — Alexandre",
        "V — César",
        "VI — Os bárbaros",
        "VII — As cruzadas",
        "XI — O Polo",
        "XII — A Morte",
        "XIII — A Missão de Purna",
        "AS VIAGENS (continuação)",
        "XIV — Sagres",
        "EPISÓDIO DA EPOPÉIA SERTANISTA NO SÉCULO - II",
        "outro - III",
        "O CAÇADOR DE ESMERALDAS (continuação) - IV",
        "O CAÇADOR DE ESMERALDAS (continuação) - V"

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
            
        poemas_estruturados.append([titulo.upper(), "Olavo Bilac", corpo])
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

ficheiro_saida = "poemas_olavo_bilac.csv"

try:
    processar_txt_poemas(ficheiro_entrada, ficheiro_saida)
except Exception as e:
    print(f"Ocorreu um erro ao processar o TXT: {e}")