# -*- coding: utf-8 -*-
"""
====================================================================
UTVT - Taller de Copilot / IA - Laboratorios 1 al 7 (Clase 1)
Script interactivo para ejecutar y visualizar los laboratorios.
====================================================================
"""

import sys
import os
import time
from pathlib import Path

# Configurar encoding UTF-8 para consola de Windows
if sys.platform == "win32":
    try:
        os.system("chcp 65001 > nul")
    except Exception:
        pass
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

# Colores ANSI para terminal
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

LABS = {
    1: {
        "title": "Laboratorio 1: Análisis de Dependencias y Herramientas (pom.xml)",
        "video": "3 Dependencias del proyecto.mp4",
        "prompt": """Actúa como un ingeniero Java senior.
Analiza el archivo pom.xml de este proyecto.

Necesito que:
1. Identifiques la versión de Java.
2. Identifiques Spring Boot.
3. Expliques las dependencias principales.
4. Indiques qué herramientas necesito para compilarlo.
5. Señales posibles problemas de compatibilidad.

No modifiques archivos.
No inventes dependencias.
Responde mediante una tabla.""",
        "content": f"""
{BOLD}{CYAN}=== MATRIZ DE ANÁLISIS DE DEPENDENCIAS (pom.xml) ==={RESET}

+-------------------------------------+---------------------------------------------------------------+
| Aspecto                             | Detalle Técnico y Explicación                                 |
+-------------------------------------+---------------------------------------------------------------+
| Versión de Java                     | Java 25 (<properties><java.version>25</java.version>)         |
| Versión de Spring Boot              | 4.1.2 (spring-boot-starter-parent:4.1.2)                      |
| Dependencia: SpringDoc OpenAPI      | springdoc-openapi-starter-webmvc-ui:3.1.1 (Swagger UI REST)   |
| Dependencia: Web MVC                | spring-boot-starter-webmvc (Tomcat embebido, REST API)        |
| Dependencia: Data JPA               | spring-boot-starter-data-jpa (Hibernate, Repositorios)        |
| Dependencia: Bean Validation        | spring-boot-starter-validation (Validaciones @Valid, @NotNull) |
| Dependencia: Flyway Core y PG       | spring-boot-starter-flyway + flyway-database-postgresql       |
| Dependencia: Driver PostgreSQL      | postgresql (runtime - Conexión JDBC a base de datos)          |
| Dependencia: Spring Boot Test       | spring-boot-starter-test (JUnit 5, Mockito, AssertJ)          |
| Dependencia: Base de datos H2       | h2 (test - BD en memoria para tests sin levantar Postgres)    |
| Herramientas de Compilación         | 1. JDK 25 configurado en JAVA_HOME                            |
|                                     | 2. Apache Maven 3.9+ (o Maven Wrapper)                        |
|                                     | 3. spring-boot-maven-plugin para generar el fat JAR           |
| Riesgos de Compatibilidad           | 1. Java 25 es una versión muy reciente; si el entorno local o |
|                                     |    CI/CD usa Java 17 o 21, la compilación fallará.            |
|                                     | 2. Plugins de análisis estático (Lombok, JaCoCo) requieren    |
|                                     |    versiones recientes para soportar bytecode de Java 25.     |
+-------------------------------------+---------------------------------------------------------------+
"""
    },
    2: {
        "title": "Laboratorio 2: Análisis de Arquitectura y Principios SOLID",
        "video": "4 Comprender la arquitectura.mp4",
        "prompt": """Actúa como arquitecto de software Java.
Analiza las clases StudentController, StudentService,
StudentRepository, StudentMapper y Student.

Explica:
1. La arquitectura utilizada.
2. La responsabilidad de cada clase.
3. El flujo para registrar un estudiante.
4. Los principios SOLID observables.
5. Posibles oportunidades de mejora.

Distingue hechos confirmados de recomendaciones.
No inventes clases ni endpoints.
No generes ni modifiques código.

Presenta un diagrama textual y una tabla.""",
        "content": f"""
{BOLD}{CYAN}1. ARQUITECTURA UTILIZADA:{RESET}
Arquitectura en Capas (Layered / N-Tier Architecture) con estilo REST:
- Capa Web / API: StudentController (Manejo HTTP, códigos de estado 200/201).
- Capa de Servicio: StudentService (Reglas de negocio, transaccionalidad @Transactional).
- Capa de Persistencia: StudentRepository (Spring Data JPA, JpaSpecificationExecutor).
- Capa de Dominio: Student (Entidad persistente con @Version para control concurrente).
- Capa de Mapeo: StudentMapper (Desacopla DTOs inmutables del modelo relacional).

{BOLD}{CYAN}2. DIAGRAMA TEXTUAL DEL FLUJO DE REGISTRO (POST /api/v1/students):{RESET}

   [ Cliente HTTP ]
          │
          │ 1. POST /api/v1/students (JSON CreateStudentRequest)
          ▼
   [ StudentController ]
          │ 2. Valida sintácticamente (@Valid)
          │ 3. Invoca service.create(request)
          ▼
   [ StudentService ]  (Transacción @Transactional activa)
          │
          ├─► 4. repository.existsByStudentNumber(num)
          │        └─► ¿Existe? ──► SÍ ──► Lanza DuplicateStudentNumberException (409)
          │                         NO
          ├─► 5. mapper.toEntity(request)  ──► Crea entidad Student
          ├─► 6. repository.saveAndFlush(student) ──► Inserta en PostgreSQL
          ├─► 7. mapper.toResponse(student) ──► Genera StudentResponse DTO
          └─► 8. log.info("Student created: id={{}}", response.id())
          │
          ▼
   [ StudentController ]
          │ 9. Genera URI del recurso (Header Location: /api/v1/students/{{id}})
          │ 10. Retorna HTTP 201 Created con StudentResponse
          ▼
   [ Cliente HTTP ]

{BOLD}{CYAN}3. TABLA DE RESPONSABILIDADES Y SOLID:{RESET}

+-------------------+----------------------------+-----------------------+-----------------------------+
| Clase             | Responsabilidad            | Principios SOLID      | Hecho Confirmado / Mejora   |
+-------------------+----------------------------+-----------------------+-----------------------------+
| StudentController | Exponer endpoints REST     | SRP (Solo capa HTTP)  | Hecho: Inyección por ctor.  |
|                   | y validación @Valid        | DIP (Depende de serv) | Mejora: Validar query params|
+-------------------+----------------------------+-----------------------+-----------------------------+
| StudentService    | Lógica escolar, control    | SRP (Reglas negocio)  | Hecho: @Transactional       |
|                   | de unicidad y auditoría    | DIP (Inyección beans) | Mejora: Extraer Specs       |
+-------------------+----------------------------+-----------------------+-----------------------------+
| StudentRepository | Abstracción de persistencia| ISP (Extiende sólo    | Hecho: Consultas derivadas  |
|                   | y consultas dinámicas      | JpaRepository/Specs)  | Mejora: Índice pg_trgm      |
+-------------------+----------------------------+-----------------------+-----------------------------+
| StudentMapper     | Conversión DTO <-> Entity  | SRP (Solo mapeo)      | Hecho: Componente inyectable|
|                   | desacoplando contratos     |                       | Mejora: Migrar a MapStruct  |
+-------------------+----------------------------+-----------------------+-----------------------------+
| Student           | Modelo relacional tabla    | SRP (Entidad dominio) | Hecho: Incluye @Version     |
|                   | 'students' y concurrencia  |                       | Mejora: Métodos de dominio  |
+-------------------+----------------------------+-----------------------+-----------------------------+
"""
    },
    3: {
        "title": "Laboratorio 3: Propuesta de Clase Utilitaria StudentNameFormatter",
        "video": "2 Inline Chat.mp4 / 5 Caso de prueba...",
        "prompt": """Actúa como desarrollador Java senior.
Propón una clase StudentNameFormatter para este proyecto.

Requisitos:
- Crear un método estático format.
- Recibir nombre, apellido paterno y materno.
- Omitir valores null o vacíos.
- Eliminar espacios sobrantes.
- No modificar entidades ni DTO existentes.
- Utilizar únicamente Java estándar.
- Documentar con JavaDoc.
- Incluir tres ejemplos de entrada y salida.

Muestra el código propuesto, sin modificar archivos.""",
        "content": f"""
{BOLD}{CYAN}CÓDIGO PROPUESTO PARA StudentNameFormatter:{RESET}

```java
package mx.edu.utvt.schoolmanagement.util;

import java.util.Objects;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Utilidad encargada de normalizar y formatear el nombre completo de un estudiante.
 * Concatenación limpia ignorando valores nulos o vacíos y eliminando espacios redundantes.
 */
public final class StudentNameFormatter {{

    private StudentNameFormatter() {{
        throw new UnsupportedOperationException("No se permite instanciar StudentNameFormatter");
    }}

    /**
     * Da formato y concatena los componentes del nombre de un estudiante.
     *
     * @param firstName       Nombre de pila (puede ser nulo o contener espacios).
     * @param paternalSurname Apellido paterno (puede ser nulo o vacío).
     * @param maternalSurname Apellido materno (puede ser nulo o vacío).
     * @return Cadena formateada sin espacios duplicados, o cadena vacía si no hay datos válidos.
     */
    public static String format(String firstName, String paternalSurname, String maternalSurname) {{
        return Stream.of(firstName, paternalSurname, maternalSurname)
                .filter(Objects::nonNull)
                .map(String::strip)
                .filter(part -> !part.isEmpty())
                .collect(Collectors.joining(" "));
    }}
}}
```

{BOLD}{GREEN}TRES EJEMPLOS DE ENTRADA Y SALIDA:{RESET}
1. format("  Juan Carlos  ", " Pérez ", "López")  -->  "Juan Carlos Pérez López"
2. format("María", "Gómez", null)                  -->  "María Gómez"
3. format("   ", "Rodríguez", "")                  -->  "Rodríguez"
"""
    },
    4: {
        "title": "Laboratorio 4: Pruebas Unitarias JUnit 5 y Mockito para StudentService",
        "video": "5 Caso de prueba y validaciones.mp4",
        "prompt": """Genera el prompt para las pruebas de JUnit y Mockito para la capa de servicicio: StudentService
Genera el código correspondiente del prompt anterior.""",
        "content": f"""
{BOLD}{CYAN}PARTE 1: PROMPT ÓPTIMO GENERADO:{RESET}
"Actúa como un ingeniero QA senior en Java 25. Genera la suite de pruebas unitarias con JUnit 5
 y Mockito para `StudentService`. Emplea `@ExtendWith(MockitoExtension.class)`, `@Mock` para
 `StudentRepository` y `StudentMapper`, e `@InjectMocks`. Cubre: create (éxito y colisión),
 findById (encontrado y 404), findAll (capturando Pageable con ArgumentCaptor), update y updateStatus.
 Aísla completamente la base de datos y usa el patrón Arrange-Act-Assert."

{BOLD}{CYAN}PARTE 2: RESUMEN DE MÉTODOS DE PRUEBA GENERADOS:{RESET}
- createsAndPersistsStudent(): Verifica éxito al guardar cuando la matrícula es única.
- rejectsDuplicateStudentNumberOnCreation(): Lanza DuplicateStudentNumberException y no guarda.
- findsStudentById(): Retorna StudentResponse cuando el id existe en el repositorio.
- reportsMissingStudentById(): Lanza StudentNotFoundException cuando el id no existe.
- returnsPagedStudentsUsingRequestedPageAndSize(): Valida ordenamiento 'id' y captura de Pageable.
- updatesStudentDetails(): Modifica atributos del estudiante si no hay colisión de matrícula.
- rejectsStudentNumberUsedByAnotherStudentOnUpdate(): Impide asignar matrícula ocupada por otro.
- updatesStudentActiveStatus(): Comprueba el soft-status (activación/desactivación).

{BOLD}{GREEN}Comando para ejecutar las pruebas en tu consola:{RESET}
  mvn test -Dtest=StudentServiceTest
"""
    },
    5: {
        "title": "Laboratorio 5: Análisis de Requerimiento (Búsqueda Parcial por Apellido Paterno)",
        "video": "5 Caso de prueba y validaciones.mp4",
        "prompt": """Analiza el requerimiento de buscar estudiantes por coincidencia parcial de apellido paterno.
Contexto: Proyecto school-management, Java 25, Spring Boot 4.1.2 y PostgreSQL.
Revisa los filtros que ya existen.

Entrega:
1. Historia de usuario.
2. Reglas funcionales.
3. Restricciones técnicas.
4. Supuestos y decisiones pendientes.
5. Criterios de aceptación Given/When/Then.
6. Riesgos de compatibilidad.
7. Archivos potencialmente afectados.

No escribas ni modifiques código.""",
        "content": f"""
{BOLD}{CYAN}1. HISTORIA DE USUARIO:{RESET}
Como administrador escolar, quiero filtrar estudiantes por coincidencia parcial de su apellido
paterno para localizarlos rápidamente sin conocer su matrícula o apellido exacto.

{BOLD}{CYAN}2. REGLAS FUNCIONALES:{RESET}
- Parámetro opcional: `paternalSurname`.
- Coincidencia parcial tipo 'contains' (%valor%).
- Insensible a mayúsculas y minúsculas (case-insensitive).
- Se combina con operador lógico AND junto a `active` y `studentNumber`.
- Espacios iniciales/finales se eliminan con strip(); cadenas vacías se ignoran.

{BOLD}{CYAN}3. RESTRICCIONES TÉCNICAS:{RESET}
- No modificar el esquema relacional de PostgreSQL.
- Mantener el contrato `PageResponse<StudentResponse>`.
- Longitud máxima permitida: 100 caracteres.
- Escapar caracteres especiales SQL (% y _).

{BOLD}{CYAN}4. CRITERIOS DE ACEPTACIÓN (GIVEN / WHEN / THEN):{RESET}
- Escenario 1: Coincidencia parcial y minúsculas (GET ?paternalSurname=her -> encuentra 'Hernández').
- Escenario 2: Coexistencia con active=true (GET ?paternalSurname=garcia&active=true).
- Escenario 3: Filtro en blanco (GET ?paternalSurname=   -> lista todos sin filtrar).
- Escenario 4: Longitud excesiva > 100 caracteres -> Retorna HTTP 400 Bad Request.

{BOLD}{CYAN}5. ARCHIVOS AFECTADOS:{RESET}
- StudentController.java (nuevo parámetro query).
- StudentService.java (nueva cláusula en CriteriaBuilder Specification).
- StudentServiceTest.java y StudentApiIntegrationTest.java (pruebas).
"""
    },
    6: {
        "title": "Laboratorio 6: Plan de Ampliación de Endpoint (/plan GET /api/v1/students)",
        "video": "6 Agent plan.mp4",
        "prompt": """/plan Diseña una ampliación de GET /api/v1/students.

Nuevo parámetro opcional: paternalSurname

Reglas:
- Coincidencia parcial.
- Ignorar diferencias entre mayúsculas y minúsculas.
- Conservar page, size, active y studentNumber.
- No cambiar el formato PageResponse.
- No crear nuevos endpoints innecesarios.
- No modificar el esquema de PostgreSQL.

Entrega el contrato HTTP, ejemplos, archivos afectados, criterios de aceptación y posibles riesgos de compatibilidad.

No implementes nada.""",
        "content": f"""
{BOLD}{CYAN}CONTRATO HTTP (OpenAPI 3 / GET /api/v1/students):{RESET}
Query Parameters:
  - page (int, default=0, min=0)
  - size (int, default=20, min=1, max=100)
  - active (boolean, opcional)
  - studentNumber (string, opcional, exacto)
  - paternalSurname (string, opcional, max=100, parcial case-insensitive)

Respuestas:
  - 200 OK: PageResponse<StudentResponse>
  - 400 Bad Request: ProblemDetail (parámetros fuera de rango o tamaño > 100)

{BOLD}{CYAN}EJEMPLO DE PETICIÓN Y RESPUESTA:{RESET}
curl -X GET "http://localhost:8080/api/v1/students?paternalSurname=lop&active=true&page=0&size=10"

Respuesta 200 OK:
{{
  "content": [
    {{
      "id": 14,
      "studentNumber": "2024-0014",
      "firstName": "Carlos",
      "paternalSurname": "López",
      "maternalSurname": "Hernández",
      "email": "carlos.lopez@utvt.edu.mx",
      "dateOfBirth": "2002-05-18",
      "active": true
    }}
  ],
  "page": 0,
  "size": 10,
  "totalElements": 1,
  "totalPages": 1
}}
"""
    },
    7: {
        "title": "Laboratorio 7: Plan de Validaciones y Excepciones (RFC 7807)",
        "video": "6 Agent plan.mp4",
        "prompt": """/plan Analiza las validaciones y excepciones de school-management.

Revisa los DTO actuales, StudentController y GlobalExceptionHandler.

Diseña la validación de paternalSurname:
- Parámetro opcional.
- Máximo 100 caracteres.
- Entrada vacía equivale a filtro ausente.
- Entradas inválidas deben generar 400.
- Mantener ProblemDetail.

Distingue errores 400, 404 y 409.
Señala lo que ya existe y lo que falta.

Entrega matriz de reglas y plan de pruebas.
No modifiques archivos.""",
        "content": f"""
{BOLD}{CYAN}TAXONOMÍA DE CÓDIGOS DE ERROR HTTP EN EL SISTEMA:{RESET}
- HTTP 400 Bad Request: Violación sintáctica (size > 100, page < 0, paternalSurname > 100 caracteres).
- HTTP 404 Not Found: Recurso no encontrado (StudentNotFoundException por ID inexistente).
- HTTP 409 Conflict: Conflicto de unicidad (DuplicateStudentNumberException) o versión concurrente.

{BOLD}{CYAN}MATRIZ DE REGLAS DE VALIDACIÓN PARA paternalSurname:{RESET}
+------------------------------+--------------------+---------------+------------------------------+
| Entrada de paternalSurname   | Código HTTP        | Formato       | Comportamiento               |
+------------------------------+--------------------+---------------+------------------------------+
| Ausente (no enviado)         | 200 OK             | PageResponse  | No se aplica filtro          |
| Válido (ej: "Gomez")         | 200 OK             | PageResponse  | Busca coincidencia parcial   |
| Con espacios ("  Perez  ")   | 200 OK             | PageResponse  | Se aplica strip() -> "perez" |
| Vacío o sólo espacios ("   ")| 200 OK             | PageResponse  | Se detecta .isBlank(), ignora|
| Exactamente 100 caracteres   | 200 OK             | PageResponse  | Aceptado, límite superior    |
| 101 caracteres o más         | 400 Bad Request    | ProblemDetail | Rechazado por Bean Validation|
+------------------------------+--------------------+---------------+------------------------------+

{BOLD}{CYAN}ESTRUCTURA DEL ERROR 400 CON ProblemDetail (RFC 7807):{RESET}
{{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Validation failed for method parameter",
  "instance": "/api/v1/students",
  "properties": {{
    "invalidParams": [
      {{ "name": "paternalSurname", "reason": "el tamaño debe estar entre 0 y 100" }}
    ]
  }}
}}
"""
    }
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print(f"{BOLD}{BLUE}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}       UTVT - TALLER DE COPILOT / IA (CLASE 1: LABORATORIOS 1 AL 7)   {RESET}")
    print(f"{BOLD}{BLUE}======================================================================{RESET}")


def show_lab(lab_id):
    lab = LABS.get(lab_id)
    if not lab:
        return
    clear_screen()
    print_header()
    print(f"\n{BOLD}{YELLOW}>> {lab['title']}{RESET}")
    print(f"{MAGENTA}Video de referencia:{RESET} {lab['video']}")
    print(f"\n{BOLD}[ PROMPT ENVIADO A LA IA ]:{RESET}")
    print(f"{YELLOW}------------------------------------------------------------{RESET}")
    print(lab["prompt"])
    print(f"{YELLOW}------------------------------------------------------------{RESET}")
    print(f"\n{BOLD}[ RESULTADO / RESOLUCIÓN GENERADA ]:{RESET}")
    print(lab["content"])
    input(f"\n{GREEN}Presione [ENTER] para volver al menú principal...{RESET}")


def run_all_labs():
    clear_screen()
    print_header()
    print(f"\n{BOLD}{GREEN}Ejecutando la secuencia completa de los 7 laboratorios...{RESET}\n")
    time.sleep(1)

    for i in range(1, 8):
        lab = LABS[i]
        print(f"\n{BOLD}{YELLOW}============================================================{RESET}")
        print(f"{BOLD}{CYAN}[{i}/7] {lab['title']}{RESET}")
        print(f"{MAGENTA}Video asociado: {lab['video']}{RESET}")
        print(f"{BOLD}{YELLOW}============================================================{RESET}")
        print(lab["content"])
        time.sleep(1)

    export_reports()
    input(f"\n{GREEN}Secuencia finalizada. Presione [ENTER] para volver al menú...{RESET}")


def export_reports():
    base_dir = Path(__file__).resolve().parent
    md_path = base_dir / "Reporte_Laboratorios_Clase_1.md"
    html_path = base_dir / "Reporte_Laboratorios_Clase_1.html"

    # Generar Markdown
    md_content = ["# UTVT - Reporte de Laboratorios Clase 1\n"]
    for i in range(1, 8):
        lab = LABS[i]
        md_content.append(f"## {lab['title']}\n")
        md_content.append(f"**Video asociado:** `{lab['video']}`\n")
        md_content.append("### Prompt:\n```text\n" + lab["prompt"] + "\n```\n")
        # Quitar códigos de escape ANSI
        clean_content = lab["content"]
        for code in [CYAN, GREEN, YELLOW, BLUE, MAGENTA, BOLD, RESET]:
            clean_content = clean_content.replace(code, "")
        md_content.append(f"### Resolución:\n{clean_content}\n")
        md_content.append("---\n")

    md_path.write_text("\n".join(md_content), encoding="utf-8")

    # Generar HTML con diseño profesional
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Reporte Laboratorios 1 al 7 - UTVT School Management</title>
<style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px 40px; background: #0f172a; color: #f1f5f9; }}
    h1 {{ color: #38bdf8; border-bottom: 2px solid #1e293b; padding-bottom: 12px; }}
    h2 {{ color: #60a5fa; margin-top: 30px; }}
    .badge {{ background: #1e293b; padding: 4px 10px; border-radius: 4px; color: #cbd5e1; font-size: 0.9em; }}
    pre {{ background: #1e293b; color: #a5f3fc; padding: 15px; border-radius: 8px; overflow-x: auto; font-family: Consolas, monospace; border: 1px solid #334155; }}
    .card {{ background: #1e293b; border-left: 4px solid #38bdf8; padding: 15px 20px; border-radius: 6px; margin: 15px 0; }}
</style>
</head>
<body>
<h1>UTVT - Reporte de Laboratorios Clase 1 (Copilot / IA)</h1>
<p><strong>Proyecto:</strong> school-management (Java 25, Spring Boot 4.1.2, PostgreSQL)</p>
<hr style="border: 0; border-top: 1px solid #334155;">
"""
    for i in range(1, 8):
        lab = LABS[i]
        clean_content = lab["content"]
        for code in [CYAN, GREEN, YELLOW, BLUE, MAGENTA, BOLD, RESET]:
            clean_content = clean_content.replace(code, "")
        html_content += f"""
<h2>{lab['title']}</h2>
<span class="badge">Video: {lab['video']}</span>
<div class="card">
<strong>Prompt:</strong>
<pre>{lab['prompt']}</pre>
<strong>Resolución:</strong>
<pre>{clean_content}</pre>
</div>
"""
    html_content += """
</body>
</html>
"""
    html_path.write_text(html_content, encoding="utf-8")
    print(f"\n{BOLD}{GREEN}>> Reportes generados con éxito:{RESET}")
    print(f"   - Markdown: {md_path}")
    print(f"   - HTML Web: {html_path}")


def main_menu():
    while True:
        clear_screen()
        print_header()
        print(f"\n{BOLD}Seleccione una opción para visualizar su ejecución:{RESET}\n")
        print(f"  {CYAN}[1]{RESET} Laboratorio 1: Análisis de Dependencias (pom.xml)")
        print(f"  {CYAN}[2]{RESET} Laboratorio 2: Arquitectura de Software y Principios SOLID")
        print(f"  {CYAN}[3]{RESET} Laboratorio 3: Propuesta StudentNameFormatter (Java estándar)")
        print(f"  {CYAN}[4]{RESET} Laboratorio 4: Pruebas JUnit 5 y Mockito para StudentService")
        print(f"  {CYAN}[5]{RESET} Laboratorio 5: Análisis de Requerimiento (Búsqueda Parcial)")
        print(f"  {CYAN}[6]{RESET} Laboratorio 6: Plan de Ampliación de Endpoint (/plan)")
        print(f"  {CYAN}[7]{RESET} Laboratorio 7: Plan de Validaciones y Excepciones (RFC 7807)")
        print(f"  {GREEN}[8]{RESET} {BOLD}Ejecutar TODOS los laboratorios en secuencia{RESET}")
        print(f"  {YELLOW}[9]{RESET} Exportar reporte completo a Markdown y HTML")
        print(f"  {MAGENTA}[0]{RESET} Salir\n")

        opcion = input(f"{BOLD}Ingrese opción [0-9]: {RESET}").strip()

        if opcion in [str(i) for i in range(1, 8)]:
            show_lab(int(opcion))
        elif opcion == "8":
            run_all_labs()
        elif opcion == "9":
            export_reports()
            input(f"\n{GREEN}Presione [ENTER] para volver al menú...{RESET}")
        elif opcion == "0":
            clear_screen()
            print(f"\n{BOLD}{GREEN}¡Hasta pronto! Éxito en tu práctica.{RESET}\n")
            sys.exit(0)
        else:
            input(f"\n{YELLOW}Opción no válida. Presione [ENTER] para reintentar...{RESET}")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Ejecución interrumpida por el usuario.{RESET}\n")
