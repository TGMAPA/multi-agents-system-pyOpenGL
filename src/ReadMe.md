# Reto

Implementación Entrega Final
Miguel Ángel Pérez Ávila A01369908

Parametros de ejecución necesarios:
--N_Ejecucion : Numero de identificación para la ejecución
--lifters : Cantidad de montacargas deseada
--Basuras : Cantidad de basura deseada
--TrailerPos : Coordenadas (x,y) para el trailer
--DescargaPos : Coordenadas (x,y) para la Zona de descarga
--Vel_lifter : Velocidad de los agentes durante las simulación (0-1.2)
--dist_min : Distancia mínima a mantener entre los agentes

Parámetros Opcionales: 
--Out_arch_path : Ruta para el archivo csv de salida con reportes de la ejecución realizada.
--Config_Out_arch_path : Ruta para el archivo txt de salida de configuración de ejecución.
--Delta : Velocidad de simulacion.
--theta
--radious


## Instruccciones

Para ejecutar el codigo asi:

```bash

python Main.py Simulacion --N_Ejecucion 0 --lifters 20 --Basuras 5 --TrailerPos 400 400 --DescargaPos -150 -150 --Vel_lifter 1.3 --dist_min 100

```