import os
import time
import random
import string
import json
import re
from datetime import datetime
from dotenv import load_dotenv
import requests
from rich.console import Console

load_dotenv()
console = Console()

API_KEY = os.getenv('SMAILPRO_API_KEY')
BASE_URL = 'https://app.sonjj.com'

headers = {'X-Api-Key': API_KEY, 'Content-Type': 'application/json'}

def generate_random_string(length=12):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def create_temp_email():
    if not API_KEY:
        console.print('[red]ERRO: API Key não configurada[/red]')
        return None
    try:
        # Get domains
        r = requests.get(f'{BASE_URL}/v1/temp_email/domains', headers=headers)
        domains = r.json().get('domains', []) if r.ok else ['outlook.com']
        domain = random.choice(domains)
        
        username = f"u{random.randint(1000,9999)}{generate_random_string(8)}"
        email = f"{username}@{domain}"
        
        params = {'email': email, 'expiry_minutes': 120}
        r = requests.get(f'{BASE_URL}/v1/temp_email/create', params=params, headers=headers)
        
        if r.ok:
            console.print(f'[green]✅ Email criado:[/green] {email}')
            return email
    except Exception as e:
        console.print(f'[red]Erro ao criar email: {e}[/red]')
    return None

def get_verification_code(email, max_tries=30):
    console.print('[yellow]Aguardando código no SmailPro...[/yellow]')
    for _ in range(max_tries):
        try:
            r = requests.get(f'{BASE_URL}/v1/temp_email/messages?email={email}', headers=headers)
            if r.ok:
                msgs = r.json().get('messages', [])
                for msg in msgs:
                    body = str(msg.get('body', '') or msg.get('text', ''))
                    match = re.search(r'\b(\d{4,8})\b', body)
                    if match:
                        code = match.group(1)
                        console.print(f'[green]✅ Código encontrado: {code}[/green]')
                        return code
        except:
            pass
        time.sleep(8)
    return None

def main():
    console.print('[bold cyan]=== Modo Manual + Desktop noVNC ===[/bold cyan]')
    accounts = []
    
    while True:
        cmd = input('\nDigite "next" para nova conta, "exit" para sair: ').strip().lower()
        if cmd == 'exit':
            break
        if cmd not in ['next', 'ok', '']:
            continue
        
        email = create_temp_email()
        if not email:
            continue
        
        password = generate_random_string(16)
        console.print(f'[blue]Senha gerada:[/blue] {password}')
        console.print(f'[bold]Email:[/bold] {email}')
        console.print('\n[bold yellow]→ Abra o navegador no desktop e cadastre no Puter.com[/bold yellow]')
        console.print('→ Após login, pegue o Auth Token (F12 → Application → Local Storage)')
        
        token = input('\nCole o Auth Token (JWT) aqui (ou Enter se não pegou): ').strip()
        
        account = {
            "email": email,
            "password": password,
            "auth_token": token,
            "created_at": datetime.now().isoformat()
        }
        accounts.append(account)
        
        with open('accounts_manual.json', 'w', encoding='utf-8') as f:
            json.dump(accounts, f, indent=2, ensure_ascii=False)
        
        console.print(f'[green]✅ Conta salva! Total: {len(accounts)}[/green]')

if __name__ == "__main__":
    main()
