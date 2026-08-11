# Diagrama de secuencia

Este diagrama muestra la secuencia de mensajes entre los distintos componentes del sistema en el momento de realizar un préstamo. Se puede ver cómo se comunica la interfaz con el sistema, cómo se consulta la disponibilidad del libro y cómo se registra la operación en la base de datos. Es especialmente útil para comprender el orden temporal de las acciones y la dependencia entre los módulos del sistema.

```mermaid
sequenceDiagram
    actor U as Estudiante
    participant UI as Interfaz
    participant S as Sistema
    participant L as Servicio de libros
    participant P as Servicio de préstamos
    participant DB as Base de datos

    U->>UI: Solicita préstamo del libro X
    UI->>S: POST /prestamos
    S->>L: buscarLibro(X)
    L->>DB: consultar ejemplar disponible
    DB-->>L: ejemplar encontrado

    alt Hay ejemplar disponible
        L-->>S: libro disponible
        S->>P: crearPrestamo(usuario, ejemplar)
        P->>DB: guardar préstamo
        DB-->>P: confirmación
        P-->>S: préstamo registrado
        S-->>UI: mensaje de éxito
        UI-->>U: muestra confirmación
    else No hay disponibilidad
        L-->>S: libro no disponible
        S-->>UI: mensaje de error
        UI-->>U: informa que no puede prestarlo
    end
```
