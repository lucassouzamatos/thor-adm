## Considerações iniciais

* Para facilitar o acesso as maquinas, utilizamos VMs na nuvem.
* A partir da Amazon, criamos instancias de uma VM em ubuntu.

* As VMs criadas na amazon serão chamadas de instâncias, com tais objetivos:
    - ter uma maquina com acesso compartilhado
    - performance, no caso não precisamos rodar várias VMS nas nossas maquinas

* As VMs criadas nas instâncias, serão chamadas de VMs, com os objetivos:
    - vão ser usadas como agentes na rede

* Utilizamos um container em docker contendo o ssh, para o acesso as instâncias 
    na nuvem.

* 