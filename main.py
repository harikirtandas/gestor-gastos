# GESTOR DE GASTOS DIARIOS EN PYTHON
from datetime import datetime
import csv
import os


# Funciónes
def cargar_movimientos():
    """
    Carga los movimientos guardados en el archivo CSV si existe.

    Lee el archivo 'gastos.csv', convierte el campo 'monto' a float y 
    agrega cada movimiento como un diccionario a una lista.

    Maneja posibles errores de lectura mostrando un mensaje descriptivo.

    Retorna:
        list: Lista de diccionarios con los movimientos cargados desde el archivo.
    """
    movimientos = []
    if os.path.exists(archivo_gastos):
        try:
            with open(archivo_gastos, mode="r", newline="", encoding="utf-8") as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    fila['monto'] = float(fila['monto'])
                    movimientos.append(fila)
        except Exception as e:
            print(f"⚠️ Error al leer el archivo CSV: {e}")
    return movimientos

def pedir_fecha():
    """
    Solicita al usuario una fecha válida en formato DD/MM/AAAA.

    Usa datetime.strptime para validar si la fecha existe realmente.
    Repite hasta que el usuario ingrese una fecha válida.

    Retorna:
        str: Fecha en formato DD/MM/AAAA.
    """
    while True:
        fecha_str = input("Ingresá la fecha (DD/MM/AAAA): ").strip()
        try:
            datetime.strptime(fecha_str, "%d/%m/%Y")
            return fecha_str
        except ValueError:
            print("⚠️ Fecha inválida. Usá el formato DD/MM/AAAA y asegurate de que sea real.")
            
def pedir_monto():
    """Solicita al usuario un monto positivo y válido, y lo devuelve como float."""
    while True:
        try:
            monto_str = input("Monto en pesos argentinos:\n").strip()
            
            if monto_str.count('.') <= 1 and monto_str.replace('.', '', 1).isdigit():
                monto = float(monto_str)
                if monto > 0:
                    return monto
                else:
                    print("⚠️ El monto debe ser mayor que cero.")
            else:
                print("⚠️ Ingrese un número válido (ej: 1234.56).")
        
        except ValueError:
            print("⚠️ Error al convertir el monto. Intente nuevamente.")

def normalizar_texto(texto):
    return texto.strip().capitalize()

def guardar_movimiento_csv(movimiento):
    """
    Guarda un movimiento individual en el archivo CSV.

    Si el archivo está vacío, escribe primero los encabezados. Luego agrega
    el movimiento recibido como una nueva fila.

    Args:
        movimiento (dict): Un diccionario con las claves 'tipo', 'monto',
                           'categoria', 'descripción' y 'fecha'.
    """
    with open(archivo_gastos, mode="a", newline="", encoding="utf-8") as f:
        campos = ['tipo', 'monto', 'categoria', 'descripción', 'fecha']
        escritor = csv.DictWriter(f, fieldnames=campos)
        if f.tell() == 0:
            escritor.writeheader()
        escritor.writerow(movimiento)

# PROGRAMA PRINCIPAL 

# Cargar movimientos existentes desde archivo CSV si existe
archivo_gastos = "gastos.csv"
movimientos = cargar_movimientos()

# Mensaje de bienvenida
print("Bienvenido/a al gestor de gastos diarios 📈\n")

# Bucle principal del menú
while True:
    print('\n--------- MENÚ ---------\n')
    print('1. Agregar nuevo movimiento (Ingreso o Gasto)')
    print("2. Ver gastos por fecha")
    print("3. Ver gastos por categoría")
    print("4. Ver total gastado")
    print("5. Ver todos los gastos cargados")
    print("6. Filtrar movimientos por tipo (ingresos o gastos)")
    print("7. Salir")

    # Entrada del usuario
    opcion = input("\nElegí una opción (1-7): ").strip()


    # OPCIÓN 1: Agregar nuevo gasto
    if opcion == '1':
        while True:
            tipo = input("¿Qué tipo de movimiento querés registrar? (ingreso/gasto): ").strip().lower()
            if tipo in ["ingreso", "gasto"]:
                break
            else:
                print("⚠️ Ingresá 'ingreso' o 'gasto'.")
        print("\n"+('-' * 24))

        # Llamamos a la función para pedir y validar el monto
        monto = pedir_monto()

        # Se registran los otros campos del movimiento y se normalizan
        if tipo == "gasto":
            categoria = normalizar_texto(input("Ingrese la categoría del gasto (ej: Verdulería, Almacén, Transporte, Otra):\n"))
            descripcion = normalizar_texto(input("Ingrese una breve descripción del gasto (ej: Colectivo, Remis, Fruta, Harina):\n"))
        else:
            categoria = "Ingreso"
            descripcion = normalizar_texto(input("Ingrese la descripción del ingreso (ej: Sueldo, Venta, Otro):\n"))

        # Fecha desglosada en día, mes y año, con validación por funciones
        fecha = pedir_fecha()

        # Se crea un nuevo diccionario con los datos y se agrega a la lista de movimientos
        nuevo_movimiento = {
            'tipo': tipo,
            'monto': monto,
            'categoria': categoria,
            'descripción': descripcion,
            'fecha': fecha
        }
        movimientos.append(nuevo_movimiento)
        print(f"\n✅ {tipo.capitalize()} agregado correctamente.")
        
        # Guardar el nuevo movimiento en el archivo CSV
        guardar_movimiento_csv(nuevo_movimiento)


    # OPCIÓN 2: Ver gastos por fecha específica
    elif opcion == '2':
        print('\n--- GASTOS POR FECHA ---\n')

        fecha_consulta = pedir_fecha()

        encontrado = False
        mostrar_fecha = True # Controla si ya mostramos la fecha o no
        subtotal = 0  # Mejora: variable para acumular el total del día

        # Se recorren los movimientos y se filtran por la fecha buscada
        for movimiento in movimientos:
            if movimiento["fecha"] == fecha_consulta:
                if mostrar_fecha:
                    print(f"\n📅 Fecha: {movimiento['fecha']}\n")
                    mostrar_fecha = False
                print(f"Monto: ${movimiento['monto']:.2f}, Categoría : {movimiento['categoria']}, Descripción: {movimiento['descripción']}")
                subtotal += movimiento["monto"]  # Sumamos el gasto al subtotal
                encontrado = True
        if not encontrado:
            print("\n❌ No hay registros para esa fecha.")
        else:
            print(f"\n🔸 Total gastado en esa fecha: ${subtotal:.2f}")

    # OPCIÓN 3: Ver gastos por categoría
    elif opcion == '3':
        print('\n--- GASTOS POR CATEGORÍA ---')
        cat = normalizar_texto(input("¿Qué categoría querés consultar? (ej: Verdulería, Almacén, Transporte): "))
        encontrado = False
        subtotal = 0  # Mejora: Acumulador de montos por categoría
        print()
        for movimiento in movimientos:
            if movimiento["categoria"] == cat:
                print(f"📌 Categoría: {movimiento['categoria']} | Monto: ${movimiento['monto']:.2f} | Descripción: {movimiento['descripción']} | Fecha: {movimiento['fecha']}")
                subtotal += movimiento["monto"]  # Sumar al total de la categoría
                encontrado = True
        if not encontrado:
            print("\n❌ No hay registros para esa categoría.")
        else:
            print(f"\n🔸 Total gastado en '{cat}': ${subtotal:.2f}")

    # OPCIÓN 4: Ver total gastado
    elif opcion == "4":
        ingresos = 0
        gastos = 0

        for movimiento in movimientos:
            if movimiento["tipo"] == "ingreso":
                ingresos += movimiento["monto"]
            elif movimiento["tipo"] == "gasto":
                gastos += movimiento["monto"]

        balance = ingresos - gastos
        
        print("\n--------- RESUMEN ---------\n")
        print(f"💰 Total de ingresos:     ${ingresos:,.2f}")
        print(f"💸 Total de gastos:       ${gastos:,.2f}")
        print(f"🧾 Balance final:         ${balance:,.2f}")

    # OPCIÓN 5: Ver todos los gastos cargados
    elif opcion == '5':
        print('\n-- 💵 TODOS LOS GASTOS ---\n')
        # Si la lista de movimientos está vacía, se informa al usuario
        if len(movimientos) == 0:
            print("❌ No hay gastos cargados.")
        else:
            campos = ['tipo', 'monto', 'categoria', 'descripción', 'fecha']
            # Recorremos la lista de movimientos con índice usando enumerate
            for i, datos in enumerate(movimientos, start=1):
                
                # Creamos una lista con los pares clave:valor del diccionario
                # Por ejemplo: ['tipo: gasto', 'monto: 250.0', 'categoría: Verdulería', ...]
                partes = [f"{campo}: {datos[campo]}" for campo in campos]
                
                # Unimos todos los elementos con comas para mostrarlo en una sola línea
                # Ejemplo: 'tipo: gasto, monto: 250.0, categoría: Verdulería, ...'
                detalle = ', '.join(partes)
                
                # Mostramos el número del movimiento (empezando desde 1) y su detalle
                print(f"Movimiento {i}: {detalle}")

    # OPCIÓN 6: “Filtrar movimientos por tipo (ingresos o gastos)”
    elif opcion == '6':
        tipo_movimiento = input('¿Qué tipo de movimiento querés ver? (ingreso/gasto): ').strip().lower()

        if tipo_movimiento not in ['ingreso', 'gasto']:
            print('⚠️ Ingresá una opción válida: ingreso/gasto')
        else:
            subtotal = 0
            encontrados = 0
            print(f"\n--- {tipo_movimiento.upper()}S REGISTRADOS ---\n")
            for movimiento in movimientos:
                if movimiento["tipo"] == tipo_movimiento:
                    print(f"💬 Monto: ${movimiento['monto']:.2f} | Categoría: {movimiento['categoria']} | Descripción: {movimiento['descripción']} | Fecha: {movimiento['fecha']}")
                    subtotal += movimiento["monto"]
                    encontrados += 1
            if encontrados == 0:
                print(f"❌ No hay movimientos registrados como '{tipo_movimiento}'.")
            else:
                simbolo = "💰" if tipo_movimiento == "ingreso" else "💸"
                print(f"\n{simbolo} Total de {tipo_movimiento}s: ${subtotal:,.2f}")
        
    # OPCIÓN 7: Salir
    elif opcion == "7":
        print("\n"+('-' * 24))
        print('👋¡Hasta luego!')
        break


    # Cualquier otra opción inválida
    else:
        print("\n❌ Opción inválida. Elegí un número del 1 al 7.")


    
# git add .
# git commit -m "mensaje"
# git push