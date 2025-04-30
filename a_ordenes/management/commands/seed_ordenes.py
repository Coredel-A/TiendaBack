import random
import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.db.models import Count
from faker import Faker
from a_usuarios.models import Usuario, DireccionEnvio
from a_productos.models import Producto
from a_sucursales.models import Sucursal
from a_ordenes.models import Orden, OrdenDetalle

class Command(BaseCommand):
    help = 'Crea órdenes de prueba con sus detalles en español'

    def add_arguments(self, parser):
        parser.add_argument('--cantidad', type=int, default=50, help='Cantidad de órdenes a crear')
        parser.add_argument('--dias-atras', type=int, default=60, help='Rango de días hacia atrás para fechas de órdenes')
        parser.add_argument('--min-productos', type=int, default=1, help='Mínimo de productos por orden')
        parser.add_argument('--max-productos', type=int, default=5, help='Máximo de productos por orden')

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        dias_atras = options['dias_atras']
        min_productos = options['min_productos']
        max_productos = options['max_productos']
        
        self.stdout.write(f'Creando {cantidad} órdenes de prueba...')
        
        # Verificar que existan datos necesarios
        usuarios_clientes = Usuario.objects.filter(rol='cliente')
        productos = Producto.objects.filter(estado='activo')
        sucursales = Sucursal.objects.all()
        
        if not usuarios_clientes:
            self.stdout.write(self.style.ERROR('No hay usuarios clientes en la base de datos. Ejecuta seed_usuarios primero.'))
            return
            
        if not productos:
            self.stdout.write(self.style.ERROR('No hay productos activos en la base de datos. Ejecuta seed_productos primero.'))
            return
            
        if not sucursales:
            self.stdout.write(self.style.ERROR('No hay sucursales en la base de datos. Ejecuta seed_sucursales primero.'))
            return
        
        # Configuramos Faker para español
        fake = Faker('es_ES')
        
        # Formas de pago disponibles
        formas_pago = [
            'Tarjeta de crédito', 
            'Tarjeta de débito', 
            'Efectivo contra entrega', 
            'Transferencia bancaria',
            'Depósito bancario'
        ]
        
        # Comenzamos la transacción
        with transaction.atomic():
            ordenes_creadas = 0
            detalles_creados = 0
            
            # Usuarios con al menos una dirección de envío
            usuarios_con_direcciones = []
            for usuario in usuarios_clientes:
                direcciones = DireccionEnvio.objects.filter(usuario=usuario)
                if direcciones.exists():
                    usuarios_con_direcciones.append((usuario, list(direcciones)))
            
            if not usuarios_con_direcciones:
                self.stdout.write(self.style.ERROR('No hay usuarios con direcciones de envío. Ejecuta seed_usuarios primero.'))
                return
            
            # Crear órdenes
            for _ in range(cantidad):
                # Seleccionar usuario aleatorio con sus direcciones
                usuario, direcciones = random.choice(usuarios_con_direcciones)
                
                # Determinar si la orden es para envío a domicilio o recoger en tienda
                tipo_envio = random.choice(['envio', 'recoger'])
                
                # Asignar fecha aleatoria en el rango especificado
                fecha_creacion = timezone.now() - datetime.timedelta(
                    days=random.randint(0, dias_atras),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                # Determinar estado según la antigüedad de la orden
                dias_desde_creacion = (timezone.now() - fecha_creacion).days
                
                # Distribución de estados según antigüedad
                if dias_desde_creacion == 0:  # Hoy
                    estados_posibles = ['carrito', 'pendiente', 'pagado']
                    pesos = [0.3, 0.4, 0.3]
                elif dias_desde_creacion <= 1:  # Ayer o hoy
                    estados_posibles = ['pendiente', 'pagado', 'enviado']
                    pesos = [0.2, 0.5, 0.3]
                elif dias_desde_creacion <= 3:  # Últimos 3 días
                    estados_posibles = ['pagado', 'enviado', 'entregado', 'cancelado']
                    pesos = [0.1, 0.4, 0.4, 0.1]
                elif dias_desde_creacion <= 7:  # Última semana
                    estados_posibles = ['enviado', 'entregado', 'cancelado']
                    pesos = [0.2, 0.7, 0.1]
                else:  # Más de una semana
                    estados_posibles = ['entregado', 'cancelado']
                    pesos = [0.9, 0.1]
                
                estado = random.choices(estados_posibles, weights=pesos, k=1)[0]
                
                # Seleccionar dirección de envío o sucursal según tipo de envío
                direccion_envio = None
                sucursal_retiro = None
                
                if tipo_envio == 'envio':
                    direccion_envio = random.choice(direcciones)
                else:  # recoger
                    # Intentar obtener sucursal en el mismo país que el usuario
                    # (Asumimos que el país está en la primera dirección del usuario)
                    pais_usuario = direcciones[0].pais
                    sucursales_pais = list(sucursales.filter(pais=pais_usuario))
                    
                    if sucursales_pais:
                        sucursal_retiro = random.choice(sucursales_pais)
                    else:
                        # Si no hay sucursales en el país del usuario, seleccionar cualquiera
                        sucursal_retiro = random.choice(list(sucursales))
                
                # Crear la orden
                orden = Orden.objects.create(
                    usuario=usuario,
                    fecha_creacion=fecha_creacion,
                    estado=estado,
                    tipo_envio=tipo_envio,
                    forma_pago=random.choice(formas_pago),
                    direccion_envio=direccion_envio,
                    sucursal_retiro=sucursal_retiro,
                    total=0  # Se calculará después de agregar los detalles
                )
                
                # Generar número de seguimiento si está enviado o entregado
                if estado in ['enviado', 'entregado']:
                    orden.seguimiento = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
                
                # Añadir productos a la orden
                num_productos = random.randint(min_productos, max_productos)
                productos_seleccionados = random.sample(list(productos), min(num_productos, len(productos)))
                
                total_orden = 0
                
                for producto in productos_seleccionados:
                    cantidad = random.randint(1, 3)
                    
                    # Para productos caros, reducir la probabilidad de cantidades mayores
                    if float(producto.precio) > 500:
                        cantidad = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1], k=1)[0]
                    
                    # Crear detalle de orden
                    detalle = OrdenDetalle.objects.create(
                        orden=orden,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio
                    )
                    
                    subtotal = float(producto.precio) * cantidad
                    total_orden += subtotal
                    
                    detalles_creados += 1
                    
                # Actualizar el total de la orden
                orden.total = total_orden
                orden.save()
                
                self.stdout.write(f"Creada orden #{orden.id} para {usuario.nombre}, estado: {orden.estado}, total: ${orden.total}")
                ordenes_creadas += 1
            
        self.stdout.write(self.style.SUCCESS(f'Se han creado {ordenes_creadas} órdenes con {detalles_creados} detalles correctamente'))