import os
import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from a_productos.models import Producto, Categoria

class Command(BaseCommand):
    help = 'Crea productos de prueba con datos en español'

    def add_arguments(self, parser):
        parser.add_argument('--cantidad', type=int, default=50, help='Cantidad de productos a crear')

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        self.stdout.write(f'Creando {cantidad} productos de prueba...')
        
        # Configuramos Faker para español
        fake = Faker('es_ES')
        
        # Obtenemos las categorías existentes
        categorias = list(Categoria.objects.all())
        if not categorias:
            self.stdout.write(self.style.ERROR('No hay categorías disponibles. Por favor, crea categorías primero.'))
            return
            
        # Listado de imágenes disponibles
        ruta_imagenes = 'media/productos'
        imagenes_disponibles = []
        
        try:
            for archivo in os.listdir(ruta_imagenes):
                if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    imagenes_disponibles.append(f'productos/{archivo}')
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('No se encontró la carpeta de imágenes. Se crearán productos sin imágenes.'))
        
        # Listado de marcas comunes en español
        marcas = [
            'Samsung', 'LG', 'Sony', 'Philips', 'Panasonic', 'Xiaomi', 'Huawei', 
            'Asus', 'HP', 'Dell', 'Lenovo', 'Acer', 'Apple', 'Microsoft', 'Bosch', 
            'Siemens', 'Balay', 'Fagor', 'Beko', 'Teka', 'Zanussi', 'Whirlpool', 
            'Telefunken', 'TCL', 'Nokia', 'BenQ', 'Toshiba', 'Hisense', 'Oppo', 'Vivo'
        ]
        
        # Estados disponibles
        estados = ['activo', 'descontinuado', 'agotado']
        
        # Palabras clave para generar descripciones más coherentes por tipo de producto
        palabras_electronica = [
            'resolución', 'pantalla', 'pulgadas', 'altavoces', 'procesador', 'memoria', 
            'almacenamiento', 'conectividad', 'batería', 'autonomía', 'smart', 'tecnología', 
            'sistema operativo', 'táctil', 'inalámbrico', 'bluetooth', 'wifi', 'usb', 'hdmi'
        ]
        
        palabras_electrodomesticos = [
            'capacidad', 'litros', 'eficiencia energética', 'consumo', 'potencia', 'revoluciones', 
            'programas', 'función', 'silencioso', 'ajustable', 'temperatura', 'velocidad', 
            'automático', 'timer', 'digital', 'panel', 'control', 'programable'
        ]
        
        palabras_informatica = [
            'procesador', 'núcleos', 'RAM', 'SSD', 'disco duro', 'gráfica', 'tarjeta gráfica', 
            'resolución', 'teclado', 'puerto', 'conectividad', 'inalámbrico', 'gaming', 
            'profesional', 'ultrabook', 'convertible', 'webcam', 'micrófono'
        ]
        
        # Función para generar nombre coherente según categoría
        def generar_nombre(categoria_nombre):
            prefijos = {
                'Televisores': ['Televisor', 'Smart TV', 'TV LED', 'TV OLED', 'TV QLED'],
                'Móviles': ['Smartphone', 'Teléfono', 'Móvil'],
                'Portátiles': ['Portátil', 'Laptop', 'Notebook', 'Ultrabook'],
                'Tablets': ['Tablet', 'Tableta'],
                'Electrodomésticos': ['Frigorífico', 'Lavadora', 'Lavavajillas', 'Horno', 'Microondas', 'Secadora'],
                'Audio': ['Auriculares', 'Altavoz', 'Barra de sonido', 'Sistema de audio', 'Equipo Hi-Fi'],
                'Cámaras': ['Cámara', 'Cámara digital', 'Cámara réflex', 'Videocámara'],
                'Informática': ['Monitor', 'Teclado', 'Ratón', 'Disco duro', 'Impresora'],
                'Gaming': ['Consola', 'Mando', 'Silla gaming', 'Auriculares gaming', 'Teclado gaming']
            }
            
            # Obtenemos prefijos para la categoría o un prefijo genérico
            prefijo_lista = prefijos.get(categoria_nombre, ['Dispositivo', 'Producto', 'Equipo'])
            prefijo = random.choice(prefijo_lista)
            
            # Añadimos algún adjetivo apropiado
            adjetivos = ['Pro', 'Avanzado', 'Ultra', 'Smart', 'Premium', 'Lite', 'Plus', 'Max']
            
            # Generamos un nombre coherente
            if random.random() < 0.7:  # 70% de probabilidad de añadir adjetivo
                return f"{prefijo} {random.choice(adjetivos)}"
            else:
                return prefijo
        
        # Función para generar una descripción coherente
        def generar_descripcion(categoria_nombre):
            palabras = palabras_electronica  # Por defecto
            
            if 'Electrodomésticos' in categoria_nombre:
                palabras = palabras_electrodomesticos
            elif 'Portátiles' in categoria_nombre or 'Informática' in categoria_nombre:
                palabras = palabras_informatica
                
            # Generamos 3-5 frases para la descripción
            num_frases = random.randint(3, 5)
            frases = []
            
            for _ in range(num_frases):
                palabras_frase = random.sample(palabras, k=min(3, len(palabras)))
                frase = fake.sentence(nb_words=10, ext_word_list=palabras_frase)
                frases.append(frase)
                
            return ' '.join(frases)
        
        # Función para generar especificaciones técnicas
        def generar_especificaciones(categoria_nombre):
            especificaciones = []
            
            # Especificaciones básicas comunes a todas las categorías
            especificaciones.append(f"• Marca: {random.choice(marcas)}")
            especificaciones.append(f"• Modelo: {fake.bothify(text='??-###?')}")
            especificaciones.append(f"• Color: {fake.color_name()}")
            especificaciones.append(f"• Peso: {random.randint(1, 15)} kg")
            especificaciones.append(f"• Dimensiones: {random.randint(10, 100)}x{random.randint(10, 100)}x{random.randint(5, 50)} cm")
            
            # Especificaciones específicas por categoría
            if 'Televisores' in categoria_nombre:
                especificaciones.append(f"• Tamaño de pantalla: {random.choice([32, 40, 43, 50, 55, 65, 75])} pulgadas")
                especificaciones.append(f"• Resolución: {random.choice(['HD', 'Full HD', '4K UHD', '8K'])}")
                especificaciones.append(f"• Tecnología: {random.choice(['LED', 'OLED', 'QLED', 'NanoCell'])}")
                especificaciones.append(f"• Smart TV: {random.choice(['Sí', 'No'])}")
                especificaciones.append(f"• Conectividad: {', '.join(random.sample(['HDMI', 'USB', 'Bluetooth', 'Wi-Fi', 'Ethernet'], k=3))}")
            
            elif 'Móviles' in categoria_nombre:
                especificaciones.append(f"• Pantalla: {random.choice([5.5, 6.1, 6.4, 6.7])} pulgadas")
                especificaciones.append(f"• Memoria RAM: {random.choice([4, 6, 8, 12])} GB")
                especificaciones.append(f"• Almacenamiento: {random.choice([64, 128, 256, 512])} GB")
                especificaciones.append(f"• Cámara principal: {random.randint(12, 108)} MP")
                especificaciones.append(f"• Batería: {random.randint(3000, 5000)} mAh")
            
            elif 'Portátiles' in categoria_nombre:
                especificaciones.append(f"• Procesador: {random.choice(['Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'AMD Ryzen 5', 'AMD Ryzen 7'])}")
                especificaciones.append(f"• Memoria RAM: {random.choice([8, 16, 32])} GB")
                especificaciones.append(f"• Almacenamiento: SSD {random.choice([256, 512, 1024])} GB")
                especificaciones.append(f"• Pantalla: {random.choice([13.3, 14, 15.6, 17])} pulgadas")
                especificaciones.append(f"• Tarjeta gráfica: {random.choice(['Integrada', 'NVIDIA GeForce', 'AMD Radeon'])}")
            
            elif 'Electrodomésticos' in categoria_nombre:
                especificaciones.append(f"• Potencia: {random.randint(800, 2500)} W")
                especificaciones.append(f"• Eficiencia energética: {random.choice(['A++', 'A+', 'A', 'B'])}")
                especificaciones.append(f"• Capacidad: {random.randint(5, 30)} L")
                especificaciones.append(f"• Número de programas: {random.randint(3, 12)}")
                especificaciones.append(f"• Nivel de ruido: {random.randint(40, 75)} dB")
            
            # Devolvemos las especificaciones como texto
            return '\n'.join(especificaciones)
        
        # Generar modelos con nombres coherentes
        def generar_modelo(marca):
            letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(1, 3)))
            numeros = ''.join(random.choices('0123456789', k=random.randint(2, 4)))
            return f"{letras}-{numeros}"
        
        # Comenzamos la transacción
        with transaction.atomic():
            # Creamos los productos
            for _ in range(cantidad):
                # Seleccionamos una categoría aleatoria
                categoria = random.choice(categorias)
                
                # Generamos nombre coherente según categoría
                nombre_base = generar_nombre(categoria.nombre)
                # Añadimos la marca al nombre para hacerlo más realista
                marca = random.choice(marcas)
                modelo = generar_modelo(marca)
                nombre = f"{nombre_base} {marca} {modelo}"
                
                # Recortamos si excede longitud máxima
                if len(nombre) > 200:
                    nombre = nombre[:197] + "..."
                
                # Asignamos una imagen aleatoria si hay disponibles
                imagen = None
                if imagenes_disponibles:
                    imagen = random.choice(imagenes_disponibles)
                
                # Generamos precio coherente
                if 'Televisores' in categoria.nombre:
                    precio = round(random.uniform(299.99, 2999.99), 2)
                elif 'Móviles' in categoria.nombre:
                    precio = round(random.uniform(149.99, 1499.99), 2)
                elif 'Portátiles' in categoria.nombre:
                    precio = round(random.uniform(399.99, 1999.99), 2)
                else:
                    precio = round(random.uniform(49.99, 999.99), 2)
                
                # Creamos el producto
                producto = Producto.objects.create(
                    nombre=nombre,
                    descripcion=generar_descripcion(categoria.nombre),
                    especificaciones=generar_especificaciones(categoria.nombre),
                    marca=marca,
                    modelo=modelo,
                    precio=precio,
                    categoria=categoria,
                    imagen=imagen,
                    estado=random.choices(
                        estados,
                        weights=[0.7, 0.2, 0.1],  # 70% activos, 20% descontinuados, 10% agotados
                        k=1
                    )[0]
                )
                
                self.stdout.write(f"Creado: {producto.nombre}")
                
        self.stdout.write(self.style.SUCCESS(f'Se han creado {cantidad} productos correctamente'))