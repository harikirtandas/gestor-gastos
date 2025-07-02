# GESTOR DE GASTOS DIARIOS EN PYTHON
from datetime import datetime
import csv
import os


# Cargar movimientos existentes desde archivo CSV si existe
archivo_gastos = "gastos.csv"
movimientos = []

if os.path.exists(archivo_gastos):
    with open(archivo_gastos, mode="r", newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            # Convertimos el monto a float
            fila['monto'] = float(fila['monto'])
            movimientos.append(fila)
            

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


# PROGRAMA PRINCIPAL 
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
    print("6. Salir")

    # Entrada del usuario
    opcion = input("\nElegí una opción (1-6): ").strip()


    # OPCIÓN 1: Agregar nuevo gasto
    if opcion == '1':
        while True:
            tipo = input("¿Qué tipo de movimiento querés registrar? (ingreso/gasto): ").strip().lower()
            if tipo in ["ingreso", "gasto"]:
                break
            else:
                print("⚠️ Ingresá 'ingreso' o 'gasto'.")
        print("\n"+('-' * 24))

        # Validación del monto: debe ser un número positivo con opción decimal y positivo
        while True:
            monto_str = input("Monto en pesos argentinos:\n").strip()
            # Esta línea hace la validación:
            # 1. monto_str.replace('.', '', 1) elimina el primer punto (si existe)
            # 2. .isdigit() verifica que el resto sean solo dígitos numéricos (0-9)
            # 3. monto_str.count('.') <= 1 asegura que haya como máximo un punto decimal en total
            # Así se permiten entradas válidas como "123", "123.45", pero se rechazan "12..3", "abc", o "123.45.67"
            if monto_str.replace('.', '', 1).isdigit() and monto_str.count('.') <= 1:
                monto = float(monto_str)
                if monto >= 0:
                    break
                else:
                    print("⚠️ El monto no puede ser negativo.")
            else:
                print("⚠️ Ingrese un número válido (ej: 1234.56).")

        # Se registran los otros campos del movimiento y se normalizan
        if tipo == "gasto":
            categoria = input("Ingrese la categoría del gasto (ej: Verdulería, Almacén, Transporte, Otra):\n").strip().capitalize()
            descripcion = input("Ingrese una breve descripción del gasto (ej: Colectivo, Remis, Fruta, Harina):\n").strip().capitalize()
        else:
            categoria = "Ingreso"
            descripcion = input("Ingrese la descripción del ingreso (ej: Sueldo, Venta, Otro):\n").strip().capitalize()

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
        with open(archivo_gastos, mode="a", newline="", encoding="utf-8") as f:
            campos = ['tipo', 'monto', 'categoria', 'descripción', 'fecha']
            escritor = csv.DictWriter(f, fieldnames=campos)

            # Si el archivo está vacío, escribimos el encabezado
            if f.tell() == 0:
                escritor.writeheader()
            escritor.writerow(nuevo_movimiento)


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
        cat = input("¿Qué categoría querés consultar? (ej: Verdulería, Almacén, Transporte): ").strip().capitalize()
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
            # Recorremos la lista de movimientos usando su índice (i)
            for i in range(len(movimientos)):
                datos = movimientos[i] # Obtenemos el diccionario correspondiente al movimiento actual
                partes = [] # Lista temporal para almacenar los elementos formateados del movimiento
                # Iteramos sobre cada clave (k) en el diccionario del movimiento
                for k in datos:
                    texto = f"{k}: {datos[k]}" # Formateamos cada par clave:valor como texto
                    partes.append(texto)       # Lo agregamos a la lista de partes

                detalle = ', '.join(partes)    # Unimos todas las partes en una sola línea separadas por comas
                # Mostramos el número de movimiento (empezando desde 1) y el detalle completo
                print(f"Movimiento {i + 1}: {detalle}")


    # OPCIÓN 6: Salir
    elif opcion == "6":
        print("\n"+('-' * 24))
        print('👋¡Hasta luego!')
        break


    # Cualquier otra opción inválida
    else:
        print("\n❌ Opción inválida. Elegí un número del 1 al 6.")


    
# git add .
# git commit -m "mensaje"
# git push