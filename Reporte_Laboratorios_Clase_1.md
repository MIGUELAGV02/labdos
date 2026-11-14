# UTVT - Reporte de Laboratorios Clase 1

## Laboratorio 1: Análisis de Dependencias y Herramientas (pom.xml)

**Video asociado:** `3 Dependencias del proyecto.mp4`

### Prompt:
```text
Actúa como un ingeniero Java senior.
Analiza el archivo pom.xml de este proyecto.

Necesito que:
1. Identifiques la versión de Java.
2. Identifiques Spring Boot.
3. Expliques las dependencias principales.
4. Indiques qué herramientas necesito para compilarlo.
5. Señales posibles problemas de compatibilidad.

No modifiques archivos.
No inventes dependencias.
Responde mediante una tabla.
```

### Resolución:

=== MATRIZ DE ANÁLISIS DE DEPENDENCIAS (pom.xml) ===

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


---

## Laboratorio 2: Análisis de Arquitectura y Principios SOLID

**Video asociado:** `4 Comprender la arquitectura.mp4`

### Prompt:
```text
Actúa como arquitecto de software Java.
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

Presenta un diagrama textual y una tabla.
```

### Resolución:

1. ARQUITECTURA UTILIZADA:
Arquitectura en Capas (Layered / N-Tier Architecture) con estilo REST:
- Capa Web / API: StudentController (Manejo HTTP, códigos de estado 200/201).
- Capa de Servicio: StudentService (Reglas de negocio, transaccionalidad @Transactional).
- Capa de Persistencia: StudentRepository (Spring Data JPA, JpaSpecificationExecutor).
- Capa de Dominio: Student (Entidad persistente con @Version para control concurrente).
- Capa de Mapeo: StudentMapper (Desacopla DTOs inmutables del modelo relacional).

2. DIAGRAMA TEXTUAL DEL FLUJO DE REGISTRO (POST /api/v1/students):

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
          └─► 8. log.info("Student created: id={}", response.id())
          │
          ▼
   [ StudentController ]
          │ 9. Genera URI del recurso (Header Location: /api/v1/students/{id})
          │ 10. Retorna HTTP 201 Created con StudentResponse
          ▼
   [ Cliente HTTP ]

3. TABLA DE RESPONSABILIDADES Y SOLID:

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


---

## Laboratorio 3: Propuesta de Clase Utilitaria StudentNameFormatter

**Video asociado:** `2 Inline Chat.mp4 / 5 Caso de prueba...`

### Prompt:
```text
Actúa como desarrollador Java senior.
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

Muestra el código propuesto, sin modificar archivos.
```

### Resolución:

CÓDIGO PROPUESTO PARA StudentNameFormatter:

```java
package mx.edu.utvt.schoolmanagement.util;

import java.util.Objects;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Utilidad encargada de normalizar y formatear el nombre completo de un estudiante.
 * Concatenación limpia ignorando valores nulos o vacíos y eliminando espacios redundantes.
 */
public final class StudentNameFormatter {

    private StudentNameFormatter() {
        throw new UnsupportedOperationException("No se permite instanciar StudentNameFormatter");
    }

    /**
     * Da formato y concatena los componentes del nombre de un estudiante.
     *
     * @param firstName       Nombre de pila (puede ser nulo o contener espacios).
     * @param paternalSurname Apellido paterno (puede ser nulo o vacío).
     * @param maternalSurname Apellido materno (puede ser nulo o vacío).
     * @return Cadena formateada sin espacios duplicados, o cadena vacía si no hay datos válidos.
     */
    public static String format(String firstName, String paternalSurname, String maternalSurname) {
        return Stream.of(firstName, paternalSurname, maternalSurname)
                .filter(Objects::nonNull)
                .map(String::strip)
                .filter(part -> !part.isEmpty())
                .collect(Collectors.joining(" "));
    }
}
```

TRES EJEMPLOS DE ENTRADA Y SALIDA:
1. format("  Juan Carlos  ", " Pérez ", "López")  -->  "Juan Carlos Pérez López"
2. format("María", "Gómez", null)                  -->  "María Gómez"
3. format("   ", "Rodríguez", "")                  -->  "Rodríguez"


---

## Laboratorio 4: Pruebas Unitarias JUnit 5 y Mockito para StudentService

**Video asociado:** `5 Caso de prueba y validaciones.mp4`

### Prompt:
```text
Genera el prompt para las pruebas de JUnit y Mockito para la capa de servicicio: StudentService
Genera el código correspondiente del prompt anterior.
```

### Resolución:

PARTE 1: PROMPT ÓPTIMO GENERADO:
"Actúa como un ingeniero QA senior en Java 25. Genera la suite de pruebas unitarias con JUnit 5
 y Mockito para `StudentService`. Emplea `@ExtendWith(MockitoExtension.class)`, `@Mock` para
 `StudentRepository` y `StudentMapper`, e `@InjectMocks`. Cubre: create (éxito y colisión),
 findById (encontrado y 404), findAll (capturando Pageable con ArgumentCaptor), update y updateStatus.
 Aísla completamente la base de datos y usa el patrón Arrange-Act-Assert."

PARTE 2: RESUMEN DE MÉTODOS DE PRUEBA GENERADOS:
- createsAndPersistsStudent(): Verifica éxito al guardar cuando la matrícula es única.
- rejectsDuplicateStudentNumberOnCreation(): Lanza DuplicateStudentNumberException y no guarda.
- findsStudentById(): Retorna StudentResponse cuando el id existe en el repositorio.
- reportsMissingStudentById(): Lanza StudentNotFoundException cuando el id no existe.
- returnsPagedStudentsUsingRequestedPageAndSize(): Valida ordenamiento 'id' y captura de Pageable.
- updatesStudentDetails(): Modifica atributos del estudiante si no hay colisión de matrícula.
- rejectsStudentNumberUsedByAnotherStudentOnUpdate(): Impide asignar matrícula ocupada por otro.
- updatesStudentActiveStatus(): Comprueba el soft-status (activación/desactivación).

Comando para ejecutar las pruebas en tu consola:
  mvn test -Dtest=StudentServiceTest


---

## Laboratorio 5: Análisis de Requerimiento (Búsqueda Parcial por Apellido Paterno)

**Video asociado:** `5 Caso de prueba y validaciones.mp4`

### Prompt:
```text
Analiza el requerimiento de buscar estudiantes por coincidencia parcial de apellido paterno.
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

No escribas ni modifiques código.
```

### Resolución:

1. HISTORIA DE USUARIO:
Como administrador escolar, quiero filtrar estudiantes por coincidencia parcial de su apellido
paterno para localizarlos rápidamente sin conocer su matrícula o apellido exacto.

2. REGLAS FUNCIONALES:
- Parámetro opcional: `paternalSurname`.
- Coincidencia parcial tipo 'contains' (%valor%).
- Insensible a mayúsculas y minúsculas (case-insensitive).
- Se combina con operador lógico AND junto a `active` y `studentNumber`.
- Espacios iniciales/finales se eliminan con strip(); cadenas vacías se ignoran.

3. RESTRICCIONES TÉCNICAS:
- No modificar el esquema relacional de PostgreSQL.
- Mantener el contrato `PageResponse<StudentResponse>`.
- Longitud máxima permitida: 100 caracteres.
- Escapar caracteres especiales SQL (% y _).

4. CRITERIOS DE ACEPTACIÓN (GIVEN / WHEN / THEN):
- Escenario 1: Coincidencia parcial y minúsculas (GET ?paternalSurname=her -> encuentra 'Hernández').
- Escenario 2: Coexistencia con active=true (GET ?paternalSurname=garcia&active=true).
- Escenario 3: Filtro en blanco (GET ?paternalSurname=   -> lista todos sin filtrar).
- Escenario 4: Longitud excesiva > 100 caracteres -> Retorna HTTP 400 Bad Request.

5. ARCHIVOS AFECTADOS:
- StudentController.java (nuevo parámetro query).
- StudentService.java (nueva cláusula en CriteriaBuilder Specification).
- StudentServiceTest.java y StudentApiIntegrationTest.java (pruebas).


---

## Laboratorio 6: Plan de Ampliación de Endpoint (/plan GET /api/v1/students)

**Video asociado:** `6 Agent plan.mp4`

### Prompt:
```text
/plan Diseña una ampliación de GET /api/v1/students.

Nuevo parámetro opcional: paternalSurname

Reglas:
- Coincidencia parcial.
- Ignorar diferencias entre mayúsculas y minúsculas.
- Conservar page, size, active y studentNumber.
- No cambiar el formato PageResponse.
- No crear nuevos endpoints innecesarios.
- No modificar el esquema de PostgreSQL.

Entrega el contrato HTTP, ejemplos, archivos afectados, criterios de aceptación y posibles riesgos de compatibilidad.

No implementes nada.
```

### Resolución:

CONTRATO HTTP (OpenAPI 3 / GET /api/v1/students):
Query Parameters:
  - page (int, default=0, min=0)
  - size (int, default=20, min=1, max=100)
  - active (boolean, opcional)
  - studentNumber (string, opcional, exacto)
  - paternalSurname (string, opcional, max=100, parcial case-insensitive)

Respuestas:
  - 200 OK: PageResponse<StudentResponse>
  - 400 Bad Request: ProblemDetail (parámetros fuera de rango o tamaño > 100)

EJEMPLO DE PETICIÓN Y RESPUESTA:
curl -X GET "http://localhost:8080/api/v1/students?paternalSurname=lop&active=true&page=0&size=10"

Respuesta 200 OK:
{
  "content": [
    {
      "id": 14,
      "studentNumber": "2024-0014",
      "firstName": "Carlos",
      "paternalSurname": "López",
      "maternalSurname": "Hernández",
      "email": "carlos.lopez@utvt.edu.mx",
      "dateOfBirth": "2002-05-18",
      "active": true
    }
  ],
  "page": 0,
  "size": 10,
  "totalElements": 1,
  "totalPages": 1
}


---

## Laboratorio 7: Plan de Validaciones y Excepciones (RFC 7807)

**Video asociado:** `6 Agent plan.mp4`

### Prompt:
```text
/plan Analiza las validaciones y excepciones de school-management.

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
No modifiques archivos.
```

### Resolución:

TAXONOMÍA DE CÓDIGOS DE ERROR HTTP EN EL SISTEMA:
- HTTP 400 Bad Request: Violación sintáctica (size > 100, page < 0, paternalSurname > 100 caracteres).
- HTTP 404 Not Found: Recurso no encontrado (StudentNotFoundException por ID inexistente).
- HTTP 409 Conflict: Conflicto de unicidad (DuplicateStudentNumberException) o versión concurrente.

MATRIZ DE REGLAS DE VALIDACIÓN PARA paternalSurname:
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

ESTRUCTURA DEL ERROR 400 CON ProblemDetail (RFC 7807):
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Validation failed for method parameter",
  "instance": "/api/v1/students",
  "properties": {
    "invalidParams": [
      { "name": "paternalSurname", "reason": "el tamaño debe estar entre 0 y 100" }
    ]
  }
}


---
