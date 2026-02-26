# Hephaestuz ⚔️

[cite_start]**Hephaestuz** é um jogo de aventura *top-down* (visão aérea) desenvolvido como parte do processo de seleção de tutores de Python (2026)[cite: 3]. O projeto foca em mecânicas de combate fluidas, utilizando uma arma personalizada chamada **Snipear** que combina ataques de curto alcance com um potente laser (Railgun).

## 🚀 Requisitos Técnicos Atendidos
[cite_start]O projeto foi desenvolvido estritamente sob as limitações impostas pelos requisitos do teste[cite: 7]:
- [cite_start]**Tecnologias:** Uso exclusivo de `PgZero`, `math` e `random`[cite: 9, 10, 11].
- [cite_start]**Gênero:** Aventura point-and-click/Top-down shooter[cite: 32].
- [cite_start]**Animação:** Sistema de animação de sprites cíclico para estados de movimento e repouso (*idle*)[cite: 25, 34].
- [cite_start]**Arquitetura:** Orientação a Objetos (Classes) para gerenciamento de herói, inimigos e armas[cite: 23].

## 🎮 Mecânicas Principais
- **Snipear Weapon:** Sistema de cooldown duplo (ataque básico e especial).
- **Railgun Special:** Disparo de alta precisão com rastro calculado via trigonometria.
- [cite_start]**Enemy AI:** Inimigos com comportamento de perseguição e detecção de colisão[cite: 22].
- [cite_start]**Game Feel:** Implementação de *hitstop* (pausa de impacto) e *iframes* (frames de invulnerabilidade) para melhorar a experiência do jogador[cite: 27].

## 🛠️ Como Executar
1. Certifique-se de ter o Python instalado.
2. Instale o Pygame Zero: `pip install pgzero`.
3. Execute o arquivo principal: `pgzrun hephaestuz.py`.

## 📜 Licença
[cite_start]Este projeto foi desenvolvido de forma independente e original para fins de avaliação técnica[cite: 28, 44].
