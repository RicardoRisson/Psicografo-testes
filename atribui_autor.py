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
        "Monólogo de uma sombra",
        "Agonia de um filósofo",
        "O Morcego",
        "Psicologia de um vencido",
        "A Idéia",
        "O Lázaro da pátria",
        "IDEALIZAÇÃO DA HUMANIDADE FUTURA",
        "SONETO",
        "VERSOS A UM CÃO",
        "O DEUS-VERME",
        "DEBAIXO DO TAMARINDO",
        "AS CISMAS DO DESTINO - I",
        "AS CISMAS DO DESTINO - II",
        "AS CISMAS DO DESTINO - III",
        "AS CISMAS DO DESTINO - IV",
        "BUDISMO MODERNO",
        "SONHO DE UM MONISTA",
        "SOLITÁRIO",
        "MATER ORIGINALIS",
        "O LUPANAR",
        "IDEALISMO",
        "ÚLTIMO CREDO",
        "O CAIXÃO FANTÁSTICO",
        "SOLILÓQUIO DE UM VISIONÁRIO",
        "A UM CARNEIRO MORTO",
        "VOZES DA MORTE",
        "INSÂNIA DE UM SIMPLES",
        "OS DOENTES - I",
        "OS DOENTES - II",
        "OS DOENTES - III",
        "OS DOENTES - IV",
        "OS DOENTES - V",
        "OS DOENTES - VI",
        "OS DOENTES - VII",
        "OS DOENTES - VIII",
        "OS DOENTES - IX",
        "ASA DE CORVO",
        "UMA NOITE NO CAIRO",
        "O MARTÍRIO DO ARTISTA",
        "DUAS ESTROFES",
        "DECADÊNCIA",
        "RICORDANZA DELLA MIA GIOVENTÚ",
        "A UM MASCARADO",
        "VOZES DE UM TÚMULO",
        "CONTRASTES",
        "Gemidos de arte - I",
        "Gemidos de arte - II",
        "Gemidos de arte - III",
        "VERSOS DE AMOR",
        "SONETOS - I",
        "SONETOS - II",
        "SONETOS - III",
        "DEPOIS DA ORGIA",
        "A ÁRVORE DA SERRA",
        "VENCIDO",
        "O CORRUPIÃO",
        "NOITE DE UM VISIONÁRIO",
        "ALUCINAÇÃO À BEIRA-MAR",
        "VANDALISMO",
        "VERSOS ÍNTIMOS",
        "VENCEDOR",
        "A ILHA DE CIPANGO",
        "MATER",
        "POEMA NEGRO",
        "ETERNA MÁGOA",
        "QUEIXAS NOTURNAS",
        "INSÔNIA",
        "BARCAROLA",
        "TRISTEZAS DE UM QUARTO MINGUANTE",
        "MISTÉRIOS DE UM FÓSFORO",
        "O LAMENTO DAS COISAS",
        "O MEU NIRVANA",
        "CAPUT IMMORTALE",
        "APÓSTROFE À CARNE",
        "LOUVOR À UNIDADE",
        "O PÂNTANO",
        "SUPRÊME CONVULSION",
        "A UM GÉRMEN",
        "NATUREZA ÍNTIMA",
        "A FLORESTA",
        "A MERETRIZ",
        "GUERRA",
        "O SARCÓFAGO",
        "HINO À DOR",
        "ULTIMA VISIO",
        "AOS MEUS FILHOS",
        "A DANÇA DA PSIQUE",
        "O POETA DO HEDIONDO",
        "A FOME E O AMOR",
        "HOMO INFIMUS",
        "MINHA FINALIDADE",
        "NUMA FORJA",
        "NOLI ME TANGERE",
        "O CANTO DOS PRESOS",
        "ABERRAÇÃO",
        "VÍTIMA DO DUALISMO",
        "AO LUAR",
        "A UM EPILÉTICO",
        "CANTO DE ONIPOTÊNCIA",
        "MINHA ÁRVORE",
        "ANSEIO",
        "À MESA",
        "MÃOS",
        "Revelação - I",
        "Revelação - II",
        "VERSOS A UM COVEIRO",
        "TREVAS",
        "AS MONTANHAS - I",
        "AS MONTANHAS - II",
        "APOCALIPSE",
        "A NAU",
        "VOLÚPIA IMORTAL",
        "O FIM DAS COISAS",
        "VIAGEM DE UM VENCIDO",
        "A NOITE",
        "A OBSESSÃO DO SANGUE",
        "VOX VICTIMAE",
        "O ÚLTIMO NÚMERO",
        "MÁGOAS",
        "O CONDENADO",
        "SONETO",
        "INFELIZ",
        "SONETO",
        "NOIVADO",
        "SONETO",
        "TRISTE REGRESSO",
        "AMOR E RELIGIÃO",
        "SONETO",
        "SAUDADE",
        "A ESMOLA DE DULCE",
        "SONETO",
        "O MAR",
        "SONETO",
        "SONETO",
        "CRAVO DE NOIVA",
        "PLENILÚNIO",
        "CÍTARA MÍSTICA",
        "SÚPLICA NUM TÚMULO",
        "AFETOS",
        "MARTÍRIO SUPREMO",
        "RÉGIO",
        "MÁRTIR DA FOME",
        "FESTIVAL",
        "NOTURNO",
        "SONETO",
        "O NEGRO",
        "SENECTUDE PRECOCE",
        "ANDRÉ CHÉNIER",
        "MYSTICA VISIO",
        "ILUSÃO",
        "GOZO INSATISFEITO",
        "DOLÊNCIAS",
        "IDEALIZAÇÕES - I",
        "IDEALIZAÇÕES - II",
        "IDEALIZAÇÕES - III",
        "IDEALIZAÇÕES - IV",
        "IDEALIZAÇÕES - V",
        "A VITÓRIA DO ESPÍRITO",
        "CANTO ÍNTIMO",
        "A LUVA",
        "A CARIDADE",
        "ABANDONADA",
        "ABANDONADA",
        "CETICISMO",
        "A MÁSCARA",
        "O COVEIRO",
        "PECADORA",
        "NO CLAUSTRO",
        "IL TROVATORE",
        "A LOUCA",
        "PRIMAVERA",
        "A ESPERANÇA",
        "SONETO",
        "SOFREDORA",
        "ECOS D’ALMA",
        "AMOR E CRENÇA",
        "ARANA",
        "TEMPOS IDOS",
        "SONETO",
        "SONETO",
        "A AERONAVE",
        "LIRIAL",
        "A MINHA ESTRELA",
        "SONETO",
        "VERSOS D’UM EXILADO",
        "AVE DOLOROSA",
        "NIMBUS",
        "NO CAMPO",
        "INSÂNIA",
        "O BANDOLIM",
        "ARA MALDITA",
        "SONETO",
        "TREVA E LUZ",
        "SONETO",
        "A PESTE",
        "IDEAL",
        "SOMBRA IMORTAL",
        "CORAÇÃO FRIO",
        "NOTURNO",
        "SEDUTORA",
        "PELO MUNDO",
        "SONETO",
        "O RISO",
        "SONETO",
        "A UM MÁRTIR",
        "PELO MAR",
        "PALLIDA LUNA",
        "A MORTE DE VÊNUS",
        "SONHO DE AMOR",
        "SONETO",
        "SONETO",
        "VAE VICTIS",
        "A DOR",
        "TERRA FÚNEBRE",
        "SONETO",
        "MEDITANDO",
        "SONETO",
        "O ÉBRIO",
        "O CANTO DA CORUJA",
        "NOME MALDITO",
        "DOLÊNCIAS",
        "A LÁGRIMA",
        "AVE LIBERTAS",
        "QUADRAS",
        "VÊNUS MORTA",
        "ODE AO AMOR",
        "CANTO DE AGONIA",
        "História de um vencido - I",
        "História de um vencido - II",
        "ESTROFES SENTIDAS",
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
            
        poemas_estruturados.append([titulo.upper(), "Augusto dos Anjos", corpo])
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
ficheiro_entrada = "EUaugustoanjos.txt"
ficheiro_saida = "poemas_augusto_dos_anjos.csv"

try:
    processar_txt_poemas(ficheiro_entrada, ficheiro_saida)
except Exception as e:
    print(f"Ocorreu um erro ao processar o TXT: {e}")