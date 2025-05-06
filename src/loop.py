import subprocess, random, os

ruta_directorio = r"C:\Users\mapae\Documents\Tec\Profe\5 S\3 P\multiagentes\leyva\Evidencia-individual\Entrega-MAPA"

matrix = []
'''
def ejecucionSecuencial(n_ejecucion, modoExec):
    comandstr = "python,Main.py,Simulacion,--M_board,4,--N_board,4,--lifters,2,--Basuras,10,--Busqueda_Secuencial,true,--Delta,1,--Out_arch_path,out.csv,--N_Ejecucion,0,--Sec_mode,espiral,--Config_Out_arch_path,config_out.txt"
    comandarr = comandstr.split(",")
    
    mOptions = [4,6,8,10]
    comandarr[4] = str(mOptions[random.randint(0,len(mOptions)-1)]) #mboard
    
    nOptions = [4,6,8,10]
    comandarr[6] = str(nOptions[random.randint(0,len(nOptions)-1)]) #nboard
    
    comandarr[8] = str(random.randint(1,((int(comandarr[4])*int(comandarr[6]))*60)//100)) # n_lifters
    
    comandarr[10] = str(random.randint(1,((int(comandarr[4])*int(comandarr[6]))*120)//100)) # n_basuras
    
    comandarr[12] = "true" # busquedaSec
    
    comandarr[18] = str(n_ejecucion )
    
    comandarr[20] = str(modoExec)
    
    return comandarr
'''


def ejecucionRandom(n_exec, n_lifters, n_basuras, X_trailerpos, Y_trailerpos, X_descargapos, Y_descargapos, dx_min):
    comandstr = "python,Main.py,Simulacion,--N_Ejecucion,0,--lifters,1,--Basuras,10,--TrailerPos,70,70,--DescargaPos,-70,-70,--Vel_lifter,1,--dist_min,50"
    comandarr = comandstr.split(",")
    
    
    comandarr[4] = str(n_exec)
    comandarr[6] = str(n_lifters)
    comandarr[8] = str(n_basuras)
    comandarr[10] = str(X_trailerpos)
    comandarr[11] = str(Y_trailerpos)
    comandarr[13] = str(X_descargapos)
    comandarr[14] = str(Y_descargapos)
    comandarr[18] = str(dx_min)
    
    
    return comandarr
    
    
def main():
    count = 0
    for i in range(50, 500+1, 10):
        matrix.append(ejecucionRandom(count, 2, 2, 300, 300, -300, -300, i))
        
        count+=1

    for comand in matrix:
        resultado = subprocess.run(comand, cwd=ruta_directorio)
        #print(comand)
        

main()