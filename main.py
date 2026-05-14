import asyncio
import random
import string
from playwright.async_api import async_playwright
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

SMAILPRO_API_KEY = os.getenv('SMAILPRO_API_KEY')

if not SMAILPRO_API_KEY:
    raise ValueError('SMAILPRO_API_KEY not found in .env')

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_password():
    return generate_random_string(12) + '@123'

async def get_smailpro_email():
    # Example endpoint - adjust based on actual SmailPro API
    url = 'https://smailpro.com/api/create'  # Placeholder - check docs
    headers = {'X-Api-Key': SMAILPRO_API_KEY}
    data = {'type': 'microsoft'}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()
        return data.get('email'), data.get('inbox_id')  # adjust fields
    return None, None

async def get_verification_code(inbox_id):
    # Poll for email
    for _ in range(30):
        # Call poll endpoint
        time.sleep(5)
        # Parse code
        pass  # Implement based on API
    return '123456'  # placeholder

async def create_puter_account(page, email, password):
    await page.goto('https://puter.com/action/signup')
    await page.fill('input[name="username"]', generate_random_string(8))
    await page.fill('input[name="email"]', email)
    await page.fill('input[name="password"]', password)
    await page.fill('input[name="confirm_password"]', password)
    await page.click('button[type="submit"]')
    # Handle verification if needed
    await asyncio.sleep(5)

async def main(num_accounts=1):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        for i in range(num_accounts):
            print(f'Gerando conta {i+1}/{num_accounts}')
            email, inbox_id = await get_smailpro_email()
            if not email:
                print('Falha ao gerar email')
                continue

            password = generate_password()
            print(f'Email: {email}')
            print(f'Senha: {password}')

            await create_puter_account(page, email, password)

            # Extract JWT token from localStorage or network
            token = await page.evaluate('''() => localStorage.getItem('authToken')''')
            print(f'Auth Token (JWT): {token}')

            # Save or display

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main(3))  # exemplo 3 contas
