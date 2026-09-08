# Acuerdos de flujo de trabajo semana 06

En esta semana se **inicia GitFlow**. El trabajo ya no se hace sobre `main`: cada historia sale de `desarrollo`, se resuelve en su propia rama y solo vuelve a `main` cuando `desarrollo` esté estable.

## Repositorios

| Nombre | Ubicación (url/directorio) | Propósito |
| :--- | :--- | :--- |
| MISW4101-202614-Grupo015 | [https://github.com/MISW-4101-Practicas/MISW4101-202614-Grupo015](https://github.com/MISW-4101-Practicas/MISW4101-202614-Grupo015) | Repositorio remoto del grupo. Integra `main`, `desarrollo` y las ramas de historia. |
| Repositorio local | Clon local de `MISW4101-202614-Grupo015` | Trabajo diario sobre la rama de la historia asignada. |

## Historias de la semana

| Historia | Rama | Responsable principal |
| :--- | :--- | :--- |
| Eliminar ingrediente | `eliminar-ingrediente` | Diego Perez |
| Reporte (primera parte) | `reporte` | William Ariza |

## Ramas

| Nombre rama | Sale de | Propósito |
| :--- | :--- | :--- |
| `main` | — | Versión funcional publicada. Solo recibe merges desde `desarrollo` cuando esa rama esté estable. |
| `desarrollo` | `main` | Integración de las historias de la semana. Es la rama base de todo el trabajo nuevo. |
| `eliminar-ingrediente` | `desarrollo` | TDD y solución de eliminar ingrediente. |
| `reporte` | `desarrollo` | TDD y solución de la primera parte del reporte. |

## Acuerdos

| Acción | Quién | Cuándo | Dónde |
| :--- | :--- | :--- | :--- |
| Crear `desarrollo` (si aún no existe) y alinearla con `main` | Diego Perez / William Ariza | Al empezar la semana | Rama `desarrollo` |
| Descargar el estado actual (`git pull`) | Diego Perez | Antes de crear o actualizar su rama | Rama `desarrollo` |
| Descargar el estado actual (`git pull`) | William Ariza | Antes de crear o actualizar su rama | Rama `desarrollo` |
| Crear la rama de historia desde `desarrollo` | Diego Perez | Al iniciar eliminar ingrediente | Rama `eliminar-ingrediente` |
| Escribir la prueba (rojo), hacerla pasar (verde) y refactorizar | Diego Perez | Durante el ciclo TDD de la historia | Rama `eliminar-ingrediente` |
| Subir la rama a GitHub | Diego Perez | Al cerrar rojo-verde-refactor | Rama `eliminar-ingrediente` |
| Merge de la historia hacia integración | Diego Perez | Cuando las pruebas pasen y el código esté refactorizado | `eliminar-ingrediente` → `desarrollo` |
| Crear la rama de historia desde `desarrollo` | William Ariza | Al iniciar el reporte | Rama `reporte` |
| Escribir la prueba (rojo), hacerla pasar (verde) y refactorizar | William Ariza | Durante el ciclo TDD de la historia | Rama `reporte` |
| Subir la rama a GitHub | William Ariza | Al cerrar rojo-verde-refactor | Rama `reporte` |
| Merge de la historia hacia integración | William Ariza | Cuando las pruebas pasen y el código esté refactorizado | `reporte` → `desarrollo` |
| Merge de integración hacia la versión publicada | William Ariza | Cuando `desarrollo` esté estable (ambas historias integradas y pruebas en verde) | `desarrollo` → `main` |
