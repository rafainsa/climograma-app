import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Lógica de Köppen con todas las letras (Ej: Csa, BWh, etc.)
def clasificar_koppen_completo(temps, precs):
    t_media = sum(temps) / 12
    p_total = sum(precs)
    t_max, t_min = max(temps), min(temps)
    
    # Grupo B (Secos)
    umbral = 20 * t_media
    if p_total < umbral:
        clase = "BW" if p_total < umbral / 2 else "BS"
        sub = "h" if t_media >= 18 else "k"
        return f"{clase}{sub}", "Clima Árido/Semiárido"

    # Grupo A (Tropical)
    if t_min >= 18:
        if min(precs) >= 60: return "Af", "Ecuatorial"
        return "Aw", "Tropical"

    # Grupos C y D
    grupo = "C" if t_min > -3 else "D"
    # Subtipo lluvia (s, w, f)
    if min(precs[5:8]) < 30 and max(precs[0:3]) > 3 * min(precs[5:8]): sub1 = "s"
    elif min(precs[0:3]) < max(precs[5:8])/10: sub1 = "w"
    else: sub1 = "f"
    # Subtipo temperatura (a, b, c)
    if t_max >= 22: sub2 = "a"
    elif len([t for t in temps if t > 10]) >= 4: sub2 = "b"
    else: sub2 = "c"

    return f"{grupo}{sub1}{sub2}", f"Clima templado/continental tipo {grupo}{sub1}{sub2}"

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Climograma Pro", layout="centered")
st.title("📊 Generador de Climogramas Profesional")

localidad = st.text_input("Nombre de la localidad:", "Valencia")

st.write("### 📥 Entrada de Datos")
meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

# Columnas para organizar la entrada
col_t, col_p = st.columns(2)
with col_t:
    st.write("**Temperaturas (°C)**")
    t_input = [st.number_input(f"T {m}", value=15.0, step=0.1, key=f"t{m}") for m in meses]
with col_p:
    st.write("**Precipitaciones (mm)**")
    p_input = [st.number_input(f"P {m}", value=40.0, step=1.0, key=f"p{m}") for m in meses]

if st.button("🚀 Generar Informe"):
    # Estadísticas
    t_anual = sum(t_input) / 12
    p_anual = sum(p_input)
    t_calido = max(t_input)
    t_frio = min(t_input)
    oscilacion = t_calido - t_frio
    martonne = p_anual / (t_anual + 10)
    kop_code, kop_desc = clasificar_koppen_completo(t_input, p_input)

    # Gráfico
    fig, ax1 = plt.subplots(figsize=(10, 7))
    ax2 = ax1.twinx()
    
    lim_p = ((max(max(p_input), max(t_input)*2, 40) // 10) + 1) * 10
    ax1.set_ylim(0, lim_p)
    ax2.set_ylim(0, lim_p / 2)

    ax1.bar(meses, p_input, color='blue', alpha=0.6, width=0.8, edgecolor='black')
    ax2.plot(meses, t_input, color='red', marker='o', linewidth=2)
    
    # Líneas de meses entre barras
    ax1.set_xticks(np.arange(len(meses)))
    ax1.set_xticklabels(meses, fontweight='bold')
    ax1.grid(axis='x', linestyle='--', alpha=0.7)

    st.pyplot(fig)

    # RESULTADOS
    st.markdown("---")
    st.subheader(f"📈 Resultados para {localidad}")
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**Temp. Media Anual:** {t_anual:.1f} °C")
        st.write(f"**Prec. Total Anual:** {p_anual:.0f} mm")
        st.write(f"**Índice de Martonne:** {martonne:.1f}")
    with c2:
        st.write(f"**Mes más Cálido:** {t_calido:.1f} °C")
        st.write(f"**Mes más Frío:** {t_frio:.1f} °C")
        st.write(f"**Oscilación Térmica:** {oscilacion:.1f} °C")
    
    st.success(f"**Clasificación de Köppen:** {kop_code} ({kop_desc})")
