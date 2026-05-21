import streamlit as st
import pandas as pd

# Configuracion de la pagina
st.set_page_config(layout="wide")

# Panel de presentacion
st.title("Calculadora de Interpolacion de Lagrange")
st.write("Ingrese las coordenadas conocidas (X, Y) en la tabla y el valor de 'x' que desea interpolar.")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Valor a Evaluar")
    x_eval = st.number_input("Ingrese el valor 'x' a estimar:", value=2.5, format="%.4f")
    
    st.markdown("### Tabla de Coordenadas")
    st.write("Agregue, modifique o elimine puntos en la tabla. Necesita al menos 2 puntos.")
    
    # Tabla dinamica para ingresar coordenadas por defecto
    df_inicial = pd.DataFrame({
        "X": [1.0, 2.0, 3.0],
        "Y": [1.0, 4.0, 9.0]
    })
    
    # El usuario puede editar esta tabla directamente en la interfaz
    df_editado = st.data_editor(df_inicial, num_rows="dynamic", use_container_width=True)

with col2:
    st.markdown("### Resultados y Procedimiento")
    if st.button("Ejecutar Calculos", use_container_width=True):
        
        # Extraer los datos de la tabla
        puntos_x = df_editado["X"].tolist()
        puntos_y = df_editado["Y"].tolist()
        n = len(puntos_x)

        # VALIDACIONES ESTRICTAS
        if n < 2:
            st.error("Error: El metodo requiere un minimo de 2 puntos para poder interpolar una linea.")
            st.stop()
            
        if len(set(puntos_x)) != len(puntos_x):
            st.error("Error Matematico: Existen valores duplicados en la columna X. Esto causa una division por cero en el polinomio.")
            st.stop()

        # Proceso Matematico de Lagrange
        resultado_final = 0
        historial = []

        for i in range(n):
            numerador = 1.0
            denominador = 1.0
            
            for j in range(n):
                if i != j:
                    numerador *= (x_eval - puntos_x[j])
                    denominador *= (puntos_x[i] - puntos_x[j])
            
            li = numerador / denominador
            termino_completo = puntos_y[i] * li
            resultado_final += termino_completo
            
            historial.append({
                "Punto Base": f"P_{i}",
                "X": round(puntos_x[i], 4),
                "Y": round(puntos_y[i], 4),
                "Coeficiente L_i(x)": round(li, 6),
                "Contribucion (Y * L_i)": round(termino_completo, 6)
            })

        # Despliegue de resultados intermedios
        st.markdown("#### Desglose de Polinomios Base (L_i)")
        df_historial = pd.DataFrame(historial)
        st.dataframe(df_historial, use_container_width=True)

        # Resultado Final
        st.markdown("---")
        st.success("Calculo completado con exito.")
        st.metric(label=f"Valor estimado final P({x_eval})", value=f"{resultado_final:.6f}")