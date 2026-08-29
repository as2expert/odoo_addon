# AS2EXPERT

**Intercambio B2B de nivel empresarial, sin la infraestructura de nivel empresarial.**

AS2EXPERT es una plataforma cloud para el intercambio seguro de documentos entre
empresas. Firma, cifra, transporta y acusa recibo de cada mensaje siguiendo los
estándares que exigen las grandes cadenas de distribución, la industria y la
logística —AS2 y EDIFACT— pero elimina el coste, la fragilidad y la carga
operativa de montar y mantener ese stack por tu cuenta.

Donde antes hacían falta un servidor AS2, certificados que renovar, un experto en
EDI y semanas de puesta en marcha por cada socio, AS2EXPERT reduce todo a una
consola clara y una API documentada.

---

## El problema que resuelve

Conectarse con un partner por AS2 debería ser trivial. En la práctica no lo es:

- **El protocolo es exigente.** Firma digital, cifrado, MDN síncronos y
  asíncronos, verificación del MIC, políticas distintas por socio. Un detalle mal
  configurado y el mensaje se rechaza sin explicación clara.
- **Los certificados caducan.** Y cuando lo hacen, el flujo se detiene —a menudo
  en silencio, hasta que alguien reclama la factura o el pedido que no llegó.
- **EDIFACT es un mundo.** Decenas de directorios UNECE, envolturas UNB/UNH,
  mensajes ORDERS, DESADV, INVOIC, CONTRL… cada cliente con su matiz.
- **Cada integración se paga dos veces:** una al construirla y otra, cada mes, en
  mantenerla viva.

El resultado habitual es un sistema crítico que nadie quiere tocar y que solo una
persona entiende. AS2EXPERT existe para que ese riesgo deje de ser tuyo.

---

## Qué obtienes

### Un motor AS2 gestionado, listo para producción
Firma y cifrado extremo a extremo, MDN **síncronos y asíncronos**, control del
MIC y **política por socio**. Tú defines con quién hablas; la plataforma se ocupa
del handshake criptográfico, del acuse de recibo y de la trazabilidad de cada
mensaje. Sin servidor AS2 que operar, sin puertos que abrir en tu red.

### Certificados sin sobresaltos
La gestión de certificados —alta, rotación, vigencia— vive dentro de la
plataforma. El objetivo es simple: que un certificado a punto de caducar nunca
sea la causa de que un pedido se pierda.

### EDIFACT como herramienta de primera clase
Más que un transporte: AS2EXPERT **entiende** el documento. Analiza envolturas
UNB/UNH, reconoce los directorios UNECE y te da una lectura clara de ORDERS,
DESADV, INVOIC o CONTRL directamente desde el mensaje recibido. El EDI deja de
ser una caja negra y pasa a ser algo que puedes inspeccionar y auditar.

### Dos vías de integración, un mismo resultado
- **API REST** con autenticación por token: estaciones, socios, certificados,
  envío y descarga de mensajes, todo desde tu propio software.
- **SFTP nativo** para los flujos por carpeta de siempre.
- **Webhooks** para reaccionar en tiempo real a cada mensaje entrante.

Elige la que encaja con cada partner sin cambiar de plataforma.

### Conectores para tu ERP
El transporte se acerca a donde ya trabajas. El **conector de Odoo** —de código
abierto— convierte tu ERP en un buzón AS2: enviar un fichero es adjuntarlo y
pulsar un botón; recibirlo, encontrarlo ya en tu bandeja. La lógica pesada se
queda en la plataforma; tu ERP solo intercambia ficheros.

---

## Por qué AS2EXPERT

**Time-to-partner en horas, no en semanas.** Dar de alta un socio es
configuración, no un proyecto. La complejidad del protocolo está resuelta de
fábrica.

**Coste total predecible.** Sin servidores que dimensionar, sin licencias de
middleware EDI, sin la partida oculta de mantenimiento que se lleva cada mes un
trozo del presupuesto de IT.

**Robusto por diseño.** La entrada de mensajes combina webhook en tiempo real con
un sondeo de respaldo: si un aviso se pierde, el mensaje llega igual. La API es la
fuente de verdad; el webhook, un acelerador.

**Seguro de serie.** Cifrado y firma en cada mensaje, tokens revocables,
verificación de firma en los webhooks. La seguridad no es una opción que haya que
acordarse de activar.

**Abierto donde importa.** API documentada, webhooks estándar y conectores de
código abierto: no quedas atrapado: integras a tu manera.

**Sin lock-in operativo.** Tú mantienes tus mapeos y tu lógica de negocio donde
ya viven. AS2EXPERT se ocupa del transporte, el protocolo y el cumplimiento —no
de secuestrar tus procesos.

---

## Para quién

- **Proveedores** que necesitan conectarse con la cadena de distribución sin
  montar una plataforma EDI propia.
- **Equipos de IT y logística** que quieren dejar de ser el sostén frágil de un
  servidor AS2 heredado.
- **Software y ERPs** que quieren ofrecer AS2/EDIFACT a sus clientes con una
  simple llamada a una API.

---

## En una frase

AS2EXPERT convierte un requisito técnico intimidante —"tienes que conectarte por
AS2 y hablar EDIFACT"— en algo que se resuelve con una cuenta, un token y una
tarde de trabajo.

> **AS2EXPERT** · Intercambio B2B seguro, sin fricción · [www.as2expert.com](https://www.as2expert.com)
