# El paper de experimentos, contado en simple

Versión de lectura fácil del borrador (`paper.md` / `paper.es.md`). Mismos resultados, sin jerga. Cada afirmación tiene detrás un experimento reproducible en este repositorio.

## De qué se trata

El paper maestro propone una arquitectura (Core v0) donde los ciudadanos dirigen partes del presupuesto público a proyectos concretos, con pagos por avance verificado y un "vector de prioridades" público que absorbe el dinero de quienes no participan. Este segundo paper cuenta qué pasó cuando **atacamos esa arquitectura con simulaciones durante todo un programa de experimentos**: poblaciones realistas que adoptan o abandonan la plataforma, atacantes que coluden y capturan agendas, presupuestos que se congelan, verificadores humanos y de inteligencia artificial, y años simulados de operación.

La regla del juego fue: **escribir las predicciones antes de correr cada experimento y publicar también las que salieron mal**. De 34 predicciones registradas, unas 10 fallaron o no se pudieron probar — y varias de esas fallas son los hallazgos más útiles.

## Los seis hallazgos, en una frase cada uno

1. **La ventaja se mantiene con gente real.** Con poblaciones que se comportan como personas (se aburren, desconfían, delegan), la arquitectura entrega entre 2 y 2.7 veces más valor verificado por peso que el sistema actual — y rinde *mejor* cuando participa poca gente, siempre que el vector de prioridades por defecto sea bueno.

2. **Sin regla por defecto, no hay sistema.** La versión "participativa pura" (solo cuenta el que participa activamente) no entrega *nada*: con 3–6% de participación real, ningún proyecto junta fondos. La pieza aburrida — la regla por defecto — es la que convierte la participación en institución.

3. **Los que opinan activamente son ~3–5% y eso no cambia.** Da igual cómo se calibre: la proporción de ciudadanos que aporta señales de prioridad es de un dígito. Coincide con lo observado en presupuestos participativos reales. El diseño debe funcionar con esa minoría — y funciona, porque la delegación y los defaults amplifican su información.

4. **Las protecciones anti-corrupción funcionan juntas o no funcionan.** Quitar cualquier protección individual (inspección, retención de pagos, boletas, memoria reputacional) cuesta casi nada — quitarlas todas hunde el sistema *por debajo* del status quo. Son como los pernos de una rueda: sobra cualquiera, pero no sobran todos. Esto se convirtió en una regla formal del corpus: cada despliegue publica su "margen de disuasión".

5. **La transición es una perilla, no un salto.** Se puede partir entregando el 10% del presupuesto al nuevo sistema y subir gradualmente: cada punto extra paga, sin valle intermedio.

6. **La tubería importa: cuándo se libera el presupuesto y cuánta verificación hay.** Liberar todo el presupuesto el día uno congela meses de plata en obras a medio verificar. La regla ganadora: liberar contra un techo de obra-en-proceso. Y la capacidad de verificación es el techo de todo el sistema — con pocos verificadores, ninguna política presupuestaria lo arregla.

## La pregunta del presupuesto: ¿cuánto valor llega por cada peso, con y sin fiscalización humana?

Piénsalo como "¿cuántos pesos de obra verificada llegan por cada 100 pesos de gasto público total?" — donde "total" incluye el costo de pagarle a quien verifica.

| Sistema | Valor bruto por 100 | Costo de control por 100 | **Valor neto por 100 de gasto total** |
|---|---:|---:|---:|
| Status quo (sistema actual) | ~13 | (su propia auditoría, no descontada aquí) | **~13** |
| Core v0, fiscalización 100% humana | ~30 | 3 a 14 | **27 a 29** |
| Core v0, IA verifica + humanos como segunda instancia | ~31 | 2 a 9 | **28 a 30** |

Lecturas directas:

- **Solo cambiar de arquitectura** (aunque toda la fiscalización siga siendo humana) ya multiplica el valor entregado por ~2.2: de 13 a 27–29 netos. La ganancia grande viene del diseño, no de la IA.
- **Pasar la fiscalización a máquinas** (con humanos auditando a las máquinas) agrega entre 1 y 3 pesos más por cada 100 — porque el costo de control baja a menos de la mitad. Es ganancia real pero secundaria… **en condiciones normales**.
- **Donde la IA cambia el partido es cuando faltan fiscalizadores**: si la capacidad humana de verificación es escasa, el sistema humano-puro se cae a ~25 brutos y nada lo arregla; el triage con IA lo devuelve a ~31. La IA es un *seguro de capacidad*.
- **"Quitar" la fiscalización humana del todo no se puede** — no por nostalgia, sino por medición: los experimentos mostraron que sin auditores humanos nadie sabe cuánto se equivoca la máquina (y en un sistema sano los errores son tan raros que la única forma de medirla es ponerle trampas conocidas: los "controles sembrados"). El piso humano que queda es pequeño — muestreo, trampas de calibración, casos graves y denuncias — y su costo está incluido en los números de arriba.
- Nota de honestidad: al status quo no le descontamos su propio costo de auditoría (contraloría, etc.); si se lo descontáramos, la ventaja de Core v0 sería aún un poco mayor.

## El experimento nuevo con modelos de verdad

Al final probamos verificación con cinco modelos de IA reales (Gemma, Qwen, DeepSeek locales; GPT y Claude por servicio) juzgando 120 expedientes de evidencia con fallas conocidas. Sorpresa doble:

- **Cazar fraude mecánico resultó trivial**: todos los modelos detectan casi el 100% de fechas imposibles, fotos de otra ciudad, facturas infladas.
- **El problema real es aprobar lo honesto**: ante la instrucción "marca cualquier cosa sospechosa", unos modelos aprueban bien el trabajo limpio (Gemma marca solo 17% de falsas alarmas) y otros rechazan casi todo (Claude 95%, Qwen 100%). Si el verificador automático es paranoico, todo termina donde el humano igual — y la ganancia de capacidad se esfuma. La regla de diseño que salió: el primer filtro debe ser un modelo calibrado-permisivo; los paranoicos sirven de árbitros de segunda mirada.

## Lo que este paper NO dice

No dice que la arquitectura funcione en la realidad — dice que sobrevive a ataques simulados serios y que sus mecanismos están bien ranqueados. Las simulaciones usan supuestos declarados (señales honestas, presupuesto discrecional tipo proyectos, ley de compras por debajo del modelo). Los datos de comportamiento vienen de modelos de lenguaje *como sustituto declarado* de encuestas humanas que aún no se hacen. Y todo el circuito de crítica es del mismo autor — la validación independiente (revisores externos, piloto real) es el paso siguiente, no este paper.
