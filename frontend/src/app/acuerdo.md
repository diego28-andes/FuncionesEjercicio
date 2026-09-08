# Acuerdos de flujo de trabajo semana 05

En esta semana el desarrollo se **centraliza solo en `main`**. No se usa GitFlow todavía: no hay rama `desarrollo` ni ramas por historia o por persona.

## Repositorios

| Nombre | Ubicación (url/directorio) | Propósito |
| :--- | :--- | :--- |
| MISW4101-202614-Grupo015 | [https://github.com/MISW-4101-Practicas/MISW4101-202614-Grupo015](https://github.com/MISW-4101-Practicas/MISW4101-202614-Grupo015) | Único repositorio del proyecto. Aquí se versiona y se comparte el código. |
| Repositorio local | Clon local del mismo repositorio | Trabajo diario de cada integrante antes de hacer `push` a `main`. |

## Historias de la semana

| Historia | Propósito |
| :--- | :--- |
| Listar recetas | Listar las recetas almacenadas en la base de datos. |
| Crear receta | Crear recetas y persistirlas en la base de datos. |
| Listar ingredientes | Listar los ingredientes almacenados en la base de datos. |

## Ramas

| Nombre rama | Propósito |
| :--- | :--- |
| `main` | Única rama de trabajo. Contiene la versión funcional más reciente y recibe todos los commits de la semana. |

## Acuerdos

| Acción | Quién | Cuándo | Dónde |
| :--- | :--- | :--- | :--- |
| Descargar el estado actual (`git pull`) | Diego Perez | Antes de empezar el ciclo TDD | Rama `main` |
| Descargar el estado actual (`git pull`) | William Ariza | Antes de empezar el ciclo TDD | Rama `main` |
| Escribir la prueba unitaria (rojo) | Diego Perez | Al iniciar cada historia | Rama `main` |
| Hacer pasar la prueba (verde) | William Ariza | Cuando la prueba ya esté en `main` | Rama `main` |
| Refactorizar sin romper las pruebas | William Ariza / Diego Perez | Cuando la prueba ya esté en verde | Rama `main` |
| Subir los cambios (`git push`) | Quien cierre el ciclo rojo-verde-refactor | Al terminar cada historia | Rama `main` en GitHub |
