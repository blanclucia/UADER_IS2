# Diagrama de casos de uso

Este diagrama representa las funcionalidades del sistema desde la perspectiva de los usuarios. Se observa que el estudiante puede buscar libros, solicitar préstamos y devolverlos, mientras que el bibliotecario administra los préstamos, las devoluciones y las multas. La importancia del caso de uso radica en mostrar qué hace el sistema y quiénes participan en cada actividad, sin entrar aún en detalles de implementación.

```mermaid
flowchart LR
    A((Estudiante)) --> U1[Buscar libro]
    A --> U2[Solicitar préstamo]
    A --> U3[Renovar préstamo]
    A --> U4[Devolver libro]

    B((Bibliotecario)) --> U5[Registrar préstamo]
    B --> U6[Registrar devolución]
    B --> U7[Generar multa]

    S((Sistema)) --> U1
    S --> U2
    S --> U3
    S --> U4
    S --> U5
    S --> U6
    S --> U7
```
