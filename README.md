Guia de Execução do Projeto Django 

1. Acesse a página do repositório no GitHub.

2. Clique no botão verde Code.

3. Selecione Download ZIP.

4. Extraia o arquivo .zip em um diretório de sua preferência.

Configuração do ambiente 

1. Abra a pasta extraída no Visual Studio Code.

2. Instale a extensão Python (Microsoft) caso ainda não esteja disponível.

3. Abra o terminal integrado (Ctrl + ') e instale as dependências do projeto: pip install -r requirements.txt

3. Criação do arquivo .env (O arquivo .env não é versionado e deve ser criado manualmente na raiz do projeto).

4. Geração dos certificados SSL

Execute o script de geração de certificados: python certificates/generate_certificate.py (Esse comando criará os arquivos key.pem e cert.pem necessários para a execução em HTTPS). 

5. Aplicação das migrações python manage.py migrate

6. Criação do superusuário (acesso ao Django Admin): python manage.py createsuperuser (Informe nome de usuário, e-mail e senha quando solicitado).

7. Execução do servidor python manage.py runserver

Acesse a aplicação em: https://localhost:8000

8. Importação do cert.pem no Google Chrome (Windows): Como o certificado é autoassinado, o Chrome exibirá um aviso de segurança. Para que o navegador confie no certificado, siga os passos abaixo:

1. Abra o Google Chrome.

2. Na barra de endereços, acesse: chrome://certificate-manager

3. Em Certificados locais, clique em Gerenciar certificados importados pelo sistema operacional (ou acesse diretamente via Painel de Controle > Gerenciar certificados de usuário).

4. Na janela aberta, selecione a aba Autoridades de Certificação Raiz Confiáveis (Trusted Root Certification Authorities).

5. Clique em Importar...

6. No assistente, clique em Avançar e depois em Procurar.

7. No seletor de arquivos, altere o filtro de extensão para Todos os arquivos (*.*) e selecione o arquivo cert.pem localizado em certificates/cert.pem dentro do projeto.

8. Clique em Avançar e selecione a opção Colocar todos os certificados no repositório a seguir, garantindo que esteja definido como Autoridades de Certificação Raiz Confiáveis.

9. Clique em Avançar e depois em Concluir.

10. Um aviso de segurança será exibido informando sobre a instalação de uma raiz confiável. Clique em Sim para confirmar.

11. Reinicie o Google Chrome completamente para que a alteração tenha efeito. Após esse procedimento, ao acessar https://localhost:8000, o navegador reconhecerá o certificado como válido e não exibirá mais o aviso de conexão não segura.
