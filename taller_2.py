# GESTOR DE GASTOS DIARIOS EN PYTHON

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

        # Se pide DIA. Validación del día (1 al 31)
        while True:
            dia = input("Ingrese el día (1-31): ").strip()
            if dia.isdigit():
                dia_num = int(dia)
                if 1 <= dia_num <= 31:
                    dia = f"{dia_num:02d}" # Asegura que tenga dos dígitos (ej. 01, 09, 22)
                    break
                else:
                    print("⚠️ El día debe estar entre 1 y 31.")
            else:
                print("⚠️ Ingrese solo números.")

        # Se pide MES. Validación del mes (1 al 12)
        while True:
            mes = input("Ingrese el mes (1-12): ").strip()
            if mes.isdigit():
                mes_num = int(mes)
                if 1 <= mes_num <= 12:
                    mes = f"{mes_num:02d}" # Asegura que tenga dos dígitos (ej. 01, 09)
                    break
                else:
                    print("⚠️ El mes debe estar entre 1 y 12.")
            else:
                print("⚠️ Ingrese solo números.")

        # Se pide AÑO. Validación del año (rango lógico)
        while True:
            año = input("Ingrese el año (por ejemplo 2025): ").strip()
            if año.isdigit():
                año_num = int(año)
                if 2000 <= año_num <= 2100:
                    año = str(año_num)
                    break
                else:
                    print("⚠️ Ingrese un año válido entre 1900 y 2100.")
            else:
                print("⚠️ Ingrese solo números.")

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

        # Se piden día, mes y año para la búsqueda. Se repiten las validaciones
        while True: # DIA
            dia_consulta = input("Ingrese el día (1-31): ").strip()
            if dia_consulta.isdigit():
                d = int(dia_consulta)
                if 1 <= d <= 31:
                    dia_consulta = f"{d:02d}"
                    break
                else:
                    print("⚠️ El día debe estar entre 1 y 31.")
            else:
                print("⚠️ Ingrese solo números.")

        while True: # MES
            mes_consulta = input("Ingrese el mes (1-12): ").strip()
            if mes_consulta.isdigit():
                m = int(mes_consulta)
                if 1 <= m <= 12:
                    mes_consulta = f"{m:02d}"
                    break
                else:
                    print("⚠️ El mes debe estar entre 1 y 12.")
            else:
                print("⚠️ Ingrese solo números.")

        while True: # AÑO
            año_consulta = input("Ingrese el año (por ejemplo 2025): ").strip()
            if año_consulta.isdigit():
                a = int(año_consulta)
                if 2000 <= a <= 2100:
                    año_consulta = str(a)
                    break
                else:
                    print("⚠️ Ingrese un año válido entre 1900 y 2100.")
            else:
                print("⚠️ Ingrese solo números.")

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
