## Considerações iniciais

* Para facilitar o acesso as maquinas, utilizamos VMs na nuvem.
* Usando a Amazon, criamos instancias baseadas em Linux, distribuição Ubuntu 20.04 LTS.

* As VMs criadas na amazon serão chamadas de instâncias, com tais objetivos:
    - ter uma maquina com acesso compartilhado
    - performance, no caso não precisamos rodar várias VMS nas nossas maquinas

* As VMs criadas nas instâncias, serão chamadas de VMs, com os objetivos:
    - vão ser usadas como agentes na rede

* Utilizamos um container em docker contendo o ssh, para o acesso as instâncias 
    na nuvem.

# Amazon
## IAM Policies
[ubuntu-free-tier-iam-policy](ubuntu-free-tier-iam-policy.json)
### Motivação
Pelo ponto de vista da segurança e gerenciamento da conta na amazon, devemos atribuir contas diferentes, para propósitos diferentes. Assim temos:
- facilidade na remoção/atualização de um usuário, sendo que este possui uma pequena responsabilidade
- no incidente de uma divulgação mal intencionada de uma das chaves, não deve comprometer o resto dos recursos

### Deployer
Este usuário tem permissão para criar instâncias. Ainda é possível definirmos que configurações a instância criada tem permissão para usar. As mais interessantes/importantes, por mim destacadas são:
- imagem (Ubuntu 20.04 LTS ou 18.04 LTS)
- grupo de segurança, quem de fora pode acessar a instância e quem de fora a instância pode acessar 
- subnet, qual rede privada ela pertence
- tipo de instância, evitando cobranças de surpresa
- tamanho e tipo do volume de armazenamento, como temos no máximo 30GB, é bom racionar

### Considerações
Montar o conjunto de regras de algumas linhas parece uma tarefa fácil, mas não foi para mim.
Inicialmente fiz vários testes usando um simulador dessas regras, que a princípio parece bem mais rápido e eficiente do que ficar tentando executar as ações e ajustando a _policy_ de acordo. Porém mesmo olhando todos os exemplos que encontrava na net, parecia que não funcionava certo, e o pior era que não tinha nenhum tipo de log ou mensagem do que estava bloqueando a ação, era um simples `sim` ou `não`. Então depois de horas errando acabei indo testar direto usando o programa da amazon, `awscli` que tenho uma breve experiência. Com ele quando um erro acontecia, uma mensagem criptografada aparecia como a mensagem de erro, e com as permissões certas, bastava decriptografa-la para acessar a mensagem de autorização negada. Com isso fui me guiando partindo sempre do princípio básico, fazer funcionar e testar o que bloqueia, demorei alguns minutos para encontrar o ponto certo, mas depois rapidamente as coisas se encaixaram e tudo funcionou perfeitamente. Amazon rocks!!

Coisas que não funcionaram bem comigo:
- simulador de policies, não vale a pena o tempo perdido, melhor testar com `awscli` usando a opção `--dry-run` então ele nunca vai realmente criar uma instância
- criador de policies, escrever a policy direto no json foi mais intuitivo e foi como fiz funcionar, mas tentaria novamente usa-lo


# Instâncias

## Ansible - Inicializando
Nesta fase serão criadas as permissões para a criação das intâncias, com segurança. Devido ao ótimo mecanismo de gerenciamento de permissões de acesso (IAM) é possível limitar a responsabilidade de cada usuário, minimizando os danos no caso de um incidente de invasão.

Após essa fase dois usuário serão criados. O primeiro usuário, criado pelo console da amazon (navegador), responsável por criar o outro usuário e configurar as suas permissões. Este último usuário terá a responsabilidade de criar instâncias `free-tier`s na amazon. 

O primeiro será chamado de `setup-manager`, mas não é necessário usar o mesmo nome; e o último está sendo chamado de `ubuntu-sim-deployer`, este está `hard-coded` nos arquivos, sendo que **para alterá-lo terá que alterar também nas dependências. Você foi avisado!**.

#### setup-manager
**Todos os passos serão executados no console da amazon.**

- IAM > Policies > Create Policy
    - mude para a aba `JSON` e troque o conteúdo com o conteúdo de [first-setup-policy](instances/ansible/policies/first-setup-policy.json)
    - o nome da policy será `IAMFirstSetupManager`
    - finalize o cadastro

- IAM > Users > Add User
    - o nome do usuário, como mencionado anteriormente será `setup-manager`
    - no tipo de acesso, habilite apenas accesso por chaves, `Programmatic access`
    - vá para a área de permissões, selecione a seção para acrescentar policies existentes diretamente, e procure pela policy criada anteriormente, no caso `IAMFirstSetupManager`
    - finalize o cadastro

Com o usuário criado e permissões setadas, podemos dar início a configuração inicial.

## Docker
**Não entrarei em detalhes sobre configuração/instalação do docker em diferentes plataformas, logo assumirei que este já esteja em perfeito funcionamento.**

### Ambiente de Deploy
- no diretório `instances` contém um Dockerfile que cria uma imagem com o ansible e o cliente ssh. Então para criar a imagem:
```bash
$ docker build instances/
```

- configurar as variáveis de ambiente da amazon, usando o arquivo [aws.env.example](instances/aws.env.example) como base. Então copiamos este para `aws.env` (automaticamente ignorado pelo git, assim espero) e o configuramos com as credenciais do usuário `setup-manager`, criado anteriormente. No final terá algo assim:
```bash
$ cat instances/aws.env
# Store your access keys, and pass it to docker with --env-file

AWS_ACCESS_KEY_ID=6bb1f81d42c1cd7ad1ee3536029e
AWS_ACCESS_SECRET_KEY=n40Rk8gUHjDchQ70ncHpMMST97c7NiN6w21U9YiirPjR3TwDKhik9Qk+Ho
AWS_DEFAULT_REGION=sa-east-1
```

- para nosso propósito, precisaremos de dois volumes sendo:
    - um volume `somente-leitura` tendo os arquivos do ansible
    - um volume para transferirmos as chaves da vpn para o host
o nome dos volumes criados na imagem docker é irrelevante, porém é aconselhado seguir o padrão:

**OBS**: adaptar `/caminho-diretório/instances` para o seu ambiente, tomando o cuidade de que seja um caminho absoluto. No windows deve ser algo como `C:\...`

```bash
$ docker run --rm -it --env-file aws.env -v /caminho-diretório/instances/ansible:/instances:ro -v /caminho-diretório/instances/vpnkeys:/vpnkeys ${IMAGE_ID}
bash-5.0# echo Alpine rocks!!!
```

Ao final do comando `docker run ...` devemos cair direto no bash da imagem.

### Testando o ambiente
Com o bash aberto no container, você deve estar apto a usar tanto o `ansible` quanto  `awscli`. Para ter certeza, execute estes testes:

- ansible:
```bash
bash-5.0# ansible-playbook instances/my-cidr.yml  
```

Ao final deve mostrar a rede do endereço IP público.

- awscli:
```bash
bash-5.0# awscli iam list-users
```

Deve listar todos os usuários pertencentes a conta. 