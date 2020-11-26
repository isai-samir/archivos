import random as r
import math


##variable global para manejar archivos y directorios
ficheros = []
#g_directorios = []

def vaciar():
    for element in ficheros:
        element.directorios.clear()
        element.archivos.clear()
    ficheros.clear()

class Usuario:

    def __init__(self,user,password):
        self.user = user 
        self.password = password


class Fichero: #representa un archivo
    grupo = []
    permisos = []   
    def __init__(self,name,size,owner,permisos,contenedor):
        self.name = name
        self.size = size
        self.owner = owner
        self.contenedor = contenedor
        if(len(permisos)>3): print ("error")

        else:
            try:
                temp = int(permisos)
                # print(temp)
            except ValueError as ve:
                print("No se pudo obtener los permisos")
            else:
                self.permisos.append(math.floor(temp/100))
                #print(self.permisos[0])
                temp = temp%100
                self.permisos.append(math.floor(temp/10))
                #print(self.permisos[1])
                self.permisos.append(temp%10)
                #print(self.permisos[2])
        self.grupo.append("No one")
    #001 = 1
    #010 = 2
    #011 = 3
    #100 = 4
    #101 = 5
    #110 = 6
    #111 = 7
    def leer(self,request): #recibe un usuario para verificar si tiene permisos
        if(request.user == self.owner):
            if(self.permisos[0]>=4):
                print(f"{self.owner} esta leyendo {self.name}")
            else:
                print("Ud no tiene permiso de leer este archivo")
        elif(request.user in self.grupo):
            if(self.permisos[0]==2 or self.permisos[0]==3 or self.permisos[0]>=6):
                print(f"{request.user} esta leyendo {self.name}")
            else:
                print("Ud no tiene permiso de leer este archivo")
        else:
            if(self.permisos[0]==1 or self.permisos[0]==3 or self.permisos[0]==5 or self.permisos[0]==7):
                print(f"{request.user} esta leyendo {self.name}")
            else:
                print("Ud no tiene permiso de leer este archivo")

    def execute(self,request):
        if(request.user == self.owner):
            if(self.permisos[2]>=4):
                print(f"{self.owner} esta ejecutando {self.name}")
            else:
                print(f"Permiso: {self.permisos[2]}")
                print(f"{self.owner} no tiene permiso de ejecutar este archivo")
        elif(request.user in self.grupo):
            if(self.permisos[2]==2 or self.permisos[2]==3 or self.permisos[2]>=6):
                print(f"{request.user} esta ejecutando {self.name}")
            else:
                print("Ud no tiene permiso de ejecutar este archivo porque no pertenece al grupo")
        else:
            if(self.permisos[2]==1 or self.permisos[2]==3 or self.permisos[2]==5 or self.permisos[2]==7):
                print(f"{request.user} esta ejecutando {self.name}")
            else:
                print("Ud no tiene permiso de ejecutar este archivo")
    def escribir(self,request):
        if(request.user == self.owner):
            if(self.permisos[1]>=4):
                print(f"{self.owner} esta escribiendo en {self.name}")
            else:
                print("Ud no tiene permiso de escribir en este archivo")
        elif(request.user in self.grupo):
            if(self.permisos[1]==2 or self.permisos[1]==3 or self.permisos[1]>=6):
                print(f"{request.user} esta escribiendo en {self.name}")
            else:
                print("Ud no tiene permiso de escribir en este archivo")
        else:
            if(self.permisos[1]==1 or self.permisos[1]==3 or self.permisos[1]==5 or self.permisos[1]==7):
                print(f"{request.user} esta escribindo en {self.name}")
            else:
                print("Ud no tiene permiso de escribir en este archivo")
    
    def changePermiso(self,request):
        if(request.user == self.owner):
            self.permisos[0] = int(input('Valor decimal de 0-7 para owner: '))
            self.permisos[1] = int(input('Valor decimal de 0-7 para grupo: '))
            self.permisos[2] = int(input('Valor decimal de 0-7 para otros: '))
        else:
            print("Error. Solo el dueño puede cambiar los permisos")

class Directorio: #representa un directorio
    archivos = [] #lista de archivos 
    directorios = [] #lista de mas directorios
    
    def __init__(self,name,carpetaPadre='nombreDeCarpeta'):
        self.name = name
        self.padre = carpetaPadre

    def archivosIsEmpty(self):
        if len(self.archivos)==0: return True
        return False
    def directoriosIsEmpty(self):
        if len(self.directorios)==0: return True
        return False


#lee usuarios guardados
def leeUsuarios():
    users = []
    users_f = open("users.txt")
    for linea in users_f:
        elementos = linea.split( )
        userName = elementos[0]
        userPass = elementos[1]
        users.append(Usuario(userName,userPass))
    users_f.close()
    return users

def crearUsuario():
    f_users = open("users.txt",'a')
    n_user = input('Nombre de nuevo usuario: ')
    p_user = input('Contraseña de nuevo usuario: ')
    f_users.write(n_user+" "+p_user+'\n')
    f_users.close()

def iniciarSesion(user,pas):
    users = leeUsuarios()
    for usuario in users:
        if(user == usuario.user):
            if(pas == usuario.password):
                return usuario
            else:
                print('Contraseña incorrecta')
                return None
    print('Usuario no encontrado')
    return None

def getDirectorioPadre(actual,list):
    for element in list:
        print(element.name)
        if element.name == actual:
            return element
    return None 

def verContenidoDe(directorio,bandera=0): 

    print(directorio.name)
    print("|")
    if bandera != 1: #cuando es 1 es solo para mostrar los archivos
        for carpeta in directorio.directorios:
            if directorio.name == carpeta.padre:
                print(carpeta.name)
                if not carpeta.directoriosIsEmpty :
                    verContenidoDe(carpeta)
    if bandera != 2: #cuando es 2 solo se usa mostrar directorios 
        for archivo in directorio.archivos:
            if directorio.name == archivo.contenedor:
                print(f"|-{archivo.name} {archivo.permisos}")

def insertaDirectorio(carpeta,carpetaPadre,lista=[]):

    if len(ficheros) == 0:
        print(f"{carpeta} creada")
        ficheros.append(Directorio(carpeta,carpetaPadre))
        #caso inicial donde se crea la carpeta raiz 
    else:
        # ficheros[0].directorios.append(Directorio(carpeta,carpetaPadre))
        print(len(lista))
        for element in lista:
            if(element.name == carpetaPadre):
                print(f"{carpeta} creada en {element.name}")
                element.directorios.append(Directorio(carpeta,carpetaPadre))
                break
            elif not element.directoriosIsEmpty():
                insertaDirectorio(carpeta,carpetaPadre,element.directorios)
                break

def insertarArchivo(archivo,contenedor,lista=[]):
    for element in lista:
        print(element.name)
        if element.name == contenedor:
            archivoFormato = archivo.split(" ")
            element.archivos.append(Fichero(archivoFormato[0],archivoFormato[1],archivoFormato[2],archivoFormato[3],contenedor))
            print(f"{archivoFormato[0]} Ingresado correctamente")
            break
        elif not element.directoriosIsEmpty():            
            insertarArchivo(archivo,contenedor,element.directorios)
            break

def cargaFicheros():
    f_directorios = open("directorios.txt","r")     
    f_archivos = open("ficheros.txt","r")   
    for line in f_directorios:
        elementos = line.split(",")#(carpeta,carpetapadre)
        #print(elementos[0]+" "+elementos[1].rstrip('\n'))
        insertaDirectorio(elementos[0],elementos[1].rstrip('\n'),ficheros)
    for line in f_archivos:
        elementos = line.split(",")#(formato_de_archivo,carpeta_contenedora)
        insertarArchivo(elementos[0],elementos[1].rstrip('\n'),ficheros)

# def cargaFicheros():
#     f_directorios = open("archivos.txt","r") #variable global para escribir en cualquier momento y usuario
#     ficheros = []
#     archivoslist = []
#     directorioslist = []
#     for line in f_directorio:
#         elementos = line.split(",")
#         t_carpeta =  Directorio(elementos[0])
#         for i in range(1,len(elementos)):
#             subElementos = elementos[i].split(' ')
#             if len(subElementos) > 2:#es un archivo
#                 archivoslist.append(Fichero(subElementos[0],subElementos[1],subElementos[2],subElementos[3]))
#             else:#es un directorio
#                 directorioslist.append(Directorio(subElementos[0],subElementos[1]))
#         t_carpeta.archivos.clear()
#         t_carpeta.directorios.clear()
#         t_carpeta.archivos = archivoslist.copy()
#         t_carpeta.directorios = directorioslist.copy()
#         ficheros.append(t_carpeta)
#         archivoslist.clear()
#         directorioslist.clear()
#     f_directorio.close()
#     return ficheros

def guardarEstado(lista):
    i = 0
    f_directorios = open("directorios.txt","w")
    f_archivos = open("ficheros.txt","w")
    for element in lista:
        for archivo in element.archivos:
            if i > 0: f_archivos.write('\n')
            cadena = archivo.name+' '+archivo.size+' '+archivo.owner+' '+str(archivo.permisos[0])+str(archivo.permisos[1])+str(archivo.permisos[2])
            f_archivos.write(cadena+','+archivo.contenedor) 
            i+=1
        f_directorios.write("raiz,.")
        for directorio in element.directorios:
            f_directorios.write('\n')
            cadena = directorio.name+','+directorio.padre
            f_directorios.write(cadena)

def borrarDirectorio(pwd):
    if(pwd.archivosIsEmpty() and pwd.directoriosIsEmpty()):
        return True
    return False

if __name__ == "__main__":
    encendido = True
    sesion = False
    while(encendido):
        print("1.-Iniciar sesión")
        print("2.-Crear usuario")
        print("3.-Salir")
        try:
            opc = int(input(": "))
        except ValueError as ve:
            print("Caracter no válido")
        else:
            if(opc == 1):
                usuario = input('Usuario: ')
                password = input('Contraseña: ')
                user = iniciarSesion(usuario,password)
                if(user):
                    sesion = True
                    cargaFicheros()
                    pwd = ficheros[0]
                    print(len(ficheros))
                    index,control = 0,0
                    # pwd = ficheros[0]
                    verContenidoDe(pwd)
                    print(f'Bienvenido {user.user}')
                    while(sesion):
                        print(f'1.-Crear archivo en este directorio: {pwd.name}')
                        print(f'2.-Crear directorio en este drectorio: {pwd.name}')
                        print(f'3.-Leer archivo')
                        print('4.-Escribir en archivo')
                        print('5.-Ejecutar archivo')
                        print('6.-Eliminar archivo')
                        print('7.-Eliminar directorio')
                        print(f'8.-Ver contendio de este directorio {pwd.name}')
                        print('9.-Subir')
                        print('10.-Bajar')
                        print('11.-Cambiar permisos')
                        print('12.-Cerrar sesión')
                        print('0.-Salir\n')
                        try:
                            opc = int(input(': '))
                        except ValueError as ve:
                            print('Caracter no válido')
                        else:
                            if(opc == 1):
                                nombre = input('Nombre: ')
                                size = input("Tamaño: ")
                                permisos = input("Permisos: ")
                                pwd.archivos.append(Fichero(nombre,size,user.user,permisos,pwd.name)) 
                            elif(opc == 2):
                                nombre = input("Nombre: ")
                                pwd.directorios.append(Directorio(nombre,pwd.name))
                            elif(opc == 3):
                                verContenidoDe(pwd,1)
                                try:
                                    index = int(input('Ingrese numero de archivo para leer: '))
                                    pwd.archivos[index].leer(user)
                                except:
                                    print("Valor no aceptado")
                                else:
                                    pass
                            elif(opc == 4):
                                verContenidoDe(pwd,1)
                                try:
                                    index = int(input('Ingrese numero de archivo para escribir: '))
                                    pwd.archivos[index].escribir(user)
                                except:
                                    print("Valor no aceptado")
                                else:
                                    pass
                            elif(opc == 5):
                                verContenidoDe(pwd,1)
                                try:
                                    index = int(input('Ingrese numero de archivo para ejecutar: '))
                                    pwd.archivos[index].execute(user)
                                except:
                                    print("Valor no aceptado")
                                else:
                                    pass
                            elif(opc == 6):
                                verContenidoDe(pwd,1)
                                index = int(input('Ingresa el archivo a borrar: '))
                                try:
                                    pwd.archivos.pop(index)
                                except IndexError as out:
                                    print("No se vale")
                            elif(opc == 7):
                                verContenidoDe(pwd,2)
                                index = int(input('Ingresa numero de directorio a borrar'))
                                if borrarDirectorio(pwd.directorios[index-1]):
                                    pwd.directorios.pop(index)
                                else:
                                    print('No se puede borrar el directorio pq tiene contenidos')
                            elif(opc == 8):
                                verContenidoDe(pwd) 
                            elif(opc == 9):#subir
                                if control != 0:
                                    control -= 1
                                    pwd = getDirectorioPadre(pwd.padre,ficheros)
                                    if(pwd == None):
                                        input('No se pudo volver')
                                else:
                                    print("Nivel mas alto alcanzado")
                            elif(opc == 10):#bajar
                                if len(pwd.directorios) > 0:
                                    verContenidoDe(pwd,2)
                                    index = int(input('Directorio a bajar: '))-1
                                    try:
                                        pwd = pwd.directorios[index]
                                    except IndexError as ie: 
                                        print('Tal indice no existe')
                                    else:
                                        control += 1
                                else:
                                    print("Nivel mas bajo alcanzado")
                            elif(opc == 11):
                                verContenidoDe(pwd,1)
                                try:
                                    index = int(input('Ingrese numero de archivo para cambiar permisos: '))
                                    pwd.archivos[index].changePermiso(user)
                                except:
                                    print("Valor no aceptado")
                            elif(opc == 12):
                                save = input('¿Desea guardar los cambios?[Y/N]')
                                if(save.upper() == 'Y'):
                                    guardarEstado(ficheros)
                                vaciar()
                                sesion = False
                            elif(opc == 0):
                                save = input('¿Desea guardar los cambios?[Y/N]')
                                if(save.upper() == 'Y'):
                                    guardarEstado(ficheros)
                                sesion = False
                                encendido = False
                                ##salvar usaurios y cosas así en archivos
                                break
                            else:
                                print('Opción no válida')
                else:
                    print("Usuario o contraseña no valido")
            elif(opc == 2):
                crearUsuario()
            elif(opc == 3):
                break
