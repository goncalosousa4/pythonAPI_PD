import requests
from bs4 import BeautifulSoup
import pandas as pd

def dados_da_noticia(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Exemplo: extraindo o conteúdo do parágrafo do artigo
        content_paragraphs = soup.find_all('p')
        content = ' '.join([paragraph.text for paragraph in content_paragraphs])

        # Outros exemplos de informações que você pode extrair
        author_element = soup.find('span', class_='author-class')
        author = author_element.text if author_element else None

        data_publicacao_element = soup.find('span', class_='date-class')
        data_publicacao = data_publicacao_element.text if data_publicacao_element else None

        fonte_element = soup.find('span', class_='source-class')
        fonte = fonte_element.text if fonte_element else None

        url_imagem_element = soup.find('img')
        url_imagem = url_imagem_element['src'] if url_imagem_element else None

        tags_elements = soup.find_all('a', class_='tag-class')
        tags = [tag.text for tag in tags_elements]

        comentarios_element = soup.find('span', class_='comments-class')
        comentarios = comentarios_element.text if comentarios_element else None

        return {
            'Content': content,
            'Author': author,
            'PublishedAt': data_publicacao,
            'Source': fonte,
            'ImageURL': url_imagem,
            'Tags': tags,
            'Comments': comentarios,
        }
    else:
        print(f"Erro ao acessar a notícia: {response.status_code}")
        return None

api_key = '58a083efe46a447ca5e29044a3a14439'

endpoint = 'https://newsapi.org/v2/top-headlines'

params = {
    'apiKey': api_key,
    'country': 'pt',  
    'category': 'sports'
}


response = requests.get(endpoint, params=params)

if response.status_code == 200:

    data = response.json()

    # Verificando se há artigos
    if 'articles' in data and len(data['articles']) > 0:

        article = data['articles'][0]

        dados_adicionais = dados_da_noticia(article['url'])


        df = pd.DataFrame({
            'Title': [article['title']],
            'Description': [article['description']],
            'URL': [article['url']],
            'PublishedAt': [article['publishedAt']],
            'Content': [dados_adicionais['Content']],
            'Author': [dados_adicionais['Author']],
            'Source': [dados_adicionais['Source']],
            'ImageURL': [dados_adicionais['ImageURL']],
            'Tags': [dados_adicionais['Tags']],
            'Comments': [dados_adicionais['Comments']],
        })

    
        print(df)
    else:
        print("Nenhum artigo encontrado.")
else:
    print(f"Erro na solicitação: {response.status_code}")
    print(response.text) 

df.to_csv("teste2.csv", index=False)
