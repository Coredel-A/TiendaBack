import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from a_sucursales.models import Sucursal

class Command(BaseCommand):
    help = 'Crea sucursales de prueba con datos en español'

    def add_arguments(self, parser):
        parser.add_argument('--cantidad', type=int, default=10, help='Cantidad de sucursales a crear')

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        self.stdout.write(f'Creando {cantidad} sucursales de prueba...')
        
        # Configuramos Faker para español
        fake = Faker('es_ES')
        
        # Datos para Guatemala (departamentos principales y sus municipios)
        departamentos_guatemala = {
            'Guatemala': ['Ciudad de Guatemala', 'Mixco', 'Villa Nueva', 'San Miguel Petapa', 'Santa Catarina Pinula'],
            'Quetzaltenango': ['Quetzaltenango', 'Coatepeque', 'Colomba', 'San Juan Ostuncalco'],
            'Escuintla': ['Escuintla', 'Puerto San José', 'Palín', 'Santa Lucía Cotzumalguapa'],
            'Alta Verapaz': ['Cobán', 'San Pedro Carchá', 'San Cristóbal Verapaz', 'Tactic'],
            'Huehuetenango': ['Huehuetenango', 'Santa Cruz Barillas', 'La Democracia', 'Jacaltenango'],
            'Izabal': ['Puerto Barrios', 'Livingston', 'Morales', 'Los Amates'],
            'Petén': ['Flores', 'San Benito', 'San Francisco', 'La Libertad'],
            'Sacatepéquez': ['Antigua Guatemala', 'Jocotenango', 'Ciudad Vieja', 'Santa María de Jesús'],
            'San Marcos': ['San Marcos', 'Malacatán', 'Ocós', 'San Pedro Sacatepéquez'],
            'Sololá': ['Sololá', 'Panajachel', 'Santiago Atitlán', 'San Lucas Tolimán']
        }
        
        # Datos para El Salvador
        departamentos_el_salvador = {
            'San Salvador': ['San Salvador', 'Soyapango', 'Mejicanos', 'Apopa'],
            'Santa Ana': ['Santa Ana', 'Chalchuapa', 'Metapán', 'El Congo'],
            'San Miguel': ['San Miguel', 'Ciudad Barrios', 'Chinameca', 'El Tránsito'],
            'La Libertad': ['Santa Tecla', 'Antiguo Cuscatlán', 'Colón', 'Zaragoza']
        }
        
        # Datos para Honduras
        departamentos_honduras = {
            'Francisco Morazán': ['Tegucigalpa', 'Santa Ana', 'Cedros', 'Talanga'],
            'Cortés': ['San Pedro Sula', 'Puerto Cortés', 'Choloma', 'Villanueva'],
            'Atlántida': ['La Ceiba', 'Tela', 'El Porvenir', 'Jutiapa']
        }
        
        # Países donde tendremos sucursales
        paises = {
            'Guatemala': departamentos_guatemala,
            'El Salvador': departamentos_el_salvador,
            'Honduras': departamentos_honduras
        }
        
        # Prefijos de teléfono por país
        prefijos_telefono = {
            'Guatemala': '+502',
            'El Salvador': '+503',
            'Honduras': '+504'
        }
        
        # Tipos de ubicaciones para crear nombres coherentes de sucursales
        tipos_ubicacion = [
            'Centro Comercial', 'Plaza', 'Edificio', 'Galerías', 'Mall', 
            'Paseo', 'Portal', 'Metrocentro', 'Boulevard', 'Pradera'
        ]
        
        # Lista para nombres de sucursales usados (para evitar duplicados)
        nombres_usados = []
        
        # Función para generar nombre de sucursal
        def generar_nombre_sucursal(ciudad, pais):
            if random.random() < 0.6:  # 60% de probabilidad de usar tipo de ubicación
                tipo = random.choice(tipos_ubicacion)
                ubicacion = f"{tipo} {ciudad}"
                
                # Añadir un número si es un tipo genérico
                if tipo in ['Centro Comercial', 'Plaza', 'Edificio']:
                    ubicacion = f"{tipo} {ciudad} {random.randint(1, 5)}"
            else:
                # Usar zona o área de la ciudad
                zona = f"Zona {random.randint(1, 15)}"
                ubicacion = f"{ciudad} {zona}"
            
            return ubicacion
        
        # Función para generar dirección detallada
        def generar_direccion(ciudad, departamento, pais):
            calle = random.choice([
                f"Calle {random.randint(1, 30)}", 
                f"Avenida {random.randint(1, 20)}",
                f"Boulevard {fake.last_name()}",
                f"Calzada {fake.last_name()}"
            ])
            
            numero = f"{random.randint(1, 100)}-{random.randint(1, 99)}"
            
            # Añadir detalles según el país
            if pais == 'Guatemala':
                zona = f"Zona {random.randint(1, 21)}"
                return f"{calle} {numero}, {zona}, {ciudad}, {departamento}, {pais}"
            else:
                colonia = f"Colonia {fake.last_name()}"
                return f"{calle} {numero}, {colonia}, {ciudad}, {departamento}, {pais}"
        
        # Generar número de teléfono según el país
        def generar_telefono(pais):
            prefijo = prefijos_telefono[pais]
            if pais == 'Guatemala':
                return f"{prefijo} {random.randint(2, 8)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
            elif pais == 'El Salvador':
                return f"{prefijo} {random.choice(['2', '7'])}{random.randint(100, 999)}{random.randint(1000, 9999)}"
            else:  # Honduras
                return f"{prefijo} {random.randint(2, 9)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
        
        # Comenzamos la transacción
        with transaction.atomic():
            sucursales_creadas = 0
            
            # Distribuir sucursales entre países (más para Guatemala)
            distribucion = {
                'Guatemala': int(cantidad * 0.6),  # 60% en Guatemala
                'El Salvador': int(cantidad * 0.2),  # 20% en El Salvador
                'Honduras': int(cantidad * 0.2)  # 20% en Honduras
            }
            
            # Ajustar si la suma no coincide con la cantidad total
            total_distribuido = sum(distribucion.values())
            if total_distribuido < cantidad:
                distribucion['Guatemala'] += (cantidad - total_distribuido)
            
            # Crear sucursales por país
            for pais, num_sucursales in distribucion.items():
                departamentos = paises[pais]
                
                for _ in range(num_sucursales):
                    # Seleccionar departamento y ciudad aleatoriamente
                    departamento = random.choice(list(departamentos.keys()))
                    ciudad = random.choice(departamentos[departamento])
                    
                    # Generar nombre único para la sucursal
                    nombre = generar_nombre_sucursal(ciudad, pais)
                    intentos = 0
                    while nombre in nombres_usados and intentos < 10:
                        nombre = generar_nombre_sucursal(ciudad, pais)
                        intentos += 1
                    
                    nombres_usados.append(nombre)
                    
                    # Crear la sucursal
                    sucursal = Sucursal.objects.create(
                        nombre=nombre,
                        direccion=generar_direccion(ciudad, departamento, pais),
                        pais=pais,
                        telefono=generar_telefono(pais)
                    )
                    
                    self.stdout.write(f"Creada sucursal: {sucursal.nombre} en {sucursal.pais}")
                    sucursales_creadas += 1
            
        self.stdout.write(self.style.SUCCESS(f'Se han creado {sucursales_creadas} sucursales correctamente'))