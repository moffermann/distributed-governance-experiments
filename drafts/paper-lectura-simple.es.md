# El paper de experimentos, contado en simple

Versión de lectura fácil del borrador (`paper.md` / `paper.es.md`). Mismos resultados, sin jerga. Cada afirmación tiene detrás un experimento reproducible en este repositorio.

## De qué se trata

El paper maestro propone una arquitectura (Core v0) donde los ciudadanos dirigen partes del presupuesto público a proyectos concretos, con pagos por avance verificado, y donde el dinero de quienes no participan igual fluye según **las reglas de asignación** de cada ciudadano (su "perfil"), no según un plan central. Este segundo paper cuenta qué pasó cuando **atacamos esa arquitectura con simulaciones durante todo un programa de experimentos**: poblaciones realistas que adoptan o abandonan la plataforma, atacantes que coluden y capturan agendas, presupuestos que se congelan, verificadores humanos y de inteligencia artificial, y años simulados de operación.

La regla del juego fue: **escribir las predicciones antes de correr cada experimento y publicar también las que salieron mal**. De más de 40 predicciones registradas, cerca de un tercio fallaron o no se pudieron probar — y varias de esas fallas son los hallazgos más útiles.

## Los hallazgos, en una frase cada uno

1. **La ventaja se mantiene con gente real.** Con poblaciones que se comportan como personas (se aburren, desconfían, delegan), la arquitectura entrega entre 2 y 2.7 veces más valor verificado por peso que el sistema actual — y rinde *mejor* cuando participa poca gente, siempre que la asignación por defecto esté bien alineada con lo que la sociedad valora.

2. **Sin regla por defecto, no hay sistema.** La versión "participativa pura" (solo cuenta el que participa activamente) no entrega *nada*: con 3–6% de participación real, ningún proyecto junta fondos. La pieza aburrida — que la parte pasiva igual se asigne por reglas distribuidas — es la que convierte la participación en institución.

3. **La calidad de asignación manda, y tiene dos capas.** Este es el hallazgo que más nos costó entender bien. Hay que separar dos cosas que el modelo antes confundía:
   - **La categorización macro** (qué *tipos* de proyecto son elegibles: "educación", "salud rural"…). No reparte plata; solo define las casillas. Un planificador central puede trazar malas casillas.
   - **Las reglas de asignación de la gente** (cómo cada ciudadano manda su parte a proyectos concretos: "cerca de mí", "por financiarse", "escuelas rurales"…). Esto es lo que *gobierna* la entrega.
   
   Lo importante: **distribuir la categorización es un seguro contra una mala planificación central.** Si la autoridad traza buenas casillas, da lo mismo. Si traza malas, el sistema distribuido *re-categoriza* hacia el valor y no se cae — mientras el sistema central queda atrapado en sus malas casillas. Por eso, comparando arquitecturas, la ventaja de Core v0 sobre el sistema central **no es fija: crece de ~2× (buena planificación) a ~5× (mala planificación)**, porque se suman dos efectos: *la ventaja de elegir* y *evitar que te impongan un mal plan*.

4. **Los que opinan activamente son ~3–5% y eso no cambia.** Da igual cómo se calibre: la proporción de ciudadanos que aporta señales de prioridad es de un dígito. Coincide con lo observado en presupuestos participativos reales. El diseño debe funcionar con esa minoría — y funciona, porque la delegación y los defaults amplifican su información.

5. **Las protecciones anti-corrupción funcionan juntas o no funcionan.** Quitar cualquier protección individual (inspección, retención de pagos, boletas, memoria reputacional) cuesta casi nada — quitarlas todas hunde el sistema *por debajo* del status quo. Son como los pernos de una rueda: sobra cualquiera, pero no sobran todos. Esto se convirtió en una regla formal del corpus: cada despliegue publica su "margen de disuasión".

6. **La transición es una perilla, no un salto.** Se puede partir entregando el 10% del presupuesto al nuevo sistema y subir gradualmente: cada punto extra paga, sin valle intermedio.

7. **La tubería importa: cuándo se libera el presupuesto y cuánta verificación hay.** Liberar todo el presupuesto el día uno congela meses de plata en obras a medio verificar. La regla ganadora: liberar contra un techo de obra-en-proceso. Y la capacidad de verificación es el techo de todo el sistema — con pocos verificadores, ninguna política presupuestaria lo arregla.

Y dos hallazgos más, que dejamos con menos confianza y lo decimos:

8. **La verificación por IA, medida de verdad — con un error corregido a la vista.** Probamos cinco modelos reales (Gemma, Qwen, DeepSeek locales; GPT y Claude por servicio) juzgando expedientes de obra con fallas conocidas. Cazar fraude mecánico (fechas imposibles, fotos de otra ciudad) es trivial: todos lo detectan. El problema real es *aprobar lo honesto sin marcarlo mal*. Una segunda ronda de revisión interna **encontró un error de constructo** en nuestro primer instrumento (las boletas "limpias" traían un ítem sin aprobar que los modelos correctamente marcaban, y los penalizábamos por eso). Corregido: los modelos de frontera (GPT, Claude) rinden bien y parejo (~3–8% de falsas alarmas); los locales pequeños son más débiles. La lección: la capa de máquina cubre solo el fraude *que está en el papeleo* — la colusión previa al contrato y la obra de mala calidad que "fotografía bien" siguen necesitando al ojo humano.

9. **La colusión es el ataque que de verdad rompe la historia.** Un anillo que controla al ejecutor, a su verificador y a la evidencia ciudadana a la vez multiplica la fuga por veinticinco — porque saltea la disuasión hito por hito. La ventaja de valor entregado *sobrevive* (la mayoría honesta carga la entrega), pero la resistencia a la colusión (identidad verificada, descentralizar quién asigna y audita) pasa a ser un requisito de primera clase, no un detalle.

## La pregunta del presupuesto: ¿cuánto valor llega por cada peso, con y sin fiscalización humana?

Piénsalo como "¿cuántos pesos de obra verificada llegan por cada 100 pesos de gasto público total?" — donde "total" incluye el costo de pagarle a quien verifica.

| Sistema | Valor bruto por 100 | Costo de control por 100 | **Valor neto por 100 de gasto total** |
|---|---:|---:|---:|
| Status quo (sistema actual) | ~13 | (su propia auditoría, no descontada aquí) | **~13** |
| Core v0, fiscalización 100% humana | ~30 | 3 a 14 | **27 a 29** |
| Core v0, IA verifica + humanos como segunda instancia | ~31 | 2 a 9 | **28 a 30** |

Lecturas directas:

- **Solo cambiar de arquitectura** (aunque toda la fiscalización siga siendo humana) ya multiplica el valor entregado por ~2.2: de 13 a 27–29 netos. La ganancia grande viene del diseño, no de la IA.
- **Pasar la fiscalización a máquinas** (con humanos auditando a las máquinas) agrega entre 1 y 3 pesos más por cada 100 — porque el costo de control baja a menos de la mitad. Ganancia real pero secundaria… **en condiciones normales**.
- **Donde la IA cambia el partido es cuando faltan fiscalizadores**: si la capacidad humana es escasa, el sistema humano-puro se cae y nada lo arregla; el triage con IA lo devuelve arriba. La IA es un *seguro de capacidad*.
- **"Quitar" la fiscalización humana del todo no se puede** — no por nostalgia, sino por medición: sin auditores humanos nadie sabe cuánto se equivoca la máquina (en un sistema sano los errores son tan raros que la única forma de medirla es ponerle trampas conocidas: los "controles sembrados"). El piso humano que queda es pequeño — muestreo, trampas de calibración, casos graves y denuncias — y su costo está incluido arriba.
- Nota de honestidad: al status quo no le descontamos su propio costo de auditoría; si se lo descontáramos, la ventaja de Core v0 sería aún un poco mayor.

## Lo que este paper NO dice

No dice que la arquitectura funcione en la realidad — dice que sobrevive a ataques simulados serios y que sus mecanismos están bien ranqueados. Las simulaciones usan supuestos declarados (señales honestas, presupuesto discrecional tipo proyectos, ley de compras por debajo del modelo). Los datos de comportamiento vienen de modelos de lenguaje *como sustituto declarado* de encuestas humanas que aún no se hacen. Y todo el circuito de crítica es del mismo autor — la validación independiente (revisores externos, piloto real) es el paso siguiente, no este paper.
