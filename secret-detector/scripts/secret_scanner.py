#!/usr/bin/env python3
"""
Secret Detector - Detecção de Credenciais Expostas

Analisa diretórios completos procurando por segredos, tokens, chaves privadas
e credenciais expostas usando padrões regex avançados.

Uso:
    python secret_scanner.py /path/to/dir [opções]

Exemplos:
    python secret_scanner.py .
    python secret_scanner.py . --patterns api-keys,github,aws
    python secret_scanner.py . --format json > report.json
    python secret_scanner.py . --exclude node_modules,dist
    python secret_scanner.py . --fail-on-critical
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class SecretMatch:
    """Representa uma detecção de segredo"""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    pattern_name: str
    file_path: str
    line_number: int
    line_content: str
    matched_text: str
    pattern: str


class SecretPatterns:
    """Padrões regex para detecção de segredos"""
    
    PATTERNS = {
        # Serviços de Pagamento
        "stripe-live-key": {
            "pattern": r"sk_live_[A-Za-z0-9]{24,}",
            "severity": "CRITICAL",
            "description": "Chave Stripe Live (produção)"
        },
        "stripe-test-key": {
            "pattern": r"sk_test_[A-Za-z0-9]{24,}",
            "severity": "HIGH",
            "description": "Chave Stripe Test"
        },
        "stripe-restricted-key": {
            "pattern": r"rk_live_[A-Za-z0-9]{24,}",
            "severity": "CRITICAL",
            "description": "Chave Restrita Stripe"
        },
        
        # GitHub
        "github-pat": {
            "pattern": r"ghp_[A-Za-z0-9]{36}",
            "severity": "CRITICAL",
            "description": "GitHub Personal Access Token"
        },
        "github-oauth": {
            "pattern": r"gho_[A-Za-z0-9]{36}",
            "severity": "CRITICAL",
            "description": "GitHub OAuth Token"
        },
        "github-app": {
            "pattern": r"ghu_[A-Za-z0-9]{36}",
            "severity": "CRITICAL",
            "description": "GitHub App Token"
        },
        "github-refresh": {
            "pattern": r"ghr_[A-Za-z0-9]{76}",
            "severity": "CRITICAL",
            "description": "GitHub Refresh Token"
        },
        
        # AWS
        "aws-access-key": {
            "pattern": r"AKIA[0-9A-Z]{16}",
            "severity": "CRITICAL",
            "description": "AWS Access Key ID"
        },
        "aws-secret-key": {
            "pattern": r"aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}",
            "severity": "CRITICAL",
            "description": "AWS Secret Access Key"
        },
        
        # Senhas e Credentials
        "password-assignment": {
            "pattern": r"password\s*[:=]\s*['\"]([^'\"]{8,})['\"]",
            "severity": "CRITICAL",
            "description": "Senha em atribuição"
        },
        "api-key-assignment": {
            "pattern": r"api[_-]?key\s*[:=]\s*['\"]([A-Za-z0-9\-._~+/]{20,})['\"]",
            "severity": "CRITICAL",
            "description": "API Key em atribuição"
        },
        
        # Chaves Privadas
        "ssh-private-key": {
            "pattern": r"-----BEGIN (?:RSA|DSA|EC) PRIVATE KEY-----",
            "severity": "CRITICAL",
            "description": "Chave Privada SSH/RSA"
        },
        "openssh-private-key": {
            "pattern": r"-----BEGIN OPENSSH PRIVATE KEY-----",
            "severity": "CRITICAL",
            "description": "Chave Privada OpenSSH"
        },
        "pgp-private-key": {
            "pattern": r"-----BEGIN PGP PRIVATE KEY BLOCK-----",
            "severity": "CRITICAL",
            "description": "Chave Privada PGP"
        },
        
        # URLs com Credenciais
        "url-with-credentials": {
            "pattern": r"https?://[A-Za-z0-9\-._]+:[A-Za-z0-9\-._@]+@[A-Za-z0-9\-._/]+",
            "severity": "CRITICAL",
            "description": "URL com user:password"
        },
        
        # Tokens Genéricos
        "bearer-token": {
            "pattern": r"Bearer\s+[A-Za-z0-9\-._~+/=]{20,}",
            "severity": "HIGH",
            "description": "Bearer Token"
        },
        "jwt-token": {
            "pattern": r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
            "severity": "HIGH",
            "description": "JWT Token"
        },
        
        # Firebase
        "firebase-api-key": {
            "pattern": r"AIza[0-9A-Za-z\-_]{35}",
            "severity": "HIGH",
            "description": "Firebase API Key"
        },
        
        # Google
        "google-oauth-token": {
            "pattern": r"ya29\.[0-9A-Za-z\-_]+",
            "severity": "HIGH",
            "description": "Google OAuth Token"
        },
        
        # Slack
        "slack-token": {
            "pattern": r"xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[A-Za-z0-9-]{24,32}",
            "severity": "CRITICAL",
            "description": "Slack Token/Webhook"
        },
        
        # Chaves Privadas Base64
        "base64-private-key": {
            "pattern": r"['\"]?-----BEGIN [A-Z]+ PRIVATE KEY-----[^-]*-----END [A-Z]+ PRIVATE KEY-----['\"]?",
            "severity": "CRITICAL",
            "description": "Chave Privada em Base64"
        },
    }


class FalsePositiveFilter:
    """Filtra falsos positivos"""
    
    EXCLUDE_PATTERNS = [
        r"<[A-Z_]+>",  # <TOKEN>, <PASSWORD>
        r"\[.*\]",     # [PASSWORD], [TOKEN]
        r"\*+",        # *** ou ****
        r"example",
        r"test",
        r"sample",
        r"placeholder",
        r"your-",
        r"replace-",
        r"change-this",
    ]
    
    @staticmethod
    def is_likely_false_positive(matched_text: str) -> bool:
        """Verifica se é provável falso positivo"""
        text_lower = matched_text.lower()
        
        for pattern in FalsePositiveFilter.EXCLUDE_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        
        return False


class SecretScanner:
    """Scanner principal de segredos"""
    
    def __init__(self, root_path: str, exclude_dirs: List[str] = None,
                 exclude_files: List[str] = None, patterns: List[str] = None):
        self.root_path = Path(root_path)
        self.exclude_dirs = set(exclude_dirs or [])
        self.exclude_files = set(exclude_files or [])
        self.matches: List[SecretMatch] = []
        
        # Padrões padrão a ignorar
        self.exclude_dirs.update([
            ".git", ".github", "node_modules", "__pycache__", ".venv",
            "venv", "dist", "build", ".next", ".nuxt", ".cache",
            ".pytest_cache", ".mypy_cache", ".tox", "coverage"
        ])
        
        self.exclude_files.update([
            ".DS_Store", "*.pyc", "*.pyo", "*.class", "*.o",
            "*.so", "*.egg-info"
        ])
        
        # Selecionar padrões
        if patterns:
            self.patterns = {
                k: v for k, v in SecretPatterns.PATTERNS.items()
                if any(p in k for p in patterns)
            }
        else:
            self.patterns = SecretPatterns.PATTERNS
    
    def should_scan_file(self, file_path: Path) -> bool:
        """Verifica se arquivo deve ser varrido"""
        # Ignorar binários
        binary_extensions = {
            ".exe", ".bin", ".so", ".o", ".class", ".pyc",
            ".png", ".jpg", ".jpeg", ".gif", ".zip", ".tar", ".gz",
            ".pdf", ".doc", ".docx", ".xls", ".xlsx"
        }
        
        if file_path.suffix.lower() in binary_extensions:
            return False
        
        # Verificar exclusões por nome
        for exclude_pattern in self.exclude_files:
            if "*" in exclude_pattern:
                pattern = exclude_pattern.replace("*", ".*")
                if re.match(pattern, file_path.name):
                    return False
            elif file_path.name == exclude_pattern:
                return False
        
        return True
    
    def should_scan_dir(self, dir_path: Path) -> bool:
        """Verifica se diretório deve ser varrido"""
        return dir_path.name not in self.exclude_dirs and not dir_path.name.startswith(".")
    
    def scan_file(self, file_path: Path) -> None:
        """Escaneia arquivo individual"""
        if not self.should_scan_file(file_path):
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception:
            return
        
        for line_num, line_content in enumerate(lines, 1):
            for pattern_name, pattern_info in self.patterns.items():
                pattern = pattern_info["pattern"]
                
                matches = re.finditer(pattern, line_content)
                for match in matches:
                    matched_text = match.group(0)
                    
                    # Filtrar falsos positivos
                    if FalsePositiveFilter.is_likely_false_positive(matched_text):
                        continue
                    
                    # Truncar para display seguro
                    display_text = matched_text[:50] + "..." if len(matched_text) > 50 else matched_text
                    
                    self.matches.append(SecretMatch(
                        severity=pattern_info["severity"],
                        pattern_name=pattern_name,
                        file_path=str(file_path.relative_to(self.root_path)),
                        line_number=line_num,
                        line_content=line_content.rstrip()[:100],
                        matched_text=display_text,
                        pattern=pattern
                    ))
    
    def scan_directory(self) -> None:
        """Escaneia diretório recursivamente"""
        for root, dirs, files in os.walk(self.root_path):
            # Filtrar diretórios
            dirs[:] = [d for d in dirs if self.should_scan_dir(Path(d))]
            
            # Escanear arquivos
            for file in files:
                file_path = Path(root) / file
                self.scan_file(file_path)
    
    def get_summary(self) -> Dict:
        """Retorna resumo das detecções"""
        severity_counts = {}
        for match in self.matches:
            severity_counts[match.severity] = severity_counts.get(match.severity, 0) + 1
        
        return {
            "total_matches": len(self.matches),
            "severity_breakdown": severity_counts,
            "scan_timestamp": datetime.now().isoformat(),
            "root_path": str(self.root_path)
        }
    
    def format_text_report(self) -> str:
        """Formata relatório em texto"""
        if not self.matches:
            return "✅ Nenhum segredo detectado!\n"
        
        report = []
        report.append(f"\n❌ {len(self.matches)} segredo(s) detectado(s)\n")
        report.append("=" * 80)
        
        # Agrupar por severidade
        by_severity = {}
        for match in self.matches:
            if match.severity not in by_severity:
                by_severity[match.severity] = []
            by_severity[match.severity].append(match)
        
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if severity not in by_severity:
                continue
            
            report.append(f"\n🔴 {severity} ({len(by_severity[severity])})")
            report.append("-" * 80)
            
            for match in by_severity[severity]:
                report.append(f"  Padrão: {match.pattern_name}")
                report.append(f"  Arquivo: {match.file_path}:{match.line_number}")
                report.append(f"  Conteúdo: {match.line_content}")
                report.append(f"  Detectado: {match.matched_text}")
                report.append("")
        
        report.append("=" * 80)
        summary = self.get_summary()
        report.append(f"\nResumo: {summary['total_matches']} match(es)")
        for sev, count in summary['severity_breakdown'].items():
            report.append(f"  {sev}: {count}")
        
        return "\n".join(report)
    
    def format_json_report(self) -> str:
        """Formata relatório em JSON"""
        data = {
            "summary": self.get_summary(),
            "matches": [asdict(m) for m in self.matches]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def format_csv_report(self) -> str:
        """Formata relatório em CSV"""
        lines = ["severity,pattern,file,line,content_preview"]
        for match in self.matches:
            content_preview = match.line_content.replace(",", ";").replace("\n", " ")[:100]
            lines.append(f"{match.severity},{match.pattern_name},{match.file_path},"
                        f"{match.line_number},\"{content_preview}\"")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Secret Detector - Encontre segredos e credenciais expostas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument("path", help="Caminho do diretório a escanear")
    parser.add_argument("--patterns", help="Padrões específicos (separados por vírgula, ex: api-keys,github,aws)")
    parser.add_argument("--format", choices=["text", "json", "csv"], default="text", help="Formato de saída")
    parser.add_argument("--exclude", help="Diretórios a ignorar (separados por vírgula)")
    parser.add_argument("--fail-on-critical", action="store_true", help="Falhar se houver CRITICAL")
    parser.add_argument("--strict", action="store_true", help="Falhar se houver qualquer segredo")
    parser.add_argument("--list-patterns", action="store_true", help="Listar padrões disponíveis")
    
    args = parser.parse_args()
    
    # Listar padrões
    if args.list_patterns:
        print("\n📋 Padrões Disponíveis:\n")
        for name, info in SecretPatterns.PATTERNS.items():
            print(f"  {name:30} [{info['severity']:8}] {info['description']}")
        print(f"\nTotal: {len(SecretPatterns.PATTERNS)} padrões\n")
        return 0
    
    # Validar diretório
    if not Path(args.path).is_dir():
        print(f"❌ Diretório não encontrado: {args.path}", file=sys.stderr)
        return 1
    
    # Preparar excludes
    exclude_dirs = args.exclude.split(",") if args.exclude else []
    
    # Preparar padrões
    patterns = args.patterns.split(",") if args.patterns else None
    
    # Executar scan
    scanner = SecretScanner(args.path, exclude_dirs=exclude_dirs, patterns=patterns)
    scanner.scan_directory()
    
    # Formatar saída
    if args.format == "json":
        output = scanner.format_json_report()
    elif args.format == "csv":
        output = scanner.format_csv_report()
    else:
        output = scanner.format_text_report()
    
    print(output)
    
    # Verificar condições de falha
    if args.strict and scanner.matches:
        return 1
    
    if args.fail_on_critical:
        for match in scanner.matches:
            if match.severity == "CRITICAL":
                return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
