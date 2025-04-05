"""Module for managing Instagram API integration and automated posting."""

import os
from dotenv import load_dotenv
from instagrapi import Client
from openai import OpenAI
from PIL import Image
from io import BytesIO
import requests
import time

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Instagram
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Configurações OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
COPY_MODEL = os.getenv('COPY_MODEL', 'gpt-4')

_instagram_session = None
_session_creation_time = None
_session_expiry_time = 28800  # Tempo de expiração da sessão em segundos (8 horas)
_max_retries = 3  # Número máximo de tentativas de login
_initial_wait = 2  # Tempo inicial de espera em segundos
_max_wait = 120  # Tempo máximo de espera (2 minutos)


def initialize_instagram_session(max_retries=_max_retries, initial_wait=_initial_wait, max_wait=_max_wait):
    """Initialize Instagram API session with enhanced rate limiting and retry mechanism."""
    global _instagram_session, _session_creation_time
    retry_count = 0
    last_error = None
    wait_time = initial_wait
    
    try:
        # Verificar se as credenciais do Instagram estão configuradas
        if not all([INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD]):
            raise ValueError("Credenciais do Instagram não configuradas. Verifique o arquivo .env")
        
        # Verificar conexão com a internet antes de prosseguir
        try:
            requests.get('https://www.instagram.com', timeout=5)
        except requests.exceptions.RequestException:
            raise Exception("Sem conexão com a internet. Verifique sua conexão e tente novamente.")
        
        # Criar e verificar diretório temporário
        script_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(script_dir, 'temp_instagram')
        
        try:
            os.makedirs(temp_dir, exist_ok=True)
            if not os.path.isdir(temp_dir):
                raise Exception("Falha ao criar diretório temporário")
        except Exception as e:
            raise Exception(f"Erro ao criar diretório temporário: {str(e)}")
        
        # Limpar arquivos de sessão antigos
        try:
            for file in os.listdir(temp_dir):
                if file.endswith(('.checkpoint', '.json.temp', '.cookie')):
                    try:
                        os.remove(os.path.join(temp_dir, file))
                    except Exception:
                        pass
        except Exception:
            pass
        
        # Criar nova sessão do Instagram
        client = Client()
        client.delay_range = [1, 3]
        
        # Configurar diretório para arquivos temporários
        client.set_settings({
            'custom_settings': {
                'temp_dir': temp_dir,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'language': 'pt-BR'
            }
        })
        
        # Tentar login com retry
        while retry_count < max_retries:
            try:
                client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
                _instagram_session = client
                _session_creation_time = time.time()
                return _instagram_session
            except Exception as e:
                last_error = e
                retry_count += 1
                print(f"Erro na tentativa {retry_count}: {str(e)}")
                
                if retry_count < max_retries:
                    print(f"Tentativa {retry_count + 1}/{max_retries}. Aguardando {wait_time} segundos...")
                    time.sleep(wait_time)
                    wait_time = min(wait_time * 1.5, max_wait)
                    continue
                break
        
        # Se chegou aqui, todas as tentativas falharam
        raise Exception(f"Falha ao inicializar sessão do Instagram após {max_retries} tentativas. Último erro: {str(last_error)}")
    except Exception as e:
        print(f"Erro ao fazer login: {str(e)}")
        raise e

def generate_post_caption(product_info):
    """Generate engaging caption for Instagram post."""
    try:
        # Gerar legenda padrão sem depender da API OpenAI
        return f"✨ {product_info['title']} ✨\n\n💰 Preço Especial: R$ {product_info['price']}\n\n🔥 Aproveite esta oferta incrível! Produto de alta qualidade com o melhor preço.\n\n🛍️ Compre agora: {product_info['url']}\n\n#moda #estilo #fashion #compras #ofertas #modamasculina"
    except Exception as e:
        raise Exception(f"Falha ao gerar legenda: {str(e)}")

def download_and_process_image(image_url):
    """Download and process image for Instagram with optimized processing."""
    if not image_url:
        raise ValueError("URL da imagem não fornecida ou inválida")

    try:
        # Validar URL da imagem
        if not isinstance(image_url, str):
            raise ValueError("URL da imagem deve ser uma string")
            
        # Criar e verificar diretório temporário
        script_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(script_dir, 'temp_instagram')
        
        # Garantir que o diretório temporário existe
        try:
            os.makedirs(temp_dir, exist_ok=True)
            if not os.path.isdir(temp_dir):
                raise Exception("Falha ao criar diretório temporário")
        except Exception as e:
            raise Exception(f"Erro ao criar diretório temporário: {str(e)}")
            
        # Verificar permissões de escrita no diretório
        test_file = os.path.join(temp_dir, 'test.txt')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except Exception as e:
            raise Exception(f"Sem permissão de escrita no diretório temporário: {str(e)}")
        
        # Download da imagem
        response = requests.get(image_url)
        if response.status_code != 200:
            raise Exception(f"Falha ao baixar imagem. Status code: {response.status_code}")
            
        # Processar imagem
        image = Image.open(BytesIO(response.content))
        
        # Redimensionar para dimensões aceitas pelo Instagram
        max_size = (1080, 1080)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Salvar imagem processada
        temp_image_path = os.path.join(temp_dir, 'temp_post_image.jpg')
        image.save(temp_image_path, 'JPEG', quality=95)
        
        return temp_image_path
    except Exception as e:
        raise Exception(f"Erro ao processar imagem: {str(e)}")

def create_instagram_post_from_product(product_data):
    """Create Instagram post from product data with enhanced error handling."""
    try:
        # Validar dados do produto
        required_fields = ['title', 'price', 'url', 'image_url']
        missing_fields = [field for field in required_fields if not product_data.get(field)]
        if missing_fields:
            raise ValueError(f"Dados do produto incompletos. Campos faltando: {', '.join(missing_fields)}")
        
        # Inicializar sessão do Instagram se necessário
        if not _instagram_session or not _session_creation_time or \
           (time.time() - _session_creation_time) > _session_expiry_time:
            initialize_instagram_session()
        
        # Processar imagem
        image_path = download_and_process_image(product_data['image_url'])
        
        # Gerar legenda
        caption = generate_post_caption(product_data)
        
        try:
            # Fazer upload da foto
            media = _instagram_session.photo_upload(
                image_path,
                caption=caption
            )
            
            # Limpar arquivo temporário
            try:
                os.remove(image_path)
            except Exception:
                pass
            
            return {
                'post_id': media.pk,
                'caption': caption,
                'image_url': media.thumbnail_url
            }
            
        except Exception as e:
            # Tentar limpar arquivo temporário mesmo em caso de erro
            try:
                os.remove(image_path)
            except Exception:
                pass
            raise e
            
    except Exception as e:
        raise Exception(f"Erro ao criar post no Instagram: {str(e)}")