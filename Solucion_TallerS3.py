# Solución de taller S3 

#Carlos Arturo Ramirez Londoño
#carlos.ramirezl@sofka.com.co


from datetime import datetime

from typing import Dict, List

Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo] # Al darle un alias a MemoriaAgente ayuda a que el código sea más legible y mantenible. De esta manera se agrega una especie de "tipado" que deja muy en claro como se recibe la estructura de la memoria del agente

# Herramienta para gestionar el historial
def gestionar_historial(accion: str, memoria: MemoriaAgente) -> str:
    """
    Gestiona el historial del agente según la acción: 'all', 'clear' o búsqueda por palabra clave.
    No imprime, solo retorna el resultado como string.
    """
    if not memoria:
        return "[Pseudoagente] No hay registros en el historial."
    if accion == "all":
        return "\n".join(str(log) for log in memoria)
    elif accion == "clear":
        memoria.clear()
        return "Historial de comandos borrado."
    else:
        coincidencias = [log for log in memoria if accion in log["descripcion"].lower()]
        if coincidencias:
            return "\n".join(str(log) for log in coincidencias) + f"\nCoincidencias encontradas: {len(coincidencias)}"
        else:
            return "[Pseudoagente] No encontré registros que coincidan con esa palabra."


def contar_letras(palabra: str) -> str:
    """
    Cuenta letras, vocales y consonantes en una palabra.
    """
    tot_letras = len(palabra)
    tot_vocales = sum(1 for p in palabra if p in "aeiou")
    tot_cons = tot_letras - tot_vocales
    return (f"Palabra ingresada: {palabra}\n"
            f"Total de letras: {tot_letras}\n"
            f"Total de vocales: {tot_vocales}\n"
            f"Total de consonantes: {tot_cons}")


def validar_password(usuario: str, nueva_contrasenia: str) -> str:
    """
    Valida una contraseña según reglas de longitud y diferencia con el usuario.
    """
    if len(nueva_contrasenia) < 8:
        return "Contraseña demasiado corta. Debe tener al menos 8 caracteres."
    elif nueva_contrasenia == usuario:
        return "Contraseña no puede ser igual al nombre de usuario."
    else:
        return "Contraseña válida."


def calculadora(num1: float, operador: str, num2: float) -> str:
    """
    Realiza operaciones básicas de calculadora. Lanza ValueError si hay error de operación.
    """
    if operador == "+":
        return f"Resultado: {num1 + num2}"
    elif operador == "-":
        return f"Resultado: {num1 - num2}"
    elif operador == "*":
        return f"Resultado: {num1 * num2}"
    elif operador == "/":
        if num2 == 0:
            raise ValueError("Error: no se puede dividir por cero.") # El error es atrapado en el cuerpo principal (except), permitiendo mostrar un mensaje sin dañar el programa. Así se blinda el flujo.
        return f"Resultado: {num1 / num2}"
    else:
        raise ValueError("Operador no válido.")


def obtener_fecha_hoy(rol: str) -> str:
    """
    Devuelve la fecha y hora actual solo si el rol es admin. Lanza PermissionError si no.
    """
    if rol != "admin":
        raise PermissionError("Privilegios insuficientes")  
    return f"Fecha y hora actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


roles = ["invitado","admin"]  # Se crea una lista con el fin de agrupar eficientemente los dos perfiles de usaurios
contrasenias = ["123thonpy","py456thon"] # Se hace lo mismo para la contraeñas teniendo en cuenta que su posición en las listas corresponde a su respectivo perfil

login_usuario = True # Bandera para el ciclo de validación del usuario y controladora de seguridad
intentos = 0         # variable que lleva el conteo de los intentos fallidos
max_intentos = 3     # Número máximo de intentos permitidos
while login_usuario:
    usuario = input("Ingrese el rol de usuario (invitado/admin): ").lower()
    if usuario in roles:
        login_contrasenia = True
        while login_contrasenia:
            rol = roles.index(usuario)
            contrasenia = input("Ingrese la contraseña: ")
            if contrasenia == contrasenias[rol]:
                print(f"Bienvenido, {usuario}. Acceso concedido.\n")
                print("----- Iniciando el pseudoagente estilo consola -----")
                sistema_activo = True
                historial_chat: MemoriaAgente = []
                mensaje = ""
                while sistema_activo:
                    cmd = input("Agente>: ").strip().lower().split()
                    try:
                        if cmd[0] == "salir":
                            print("-----Agente apagado. Vuelve pronto. -----")
                            sistema_activo = False
                            login_contrasenia = False
                            login_usuario = False
                            mensaje = "Se ha solicitado terminar la sesión."
                        elif cmd[0] == "ping":
                            print("pong.")
                            mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."
                        elif cmd[0] == "contar":
                            palabra = input("Ingrese una palabra: ").lower()
                            mensaje = contar_letras(palabra)
                            print(mensaje)
                        elif cmd[0] == "fecha_hoy":
                            try:
                                mensaje = obtener_fecha_hoy(usuario)
                                print(mensaje)
                            except PermissionError as e:
                                print(f"[Alerta] {e}")
                                mensaje = str(e)
                        elif cmd[0] == "validar_pass":
                            nueva_contrasenia = input("Ingrese una nueva contraseña: ")
                            mensaje = validar_password(usuario, nueva_contrasenia)
                            print(mensaje)
                        elif cmd[0] == "calculadora":
                            try:
                                num1 = float(input("Ingresa el primer número: "))
                                operador = input("Ingresa el operador (+, -, *, /): ")
                                num2 = float(input("Ingresa el segundo número: "))
                                mensaje = calculadora(num1, operador, num2)
                                print(mensaje)
                            except ValueError as ve:
                                print(f"[Error] {ve}")
                                mensaje = str(ve)
                        elif cmd[0] == "historial":
                            if len(cmd) > 1 and cmd[1] in ("all", "clear"):
                                resultado = gestionar_historial(cmd[1], historial_chat)
                                print(resultado)
                                mensaje = resultado
                            else:
                                clave = input("Ingrese la palabra clave a buscar: ").lower()
                                resultado = gestionar_historial(clave, historial_chat)
                                print(resultado)
                                mensaje = resultado
                        else:
                            mensaje = "-----Comando desconocido. Intente de nuevo. -----"
                            print(mensaje)
                    except IndexError:
                        print("[Error] Debe ingresar un comando.")
                        mensaje = "Comando vacío."
                    d_log = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             "cmd": str(cmd),
                             "rol": usuario,
                             "descripcion": mensaje}
                    historial_chat.append(d_log)
            else:
                print("Contraseña incorrecta. Intente de nuevo.")
                intentos += 1
            if intentos >= max_intentos:
                login_contrasenia = False
        login_usuario = False
    else:
        print("Usuario no reconocido. Intente de nuevo.")
        intentos += 1
    if intentos >= max_intentos:
        print("[Alerta] Usuario bloqueado. Cerrando sistema.")
        login_usuario = False
