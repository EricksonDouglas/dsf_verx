# dsv_verx

Desafio Verx para criar um crawler para extrair Finance Yahoo

## Tecnologias Utilizadas:

- Python 3.8
- Pytest
- Browsers:
    - Selenium
    - Httpx
- Treatment_html:
    - beautifulsoup4
    - Lxml

### Pré-requisito no Linux

* Ubuntu
  ```sh
  apt-get install python3-virtualenv
  ```
  ```sh
  virtualenv -p=python3.8 venv
  ```
  ```sh
  source venv/bin/activate
  ```
  ```sh
  pip install -r requirements.txt
  ```

### Instalar libs para rodar o Selenium

 ```sh
  chmod +x install_libs_chrome.sh
  ```

  ```sh
  ./install_libs_chrome.sh
  ```

### Executar o crawler

Isso é só uma demostração, poderia fazer várias formas para acionar...

  ```sh
  python -m app.spiders.finance_yahoo
  ```

Resultado da execução está na pasta 'results'

## Executar Tests

  ```sh
  pytest --cov=app tests/
  ```

"Falta finalizar"
  
  


    

    

