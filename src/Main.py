# Importación de librerías requeridas
import argparse, LIB_TC2008B

def main():
	parser = argparse.ArgumentParser("Entrega - Final: Miguel Pérez", description = "Entrega Agentes Multiagentes 2024")
	subparsers = parser.add_subparsers()

	subparser = subparsers.add_parser("Simulacion",  description = "Corre simulacion")
	subparser.add_argument("--N_Ejecucion", required = True, type = int, default = 0, help = "Control de Número de ejecución")
	subparser.add_argument("--lifters", required = True, type = int, help = "Numero de montacargas")
	subparser.add_argument("--Basuras", required = True, type = int, help = "Numero de basuras para trailer")
	subparser.add_argument("--TrailerPos", required = True, nargs=2, type = float, help = "Ubicación x,y del trailer")
	subparser.add_argument("--DescargaPos", required = True, nargs=2, type = float, help = "Ubicación x,y de la zona de descarga y origen")
	subparser.add_argument("--Vel_lifter", required = True, type = float, help = "Velocidad de los agentes durante las simulación (0-1.2)")
	subparser.add_argument("--dist_min", required = True, type = float, help = "Distancia mínima a guardar entre agentes")

	subparser.add_argument("--Out_arch_path", required = False, type = str, default= "out.csv", help = "Archivo csv de salida")
	subparser.add_argument("--Config_Out_arch_path", required = False, type = str, default= "config_out.txt", help = "Archivo csv de configuración de execución")
	
	subparser.add_argument("--Delta", required = False, type = float, default = 0.05, help = "Velocidad de simulacion")
	subparser.add_argument("--theta", required = False, type = float, default = 0, help = "")
	subparser.add_argument("--radious", required = False, type = float, default = 30, help = "")
	
	subparser.set_defaults(func = LIB_TC2008B.Simulacion)

	Options = parser.parse_args()
	print("Nombre: Miguel Ángel Pérez Ávila")
	print("Matricula: A01369908")
	print("Multiagentes")
	print("Roberto Leyva Fernandez")
	Options.func(Options)

if __name__ == "__main__":
	main()
