import streamlit as st
import matlab.engine
import concurrent.futures
import requests
import matplotlib.pyplot as plt
import numpy as np

# Inyectar CSS personalizado para cambiar el fondo y otros estilos
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f0f4f7;
}

[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}

[data-testid="stSidebar"] {
    background-color: #ffffff;
}

.main {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    margin-top: 20px;
}

h1 {
    color: #007BFF;
    text-align: center;
    font-size: 3em;
}

h2 {
    color: #007BFF;
    text-align: left;
    font-size: 2em;
}

.stImage > img {
    border-radius: 10px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Encabezado principal estilizado
st.markdown("<h1>🌍 Evaluación de Energía Renovable en el Hogar 🌞</h1>", unsafe_allow_html=True)

# Añadir un banner visual al principio
st.image("https://png.pngtree.com/png-vector/20240908/ourmid/pngtree-3d-renewable-energy-icons-banner-solar-wind-and-sustainable-power-png-image_13791641.png", 
         caption="🌞 Evaluación de Energía Renovable 🌱", use_column_width=True)

# Añadir una barra de progreso mientras carga la página
with st.spinner('Cargando la interfaz...'):
    st.progress(100)

# Lista de países y sus códigos (ISO 3166-1 alfa-2)
lista_paises = {
    "México": "MX",
    "Estados Unidos": "US",
    "Reino Unido": "GB",
    "Canadá": "CA",
    "Alemania": "DE",
    "Brasil": "BR",
    "Francia": "FR",
    "España": "ES",
    "Italia": "IT",
    "Argentina": "AR",
    "Colombia": "CO",
    "Chile": "CL",
    "Japón": "JP",
    "China": "CN",
    "India": "IN",
    "Australia": "AU",
    "Sudáfrica": "ZA",
    "Rusia": "RU"
}

# Función para obtener latitud y longitud usando la API de OpenWeatherMap con ciudad y país
def obtener_lat_lon_openweather_ciudad(ciudad, pais, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={ciudad},{pais}&limit=1&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if data and data[0]['country'] == pais:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    else:
        st.error(f"❌ No se encontraron coincidencias para la ciudad '{ciudad}' en el país seleccionado.")
        return None, None

# Función para obtener datos de NASA POWER (irradiancia solar y velocidad del viento)
def obtener_datos_nasa_power(lat, lon):
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?start=20220101&end=20220131&latitude={lat}&longitude={lon}&community=RE&parameters=ALLSKY_SFC_SW_DWN,WS10M&format=JSON"
    response = requests.get(url)
    data = response.json()

    radiacion_solar_diaria = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
    velocidad_viento = data['properties']['parameter']['WS10M']
    
    return radiacion_solar_diaria, velocidad_viento

# Función para ejecutar la simulación de MATLAB
def simular_energia_renovable(tipo_energia, lat, lon, tamano_techo):
    # Iniciar MATLAB
    eng = matlab.engine.start_matlab()
    eng.cd('C:/Users/saula/OneDrive/Imágenes/Escritorio/proyecto_hack/matlab', nargout=0)

    # Obtener datos de NASA POWER (irradiancia solar y velocidad del viento)
    radiacion_solar_diaria, velocidad_viento = obtener_datos_nasa_power(lat, lon)

    if tipo_energia == "Solar":
        energia_generada = eng.calcular_energia_solar(float(tamano_techo), float(radiacion_solar_diaria['20220101']))
    elif tipo_energia == "Eólica":
        energia_generada = eng.calcular_energia_eolica(float(tamano_techo), float(velocidad_viento['20220101']))
    
    eng.quit()
    return energia_generada

# Función para graficar el costo-beneficio con validación
def graficar_costo_beneficio(energia_generada, tamano_techo):
    costo_por_m2 = 100  
    costo_inversion = tamano_techo * costo_por_m2
    
    ahorro_por_kwh = 2  
    ahorro_mensual = energia_generada * ahorro_por_kwh
    
    meses = np.arange(1, 121)  
    inversion_acumulada = np.full(meses.shape, costo_inversion)
    ahorro_acumulado = ahorro_mensual * meses

    if ahorro_acumulado[-1] < costo_inversion:
        mes_recuperacion = None
    else:
        mes_recuperacion = np.argmax(ahorro_acumulado >= costo_inversion) + 1

    plt.figure(figsize=(10, 5))
    plt.plot(meses, inversion_acumulada, label="Costo de Inversión", color="red", linestyle="--", linewidth=2)
    plt.plot(meses, ahorro_acumulado, label="Ahorro Acumulado", color="green", linestyle="-", linewidth=2)
    plt.axhline(0, color="black", linewidth=0.5)
    
    plt.xlabel("Meses", fontsize=12)
    plt.ylabel("Dinero (USD)", fontsize=12)
    plt.title("Gráfica de Costo-Beneficio", fontsize=14, fontweight="bold")
    plt.legend(loc="best", fontsize=10)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

    if mes_recuperacion:
        st.write(f"""
        **Explicación de la Gráfica**:
        - La línea roja representa el costo de la inversión inicial, que es de ${costo_inversion:.2f} USD.
        - La línea verde representa el ahorro acumulado mes a mes en tu factura de electricidad.
        - En el mes {mes_recuperacion}, habrás recuperado tu inversión inicial.
        """)
    else:
        st.write(f"""
        **Explicación de la Gráfica**:
        - La línea roja representa el costo de la inversión inicial, que es de ${costo_inversion:.2f} USD.
        - La línea verde representa el ahorro acumulado mes a mes.
        - No se recuperará la inversión inicial en 10 años.
        """)

# Interfaz de usuario
st.subheader("🔍 Ingresar datos")
col1, col2 = st.columns([2, 1])

with col1:
    ciudad = st.text_input("🏙️ Ingrese su ciudad:", "")
    pais_seleccionado = st.selectbox("🌎 Seleccione su país:", list(lista_paises.keys()))
    codigo_pais = lista_paises[pais_seleccionado]
    tamano_techo = st.number_input("🏠 Tamaño del techo (en metros cuadrados):", min_value=0.0)
    tipo_energia = st.selectbox("🔋 Seleccione el tipo de energía renovable", ("Solar", "Eólica"))
    consumo_actual = st.number_input("💡 Consumo energético actual (kWh por mes):", min_value=0.0)

# Mostrar imagen según el tipo de energía seleccionado
with col2:
    if tipo_energia == "Solar":
        st.image("https://cdn-icons-png.flaticon.com/512/5673/5673489.png", caption="Panel Solar", use_column_width=True)
    elif tipo_energia == "Eólica":
        st.image("https://cdn-icons-png.flaticon.com/512/5782/5782302.png", caption="Turbina Eólica", use_column_width=True)

# Separador
st.markdown("***")

# Clave API de OpenWeatherMap
api_key_openweather = '8238cebededd8aa41300614e00ea4dec'

# Botón para iniciar la simulación
if st.button("⚡ Calcular potencial de energía renovable ⚡"):
    lat, lon = obtener_lat_lon_openweather_ciudad(ciudad, codigo_pais, api_key_openweather)
    
    if lat and lon:
        with st.spinner('⏳ Calculando el potencial de energía renovable...'):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(simular_energia_renovable, tipo_energia, lat, lon, tamano_techo)
                energia_generada = future.result()
            
            st.success(f"✅ Energía potencial generada: {energia_generada} kWh")
            
            # Graficar el costo-beneficio
            graficar_costo_beneficio(energia_generada, tamano_techo)
