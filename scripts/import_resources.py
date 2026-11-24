#!/usr/bin/env python3
"""Import public course fields from an .xlsx workbook into src/resources.json."""

import json
import posixpath
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse
from zipfile import ZipFile
from xml.etree import ElementTree


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"m": MAIN_NS, "r": REL_NS, "p": PKG_REL_NS}

BUSINESS_TERMS = (
    "administracao financeira", "administracao", "empreend", "negocio",
    "empresa", "gestao", "financ", "contab", "marketing", "venda",
    "comerc", "estoque", "projeto", "recursos humanos", "rh", "econom",
    "publicidade", "tribut", "precific", "fluxo de caixa", "empreendedor",
    "copywriting", "inbound", "seo", "growth hacking", "lideranca",
    "organizacional", "gestor", "tga", "funcao adm", "adm.",
)
STRONG_BUSINESS_TERMS = (
    "empreend", "negocio", "empresa", "financ", "contab", "marketing",
    "venda", "comerc", "estoque", "recursos humanos", "rh", "econom",
    "publicidade", "tribut", "precific", "fluxo de caixa", "copywriting",
    "inbound", "seo", "growth hacking",
)
CAREER_TERMS = (
    "carreira", "vaga", "emprego", "profissao", "profissional",
    "mercado de trabalho", "salarial", "salario", "concurso",
    "curriculo", "estagio", "empregabilidade",
)
PERSONAL_GROWTH_TERMS = (
    "crescimento pessoal", "autoconhecimento", "felicidade",
    "bem-estar", "bem estar", "saude mental", "mindfulness",
    "meditacao", "relacionamento", "psicologia",
    "comunicacao nao-violenta", "comunicacao nao violenta",
)
BUSINESS_AREAS = {"administracao", "marketing", "ciencias contabeis"}
NON_BUSINESS_CATEGORIES = {
    "saude", "ciencias", "farmacologia", "emergencia", "anatomia",
    "nutricao", "psicologia", "literatura", "urbanismo",
}


def normalize(value):
    value = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in value if not unicodedata.combining(char))


def cell_text(cell, shared_strings):
    value = cell.find("m:v", NS)
    inline = cell.find("m:is", NS)
    text = value.text if value is not None and value.text else ""
    if cell.attrib.get("t") == "s" and text:
        return shared_strings[int(text)].strip()
    if inline is not None:
        return "".join(item.text or "" for item in inline.findall(".//m:t", NS)).strip()
    return text.strip()


def resolve_path(target):
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join("xl", target))


def sheet_hyperlinks(archive, sheet_path):
    relationship_path = posixpath.join(
        posixpath.dirname(sheet_path),
        "_rels",
        posixpath.basename(sheet_path) + ".rels",
    )
    if relationship_path not in archive.namelist():
        return {}
    root = ElementTree.fromstring(archive.read(relationship_path))
    return {
        relationship.attrib["Id"]: relationship.attrib["Target"]
        for relationship in root.findall("p:Relationship", NS)
        if relationship.attrib.get("TargetMode") == "External"
    }


def classify(area, title, category, platform, format_name):
    text = normalize(" ".join((title, category, platform, format_name)))
    area_key = normalize(area)

    if any(term in text for term in CAREER_TERMS):
        if any(term in text for term in STRONG_BUSINESS_TERMS):
            return "negocios"
        return "carreiras"
    if any(term in text for term in BUSINESS_TERMS):
        return "negocios"
    if any(term in text for term in PERSONAL_GROWTH_TERMS):
        return "crescimento-pessoal"
    if area_key in BUSINESS_AREAS and normalize(category) not in NON_BUSINESS_CATEGORIES:
        return "negocios"
    return "carreiras"


def import_workbook(input_path):
    with ZipFile(input_path) as archive:
        workbook = ElementTree.fromstring(archive.read("xl/workbook.xml"))
        relationships = ElementTree.fromstring(
            archive.read("xl/_rels/workbook.xml.rels")
        )
        workbook_links = {
            relationship.attrib["Id"]: relationship.attrib["Target"]
            for relationship in relationships.findall("p:Relationship", NS)
        }
        shared_strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
            shared_strings = [
                "".join(item.text or "" for item in entry.findall(".//m:t", NS))
                for entry in root.findall("m:si", NS)
            ]

        resources = {}
        for sheet in workbook.findall("m:sheets/m:sheet", NS):
            sheet_path = resolve_path(
                workbook_links[sheet.attrib[f"{{{REL_NS}}}id"]]
            )
            root = ElementTree.fromstring(archive.read(sheet_path))
            hyperlinks = sheet_hyperlinks(archive, sheet_path)

            for row in root.findall("m:sheetData/m:row", NS)[1:]:
                values = {}
                for cell in row.findall("m:c", NS):
                    match = re.match(r"([A-Z]+)", cell.attrib.get("r", ""))
                    if not match:
                        continue
                    column = match.group(1)
                    text = cell_text(cell, shared_strings)
                    if column == "F":
                        hyperlink = root.find(
                            f".//m:hyperlink[@ref='{cell.attrib.get('r', '')}']",
                            NS,
                        )
                        if hyperlink is not None:
                            relation_id = hyperlink.attrib.get(f"{{{REL_NS}}}id")
                            text = hyperlinks.get(relation_id, text)
                    values[column] = text

                title = values.get("A", "").strip()
                if not title or normalize(title) == "nome do conteudo":
                    continue
                url = values.get("F", "").strip()
                if url:
                    parsed_url = urlparse(url)
                    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
                        url = ""

                platform = values.get("B", "").strip()
                category = values.get("C", "").strip()
                format_name = values.get("D", "").strip()
                duration = values.get("E", "").strip()
                area = sheet.attrib["name"].strip()
                key = (normalize(title), url.casefold())
                resource = resources.get(key)
                if resource is None:
                    resources[key] = {
                        "title": title,
                        "areas": [area],
                        "platform": platform,
                        "category": category,
                        "format": format_name,
                        "duration": duration,
                        "url": url,
                        "group": classify(
                            area, title, category, platform, format_name
                        ),
                    }
                elif area not in resource["areas"]:
                    resource["areas"].append(area)

        group_order = {"negocios": 0, "carreiras": 1, "crescimento-pessoal": 2}
        return sorted(
            resources.values(),
            key=lambda resource: (
                group_order[resource["group"]],
                normalize(resource["title"]),
                normalize(resource["areas"][0]),
            ),
        )


def main():
    if len(sys.argv) not in (2, 3):
        raise SystemExit(
            "Uso: python3 scripts/import_resources.py <arquivo.xlsx> [arquivo.json]"
        )
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) == 3 else Path("src/resources.json")
    resources = import_workbook(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(resources, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    linked = sum(bool(resource["url"]) for resource in resources)
    print(
        f"{len(resources)} conteúdos importados; {linked} com link de acesso; "
        f"arquivo gerado: {output_path}"
    )


if __name__ == "__main__":
    main()
