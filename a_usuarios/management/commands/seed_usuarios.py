import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from a_usuarios.models import Usuario, DireccionEnvio
from a_sucursales.models import Sucursal

class Command(BaseCommand):
    help = 'Crea usuarios de tipo cliente y sus direcciones de envío con datos en español'

    def add_arguments(self, parser):
        parser.add_argument('--cantidad', type=int, default=30, help='Cantidad de usuarios clientes a crear')
        parser.add_argument('--min-direcciones', type=int, default=1, help='Mínimo de direcciones por usuario')
        parser.add_argument('--max-direcciones', type=int, default=3, help='Máximo de direcciones por usuario')

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        min_direcciones = options['min_direcciones']
        max_direcciones = options['max_direcciones']
        
        self.stdout.write(f'Creando {cantidad} usuarios clientes con {min_direcciones}-{max_direcciones} direcciones cada uno...')
        
        # Verificar que existan sucursales
        sucursales_count = Sucursal.objects.count()
        if sucursales_count == 0:
            self.stdout.write(self.style.WARNING('No hay sucursales en la base de datos. Se recomienda crear sucursales primero.'))
        
        # Configuramos Faker para español
        fake = Faker('es_ES')
        
        # Datos para Guatemala (departamentos y municipios)
        departamentos_guatemala = {
            'Guatemala': ['Ciudad de Guatemala', 'Mixco', 'Villa Nueva', 'San Miguel Petapa', 'Santa Catarina Pinula'],
            'Quetzaltenango': ['Quetzaltenango', 'Coatepeque', 'Colomba', 'San Juan Ostuncalco'],
            'Escuintla': ['Escuintla', 'Puerto San José', 'Palín', 'Santa Lucía Cotzumalguapa'],
            'Alta Verapaz': ['Cobán', 'San Pedro Carchá', 'San Cristóbal Verapaz', 'Tactic'],
            'Huehuetenango': ['Huehuetenango', 'Santa Cruz Barillas', 'La Democracia', 'Jacaltenango'],
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
        
        # Países donde tendremos usuarios
        paises = {
            'Guatemala': departamentos_guatemala,
            'El Salvador': departamentos_el_salvador,
            'Honduras': departamentos_honduras
        }
        
        # Dominios de correo para generar emails realistas
        dominios_correo = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com', 'live.com']
        
        # Prefijos de teléfono por país
        prefijos_telefono = {
            'Guatemala': '+502',
            'El Salvador': '+503',
            'Honduras': '+504'
        }
        
        # Función para generar un correo electrónico único
        def generar_email(nombre, apellido):
            dominio = random.choice(dominios_correo)
            separador = random.choice(['', '.', '_'])
            
            if random.random() < 0.3:  # 30% de probabilidad de incluir un número
                numero = random.randint(1, 99)
                email = f"{nombre.lower()}{separador}{apellido.lower()}{numero}@{dominio}"
            else:
                email = f"{nombre.lower()}{separador}{apellido.lower()}@{dominio}"
                
            return email
        
        # Función para generar nombre completo sin caracteres especiales
        def generar_nombre_completo():
            nombre = fake.first_name().replace('ñ', 'n').replace('Ñ', 'N')
            apellido = fake.last_name().replace('ñ', 'n').replace('Ñ', 'N')
            return nombre, apellido
        
        # Función para generar dirección
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
                return f"{calle} {numero}, {zona}, {ciudad}, {departamento}"
            else:
                colonia = f"Colonia {fake.last_name()}"
                return f"{calle} {numero}, {colonia}, {ciudad}, {departamento}"
        
        # Generar número de teléfono según el país
        def generar_telefono(pais):
            prefijo = prefijos_telefono[pais]
            if pais == 'Guatemala':
                return f"{prefijo} {random.randint(2, 8)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
            elif pais == 'El Salvador':
                return f"{prefijo} {random.choice(['2', '7'])}{random.randint(100, 999)}{random.randint(1000, 9999)}"
            else:  # Honduras
                return f"{prefijo} {random.randint(2, 9)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
        
        # Generar código postal
        def generar_codigo_postal(pais, departamento=None):
            if pais == 'Guatemala':
                return f"{random.randint(1, 22):02d}{random.randint(1, 99):02d}"
            elif pais == 'El Salvador':
                return f"CP-{random.randint(1000, 9999)}"
            else:  # Honduras
                return f"{random.randint(10000, 99999)}"
        
        # Comenzamos la transacción
        with transaction.atomic():
            # Lista para almacenar correos usados
            emails_usados = []
            usuarios_creados = 0
            direcciones_creadas = 0
            
            # Crear usuarios
            for _ in range(cantidad):
                # Generar datos básicos
                nombre, apellido = generar_nombre_completo()
                nombre_completo = f"{nombre} {apellido}"
                
                # Asignar país (mayor probabilidad para Guatemala)
                pais = random.choices(
                    list(paises.keys()),
                    weights=[0.7, 0.15, 0.15],  # 70% Guatemala, 15% El Salvador, 15% Honduras
                    k=1
                )[0]
                
                # Generar correo único
                email = generar_email(nombre, apellido)
                intentos = 0
                while email in emails_usados and intentos < 10:
                    email = generar_email(nombre, apellido)
                    intentos += 1
                
                if email in emails_usados:
                    email = f"{nombre.lower()}.{apellido.lower()}.{random.randint(100, 999)}@{random.choice(dominios_correo)}"
                
                emails_usados.append(email)
                
                # Crear usuario
                usuario = Usuario.objects.create(
                    email=email,
                    nombre=nombre_completo,
                    telefono=generar_telefono(pais),
                    estado='activo',
                    rol='cliente',
                    is_active=True
                )
                
                # Establecer contraseña simple para pruebas
                usuario.set_password('password123')
                usuario.save()
                
                self.stdout.write(f"Creado usuario cliente: {usuario.nombre} ({usuario.email})")
                usuarios_creados += 1
                
                # Crear direcciones de envío para este usuario
                num_direcciones = random.randint(min_direcciones, max_direcciones)
                
                for _ in range(num_direcciones):
                    # Seleccionar departamento y ciudad
                    departamento = random.choice(list(paises[pais].keys()))
                    ciudad = random.choice(paises[pais][departamento])
                    
                    direccion = DireccionEnvio.objects.create(
                        usuario=usuario,
                        direccion=generar_direccion(ciudad, departamento, pais),
                        ciudad=ciudad,
                        departamento=departamento,
                        pais=pais,
                        codigo_postal=generar_codigo_postal(pais, departamento),
                        telefono_contacto=generar_telefono(pais)
                    )
                    
                    self.stdout.write(f"  - Creada dirección: {direccion.direccion}")
                    direcciones_creadas += 1
            
        self.stdout.write(self.style.SUCCESS(f'Se han creado {usuarios_creados} usuarios clientes con {direcciones_creadas} direcciones de envío correctamente'))