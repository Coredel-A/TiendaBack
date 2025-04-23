CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contraseña VARCHAR(100) NOT NULL,
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de productos
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    imagen_url TEXT
);

-- Tabla de pedidos
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    estado VARCHAR(50) DEFAULT 'en proceso', -- opciones: en proceso, verificando, pagado
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    forma_entrega VARCHAR(50), -- tienda o delivery
    forma_pago VARCHAR(50), -- tarjeta o QR
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) -- Relación de uno a muchos
);

-- Tabla de detalles del pedido
CREATE TABLE pedido_detalle (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id), -- Relación de uno a muchos
    FOREIGN KEY (producto_id) REFERENCES productos(id) -- Relación de uno a muchos
);

-- (Opcional) Tabla de chat_ia (solo si vas a almacenar el chat de la IA)
CREATE TABLE chat_ia (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    mensaje_usuario TEXT,
    respuesta_ia TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) -- Relación de uno a muchos
);