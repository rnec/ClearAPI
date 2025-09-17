#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Algoritmo para ler e processar URLs do arquivo urls_clear.txt
Autor: Assistente IA
Data: 2025-09-15
"""

import os
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class URLEntry:
    """Classe para representar uma entrada de URL com sua categoria"""
    url: str
    category: str
    line_number: int


class URLReader:
    """Classe para ler e processar URLs do arquivo urls_clear.txt"""
    
    def __init__(self, file_path: str = "urls_clear.txt"):
        """
        Inicializa o leitor de URLs
        
        Args:
            file_path (str): Caminho para o arquivo de URLs
        """
        self.file_path = Path(file_path)
        self.urls: List[URLEntry] = []
        self.categories: Dict[str, List[URLEntry]] = {}
        
    def read_file(self) -> bool:
        """
        Lê o arquivo de URLs e processa seu conteúdo
        
        Returns:
            bool: True se o arquivo foi lido com sucesso, False caso contrário
        """
        if not self.file_path.exists():
            print(f"Erro: Arquivo '{self.file_path}' não encontrado!")
            return False
            
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            self._process_lines(lines)
            self._organize_by_categories()
            
            print(f"Arquivo lido com sucesso! {len(self.urls)} URLs encontradas.")
            return True
            
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False
    
    def _process_lines(self, lines: List[str]) -> None:
        """
        Processa as linhas do arquivo, extraindo URLs e suas categorias
        
        Args:
            lines (List[str]): Lista de linhas do arquivo
        """
        current_category = "Geral"
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Ignora linhas vazias
            if not line:
                continue
                
            # Identifica categorias (comentários que não começam com "# URLs")
            if line.startswith('#') and not line.startswith('# URLs'):
                # Remove o # e espaços para obter o nome da categoria
                category_match = re.match(r'^#\s*(.+)$', line)
                if category_match:
                    potential_category = category_match.group(1).strip()
                    # Só considera como categoria se não contém "URLs" e não é muito longo
                    if "URLs" not in potential_category and len(potential_category) < 50:
                        current_category = potential_category
                continue
            
            # Ignora outras linhas de comentário
            if line.startswith('#'):
                continue
                
            # Verifica se a linha contém uma URL válida
            if self._is_valid_url(line):
                url_entry = URLEntry(
                    url=line,
                    category=current_category,
                    line_number=line_num
                )
                self.urls.append(url_entry)
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Verifica se uma string é uma URL válida
        
        Args:
            url (str): String para verificar
            
        Returns:
            bool: True se for uma URL válida
        """
        url_pattern = re.compile(
            r'^https?://'  # http:// ou https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domínio
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # porta opcional
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def _organize_by_categories(self) -> None:
        """Organiza as URLs por categorias"""
        self.categories = {}
        for url_entry in self.urls:
            if url_entry.category not in self.categories:
                self.categories[url_entry.category] = []
            self.categories[url_entry.category].append(url_entry)
    
    def get_all_urls(self) -> List[str]:
        """
        Retorna todas as URLs como uma lista de strings
        
        Returns:
            List[str]: Lista com todas as URLs
        """
        return [url_entry.url for url_entry in self.urls]
    
    def get_urls_by_category(self, category: str) -> List[str]:
        """
        Retorna URLs de uma categoria específica
        
        Args:
            category (str): Nome da categoria
            
        Returns:
            List[str]: Lista de URLs da categoria
        """
        if category in self.categories:
            return [url_entry.url for url_entry in self.categories[category]]
        return []
    
    def get_categories(self) -> List[str]:
        """
        Retorna lista de todas as categorias disponíveis
        
        Returns:
            List[str]: Lista de categorias
        """
        return list(self.categories.keys())
    
    def print_summary(self) -> None:
        """Imprime um resumo das URLs lidas"""
        print(f"\n{'='*50}")
        print("RESUMO DAS URLs LIDAS")
        print(f"{'='*50}")
        print(f"Total de URLs: {len(self.urls)}")
        print(f"Total de categorias: {len(self.categories)}")
        print(f"\nCategorias encontradas:")
        
        for category, urls in self.categories.items():
            print(f"  • {category}: {len(urls)} URLs")
    
    def print_urls_by_category(self, category: Optional[str] = None) -> None:
        """
        Imprime URLs organizadas por categoria
        
        Args:
            category (Optional[str]): Categoria específica para imprimir (None para todas)
        """
        if category and category not in self.categories:
            print(f"Categoria '{category}' não encontrada!")
            return
            
        categories_to_print = [category] if category else self.categories.keys()
        
        for cat in categories_to_print:
            print(f"\n[{cat.upper()}]")
            print("-" * (len(cat) + 2))
            for url_entry in self.categories[cat]:
                print(f"  {url_entry.url}")
    
    def save_urls_to_file(self, output_file: str, category: Optional[str] = None) -> bool:
        """
        Salva URLs em um arquivo de texto
        
        Args:
            output_file (str): Nome do arquivo de saída
            category (Optional[str]): Categoria específica (None para todas)
            
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            urls_to_save = []
            
            if category:
                if category not in self.categories:
                    print(f"Categoria '{category}' não encontrada!")
                    return False
                urls_to_save = self.get_urls_by_category(category)
                header = f"URLs da categoria: {category}\n"
            else:
                urls_to_save = self.get_all_urls()
                header = "Todas as URLs extraídas\n"
            
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(header)
                file.write(f"Total: {len(urls_to_save)} URLs\n")
                file.write("=" * 50 + "\n\n")
                
                for url in urls_to_save:
                    file.write(f"{url}\n")
            
            print(f"URLs salvas em '{output_file}' com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
            return False


def main():
    """Função principal para demonstrar o uso da classe URLReader"""
    print("Algoritmo de Leitura de URLs - Clear API")
    print("=" * 50)
    
    # Cria uma instância do leitor
    reader = URLReader("urls_clear.txt")
    
    # Lê o arquivo
    if not reader.read_file():
        return
    
    # Exibe resumo
    reader.print_summary()
    
    # Menu interativo
    while True:
        print(f"\n{'='*50}")
        print("OPÇÕES DISPONÍVEIS:")
        print("1. Ver todas as URLs")
        print("2. Ver URLs por categoria")
        print("3. Listar categorias")
        print("4. Salvar URLs em arquivo")
        print("5. Sair")
        print("=" * 50)
        
        choice = input("Escolha uma opção (1-5): ").strip()
        
        if choice == '1':
            print(f"\n{'='*50}")
            print("TODAS AS URLs:")
            print("=" * 50)
            reader.print_urls_by_category()
            
        elif choice == '2':
            categories = reader.get_categories()
            print(f"\nCategorias disponíveis:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            
            try:
                cat_choice = int(input("Escolha o número da categoria: ")) - 1
                if 0 <= cat_choice < len(categories):
                    selected_category = categories[cat_choice]
                    print(f"\n{'='*50}")
                    print(f"URLs DA CATEGORIA: {selected_category.upper()}")
                    print("=" * 50)
                    reader.print_urls_by_category(selected_category)
                else:
                    print("Opção inválida!")
            except ValueError:
                print("Por favor, digite um número válido!")
                
        elif choice == '3':
            print(f"\n{'='*50}")
            print("CATEGORIAS DISPONÍVEIS:")
            print("=" * 50)
            for i, category in enumerate(reader.get_categories(), 1):
                count = len(reader.get_urls_by_category(category))
                print(f"{i:2d}. {category} ({count} URLs)")
                
        elif choice == '4':
            output_file = input("Nome do arquivo de saída (ex: urls_output.txt): ").strip()
            if not output_file:
                output_file = "urls_output.txt"
            
            save_all = input("Salvar todas as URLs? (s/n): ").strip().lower()
            if save_all in ['s', 'sim', 'y', 'yes']:
                reader.save_urls_to_file(output_file)
            else:
                categories = reader.get_categories()
                print("Categorias disponíveis:")
                for i, cat in enumerate(categories, 1):
                    print(f"{i}. {cat}")
                
                try:
                    cat_choice = int(input("Escolha o número da categoria: ")) - 1
                    if 0 <= cat_choice < len(categories):
                        selected_category = categories[cat_choice]
                        reader.save_urls_to_file(output_file, selected_category)
                    else:
                        print("Opção inválida!")
                except ValueError:
                    print("Por favor, digite um número válido!")
                    
        elif choice == '5':
            print("Encerrando o programa...")
            break
            
        else:
            print("Opção inválida! Por favor, escolha entre 1-5.")


if __name__ == "__main__":
    main()

