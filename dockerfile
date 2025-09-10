# Usa Ubuntu 24.04 como base
FROM ubuntu:24.04

WORKDIR /app

# =============================================
# 1. Instala herramientas base y Node.js 20
# =============================================
RUN apt-get update && apt-get install -yq --no-install-recommends \
    gnupg \
    dirmngr \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Agrega el repositorio de NodeSource para Node.js 20
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" \
    | tee /etc/apt/sources.list.d/nodesource.list

# Instala Node.js y limpia
RUN apt-get update && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Instala Firebase CLI globalmente
RUN npm install -g firebase-tools

# =============================================
# 2. Instala Java 17 (para emuladores de Firebase)
# =============================================
RUN apt-get update && apt-get install -y openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# =============================================
# 3. Instala Python 3.12 + pip + venv
# =============================================
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3.12-venv \
    python3.12-dev \
    && rm -rf /var/lib/apt/lists/*

# =============================================
# 4. Copia requirements primero (para cache)
# =============================================
WORKDIR /app/functions
COPY functions/requirements.txt /app/functions/requirements.txt

# =============================================
# 5. Crear entorno virtual en /app/functions/venv
# =============================================
RUN python3.12 -m venv /app/functions/venv && \
    /app/functions/venv/bin/pip install --upgrade pip && \
    /app/functions/venv/bin/pip install --no-cache-dir -r requirements.txt

# =============================================
# 6. Copiar el resto del código
# =============================================
COPY firebase.json /app/
COPY functions/ /app/functions/

# =============================================
# 7. Expone puertos comunes de Firebase Emulators
# =============================================
EXPOSE 5001  
EXPOSE 4000  
EXPOSE 8080  
EXPOSE 9099  

# =============================================
# 8. Comando por defecto (usar Python del venv)
# =============================================
CMD ["/app/functions/venv/bin/python", "main.py"]
