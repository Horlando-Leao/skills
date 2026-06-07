#!/usr/bin/env python3
"""
Setup Script for Agent Skills Generator

Automatiza a criação da estrutura completa de uma nova skill seguindo o padrão
agentskills.io com divulgação progressiva de contexto.

Uso:
    python scripts/setup_skill.py --name minha-skill --description "Descrição clara da skill"

Opções:
    --name              Nome da skill (obrigatório, formato: lowercase-com-hifen)
    --description       Descrição da skill (obrigatório, 1-1024 caracteres)
    --license           Licença (opcional, padrão: MIT)
    --compatibility     Requisitos de compatibilidade (opcional)
    --output-dir        Diretório de saída (opcional, padrão: ./)
    --no-assets         Não criar pasta assets/ (opcional)
    --no-scripts        Não criar pasta scripts/ (opcional)
    --no-references     Não criar pasta references/ (opcional)
"""

import argparse
import os
import re
import sys
from pathlib import Path
from datetime import datetime


class SkillValidator:
    """Valida conformidade com a especificação agentskills.io"""
    
    @staticmethod
    def validate_name(name: str) -> tuple[bool, str]:
        """
        Valida o campo 'name' conforme especificação.
        
        Retorna: (é_válido, mensagem_erro)
        """
        if not name:
            return False, "Nome não pode estar vazio"
        
        if len(name) > 64:
            return False, f"Nome exceede 64 caracteres ({len(name)} fornecidos)"
        
        if len(name) < 1:
            return False, "Nome deve ter pelo menos 1 caractere"
        
        # Apenas lowercase, números e hífens
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, "Nome contém caracteres inválidos. Apenas a-z, 0-9 e - permitidos"
        
        if name.startswith('-') or name.endswith('-'):
            return False, "Nome não pode começar ou terminar com hífen"
        
        if '--' in name:
            return False, "Nome não pode conter hífens consecutivos (--)"
        
        return True, ""
    
    @staticmethod
    def validate_description(description: str) -> tuple[bool, str]:
        """
        Valida o campo 'description' conforme especificação.
        
        Retorna: (é_válido, mensagem_erro)
        """
        if not description:
            return False, "Descrição não pode estar vazia"
        
        if len(description) > 1024:
            return False, f"Descrição exceede 1024 caracteres ({len(description)} fornecidos)"
        
        if len(description) < 1:
            return False, "Descrição deve ter pelo menos 1 caractere"
        
        return True, ""


class SkillGenerator:
    """Gera estrutura completa de uma nova skill"""
    
    def __init__(self, name: str, description: str, license: str = "MIT",
                 compatibility: str = None, output_dir: str = "./",
                 create_assets: bool = True, create_scripts: bool = True,
                 create_references: bool = True):
        self.name = name
        self.description = description
        self.license = license
        self.compatibility = compatibility or ""
        self.output_dir = Path(output_dir)
        self.skill_dir = self.output_dir / name
        self.create_assets = create_assets
        self.create_scripts = create_scripts
        self.create_references = create_references
        self.created_paths = []
    
    def validate(self) -> bool:
        """Valida todos os parâmetros antes de gerar"""
        is_valid, error = SkillValidator.validate_name(self.name)
        if not is_valid:
            print(f"❌ Erro no nome: {error}", file=sys.stderr)
            return False
        
        is_valid, error = SkillValidator.validate_description(self.description)
        if not is_valid:
            print(f"❌ Erro na descrição: {error}", file=sys.stderr)
            return False
        
        return True
    
    def create_directories(self) -> bool:
        """Cria estrutura de diretórios"""
        try:
            self.skill_dir.mkdir(parents=True, exist_ok=True)
            self.created_paths.append(self.skill_dir)
            
            if self.create_scripts:
                scripts_dir = self.skill_dir / "scripts"
                scripts_dir.mkdir(exist_ok=True)
                self.created_paths.append(scripts_dir)
            
            if self.create_references:
                references_dir = self.skill_dir / "references"
                references_dir.mkdir(exist_ok=True)
                self.created_paths.append(references_dir)
            
            if self.create_assets:
                assets_dir = self.skill_dir / "assets"
                assets_dir.mkdir(exist_ok=True)
                self.created_paths.append(assets_dir)
            
            return True
        except Exception as e:
            print(f"❌ Erro ao criar diretórios: {e}", file=sys.stderr)
            return False
    
    def create_skill_md(self) -> bool:
        """Cria arquivo SKILL.md principal"""
        try:
            skill_md_path = self.skill_dir / "SKILL.md"
            
            # Construir frontmatter YAML
            frontmatter = f"""---
name: {self.name}
description: {self.description}
license: {self.license}"""
            
            if self.compatibility:
                frontmatter += f"\ncompatibility: {self.compatibility}"
            
            frontmatter += f"""
metadata:
  created: {datetime.now().isoformat()}
---

# {self.name.replace('-', ' ').title()}

## Descrição

{self.description}

## Uso

Ative esta skill quando necessário para {self.description.lower().rstrip('.')}

## Estrutura

Esta skill possui os seguintes componentes:
"""
            
            if self.create_scripts:
                frontmatter += "\n- **scripts/**: Código executável para automação"
            if self.create_references:
                frontmatter += "\n- **references/**: Documentação técnica detalhada"
            if self.create_assets:
                frontmatter += "\n- **assets/**: Templates e recursos estáticos"
            
            frontmatter += "\n\n## Próximos Passos\n\n1. Adicione instruções de funcionamento neste arquivo\n"
            
            if self.create_references:
                frontmatter += "2. Expanda a documentação em [references/](references/)\n"
            if self.create_scripts:
                frontmatter += f"3. Implemente scripts em [scripts/](scripts/)\n"
            
            frontmatter += "4. Execute `skills-ref validate ./{self.name}` para validar\n"
            
            with open(skill_md_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter)
            
            self.created_paths.append(skill_md_path)
            return True
        except Exception as e:
            print(f"❌ Erro ao criar SKILL.md: {e}", file=sys.stderr)
            return False
    
    def create_scripts_template(self) -> bool:
        """Cria template para scripts (se habilitado)"""
        if not self.create_scripts:
            return True
        
        try:
            # Criar exemplo de script Python
            example_script = self.skill_dir / "scripts" / "example.py"
            
            template = """#!/usr/bin/env python3
\"\"\"
Exemplo de script para a skill {name}
\"\"\"

def main():
    print("Execute me para testar a skill {name}")

if __name__ == "__main__":
    main()
""".format(name=self.name)
            
            with open(example_script, 'w', encoding='utf-8') as f:
                f.write(template)
            
            # Tornar executável
            os.chmod(example_script, 0o755)
            self.created_paths.append(example_script)
            return True
        except Exception as e:
            print(f"❌ Erro ao criar template de script: {e}", file=sys.stderr)
            return False
    
    def create_references_template(self) -> bool:
        """Cria template para referências (se habilitado)"""
        if not self.create_references:
            return True
        
        try:
            reference_md = self.skill_dir / "references" / "REFERENCE.md"
            
            template = f"""# Referência Técnica - {self.name.replace('-', ' ').title()}

## Visão Geral

Documentação técnica detalhada para a skill **{self.name}**.

## Conceitos Principais

### Conceito 1
Descreva aqui...

### Conceito 2
Descreva aqui...

## API/Interfaces

Documente os pontos de entrada ou interfaces principais.

## Exemplos

Forneça exemplos de uso prático.

## Referências Externas

- [Link 1](https://exemplo.com)
- [Link 2](https://exemplo.com)
"""
            
            with open(reference_md, 'w', encoding='utf-8') as f:
                f.write(template)
            
            self.created_paths.append(reference_md)
            return True
        except Exception as e:
            print(f"❌ Erro ao criar template de referência: {e}", file=sys.stderr)
            return False
    
    def create_assets_template(self) -> bool:
        """Cria template para assets (se habilitado)"""
        if not self.create_assets:
            return True
        
        try:
            # Criar template JSON para estrutura de dados
            example_template = self.skill_dir / "assets" / "template.json"
            
            template = """{
  "description": "Template de estrutura para a skill""" + f' "{self.name}"' + """",
  "properties": {
    "property1": {
      "type": "string",
      "description": "Descrição da propriedade"
    }
  }
}
"""
            
            with open(example_template, 'w', encoding='utf-8') as f:
                f.write(template)
            
            self.created_paths.append(example_template)
            return True
        except Exception as e:
            print(f"❌ Erro ao criar template de assets: {e}", file=sys.stderr)
            return False
    
    def generate(self) -> bool:
        """Executa geração completa"""
        if not self.validate():
            return False
        
        if not self.create_directories():
            return False
        
        if not self.create_skill_md():
            return False
        
        if not self.create_scripts_template():
            return False
        
        if not self.create_references_template():
            return False
        
        if not self.create_assets_template():
            return False
        
        return True
    
    def print_summary(self):
        """Imprime resumo da skill gerada"""
        print(f"\n✅ Skill '{self.name}' criada com sucesso!\n")
        print(f"📍 Localização: {self.skill_dir.absolute()}")
        print(f"\n📁 Arquivos criados:")
        
        for path in sorted(self.created_paths):
            rel_path = path.relative_to(self.skill_dir)
            if rel_path == Path("."):
                print(f"  └─ {self.skill_dir.name}/")
            else:
                indent = "     " if str(rel_path).count(os.sep) > 0 else "  └─"
                print(f"  {indent} {rel_path}")
        
        print(f"\n🔍 Próximos passos:")
        print(f"  1. cd {self.skill_dir}")
        print(f"  2. Edite SKILL.md com instruções detalhadas")
        print(f"  3. Valide com: skills-ref validate .")
        print(f"  4. Compartilhe sua skill!\n")


def main():
    parser = argparse.ArgumentParser(
        description="Gerador de Agent Skills para agentskills.io",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument("--name", required=True, help="Nome da skill (formato: lowercase-com-hifen)")
    parser.add_argument("--description", required=True, help="Descrição da skill (1-1024 caracteres)")
    parser.add_argument("--license", default="MIT", help="Licença da skill (padrão: MIT)")
    parser.add_argument("--compatibility", help="Requisitos de compatibilidade")
    parser.add_argument("--output-dir", default="./", help="Diretório de saída (padrão: ./)")
    parser.add_argument("--no-assets", action="store_true", help="Não criar pasta assets/")
    parser.add_argument("--no-scripts", action="store_true", help="Não criar pasta scripts/")
    parser.add_argument("--no-references", action="store_true", help="Não criar pasta references/")
    
    args = parser.parse_args()
    
    generator = SkillGenerator(
        name=args.name,
        description=args.description,
        license=args.license,
        compatibility=args.compatibility,
        output_dir=args.output_dir,
        create_assets=not args.no_assets,
        create_scripts=not args.no_scripts,
        create_references=not args.no_references
    )
    
    if generator.generate():
        generator.print_summary()
        return 0
    else:
        print("\n❌ Falha ao gerar skill", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
