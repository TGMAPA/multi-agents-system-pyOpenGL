# Importación de librerías requeridas
import yaml, pygame, glob, math, datetime, numpy
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Importación de librerías locales requeridas
from Lifter import Lifter
import DrawBoard as DB
from Trailer import *
from CCamera import *
import Tools
from NodeSet import *


def loadSettingsYAML(File):
    class Settings: pass
    with open(File) as f:
        docs = yaml.load_all(f, Loader = yaml.FullLoader)
        for doc in docs:
            for k, v in doc.items():
                setattr(Settings, k, v)
    return Settings
Settings = loadSettingsYAML("Settings.yaml")

textures = [] # Arreglo de texturas
delta = 0     

lifters = []   # Arreglo total de agentes
startedLifters = []  # Arrgelo de agantes inicializados
trailer = None  # Objeto tipo Trailer
nodeset = None  # Objeto tipo NodeSet

origenPos = None  # Posición del Nodo origen
trailerPos = None   # Posición del Trailer 

dimSize = None  # Dimensión del plano

lastlifterFinish = False  # Bandera para indicar que el último agente en recoger una basura termino su trabajo en la Zona de Descarga
trailerCleaned = False  # Bandera que indica si el Trailer ha sido descargado por completo

n_lifters  = 0   # numero de agentes
camera     = None  # Objeto tipo Camera
screen     = None  # variable tipo pygame.display

def Texturas(filepath):
    # Arreglo para el manejo de texturas
    global textures
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)

# Definición de parámetros iniciales, generación de nodos, creación de agentes y creación de carga/trailer
def Init(Options):
    global screen, camera, textures, dimSize
    global lifters, n_lifters, trailer, nodeset, origenPos, trailerPos

    # Condiguración y parámetros para la pantalla y proyección
    screen = pygame.display.set_mode( (Settings.screen_width, Settings.screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL - Miguel Pérez")
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(Settings.FOVY, Settings.screen_width/Settings.screen_height, Settings.ZNEAR, Settings.ZFAR)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        Settings.EYE_X,
        Settings.EYE_Y,
        Settings.EYE_Z,
        Settings.CENTER_X,
        Settings.CENTER_Y,
        Settings.CENTER_Z,
        Settings.UP_X,
        Settings.UP_Y,
        Settings.UP_Z
    )
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    for File in glob.glob(Settings.Materials + "*.*"):
        Texturas(File) 
    # ==============================================================================================================

    # Inicializar Camara con posición determinada 
    camera = Camera([-323.334, 150, 307.532], [-160.0, -200.0])
    
    #Determinar posiciones deseadas para la zona de descarga y zona de trailer
    origenPos  = Options.DescargaPos
    trailerPos = Options.TrailerPos
    origenPos, trailerPos = Tools.get_descarga_trailer_positions(origenPos, trailerPos)
    
    # Ajustar tablero a valor maximo de coordenadas determinado o mantener predeterminado
    if((max(trailerPos) > Settings.DimBoard/2) or (max(origenPos) > Settings.DimBoard/2)):
        if(max(trailerPos) > max(origenPos)):
            dimSize = max(trailerPos) *2 
        else:
            dimSize = max(origenPos) *2
    else:
        dimSize = Settings.DimBoard
    
    # Instancia de set de nodos
    distMin = float(Options.dist_min)
    nodeset = NodeSet(origenPos, trailerPos, distMin, Tools.ComputeDistance(origenPos, trailerPos))
    
    # Arreglo de nodos a recorrer
    Node2Visit = nodeset.nodes
    
    # Instancia de Trailer
    Trailer.Board_Size = dimSize
    Trailer.trash_textures = textures
    trailer = Trailer(nodeset.nodes[3], int(Options.Basuras), distMin)
    
    #Número de agentes
    n_lifters = int(Options.lifters)
    
    # Velocidad de agentes
    agent_vel = float(Options.Vel_lifter)

    # Inicializar y escribir header para csv de salida
    header = "n_ejecucion,n_agents_deseado,n_agents_created,agent_vel,X_descargaPos,Z_descargaPos,X_trailerPos,Z_trailerPos,distancia_descarga_trailer,n_basura,t_total_descarga,distancia_minima_agentes\n"
    Tools.initializeCSVout(header, str(Options.Out_arch_path))
    
    # Posiciones iniciales de los montacargas
    Positions = []
    auxnode= Node2Visit[0].position
    InitalPos=[auxnode[0], auxnode[1], auxnode[2]]
    for i in range(n_lifters):
        Positions.append(InitalPos)
    Positions = numpy.array(Positions, dtype=numpy.float64)
    
    # Inicializar los agentes con posicion inicial
    for id,position0 in enumerate(Positions):
        lifter = Lifter(dimSize, agent_vel, textures, id, position0, Node2Visit[0], Options.Out_arch_path, Options.N_Ejecucion, distMin=distMin)
        lifters.append(lifter)

# Buscar colisiones entre agentes activos únicamente y basura
def checkTrashCollisions():
    global trailer, startedLifters
    # Iterar únicamente sobre el arreglo con los agentes activos al momento
    for c in startedLifters:
        for b in trailer.basuras:
            # Distancia entre agentes evaluados
            distance = math.sqrt(math.pow((b.Position[0] - c.Position[0]), 2) + math.pow((b.Position[2] - c.Position[2]), 2))
            if distance <= c.radiusCol: 
                if c.status == "searching" and b.alive:
                    # Colision registrada entre un agente y una basura
                    b.alive = False
                    c.status = "lifting"
                    trailer.nbasuras -= 1
                    if(trailer.nbasuras == 0):
                        # Si el agente actual recogió la última basura, establecer este agente como el finisher
                        c.finisher = True

def calcDistanceAgentNode(agent, node):
    return math.sqrt( math.pow((node.position[0] - agent.Position[0]), 2) + math.pow((node.position[2] - agent.Position[2]), 2) )

def calcDistanceAgents(agent1, agent2):
    return math.sqrt( math.pow((agent2.Position[0] - agent1.Position[0]), 2) + math.pow((agent2.Position[2] - agent1.Position[2]), 2) )

def checkLifterCollisions():
    global startedLifters, trailer
    # Iterar únicamente sobre el arreglo con los agentes activos al momento
    for c1 in startedLifters:
        if(calcDistanceAgentNode(c1, trailer.Node) <= trailer.dx):
            # Agente llego a zona de espera
            if(not trailer.isOcupied):
                if(len(c1.collisionwith)>0):
                    if(c1.collisionwith[0][0] != None):
                        c1.collisionwith[0][0].resume()
                        
                if(numpy.allclose(numpy.asarray(c1.Position, dtype=numpy.int64), numpy.asarray(trailer.Node.position, dtype=numpy.int64))):  #,  rtol=0.07)
                
                    # Trailer desocupado, continuar...
                    print("en trailer, desocupado")
                    trailer.changeisOcupied(True)
                    trailer.changeOcupiedBy(c1)
                    c1.resume()
                    continue
                else:
                    c1.status = "searching"
            else:
                if(trailer.ocupiedwith != c1):
                    # Trailer ocupado, esperar...
                    c1.status = "waiting"
                    c1.waiting()
                    continue
        
        if(c1.status == "lifting" or calcDistanceAgentNode(c1, trailer.Node) <= trailer.dx):
            trailer.changeisOcupied(True)
            trailer.changeOcupiedBy(c1)
            c1.resume()
            continue
        
        if(c1.status == "delivering" and numpy.isclose(calcDistanceAgentNode(c1, trailer.Node), trailer.dx, rtol=0.05)): # 0.15  0.05
            #print("1 Desocupando...")
            c1.resume()
            trailer.ocupiedwith = None
            trailer.isOcupied = False
        
        if(c1.status == "searching" and trailer.ocupiedwith == c1 and numpy.isclose(calcDistanceAgentNode(c1, trailer.Node), trailer.dx, rtol=0.1)):
            #print("2 Desocupando...")
            c1.resume()
            trailer.ocupiedwith = None
            trailer.isOcupied = False
            
        if(len(c1.collisionwith)>0):
            if(calcDistanceAgents(c1, c1.collisionwith[0][0]) > c1.radius2lifter):
                c1.resume()
                continue
        
        for c2 in startedLifters:
            if(c1 != c2):
                distance = calcDistanceAgents(c1, c2)
                if(c1.alive):
                    if distance <= c1.radius2lifter: 
                        bol = False
                        if(c2.status == "waiting"):
                            c1.bol = True
                        # Colisión registrada entre un agente activo y otro
                        c1.stop([c2, bol]) # Parar al agente actual  


# Revisar lifters no iniciados e iniciarlos
def checkNonStartedLifterCollisions():
    global lifters, startedLifters
    
    # Iterar sobre el arreglo total de agentes
    for grallifter in lifters:
        # Variable acumuladora para hacer check por todos los agentes activos
        count = 0
        #Iterar para comparar entre el agente actual y todos los agentes activos al momento
        for startedlifter in startedLifters:
            if(grallifter != startedlifter and not grallifter.started):
                distance = math.sqrt(math.pow((grallifter.Position[0] - startedlifter.Position[0]), 2) + math.pow((grallifter.Position[2] - startedlifter.Position[2]), 2))
                if( distance > grallifter.radius2lifter+5): #================================================================AGREGAR EN CASO DE ERROR
                    # Si la distancia entre los agentes es suficientemente lejana, se actualiza el contador
                    count +=1
        # Arrancar el lifter en caso de haber tenido una distancia suficientemente lejana con respecto a todos los agentes activos al momento
        if(count == len(startedLifters)):
            grallifter.started = True
            grallifter.alive = True
            startedLifters.append(grallifter) # Agregar agente al arreglo de agentes activos e inicializados

# Inicializar agentes 
def startlifters():
    global lifters, startedLifters
    
    if(len(startedLifters) == 0 and len(lifters) != 0):
        # Inicializar primer agente
        lifters[0].started = True
        lifters[0].alive = True
        startedLifters.append(lifters[0])
    else:
        # Verificar e Inicializar resto de agentes
        checkNonStartedLifterCollisions()    

# Actualización de pantalla y objetos
def display():
    global startedLifters, lifters, delta, camera, screen, trailer, nodeset, dimSize, trailerCleaned, lastlifterFinish
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera_init(camera, screen) # Actualización de cámara
    
    #dibujar tablero y nodos
    DB.drawPlane(dimSize, nodeset.nodes)
    
    # Revisar si faltan agentes por inicializar
    if(len(startedLifters)< len(lifters)):
        startlifters()
    
    #Se dibujan los agentes
    for i in range(len(startedLifters)):
        startedLifters[i].draw()
        startedLifters[i].update(delta)
        if(startedLifters[i].status == "finish"):
            # En caso de encontrar un agente finisher se activa la bandera correspondiente
            lastlifterFinish = True
    
    # Se dibuja la carga de basura en el trailer
    for trash in trailer.basuras:
        trash.draw()
    
    # Actualización de cantidad de basura en el trailer
    trailerCleaned = trailer.update()
    
    # Verificación de colisiones tipo basura-agente y agente-agente
    checkLifterCollisions()
    checkTrashCollisions()

# Ejecución de la Simulación principal
def Simulacion(Options):
    # Variables para el control del observador
    global delta, lifters, trailer, trailerCleaned, lastlifterFinish, trailerPos, origenPos, startedLifters
    delta = Options.Delta
    
    print("\n" + str(Options) + "\n")
    Tools.verifyConfigArch(Options.Config_Out_arch_path)
    Tools.writeConfigArch(Options.Config_Out_arch_path, "== Exec: " + str(Options.N_Ejecucion) + "\n" + str(Options) + "\n\n")
    
    Init(Options)
    
    trailer.starttime() # Iniciar tiempo de descarga del trailer
    done = False
    
    start = datetime.datetime.now()
    print("\n" + "\033[0;32m" + "[start] " + str(start) + "\033[0m" + "\n")
    
    while not done:
        keys = pygame.key.get_pressed()  # Checking pressed keys
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    done = True
        if(trailerCleaned and lastlifterFinish):
            done = True
        display()
        display()
        pygame.display.flip()
        pygame.time.wait(10)
        
    end = datetime.datetime.now()
    print( "dt : ", end-start)
    print("\n" + "\033[0;32m" + "[end] " + str(end) + "\033[0m" + "\n")
    
    pygame.quit() 
    
    # Distancia entre zona de origen/descarga y trailer
    distance_descarga_trailer = Tools.ComputeDistance(origenPos, trailerPos)
    
    # Tiempo Total
    dt = end-start
    
    # Escritura de salida a csv
    outfile = open(Options.Out_arch_path, "a")
    out = f"{Options.N_Ejecucion},{Options.lifters},{len(startedLifters)},{Options.Vel_lifter},{origenPos[0]},{origenPos[2]},{trailerPos[0]},{trailerPos[2]},{distance_descarga_trailer},{Options.Basuras},{dt.total_seconds()},{Options.dist_min}\n"
    outfile.write(out)
    outfile.close()
