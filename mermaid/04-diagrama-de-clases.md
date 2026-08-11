# Diagrama de clases

Este diagrama presenta la estructura estática del sistema mediante clases y relaciones. Se identifica la jerarquía entre Usuario, Estudiante y Bibliotecario, así como la relación entre Libro, Ejemplar y Prestamo. También se incorpora la clase Multa para representar la penalización por retraso. Este tipo de diagrama permite entender cómo están organizadas las entidades del sistema y cómo interactúan entre sí.

```mermaid
classDiagram
    class Usuario {
        +idUsuario: int
        +nombre: string
        +email: string
        +login()
    }

    class Estudiante {
        +carrera: string
        +solicitarPrestamo()
        +renovarPrestamo()
    }

    class Bibliotecario {
        +registrarDevolucion()
        +generarMulta()
    }

    class Libro {
        +isbn: string
        +titulo: string
        +autor: string
        +disponible: bool
    }

    class Ejemplar {
        +idEjemplar: int
        +estado: string
    }

    class Prestamo {
        +idPrestamo: int
        +fechaPrestamo: date
        +fechaVencimiento: date
        +estado: string
    }

    class Multa {
        +idMulta: int
        +monto: float
        +calcularMonto()
    }

    Usuario <|-- Estudiante
    Usuario <|-- Bibliotecario
    Libro "1" --> "1..*" Ejemplar
    Estudiante "1" --> "0..*" Prestamo
    Bibliotecario "1" --> "0..*" Prestamo
    Ejemplar "1" --> "0..1" Prestamo
    Prestamo "1" --> "0..1" Multa
```
