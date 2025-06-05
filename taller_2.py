# GESTOR DE GASTOS DIARIOS EN PYTHON

# Función para solicitar y validar el día (1-31)
def pedir_dia():
    """
    Solicita al usuario ingresar un día válido.

    La función repite la solicitud hasta que el usuario ingrese un número entero
    entre 1 y 31. Luego devuelve el día formateado como string con dos dígitos,
    por ejemplo '01', '15'.

    Retorna:
        str: Día formateado con dos dígitos.
    """
    while True:
        # Pedimos al usuario que ingrese el día y limpiamos espacios en blanco
        dia = input("Ingrese el día (1-31): ").strip()
        # Verificamos que la entrada sea solo números (sin letras ni símbolos)
        if dia.isdigit():
            dia_num = int(dia)  # Convertimos el valor a entero para hacer validaciones numéricas
            if 1 <= dia_num <= 31:
                # Si el día está dentro del rango válido, lo devolvemos con formato 'dd'
                return f"{dia_num:02d}"
            else:
                # Mensaje de error si el número no está entre 1 y 31
                print("⚠️ El día debe estar entre 1 y 31.")
        else:
            # Mensaje de error si la entrada contiene caracteres no numéricos
            print("⚠️ Ingrese solo números.")


# Función para solicitar y validar el mes (1-12)
def pedir_mes():
    """
    Solicita al usuario ingresar un mes válido.

    La función repite la solicitud hasta que el usuario ingrese un número entero
    entre 1 y 12. Luego devuelve el mes formateado como string con dos dígitos,
    por ejemplo '01', '12'.

    Retorna:
        str: Mes formateado con dos dígitos.
    """
    while True:
        # Solicitamos el mes y eliminamos espacios en blanco
        mes = input("Ingrese el mes (1-12): ").strip()
        # Verificamos que el input contenga solo números
        if mes.isdigit():
            mes_num = int(mes)  # Convertimos el valor a entero para validar rango
            if 1 <= mes_num <= 12:
                # Si está dentro del rango, devolvemos el mes formateado
                return f"{mes_num:02d}"
            else:
                # Mensaje de error si el número no está entre 1 y 12
                print("⚠️ El mes debe estar entre 1 y 12.")
        else:
            # Mensaje de error si la entrada tiene caracteres no numéricos
            print("⚠️ Ingrese solo números.")


# Función para solicitar y validar el año (2000-2100)
def pedir_año():
    """
    Solicita al usuario ingresar un año válido.

    La función repite la solicitud hasta que el usuario ingrese un número entero
    entre 2000 y 2100. Luego devuelve el año como string.

    Retorna:
        str: Año ingresado.
    """
    while True:
        # Pedimos el año y limpiamos espacios
        año = input("Ingrese el año (por ejemplo 2025): ").strip()
        # Verificamos que sea solo números
        if año.isdigit():
            año_num = int(año)  # Convertimos a entero para validar rango
            if 2000 <= año_num <= 2100:
                # Devolvemos el año como string
                return str(año_num)
            else:
                # Mensaje si el año está fuera del rango esperado
                print("⚠️ Ingrese un año válido entre 1900 y 2100.")
        else:
            # Mensaje si la entrada contiene caracteres inválidos
            print("⚠️ Ingrese solo números.")
# Mensaje de bienvenida
print("Bienvenido/a al gestor de gastos diarios 📈\n")

# Lista vacía para almacenar los gastos.
# Cada gasto será un diccionario con los campos: monto, categoría, descripción y fecha
gastos = []

# Bucle principal del menú
while True:
    print('\n--------- MENÚ ---------\n')
    print('1. Agregar nuevo gasto')
    print("2. Ver gastos por fecha")
    print("3. Ver gastos por categoría")
    print("4. Ver total gastado")
    print("5. Ver todos los gastos cargados")
    print("6. Salir")

    # Entrada del usuario
    opcion = input("\nElegí una opción (1-6): ").strip()


    # OPCIÓN 1: Agregar nuevo gasto
    if opcion == '1':
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

        # Se registran los otros campos del gasto y se normalizan
        categoria = input("Categoría (almacén, verdulería, transporte, otra):\n").strip().capitalize()
        descripcion = input("Descripción (colectivo, remis, alimento, varios):\n").strip().capitalize()

        # Fecha desglosada en día, mes y año, con validación de entrada

        dia = pedir_dia()
        mes = pedir_mes()
        año = pedir_año()

        # Composición final de la fecha en formato DD/MM/AAAA
        fecha = f"{dia}/{mes}/{año}"

        # Se crea un nuevo diccionario con los datos y se agrega a la lista de gastos
        nuevo_gasto = {
            'monto': monto,
            'categoria': categoria,
            'descripción': descripcion,
            'fecha': fecha
        }
        gastos.append(nuevo_gasto)
        print("\n✅ Gasto agregado correctamente.")


    # OPCIÓN 2: Ver gastos por fecha específica
    elif opcion == '2':
        print('\n--- GASTOS POR FECHA ---\n')

        dia_consulta = pedir_dia()
        mes_consulta = pedir_mes()
        año_consulta = pedir_año()

        # Se arma la fecha de consulta
        print("\n" + ('-' * 24))
        fecha_consulta = f"{dia_consulta}/{mes_consulta}/{año_consulta}"

        encontrado = False
        mostrar_fecha = True # Controla si ya mostramos la fecha o no

        # Se recorren los gastos y se filtran por la fecha buscada
        for gasto in gastos:
            if gasto["fecha"] == fecha_consulta:
                if mostrar_fecha:
                    print(f"\n📅 Fecha: {gasto['fecha']}\n")
                    mostrar_fecha = False
                print(f"Monto: ${gasto['monto']:.2f}, Categoría : {gasto['categoria']}, Descripción: {gasto['descripción']}")
                encontrado = True
        if not encontrado:
            print("\n❌ No hay registros para esa fecha.")


    # OPCIÓN 3: Ver gastos por categoría
    elif opcion == '3':
        print('\n--- GASTOS POR CATEGORÍA ---')
        cat = input("Ingresá la categoría a consultar: ").strip().capitalize()
        encontrado = False
        print()
        for gasto in gastos:
            if gasto["categoria"] == cat:
                print(f"📌 Categoría: {gasto['categoria']} | Monto: ${gasto['monto']:.2f} | Descripción: {gasto['descripción']} | Fecha: {gasto['fecha']}")
                encontrado = True
        if not encontrado:
            print("\n❌ No hay registros para esa categoría.")


    # OPCIÓN 4: Ver total gastado
    elif opcion == "4":
        total = 0
        for gasto in gastos:
            total += gasto["monto"]
        print('\n--------- TOTAL --------\n')
        print(f"💵 Total gastado: ${total:.2f}")


    # OPCIÓN 5: Ver todos los gastos cargados
    elif opcion == '5':
        print('\n-- 💵 TODOS LOS GASTOS ---\n')
        # Si la lista de gastos está vacía, se informa al usuario
        if len(gastos) == 0:
            print("❌ No hay gastos cargados.")
        else:
            # Recorremos la lista de gastos usando su índice (i)
            for i in range(len(gastos)):
                datos = gastos[i] # Obtenemos el diccionario correspondiente al gasto actual
                partes = [] # Lista temporal para almacenar los elementos formateados del gasto
                # Iteramos sobre cada clave (k) en el diccionario del gasto
                for k in datos:
                    texto = f"{k}: {datos[k]}" # Formateamos cada par clave:valor como texto
                    partes.append(texto)       # Lo agregamos a la lista de partes

                detalle = ', '.join(partes)    # Unimos todas las partes en una sola línea separadas por comas
                # Mostramos el número de gasto (empezando desde 1) y el detalle completo
                print(f"Gasto{i + 1}: {detalle}")


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